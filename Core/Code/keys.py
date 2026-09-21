"""Editing a log's keys the way the graph editor does: move, insert, delete.

A log layer is three parallel arrays - `times`, `values` and (in SFM's
files, present but usually empty) `curvetypes`.  Every edit here is one
command that swaps the whole top layer for a new one and back, so undo is
exact whatever the edit did to the ordering.

Values are edited per component: a vector log has one curve per axis, a
quaternion log shows as pitch / yaw / roll and a float log is one curve.
`components()` says how a log's values split into curves and
`with_component()` puts an edited curve value back into a whole value.
"""
from __future__ import annotations

from typing import Any, Callable, List, Optional, Sequence, Tuple

from Core.API.dmx import ARRAY_OFFSET, AttrType, Time
from Core.API.session import Log

from .animation import _layer_keys
from .editing import Command, top_layer, value_type_of
from .transform import angles_from_quaternion, quaternion_from_angles

__all__ = ["ReplaceKeys", "components", "component_value", "with_component",
           "move_keys", "insert_key", "delete_keys", "key_count"]

_AXES = ("X", "Y", "Z", "W")
_ANGLES = ("pitch", "yaw", "roll")


# ---------------------------------------------------------------------------
#  Curves of a log
# ---------------------------------------------------------------------------
def components(kind: Optional[int]) -> List[str]:
    """The curve names a log of this value type shows: one per component."""
    if kind in (AttrType.FLOAT, AttrType.INT, AttrType.BOOL, AttrType.TIME):
        return ["value"]
    if kind == AttrType.VECTOR2:
        return list(_AXES[:2])
    if kind == AttrType.VECTOR3:
        return list(_AXES[:3])
    if kind == AttrType.VECTOR4:
        return list(_AXES)
    if kind == AttrType.QANGLE:
        return list(_ANGLES)
    if kind == AttrType.QUATERNION:
        return list(_ANGLES)
    if kind == AttrType.COLOR:
        return ["R", "G", "B", "A"]
    return []


def component_value(kind: Optional[int], value: Any, component: int) -> float:
    """One curve's number out of a whole log value."""
    if kind == AttrType.QUATERNION:
        return float(angles_from_quaternion(tuple(value))[component])
    if kind == AttrType.TIME:
        return value.seconds
    if kind in (AttrType.FLOAT, AttrType.INT, AttrType.BOOL):
        return float(value)
    return float(value[component])


def with_component(kind: Optional[int], value: Any, component: int, number: float) -> Any:
    """The whole log value with one curve's number replaced."""
    if kind == AttrType.FLOAT:
        return float(number)
    if kind == AttrType.INT:
        return int(round(number))
    if kind == AttrType.BOOL:
        return number >= 0.5
    if kind == AttrType.TIME:
        return Time.from_seconds(number)
    if kind == AttrType.QUATERNION:
        angles = list(angles_from_quaternion(tuple(value)))
        angles[component] = float(number)
        return quaternion_from_angles(*angles)
    if kind == AttrType.COLOR:
        out = list(value)
        out[component] = max(0, min(255, int(round(number))))
        return tuple(out)
    out = list(value)
    out[component] = float(number)
    return tuple(out)


def key_count(log: Log) -> int:
    """Number of keys in the log's top layer."""
    layer = top_layer(log)
    return len(layer.get("times") or []) if layer is not None else 0


# ---------------------------------------------------------------------------
#  The one command
# ---------------------------------------------------------------------------
class ReplaceKeys(Command):
    """Swap a layer's key arrays for new ones; revert puts the old ones back."""

    def __init__(self, log: Log, times: Sequence[Time], values: Sequence[Any],
                 curvetypes: Optional[Sequence[int]] = None, label: str = "edit keys") -> None:
        self.log = log
        self.layer = top_layer(log)
        self.label = label
        layer = self.layer
        self.old_times: List[Time] = list(layer.get("times") or []) if layer is not None else []
        self.old_values: List[Any] = list(layer.get("values") or []) if layer is not None else []
        self.old_types: Optional[List[int]] = None
        if layer is not None and layer.attribute("curvetypes") is not None:
            self.old_types = list(layer.get("curvetypes") or [])
        self.new_times = list(times)
        self.new_values = list(values)
        self.new_types = list(curvetypes) if curvetypes is not None else None

    def apply(self) -> None:
        """Write the new arrays."""
        self._write(self.new_times, self.new_values, self.new_types)

    def revert(self) -> None:
        """Write the old arrays back."""
        self._write(self.old_times, self.old_values, self.old_types)

    def _write(self, times: List[Time], values: List[Any], types: Optional[List[int]]) -> None:
        layer = self.layer
        if layer is None:
            return
        layer.set("times", AttrType.TIME + ARRAY_OFFSET, list(times))
        values_attr = layer.attribute("values")
        kind = values_attr.type if values_attr is not None else (value_type_of(self.log) or AttrType.FLOAT) + ARRAY_OFFSET
        layer.set("values", kind, list(values))
        if types is not None:
            layer.set("curvetypes", AttrType.INT + ARRAY_OFFSET, list(types))


