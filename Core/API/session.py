"""
A Source Filmmaker session, read through typed views.

The session is a DMX document (format `sfm_session`). Everything here is a
thin view over an Element: reading an attribute reads the element, setting
one writes it, and saving the document writes exactly what SFM would read
back. Nothing is copied, so there is one truth.

    session = Session(load_dmx(path))
    clip = session.active_clip                 # FilmClip
    for shot in clip.shots:                    # FilmClips on the film track
        shot.time_frame.start, shot.time_frame.duration
        for node in shot.scene.walk():         # the DAG
            if isinstance(node, GameModel): node.model_name, node.world_matrix()

The element types are SFM's own (DmeFilmClip, DmeDag, DmeGameModel...); the
views only name the attributes those types have.
"""
from __future__ import annotations

from typing import Iterator, List, Optional, Sequence, Tuple

from Core.Code.transform import IDENTITY, Mat34, matrix_from, multiply

from .dmx import ARRAY_OFFSET, AttrType, DmxDocument, Element, Time

__all__ = [
    "Session", "FilmClip", "ChannelsClip", "SoundClip", "Clip", "TimeFrame", "TrackGroup",
    "Track", "Dag", "GameModel", "Camera", "Transform", "AnimationSet", "Channel", "Log",
    "LogLayer", "wrap",
]

Vec3 = Tuple[float, float, float]
Quat = Tuple[float, float, float, float]


class View:
    """Base of every typed view: holds the element, reads with defaults."""

    __slots__ = ("element",)
    TYPE = "DmElement"

    def __init__(self, element: Element) -> None:
        self.element = element

    @property
    def name(self) -> str:
        return self.element.name

    @name.setter
    def name(self, value: str) -> None:
        self.element.name = value

    def _get(self, key: str, default=None):
        return self.element.get(key, default)

    def _elements(self, key: str) -> List[Element]:
        value = self.element.get(key)
        return [e for e in value if isinstance(e, Element)] if isinstance(value, list) else []

    def _child(self, key: str, cls):
        value = self.element.get(key)
        return cls(value) if isinstance(value, Element) else None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, View) and other.element is self.element

    def __hash__(self) -> int:
        return id(self.element)

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.name!r}>"


# ---------------------------------------------------------------------------
#  Transforms and the DAG
# ---------------------------------------------------------------------------
class Transform(View):
    TYPE = "DmeTransform"

    @property
    def position(self) -> Vec3:
        return tuple(self._get("position", (0.0, 0.0, 0.0)))

    @position.setter
    def position(self, value: Vec3) -> None:
        self.element.set("position", AttrType.VECTOR3, tuple(value))

    @property
    def orientation(self) -> Quat:
        return tuple(self._get("orientation", (0.0, 0.0, 0.0, 1.0)))

    @orientation.setter
    def orientation(self, value: Quat) -> None:
        self.element.set("orientation", AttrType.QUATERNION, tuple(value))

    def matrix(self) -> Mat34:
        return matrix_from(self.position, self.orientation)


class Dag(View):
    """A node of the scene graph: a transform, optional shape, children."""
    TYPE = "DmeDag"

    @property
    def transform(self) -> Optional[Transform]:
        return self._child("transform", Transform)

    @property
    def visible(self) -> bool:
        return bool(self._get("visible", True))

    @property
    def children(self) -> List["Dag"]:
        return [wrap(e) for e in self._elements("children")]

    @property
    def shape(self) -> Optional[Element]:
        return self._get("shape")

    def local_matrix(self) -> Mat34:
        t = self.transform
        return t.matrix() if t is not None else IDENTITY

    def walk(self, parent_matrix: Mat34 = IDENTITY, include_hidden: bool = False
             ) -> Iterator[Tuple["Dag", Mat34]]:
        """Every node under this one, depth first, with its world matrix."""
        if not include_hidden and not self.visible:
            return
        world = multiply(parent_matrix, self.local_matrix())
        yield self, world
        for child in self.children:
            yield from child.walk(world, include_hidden)

    def world_matrix(self, parent_matrix: Mat34 = IDENTITY) -> Mat34:
        return multiply(parent_matrix, self.local_matrix())


