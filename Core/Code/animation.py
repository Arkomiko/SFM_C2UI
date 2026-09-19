"""
Evaluating a session at a moment in time.

Animation in a session is a set of *channels*. Each one reads a log - keys
sorted by time with a value each - and writes the interpolated value into
one attribute of one element: a bone's position, a flex weight, a camera's
field of view. Evaluating the session at time t means running every channel
whose clip covers t, after mapping t through each clip's time frame; the
elements then hold the state of that moment and the scene can be rebuilt
from them. That is exactly what Source Filmmaker does, so a session
evaluated here and saved is one SFM would show the same way.

    evaluator = Evaluator()
    evaluator.evaluate(session.active_clip, Time.from_seconds(3.2))
    # every DmeTransform, flex weight and camera field now holds its value at 3.2 s

Interpolation follows the log's type: floats and vectors blend linearly,
quaternions by shortest arc, integers, booleans and strings hold the last
key. Time before the first key gives the first value, after the last key
the last one.
"""
from __future__ import annotations

from bisect import bisect_right
from typing import Any, Dict, List, Optional, Sequence, Tuple

from Core.API.dmx import ARRAY_OFFSET, AttrType, Element, Time
from Core.API.session import Channel, ChannelsClip, Clip, FilmClip, Log

from .operators import OperatorRunner
from .transform import quaternion_slerp

__all__ = ["Evaluator", "sample_log", "interpolate"]

#: channel modes as SFM numbers them
MODE_OFF = 0
MODE_PASS = 1
MODE_PLAY = 2
MODE_RECORD = 3


def interpolate(kind: int, a: Any, b: Any, t: float) -> Any:
    """Blend two log values of a type; a step for anything not continuous."""
    if kind == AttrType.FLOAT:
        return a + (b - a) * t
    if kind == AttrType.QUATERNION:
        return quaternion_slerp(tuple(a), tuple(b), t)
    if kind in (AttrType.VECTOR2, AttrType.VECTOR3, AttrType.VECTOR4, AttrType.QANGLE):
        return tuple(x + (y - x) * t for x, y in zip(a, b))
    if kind == AttrType.COLOR:
        return tuple(int(round(x + (y - x) * t)) for x, y in zip(a, b))
    if kind == AttrType.TIME:
        return Time(round(a.ticks + (b.ticks - a.ticks) * t))
    return a


class _Keys:
    """A log layer's keys, ready for lookup."""

    __slots__ = ("ticks", "values", "kind")

    def __init__(self, times: Sequence[Time], values: Sequence[Any], kind: int) -> None:
        self.ticks: List[int] = [t.ticks for t in times]
        self.values = list(values)
        self.kind = kind

    def sample(self, time: Time) -> Any:
        ticks = self.ticks
        i = bisect_right(ticks, time.ticks)
        if i == 0:
            return self.values[0]
        if i >= len(ticks):
            return self.values[-1]
        t0, t1 = ticks[i - 1], ticks[i]
        if t1 == t0:
            return self.values[i]
        return interpolate(self.kind, self.values[i - 1], self.values[i],
                           (time.ticks - t0) / (t1 - t0))


def _layer_keys(layer: Element) -> Optional[_Keys]:
    times = layer.get("times")
    values_attr = layer.attribute("values")
    if not times or values_attr is None or not values_attr.value:
        return None
    kind = values_attr.type - ARRAY_OFFSET if values_attr.type > ARRAY_OFFSET else values_attr.type
    count = min(len(times), len(values_attr.value))
    return _Keys(times[:count], values_attr.value[:count], kind)


def sample_log(log: Log, time: Time, cache: Optional[Dict[int, Optional[_Keys]]] = None) -> Tuple[bool, Any]:
    """The log's value at `time`.  Returns (found, value): the topmost layer
    with keys is used; with none, the default value if the log says so."""
    for layer in reversed(log.element.get("layers") or []):
        if not isinstance(layer, Element):
            continue
        keys = None
        if cache is not None:
            keys = cache.get(id(layer))
            if keys is None and id(layer) not in cache:
                keys = _layer_keys(layer)
                cache[id(layer)] = keys
        else:
            keys = _layer_keys(layer)
        if keys is not None:
            return True, keys.sample(time)
    if log.uses_default and "defaultvalue" in log.element:
        return True, log.default_value
    return False, None