def _arrays(log: Log) -> Tuple[List[Time], List[Any], Optional[List[int]]]:
    layer = top_layer(log)
    if layer is None:
        return [], [], None
    times = list(layer.get("times") or [])
    values = list(layer.get("values") or [])
    types = None
    if layer.attribute("curvetypes") is not None:
        types = list(layer.get("curvetypes") or [])
        if len(types) != len(times):             # SFM leaves this empty: keep it that way
            types = [] if not types else types[:len(times)] + [0] * (len(times) - len(types))
    n = min(len(times), len(values))
    return times[:n], values[:n], types


def _rebuilt(entries: List[Tuple[int, Any, int]], types_present: bool, keep_types: bool
             ) -> Tuple[List[Time], List[Any], Optional[List[int]]]:
    """Sort by time; a later entry at the same tick wins (the moved key covers the one it landed on)."""
    entries = sorted(entries, key=lambda e: e[0])
    times: List[Time] = []
    values: List[Any] = []
    types: List[int] = []
    for tick, value, ctype in entries:
        if times and times[-1].ticks == tick:
            values[-1] = value
            types[-1] = ctype
            continue
        times.append(Time(tick))
        values.append(value)
        types.append(ctype)
    if not types_present:
        return times, values, None
    return times, values, (types if keep_types else [])


# ---------------------------------------------------------------------------
#  Edits
# ---------------------------------------------------------------------------
def move_keys(log: Log, indices: Sequence[int], delta_ticks: int,
              change: Optional[Callable[[Any], Any]] = None, label: str = "move keys") -> Optional[ReplaceKeys]:
    """Shift the keys at `indices` by `delta_ticks`, passing each value through `change`."""
    times, values, types = _arrays(log)
    if not times:
        return None
    chosen = set(i for i in indices if 0 <= i < len(times))
    if not chosen:
        return None
    keep_types = types is not None and len(types) == len(times)
    entries = []
    for i, (t, v) in enumerate(zip(times, values)):
        ctype = types[i] if keep_types else 0
        if i in chosen:
            entries.append((t.ticks + delta_ticks, change(v) if change is not None else v, ctype))
        else:
            entries.append((t.ticks, v, ctype))
    # a moved key landing on a fixed one must win: put moved entries last among equals
    entries = [e for i, e in enumerate(entries) if i not in chosen] + [e for i, e in enumerate(entries) if i in chosen]
    new_times, new_values, new_types = _rebuilt(entries, types is not None, keep_types)
    return ReplaceKeys(log, new_times, new_values, new_types, label)


def insert_key(log: Log, time: Time, value: Any = None, label: str = "insert key") -> Optional[ReplaceKeys]:
    """A key at `time` with the log's value there (or `value`); an existing key is replaced."""
    layer = top_layer(log)
    if layer is None:
        return None
    times, values, types = _arrays(log)
    if value is None:
        keys = _layer_keys(layer)
        if keys is None:
            return None
        value = keys.sample(time)
    keep_types = types is not None and len(types) == len(times)
    entries = [(t.ticks, v, types[i] if keep_types else 0) for i, (t, v) in enumerate(zip(times, values))]
    entries.append((time.ticks, value, 0))
    new_times, new_values, new_types = _rebuilt(entries, types is not None, keep_types)
    return ReplaceKeys(log, new_times, new_values, new_types, label)


def delete_keys(log: Log, indices: Sequence[int], label: str = "delete keys") -> Optional[ReplaceKeys]:
    """A command deleting the keys at `indices`; None when nothing changes."""
    times, values, types = _arrays(log)
    chosen = set(i for i in indices if 0 <= i < len(times))
    if not chosen or len(chosen) >= len(times):          # a log keeps at least one key
        return None
    keep_types = types is not None and len(types) == len(times)
    entries = [(t.ticks, v, types[i] if keep_types else 0)
               for i, (t, v) in enumerate(zip(times, values)) if i not in chosen]
    new_times, new_values, new_types = _rebuilt(entries, types is not None, keep_types)
    return ReplaceKeys(log, new_times, new_values, new_types, label)