class GameModel(Dag):
    """A model placed in the scene, with the pose its bones are in."""
    TYPE = "DmeGameModel"

    @property
    def model_name(self) -> str:
        return str(self._get("modelName", "")).replace("\\", "/")

    @property
    def skin(self) -> int:
        return int(self._get("skin", 0))

    @property
    def body(self) -> int:
        return int(self._get("body", 0))

    @property
    def bones(self) -> List[Transform]:
        """Local bone transforms in the model's bone order - the pose."""
        return [Transform(e) for e in self._elements("bones")]

    @property
    def flex_weights(self) -> List[float]:
        return list(self._get("flexWeights", []))

    @property
    def flex_names(self) -> List[str]:
        return list(self._get("flexnames", []))


class Camera(Dag):
    TYPE = "DmeCamera"

    @property
    def field_of_view(self) -> float:
        return float(self._get("fieldOfView", 75.0))

    @property
    def znear(self) -> float:
        return float(self._get("znear", 3.0))

    @property
    def zfar(self) -> float:
        return float(self._get("zfar", 28377.0))

    @property
    def focal_distance(self) -> float:
        return float(self._get("focalDistance", 72.0))


# ---------------------------------------------------------------------------
#  Clips and tracks
# ---------------------------------------------------------------------------
class TimeFrame(View):
    TYPE = "DmeTimeFrame"

    @property
    def start(self) -> Time:
        return self._get("start", Time(0))

    @start.setter
    def start(self, value: Time) -> None:
        self.element.set("start", AttrType.TIME, value)

    @property
    def duration(self) -> Time:
        return self._get("duration", Time(0))

    @duration.setter
    def duration(self, value: Time) -> None:
        self.element.set("duration", AttrType.TIME, value)

    @property
    def offset(self) -> Time:
        return self._get("offset", Time(0))

    @property
    def scale(self) -> float:
        return float(self._get("scale", 1.0))

    @property
    def end(self) -> Time:
        return Time(self.start.ticks + self.duration.ticks)

    def to_child_time(self, parent_time: Time) -> Time:
        """A time in the containing clip, expressed inside this one."""
        return Time(round((parent_time.ticks - self.start.ticks) * self.scale) + self.offset.ticks)


class Clip(View):
    TYPE = "DmeClip"

    @property
    def time_frame(self) -> TimeFrame:
        frame = self._child("timeFrame", TimeFrame)
        if frame is None:
            frame = TimeFrame(Element("DmeTimeFrame", "unnamed"))
        return frame

    @property
    def color(self) -> Tuple[int, int, int, int]:
        return tuple(self._get("color", (0, 0, 0, 0)))

    @property
    def mute(self) -> bool:
        return bool(self._get("mute", False))

    @property
    def track_groups(self) -> List["TrackGroup"]:
        return [TrackGroup(e) for e in self._elements("trackGroups")]


class ChannelsClip(Clip):
    TYPE = "DmeChannelsClip"

    @property
    def channels(self) -> List["Channel"]:
        return [Channel(e) for e in self._elements("channels")]


class SoundClip(Clip):
    TYPE = "DmeSoundClip"

    @property
    def sound_name(self) -> str:
        sound = self._get("sound")
        return str(sound.get("soundname", "")) if isinstance(sound, Element) else ""


class FilmClip(Clip):
    """A film clip: the session's sequence, or one shot on its film track."""
    TYPE = "DmeFilmClip"

    @property
    def scene(self) -> Optional[Dag]:
        return self._child("scene", Dag)

    @property
    def camera(self) -> Optional[Camera]:
        return self._child("camera", Camera)

    @property
    def map_name(self) -> str:
        return str(self._get("mapname", ""))

    @property
    def animation_sets(self) -> List["AnimationSet"]:
        return [AnimationSet(e) for e in self._elements("animationSets")]

    @property
    def sub_clip_track_group(self) -> Optional["TrackGroup"]:
        return self._child("subClipTrackGroup", TrackGroup)

    @property
    def shots(self) -> List["FilmClip"]:
        """Film clips on the sub-clip track, in time order."""
        group = self.sub_clip_track_group
        if group is None:
            return []
        shots = [c for t in group.tracks for c in t.clips if isinstance(c, FilmClip)]
        shots.sort(key=lambda c: c.time_frame.start.ticks)
        return shots

    def game_models(self) -> List[Tuple[GameModel, Mat34]]:
        """Every visible game model in the scene with its world matrix."""
        scene = self.scene
        if scene is None:
            return []
        return [(node, world) for node, world in scene.walk() if isinstance(node, GameModel)]


