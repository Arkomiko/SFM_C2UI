"""
The motion editor's time selection: a change applied over a span of time.

A time selection has a hold range, where a change applies in full, and a
falloff on either side, where it fades to nothing along an interpolator
curve. Applying an offset over it means: for every moment inside, the log's
value becomes `value + offset * weight(t)`. SFM keeps the shape of the
falloff by resampling the log there at a fixed interval, and so does this.

    selection = TimeSelection.from_element(session.settings["timeSelection"])
    command = OffsetOverSelection(log, kind, selection_in_log_time, offset)
    undo.push(command)

Times in a `TimeSelection` are whatever the caller says; the session stores
them in sequence time, and a log lives in its channel clip's time, so the
caller maps the selection through the clip first (`mapped`).
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Sequence, Tuple

from Core.API.dmx import ARRAY_OFFSET, AttrType, Element, Time
from Core.API.session import Log, TimeFrame

from .animation import _layer_keys, interpolate
from .editing import Command, top_layer
from .transform import quaternion_multiply, quaternion_normalize, quaternion_slerp

__all__ = ["TimeSelection", "OffsetOverSelection", "INFINITE", "weight_curve", "offset_value",
           "offset_between"]

#: what SFM writes for "no bound on this side"
INFINITE = Time(2147483647)

# interpolator types, as SFM numbers them
INTERP_DEFAULT = 0
INTERP_EASE_IN = 2
INTERP_EASE_OUT = 3
INTERP_EASE_INOUT = 4
INTERP_LINEAR = 6
INTERP_HOLD = 13


def _seconds(value: Any) -> float:
    """A duration stored as a Time (sessions do) or a number."""
    if isinstance(value, Time):
        return value.seconds
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.01


def weight_curve(t: float, interpolator: int) -> float:
    """0..1 in, 0..1 out along the interpolator's shape."""
    t = 0.0 if t < 0.0 else 1.0 if t > 1.0 else t
    if interpolator == INTERP_EASE_IN:
        return t * t
    if interpolator == INTERP_EASE_OUT:
        return 1.0 - (1.0 - t) * (1.0 - t)
    if interpolator == INTERP_EASE_INOUT:
        return t * t * (3.0 - 2.0 * t)
    if interpolator == INTERP_HOLD:
        return 1.0 if t >= 1.0 else 0.0
    return t


@dataclass
class TimeSelection:
    falloff_left: Time = Time(-INFINITE.ticks)
    hold_left: Time = Time(-INFINITE.ticks)
    hold_right: Time = INFINITE
    falloff_right: Time = INFINITE
    interpolator_left: int = INTERP_EASE_INOUT
    interpolator_right: int = INTERP_EASE_INOUT
    enabled: bool = True
    #: seconds between samples where the falloff reshapes the log
    resample_interval: float = 0.01

    @classmethod
    def from_element(cls, element: Element) -> "TimeSelection":
        return cls(
            falloff_left=element.get("falloff_left", Time(-INFINITE.ticks)),
            hold_left=element.get("hold_left", Time(-INFINITE.ticks)),
            hold_right=element.get("hold_right", INFINITE),
            falloff_right=element.get("falloff_right", INFINITE),
            interpolator_left=int(element.get("interpolator_left", INTERP_EASE_INOUT)),
            interpolator_right=int(element.get("interpolator_right", INTERP_EASE_INOUT)),
            enabled=bool(element.get("enabled", False)),
            resample_interval=_seconds(element.get("resampleinterval", 0.01)),
        )

    def write(self, element: Element) -> None:
        element.set("falloff_left", AttrType.TIME, self.falloff_left)
        element.set("hold_left", AttrType.TIME, self.hold_left)
        element.set("hold_right", AttrType.TIME, self.hold_right)
        element.set("falloff_right", AttrType.TIME, self.falloff_right)
        element.set("interpolator_left", AttrType.INT, self.interpolator_left)
        element.set("interpolator_right", AttrType.INT, self.interpolator_right)
        element.set("enabled", AttrType.BOOL, self.enabled)

    @property
    def is_infinite(self) -> bool:
        return (self.falloff_left.ticks <= -INFINITE.ticks and self.falloff_right.ticks >= INFINITE.ticks)

    def weight(self, time: Time) -> float:
        t = time.ticks
        if t < self.falloff_left.ticks or t > self.falloff_right.ticks:
            return 0.0
        if t < self.hold_left.ticks:
            span = self.hold_left.ticks - self.falloff_left.ticks
            return weight_curve((t - self.falloff_left.ticks) / span, self.interpolator_left) if span > 0 else 1.0
        if t > self.hold_right.ticks:
            span = self.falloff_right.ticks - self.hold_right.ticks
            return weight_curve((self.falloff_right.ticks - t) / span, self.interpolator_right) if span > 0 else 1.0
        return 1.0

    def mapped(self, frame: TimeFrame) -> "TimeSelection":
        """The same selection expressed in a clip's local time."""
        def convert(time: Time) -> Time:
            if abs(time.ticks) >= INFINITE.ticks:
                return time
            return frame.to_child_time(time)
        return TimeSelection(convert(self.falloff_left), convert(self.hold_left),
                             convert(self.hold_right), convert(self.falloff_right),
                             self.interpolator_left, self.interpolator_right, self.enabled,
                             self.resample_interval)