class Evaluator:
    """Runs a clip's channels for a time and writes their results.

    Keys are cached per log layer between calls; call `invalidate()` after
    editing a log.
    """

    def __init__(self) -> None:
        self._cache: Dict[int, Optional[_Keys]] = {}
        self._runners: Dict[int, OperatorRunner] = {}
        self.channels_run = 0
        self.operators_run = 0
        self.errors: List[str] = []

    def invalidate(self) -> None:
        self._cache.clear()
        self._runners.clear()

    # -- clips -----------------------------------------------------------------------
    def evaluate(self, clip: Clip, time: Time) -> None:
        """Evaluate `clip` at its own local `time`, then whichever of its
        shots covers that time at the shot's local time."""
        self.channels_run = 0
        self.operators_run = 0
        self._evaluate_clip(clip, time, depth=0)

    def _evaluate_clip(self, clip: Clip, time: Time, depth: int) -> None:
        if depth > 8:
            return
        channel_clips = [(child, child.time_frame.to_child_time(time))
                         for group in clip.track_groups
                         for track in group.tracks if not track.mute
                         for child in track.clips
                         if isinstance(child, ChannelsClip) and not child.mute]
        for child, child_time in channel_clips:
            self._evaluate_channels(child, child_time)
        if isinstance(clip, FilmClip):
            self._run_flex_operators(clip)
            if clip.animation_sets:
                # expressions and rig constraints, then the channels that carry
                # their results onward
                runner = self._runners.get(id(clip.element))
                if runner is None:
                    runner = OperatorRunner(clip)
                    self._runners[id(clip.element)] = runner
                runner.run(time)
                self.operators_run += runner.operators_run
                if runner.errors:
                    self.errors.extend(runner.errors[-5:])
                    runner.errors.clear()
                for child, child_time in channel_clips:
                    for channel in child.channels:
                        if channel.mode == MODE_PASS:
                            self.evaluate_channel(channel, child_time)
            for shot in clip.shots:
                frame = shot.time_frame
                if frame.start.ticks <= time.ticks < frame.end.ticks:
                    self._evaluate_clip(shot, frame.to_child_time(time), depth + 1)
                    break

    @staticmethod
    def _run_flex_operators(clip: FilmClip) -> None:
        """A DmeGlobalFlexControllerOperator carries a face control's value;
        the operator copies it into its game model's flexWeights slot, which is
        what the model reads. Matching is by name, since a model may have
        gained or lost controls since the session was made."""
        scene = clip.scene
        if scene is None:
            return
        for node, _world, _visible in scene.walk_visibility():
            names = node.element.get("flexnames")
            weights = node.element.attribute("flexWeights")
            operators = node.element.get("globalFlexControllers")
            if not names or weights is None or not operators:
                continue
            slots = {name: i for i, name in enumerate(names)}
            values = weights.value
            for op in operators:
                if not isinstance(op, Element):
                    continue
                i = slots.get(op.name)
                value = op.get("flexWeight")
                if i is not None and i < len(values) and isinstance(value, (int, float)):
                    values[i] = float(value)

    def _evaluate_channels(self, clip: ChannelsClip, time: Time) -> None:
        for channel in clip.channels:
            self.evaluate_channel(channel, time)

    # -- channels --------------------------------------------------------------------
    def evaluate_channel(self, channel: Channel, time: Time) -> bool:
        mode = channel.mode
        if mode == MODE_OFF:
            return False
        target = channel.to_element
        attribute = channel.to_attribute
        if target is None or not attribute:
            return False
        found = False
        value: Any = None
        if mode != MODE_PASS:
            log = channel.log
            if log is not None:
                found, value = sample_log(log, time, self._cache)
        if not found:
            source = channel.from_element
            if source is None or not channel.from_attribute:
                return False
            value = _read(source, channel.from_attribute, int(channel.element.get("fromIndex", -1)))
            if value is None:
                return False
        self.channels_run += 1
        return _write(target, attribute, int(channel.element.get("toIndex", -1)), value)


def _read(element: Element, name: str, index: int) -> Any:
    attr = element.attribute(name)
    if attr is None:
        return None
    if attr.is_array:
        return attr.value[index] if 0 <= index < len(attr.value) else None
    return attr.value


def _write(element: Element, name: str, index: int, value: Any) -> bool:
    attr = element.attribute(name)
    if attr is None:
        return False
    if attr.is_array:
        if 0 <= index < len(attr.value):
            attr.value[index] = _coerce(attr.type - ARRAY_OFFSET, value)
            return True
        return False
    attr.value = _coerce(attr.type, value)
    return True


def _coerce(kind: int, value: Any) -> Any:
    """Keep the attribute's own type: a float log driving an int attribute
    must not turn it into a float, or the file would change shape."""
    if kind == AttrType.INT and not isinstance(value, int):
        return int(round(value))
    if kind == AttrType.FLOAT and isinstance(value, int):
        return float(value)
    if kind == AttrType.BOOL:
        return bool(value)
    if kind in (AttrType.VECTOR2, AttrType.VECTOR3, AttrType.VECTOR4, AttrType.QANGLE,
                AttrType.QUATERNION, AttrType.COLOR) and not isinstance(value, tuple):
        return tuple(value)
    return value