class Track(View):
    TYPE = "DmeTrack"

    @property
    def clips(self) -> List[Clip]:
        return [wrap(e) for e in self._elements("children")]

    @property
    def mute(self) -> bool:
        return bool(self._get("mute", False))


class TrackGroup(View):
    TYPE = "DmeTrackGroup"

    @property
    def tracks(self) -> List[Track]:
        return [Track(e) for e in self._elements("tracks")]

    @property
    def visible(self) -> bool:
        return bool(self._get("visible", True))


# ---------------------------------------------------------------------------
#  Animation
# ---------------------------------------------------------------------------
class LogLayer(View):
    TYPE = "DmeLogLayer"

    @property
    def times(self) -> List[Time]:
        return list(self._get("times", []))

    @property
    def values(self) -> list:
        return list(self._get("values", []))


class Log(View):
    TYPE = "DmeLog"

    @property
    def layers(self) -> List[LogLayer]:
        return [LogLayer(e) for e in self._elements("layers")]

    @property
    def default_value(self):
        return self._get("defaultvalue")

    @property
    def uses_default(self) -> bool:
        return bool(self._get("usedefaultvalue", False))


class Channel(View):
    """Drives one attribute of one element from a log over time."""
    TYPE = "DmeChannel"

    @property
    def to_element(self) -> Optional[Element]:
        return self._get("toElement")

    @property
    def to_attribute(self) -> str:
        return str(self._get("toAttribute", ""))

    @property
    def from_element(self) -> Optional[Element]:
        return self._get("fromElement")

    @property
    def from_attribute(self) -> str:
        return str(self._get("fromAttribute", ""))

    @property
    def mode(self) -> int:
        return int(self._get("mode", 0))

    @property
    def log(self) -> Optional[Log]:
        return self._child("log", Log)


class AnimationSet(View):
    TYPE = "DmeAnimationSet"

    @property
    def game_model(self) -> Optional[GameModel]:
        return self._child("gameModel", GameModel)

    @property
    def camera(self) -> Optional[Camera]:
        return self._child("camera", Camera)

    @property
    def controls(self) -> List[Element]:
        return self._elements("controls")


# ---------------------------------------------------------------------------
#  The session
# ---------------------------------------------------------------------------
class Session(View):
    def __init__(self, document: DmxDocument) -> None:
        if document.root is None:
            raise ValueError("the document has no root element")
        super().__init__(document.root)
        self.document = document

    @property
    def is_session(self) -> bool:
        return self.document.format == "sfm_session" or "activeClip" in self.element

    @property
    def active_clip(self) -> Optional[FilmClip]:
        return self._child("activeClip", FilmClip)

    @property
    def clips(self) -> List[FilmClip]:
        return [FilmClip(e) for e in self._elements("clipBin")]

    @property
    def settings(self) -> Optional[Element]:
        return self._get("settings")

    def summary(self) -> str:
        clip = self.active_clip
        if clip is None:
            return f"{self.name}: no active clip"
        shots = clip.shots
        models = sum(len(s.game_models()) for s in shots)
        return (f"{clip.name}: {clip.time_frame.duration.seconds:.2f} s, {len(shots)} shots, "
                f"{models} models, map {clip.map_name or '<none>'}")


_VIEWS = {
    "DmeDag": Dag, "DmeGameModel": GameModel, "DmeCamera": Camera, "DmeRig": Dag,
    "DmeRigHandle": Dag, "DmeJoint": Dag, "DmeGameSprite": Dag, "DmeGameParticleSystem": Dag,
    "DmeProjectedLight": Dag, "DmeModel": Dag,
    "DmeFilmClip": FilmClip, "DmeChannelsClip": ChannelsClip, "DmeSoundClip": SoundClip,
    "DmeClip": Clip, "DmeTrack": Track, "DmeTrackGroup": TrackGroup, "DmeTimeFrame": TimeFrame,
    "DmeTransform": Transform, "DmeAnimationSet": AnimationSet, "DmeChannel": Channel,
}


def wrap(element: Element) -> View:
    """The view class for an element's type; a Dag for unknown DAG-like types
    (anything with a `transform` and `children`), a Clip for anything with a
    `timeFrame`, a plain View otherwise."""
    cls = _VIEWS.get(element.type)
    if cls is None:
        if "children" in element and "transform" in element:
            cls = Dag
        elif "timeFrame" in element:
            cls = Clip
        else:
            cls = View
    return cls(element)