def offset_value(kind: int, value: Any, offset: Any, weight: float) -> Any:
    """`value` moved by `offset` scaled to `weight`, by type."""
    if weight <= 0.0:
        return value
    if kind == AttrType.FLOAT:
        return value + offset * weight
    if kind == AttrType.INT:
        return int(round(value + offset * weight))
    if kind in (AttrType.VECTOR2, AttrType.VECTOR3, AttrType.VECTOR4, AttrType.QANGLE):
        return tuple(v + o * weight for v, o in zip(value, offset))
    if kind == AttrType.QUATERNION:
        # offset is a rotation to apply on top; a fraction of it by slerp from identity
        part = quaternion_slerp((0.0, 0.0, 0.0, 1.0), tuple(offset), weight)
        return quaternion_normalize(quaternion_multiply(part, tuple(value)))
    if kind == AttrType.COLOR:
        return tuple(max(0, min(255, int(round(v + o * weight)))) for v, o in zip(value, offset))
    return value if weight < 1.0 else offset


def offset_between(kind: int, old: Any, new: Any) -> Any:
    """The offset that takes `old` to `new`, in the form offset_value applies."""
    if old is None or new is None:
        return None
    if kind in (AttrType.FLOAT, AttrType.INT):
        return new - old
    if kind in (AttrType.VECTOR2, AttrType.VECTOR3, AttrType.VECTOR4, AttrType.QANGLE, AttrType.COLOR):
        return tuple(n - o for n, o in zip(new, old))
    if kind == AttrType.QUATERNION:
        from .transform import quaternion_inverse
        return quaternion_normalize(quaternion_multiply(tuple(new), quaternion_inverse(tuple(old))))
    return new


class OffsetOverSelection(Command):
    """Move a log's values by an offset, weighted by a time selection.

    Keys are added at the selection's four edges so nothing outside moves;
    inside the falloffs the log is resampled at the selection's interval so
    the curve's shape is kept; keys in the hold get the full offset.
    """

    def __init__(self, log: Log, kind: int, selection: TimeSelection, offset: Any,
                 label: Optional[str] = None) -> None:
        self.log = log
        self.kind = kind
        self.selection = selection
        self.offset = offset
        self.label = label or "motion edit"
        layer = top_layer(log)
        self.layer = layer
        self.old_times: List[Time] = list(layer.get("times") or []) if layer is not None else []
        self.old_values: List[Any] = list(layer.get("values") or []) if layer is not None else []
        self.new_times, self.new_values = self._compute() if layer is not None else ([], [])

    def _compute(self) -> Tuple[List[Time], List[Any]]:
        keys = _layer_keys(self.layer)
        sel = self.selection
        times: List[int] = [t.ticks for t in self.old_times]
        values: List[Any] = list(self.old_values)
        if keys is None:
            return list(self.old_times), values
        sample = keys.sample

        wanted = set(times)
        # edges, where they are finite
        for edge in (sel.falloff_left, sel.hold_left, sel.hold_right, sel.falloff_right):
            if abs(edge.ticks) < INFINITE.ticks:
                wanted.add(edge.ticks)
        # a falloff of no width is a step: pin the outside one tick beyond the edge
        if abs(sel.falloff_left.ticks) < INFINITE.ticks and sel.falloff_left.ticks == sel.hold_left.ticks:
            wanted.add(sel.falloff_left.ticks - 1)
        if abs(sel.falloff_right.ticks) < INFINITE.ticks and sel.falloff_right.ticks == sel.hold_right.ticks:
            wanted.add(sel.falloff_right.ticks + 1)
        # resample the falloffs
        step = max(1, int(round(sel.resample_interval * Time.PER_SECOND)))
        for lo, hi in ((sel.falloff_left, sel.hold_left), (sel.hold_right, sel.falloff_right)):
            if abs(lo.ticks) >= INFINITE.ticks or abs(hi.ticks) >= INFINITE.ticks or hi.ticks <= lo.ticks:
                continue
            t = lo.ticks + step
            while t < hi.ticks:
                wanted.add(t)
                t += step
        ordered = sorted(wanted)
        new_times = [Time(t) for t in ordered]
        new_values = []
        for t in ordered:
            base = sample(Time(t))
            new_values.append(offset_value(self.kind, base, self.offset, sel.weight(Time(t))))
        return new_times, new_values

    def apply(self) -> None:
        self._write(self.new_times, self.new_values)

    def revert(self) -> None:
        self._write(self.old_times, self.old_values)

    def _write(self, times: List[Time], values: List[Any]) -> None:
        if self.layer is None:
            return
        self.layer.set("times", AttrType.TIME + ARRAY_OFFSET, list(times))
        values_attr = self.layer.attribute("values")
        kind = values_attr.type if values_attr is not None else self.kind + ARRAY_OFFSET
        self.layer.set("values", kind, list(values))
