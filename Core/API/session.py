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

from typing import Dict, Iterator, List, Optional, Tuple

from Core.Code.transform import IDENTITY, Mat34, matrix_from, multiply

from .dmx import AttrType, DmxDocument, Element, Time

__all__ = [
    "Session", "FilmClip", "ChannelsClip", "SoundClip", "Clip", "TimeFrame", "TrackGroup",
    "Track", "Dag", "GameModel", "Camera", "ProjectedLight", "Transform", "AnimationSet", "Channel", "Log",
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
        """The element's name."""
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
    """DmeTransform: a position and an orientation."""
    TYPE = "DmeTransform"

    @property
    def position(self) -> Vec3:
        """Translation, three floats."""
        return tuple(self._get("position", (0.0, 0.0, 0.0)))

    @position.setter
    def position(self, value: Vec3) -> None:
        self.element.set("position", AttrType.VECTOR3, tuple(value))

    @property
    def orientation(self) -> Quat:
        """Rotation as a quaternion (x, y, z, w)."""
        return tuple(self._get("orientation", (0.0, 0.0, 0.0, 1.0)))

    @orientation.setter
    def orientation(self, value: Quat) -> None:
        self.element.set("orientation", AttrType.QUATERNION, tuple(value))

    def matrix(self) -> Mat34:
        """The 3x4 matrix of this transform."""
        return matrix_from(self.position, self.orientation)


class Dag(View):
    """A node of the scene graph: a transform, optional shape, children."""
    TYPE = "DmeDag"

    @property
    def transform(self) -> Optional[Transform]:
        """The dag's transform, or None."""
        return self._child("transform", Transform)

    @property
    def visible(self) -> bool:
        """The `visible` flag, true when unset."""
        return bool(self._get("visible", True))

    @property
    def children(self) -> List["Dag"]:
        """Child dags, wrapped by their type."""
        return [wrap(e) for e in self._elements("children")]

    @property
    def shape(self) -> Optional[Element]:
        """The shape element (a DmeModel's mesh), or None."""
        return self._get("shape")

    def local_matrix(self) -> Mat34:
        """This dag's matrix in its parent's space."""
        t = self.transform
        return t.matrix() if t is not None else IDENTITY

    def walk(self, parent_matrix: Mat34 = IDENTITY, include_hidden: bool = False
             ) -> Iterator[Tuple["Dag", Mat34]]:
        """Every node under this one, depth first, with its world matrix.
        A hidden node hides everything under it."""
        if not include_hidden and not self.visible:
            return
        world = multiply(parent_matrix, self.local_matrix())
        yield self, world
        for child in self.children:
            yield from child.walk(world, include_hidden)

    def walk_visibility(self, parent_matrix: Mat34 = IDENTITY, parent_visible: bool = True
                        ) -> Iterator[Tuple["Dag", Mat34, bool]]:
        """Every node with its world matrix and whether it is shown, hidden
        ancestors included."""
        visible = parent_visible and self.visible
        world = multiply(parent_matrix, self.local_matrix())
        yield self, world, visible
        for child in self.children:
            yield from child.walk_visibility(world, visible)

    def world_matrix(self, parent_matrix: Mat34 = IDENTITY) -> Mat34:
        """This dag's matrix in the parent's world space."""
        return multiply(parent_matrix, self.local_matrix())


class GameModel(Dag):
    """A model placed in the scene, with the pose its bones are in."""
    TYPE = "DmeGameModel"

    @property
    def model_name(self) -> str:
        """Path of the .mdl, forward slashes."""
        return str(self._get("modelName", "")).replace("\\", "/")

    @property
    def skin(self) -> int:
        """Skin family index."""
        return int(self._get("skin", 0))

    @property
    def body(self) -> int:
        """Body group choice."""
        return int(self._get("body", 0))

    @property
    def bones(self) -> List[Transform]:
        """Local bone transforms in the model's bone order - the pose."""
        return [Transform(e) for e in self._elements("bones")]

    @property
    def flex_weights(self) -> List[float]:
        """Current flex controller weights."""
        return list(self._get("flexWeights", []))

    @property
    def flex_names(self) -> List[str]:
        """Flex controller names, matching `flex_weights`."""
        return list(self._get("flexnames", []))

    @property
    def flex_operators(self) -> List[Element]:
        """DmeGlobalFlexControllerOperator elements: one per face control,
        named after it, holding the animated `flexWeight` (0..1)."""
        return self._elements("globalFlexControllers")

    def flex_values(self) -> Dict[str, float]:
        """Face control values by name, as the operators hold them."""
        out: Dict[str, float] = {}
        for op in self.flex_operators:
            value = op.get("flexWeight")
            if isinstance(value, (int, float)):
                out[op.name] = float(value)
        return out


class Camera(Dag):
    """DmeCamera: a dag with lens settings."""
    TYPE = "DmeCamera"

    @property
    def field_of_view(self) -> float:
        """Vertical field of view in degrees."""
        return float(self._get("fieldOfView", 75.0))

    @property
    def znear(self) -> float:
        """Near clip plane in units."""
        return float(self._get("znear", 3.0))

    @property
    def zfar(self) -> float:
        """Far clip plane in units."""
        return float(self._get("zfar", 28377.0))

    @property
    def focal_distance(self) -> float:
        """Focus distance for depth of field."""
        return float(self._get("focalDistance", 72.0))


class ProjectedLight(Dag):
    """SFM's spot light: a projected texture with a frustum, colour, intensity and
    Source's flashlight attenuation (constant + linear / d + quadratic / d^2)."""
    TYPE = "DmeProjectedLight"

    @property
    def color(self) -> Tuple[float, float, float]:
        """Light colour as 0..1 floats."""
        c = self._get("color", (255, 255, 255, 255))
        return (c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)

    @property
    def intensity(self) -> float:
        """Light intensity multiplier."""
        return float(self._get("intensity", 1.0))

    @property
    def attenuation(self) -> Tuple[float, float, float]:
        """Constant, linear and quadratic attenuation."""
        return (float(self._get("constantAttenuation", 1.0)), float(self._get("linearAttenuation", 0.0)),
                float(self._get("quadraticAttenuation", 0.0)))

    @property
    def min_distance(self) -> float:
        """Where the light starts to shine."""
        return float(self._get("minDistance", 4.0))

    @property
    def max_distance(self) -> float:
        """Where the light stops shining."""
        return float(self._get("maxDistance", 750.0))

    @property
    def far_z_atten(self) -> float:
        """Where the fade to `max_distance` begins."""
        return float(self._get("farZAtten", self.max_distance))

    @property
    def horizontal_fov(self) -> float:
        """Horizontal cone angle in degrees."""
        return float(self._get("horizontalFOV", 45.0))

    @property
    def vertical_fov(self) -> float:
        """Vertical cone angle in degrees."""
        return float(self._get("verticalFOV", 45.0))

    @property
    def ambient_intensity(self) -> float:
        """Ambient light the source adds everywhere."""
        return float(self._get("ambientIntensity", 0.0))

    @property
    def casts_shadows(self) -> bool:
        """Whether the light casts shadows."""
        return bool(self._get("castsShadows", True))



# ---------------------------------------------------------------------------
#  Clips and tracks
# ---------------------------------------------------------------------------
class TimeFrame(View):
    """DmeTimeFrame: where a clip sits on its parent's time."""
    TYPE = "DmeTimeFrame"

    @property
    def start(self) -> Time:
        """Start on the parent's time."""
        return self._get("start", Time(0))

    @start.setter
    def start(self, value: Time) -> None:
        self.element.set("start", AttrType.TIME, value)

    @property
    def duration(self) -> Time:
        """Length in parent time."""
        return self._get("duration", Time(0))

    @duration.setter
    def duration(self, value: Time) -> None:
        self.element.set("duration", AttrType.TIME, value)

    @property
    def offset(self) -> Time:
        """Shift applied when mapping into child time."""
        return self._get("offset", Time(0))

    @property
    def scale(self) -> float:
        """Playback speed factor."""
        return float(self._get("scale", 1.0))

    @property
    def end(self) -> Time:
        """Start plus duration."""
        return Time(self.start.ticks + self.duration.ticks)

    def to_child_time(self, parent_time: Time) -> Time:
        """A time in the containing clip, expressed inside this one."""
        return Time(round((parent_time.ticks - self.start.ticks) * self.scale) + self.offset.ticks)

    def to_parent_time(self, child_time: Time) -> Time:
        """The inverse: a time inside this clip, expressed in the containing one."""
        scale = self.scale or 1.0
        return Time(round((child_time.ticks - self.offset.ticks) / scale) + self.start.ticks)


class Clip(View):
    """DmeClip: anything placed on a track."""
    TYPE = "DmeClip"

    @property
    def time_frame(self) -> TimeFrame:
        """The clip's time frame; a zero one when the clip has none."""
        frame = self._child("timeFrame", TimeFrame)
        if frame is None:
            frame = TimeFrame(Element("DmeTimeFrame", "unnamed"))
        return frame

    @property
    def color(self) -> Tuple[int, int, int, int]:
        """Track colour as RGBA bytes."""
        return tuple(self._get("color", (0, 0, 0, 0)))

    @property
    def mute(self) -> bool:
        """True when the clip or track is muted."""
        return bool(self._get("mute", False))

    @property
    def track_groups(self) -> List["TrackGroup"]:
        """The clip's track groups."""
        return [TrackGroup(e) for e in self._elements("trackGroups")]


class ChannelsClip(Clip):
    """DmeChannelsClip: a clip of animation channels."""
    TYPE = "DmeChannelsClip"

    @property
    def channels(self) -> List["Channel"]:
        """The clip's channels."""
        return [Channel(e) for e in self._elements("channels")]


class SoundClip(Clip):
    """DmeSoundClip: a clip that plays a sound."""
    TYPE = "DmeSoundClip"

    @property
    def sound_name(self) -> str:
        """The sound's path, or ""."""
        sound = self._get("sound")
        return str(sound.get("soundname", "")) if isinstance(sound, Element) else ""


class FilmClip(Clip):
    """A film clip: the session's sequence, or one shot on its film track."""
    TYPE = "DmeFilmClip"

    @property
    def scene(self) -> Optional[Dag]:
        """The shot's scene root, or None."""
        return self._child("scene", Dag)

    @property
    def camera(self) -> Optional[Camera]:
        """The camera, or None."""
        return self._child("camera", Camera)

    @property
    def map_name(self) -> str:
        """The map the shot plays on, e.g. "cp_badlands.bsp"."""
        return str(self._get("mapname", ""))

    @property
    def animation_sets(self) -> List["AnimationSet"]:
        """The shot's animation sets."""
        return [AnimationSet(e) for e in self._elements("animationSets")]

    @property
    def sub_clip_track_group(self) -> Optional["TrackGroup"]:
        """The track group holding the sub clips, or None."""
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

    def shot_at(self, time: Time) -> Optional["FilmClip"]:
        """The shot playing at `time` (this clip's time), or None between shots."""
        for shot in self.shots:
            frame = shot.time_frame
            if frame.start.ticks <= time.ticks < frame.end.ticks:
                return shot
        return None

    def game_models(self, include_hidden: bool = False) -> List[Tuple[GameModel, Mat34]]:
        """Every game model in the scene with its world matrix; hidden ones
        too when asked, since animation can show them later."""
        scene = self.scene
        if scene is None:
            return []
        return [(node, world) for node, world in scene.walk(include_hidden=include_hidden)
                if isinstance(node, GameModel)]


class Track(View):
    """DmeTrack: an ordered row of clips."""
    TYPE = "DmeTrack"

    @property
    def clips(self) -> List[Clip]:
        """The clips on this track."""
        return [wrap(e) for e in self._elements("children")]

    @property
    def mute(self) -> bool:
        """True when the clip or track is muted."""
        return bool(self._get("mute", False))


class TrackGroup(View):
    """DmeTrackGroup: a named set of tracks."""
    TYPE = "DmeTrackGroup"

    @property
    def tracks(self) -> List[Track]:
        """The tracks in this group."""
        return [Track(e) for e in self._elements("tracks")]

    @property
    def visible(self) -> bool:
        """Whether the group is shown in the timeline."""
        return bool(self._get("visible", True))


# ---------------------------------------------------------------------------
#  Animation
# ---------------------------------------------------------------------------
class LogLayer(View):
    """DmeLogLayer: parallel arrays of times and values."""
    TYPE = "DmeLogLayer"

    @property
    def times(self) -> List[Time]:
        """Key times."""
        return list(self._get("times", []))

    @property
    def values(self) -> list:
        """Key values, parallel to `times`."""
        return list(self._get("values", []))


class Log(View):
    """DmeLog: the layers of one animated attribute."""
    TYPE = "DmeLog"

    @property
    def layers(self) -> List[LogLayer]:
        """The log's layers, base first."""
        return [LogLayer(e) for e in self._elements("layers")]

    @property
    def default_value(self):
        """Value used when `uses_default` is set."""
        return self._get("defaultvalue")

    @property
    def uses_default(self) -> bool:
        """True when the log ignores its keys."""
        return bool(self._get("usedefaultvalue", False))


class Channel(View):
    """Drives one attribute of one element from a log over time."""
    TYPE = "DmeChannel"

    @property
    def to_element(self) -> Optional[Element]:
        """The element written by the channel."""
        return self._get("toElement")

    @property
    def to_attribute(self) -> str:
        """The attribute written by the channel."""
        return str(self._get("toAttribute", ""))

    @property
    def from_element(self) -> Optional[Element]:
        """The element read by the channel."""
        return self._get("fromElement")

    @property
    def from_attribute(self) -> str:
        """The attribute read by the channel."""
        return str(self._get("fromAttribute", ""))

    @property
    def mode(self) -> int:
        """Channel mode: off, pass, record or play."""
        return int(self._get("mode", 0))

    @property
    def log(self) -> Optional[Log]:
        """The channel's log, or None."""
        return self._child("log", Log)


class AnimationSet(View):
    """DmeAnimationSet: a model or camera with its controls."""
    TYPE = "DmeAnimationSet"

    @property
    def game_model(self) -> Optional[GameModel]:
        """The set's game model, or None."""
        return self._child("gameModel", GameModel)

    @property
    def camera(self) -> Optional[Camera]:
        """The camera, or None."""
        return self._child("camera", Camera)

    @property
    def controls(self) -> List[Element]:
        """Control elements of the set."""
        return self._elements("controls")


# ---------------------------------------------------------------------------
#  The session
# ---------------------------------------------------------------------------
class Session(View):
    """The root of an SFM session document."""
    def __init__(self, document: DmxDocument) -> None:
        if document.root is None:
            raise ValueError("the document has no root element")
        super().__init__(document.root)
        self.document = document

    @property
    def is_session(self) -> bool:
        """True for an sfm_session document."""
        return self.document.format == "sfm_session" or "activeClip" in self.element

    @property
    def active_clip(self) -> Optional[FilmClip]:
        """The clip being edited, or None."""
        return self._child("activeClip", FilmClip)

    @property
    def clips(self) -> List[FilmClip]:
        """Every shot in the clip bin."""
        return [FilmClip(e) for e in self._elements("clipBin")]

    @property
    def settings(self) -> Optional[Element]:
        """The session settings element, or None."""
        return self._get("settings")

    @property
    def frame_rate(self) -> float:
        """Frames per second from the render settings; SFM's default 24 when unset."""
        settings = self.settings
        render = settings.get("renderSettings") if settings is not None else None
        rate = render.get("frameRate") if isinstance(render, Element) else None
        return float(rate) if rate else 24.0

    @property
    def movie_size(self) -> Tuple[int, int]:
        """Width and height from the movie settings; 1280 x 720 when unset."""
        settings = self.settings
        movie = settings.get("movieSettings") if settings is not None else None
        if isinstance(movie, Element):
            width, height = int(movie.get("width", 0) or 0), int(movie.get("height", 0) or 0)
            if width > 0 and height > 0:
                return width, height
        return 1280, 720

    def summary(self) -> str:
        """One line: name, active clip, shot count."""
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
    "DmeProjectedLight": ProjectedLight, "DmeModel": Dag,
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
