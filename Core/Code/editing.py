"""
Changing a session: undoable edits and keys in logs.

Every change to a document goes through an `UndoStack` as a command that
knows how to apply and revert itself. Commands are small and literal - set
this attribute, put this key in this log - so the stack can be replayed
exactly and a saved file reflects precisely what was done.

    stack = UndoStack()
    stack.push(SetAttribute(element, "position", (1, 2, 3)))
    stack.undo(); stack.redo()

Keys: a channel's log holds sorted times and values in its top layer;
`set_key` inserts or replaces the key at a time, which is what recording a
change at the time cursor means.
"""
from __future__ import annotations

from bisect import bisect_left
from typing import Any, Callable, List, Optional, Sequence

from Core.API.dmx import ARRAY_OFFSET, AttrType, Element, Time
from Core.API.session import Channel, Log

__all__ = ["Command", "SetAttribute", "SetKey", "Group", "UndoStack", "set_key", "remove_key",
           "top_layer", "value_type_of", "channel_index", "record_edit", "DrivenAttribute", "slot_of"]


class Command:
    """One reversible change."""
    label = "edit"

    def apply(self) -> None:
        raise NotImplementedError

    def revert(self) -> None:
        raise NotImplementedError


class SetAttribute(Command):
    """Set one attribute, or one slot of an array attribute."""

    def __init__(self, element: Element, name: str, value: Any, index: int = -1,
                 label: Optional[str] = None) -> None:
        self.element = element
        self.name = name
        self.index = index
        self.value = value
        attr = element.attribute(name)
        if attr is None:
            raise KeyError(f"{element!r} has no attribute {name!r}")
        self.old = attr.value[index] if index >= 0 else attr.value
        self.label = label or f"set {name}"

    def apply(self) -> None:
        _write(self.element, self.name, self.index, self.value)

    def revert(self) -> None:
        _write(self.element, self.name, self.index, self.old)


def _write(element: Element, name: str, index: int, value: Any) -> None:
    attr = element.attribute(name)
    if attr is None:
        return
    if index >= 0:
        attr.value[index] = value
    else:
        attr.value = value


class SetKey(Command):
    """Put a key into a log at a time (replacing one already there)."""

    def __init__(self, log: Log, time: Time, value: Any, label: Optional[str] = None) -> None:
        self.log = log
        self.time = time
        self.value = value
        self.label = label or f"key at {time.seconds:.3f}s"
        layer = top_layer(log)
        self.previous = _key_at(layer, time) if layer is not None else None

    def apply(self) -> None:
        set_key(self.log, self.time, self.value)

    def revert(self) -> None:
        if self.previous is None:
            remove_key(self.log, self.time)
        else:
            set_key(self.log, self.time, self.previous)


class Group(Command):
    """Several commands that undo as one."""

    def __init__(self, commands: Sequence[Command], label: str = "edit") -> None:
        self.commands = list(commands)
        self.label = label

    def apply(self) -> None:
        done = []
        try:
            for command in self.commands:
                command.apply()
                done.append(command)
        except Exception:
            for command in reversed(done):          # all or nothing
                command.revert()
            raise

    def revert(self) -> None:
        for command in reversed(self.commands):
            command.revert()


class UndoStack:
    def __init__(self, limit: int = 1000) -> None:
        self._done: List[Command] = []
        self._undone: List[Command] = []
        self.limit = limit
        #: called after any push, undo or redo
        self.changed: List[Callable[[], None]] = []
        #: the number of pushes since the last save; 0 means clean
        self._clean_at = 0

    def push(self, command: Command) -> None:
        """Apply and remember; a command that fails to apply is not kept."""
        command.apply()
        self._done.append(command)
        if len(self._done) > self.limit:
            del self._done[0]
            self._clean_at -= 1
        self._undone.clear()
        self._notify()

    def undo(self) -> Optional[Command]:
        if not self._done:
            return None
        command = self._done.pop()
        command.revert()
        self._undone.append(command)
        self._notify()
        return command

    def redo(self) -> Optional[Command]:
        if not self._undone:
            return None
        command = self._undone.pop()
        command.apply()
        self._done.append(command)
        self._notify()
        return command

    @property
    def can_undo(self) -> bool:
        return bool(self._done)

    @property
    def can_redo(self) -> bool:
        return bool(self._undone)

    @property
    def undo_label(self) -> str:
        return self._done[-1].label if self._done else ""

    @property
    def redo_label(self) -> str:
        return self._undone[-1].label if self._undone else ""

    @property
    def dirty(self) -> bool:
        return len(self._done) != self._clean_at

    def mark_clean(self) -> None:
        self._clean_at = len(self._done)
        self._notify()

    def clear(self) -> None:
        self._done.clear()
        self._undone.clear()
        self._clean_at = 0
        self._notify()

    def _notify(self) -> None:
        for callback in list(self.changed):
            callback()


# ---------------------------------------------------------------------------
#  Keys
# ---------------------------------------------------------------------------
def top_layer(log: Log) -> Optional[Element]:
    layers = log.element.get("layers")
    if isinstance(layers, list):
        for layer in reversed(layers):
            if isinstance(layer, Element):
                return layer
    return None


def _key_at(layer: Element, time: Time) -> Any:
    times = layer.get("times") or []
    values = layer.get("values") or []
    i = bisect_left([t.ticks for t in times], time.ticks)
    if i < len(times) and times[i].ticks == time.ticks and i < len(values):
        return values[i]
    return None


def set_key(log: Log, time: Time, value: Any) -> bool:
    """Insert or replace the key at `time` in the log's top layer."""
    layer = top_layer(log)
    if layer is None:
        return False
    times_attr = layer.attribute("times")
    values_attr = layer.attribute("values")
    if times_attr is None or values_attr is None:
        return False
    times = times_attr.value
    values = values_attr.value
    ticks = [t.ticks for t in times]
    i = bisect_left(ticks, time.ticks)
    if i < len(times) and times[i].ticks == time.ticks:
        values[i] = value
    else:
        times.insert(i, Time(time.ticks))
        values.insert(i, value)
    return True


def remove_key(log: Log, time: Time) -> bool:
    layer = top_layer(log)
    if layer is None:
        return False
    times = layer.get("times") or []
    values = layer.get("values") or []
    i = bisect_left([t.ticks for t in times], time.ticks)
    if i < len(times) and times[i].ticks == time.ticks:
        del times[i]
        if i < len(values):
            del values[i]
        return True
    return False


def value_type_of(log: Log) -> Optional[int]:
    layer = top_layer(log)
    if layer is None:
        return None
    attr = layer.attribute("values")
    if attr is None:
        return None
    return attr.type - ARRAY_OFFSET if attr.type > ARRAY_OFFSET else attr.type


# ---------------------------------------------------------------------------
#  Recording an edit at a time
# ---------------------------------------------------------------------------
class DrivenAttribute:
    """A channel that writes an attribute, with the clip it lives in."""

    __slots__ = ("channel", "clip")

    def __init__(self, channel: Channel, clip) -> None:
        self.channel = channel
        self.clip = clip


def channel_index(clip) -> dict:
    """(element id, attribute, index) -> DrivenAttribute for every channel of
    a clip's channel clips, so an edit can find the log to record into."""
    from Core.API.session import ChannelsClip
    out = {}
    for group in clip.track_groups:
        for track in group.tracks:
            for child in track.clips:
                if not isinstance(child, ChannelsClip):
                    continue
                for channel in child.channels:
                    target = channel.to_element
                    if target is None or not channel.to_attribute:
                        continue
                    key = (id(target), channel.to_attribute,
                           slot_of(target, channel.to_attribute, int(channel.element.get("toIndex", -1))))
                    out[key] = DrivenAttribute(channel, child)
    return out


def _read_slot(element: Element, name: str, slot: int) -> Any:
    attr = element.attribute(name)
    if attr is None:
        return None
    return attr.value[slot] if slot >= 0 and slot < len(attr.value) else attr.value


def slot_of(element: Element, name: str, index: int) -> int:
    """SFM writes toIndex 0 for scalars too; an index only means something
    for an array attribute, so a scalar's slot is always -1."""
    attr = element.attribute(name)
    if attr is None or not attr.is_array:
        return -1
    return index


def record_edit(index: dict, element: Element, name: str, value: Any, shot_time: Time,
                slot: int = -1, label: Optional[str] = None, selection=None) -> Command:
    """The command for changing `element.name` at a moment of the shot.

    When a channel drives the attribute, the value also becomes a key in
    the channel's log at the clip's local time - otherwise the next
    evaluation would put the old value back. With a time `selection` (in
    shot time) the difference is instead spread over the selection as the
    motion editor does. The channel's control gets the value too, so the
    animation set's slider agrees.
    """
    slot = slot_of(element, name, slot)
    old = _read_slot(element, name, slot)
    commands: List[Command] = [SetAttribute(element, name, value, slot, label)]
    driven = index.get((id(element), name, slot))
    if driven is not None:
        log = driven.channel.log
        if log is not None and top_layer(log) is not None:
            if selection is not None and top_layer(log).get("times"):
                from .animation import sample_log
                from .motion import OffsetOverSelection, offset_between
                kind = value_type_of(log)
                # the offset is from what the log says at the cursor, which is what was seen
                found, at_cursor = sample_log(log, driven.clip.time_frame.to_child_time(shot_time))
                offset = offset_between(kind, at_cursor if found else old, value)
                if offset is not None:
                    commands.append(OffsetOverSelection(
                        log, kind, selection.mapped(driven.clip.time_frame), offset))
            else:
                clip_time = driven.clip.time_frame.to_child_time(shot_time)
                commands.append(SetKey(log, clip_time, value))
        source = driven.channel.from_element
        from_attribute = driven.channel.from_attribute
        if source is not None and from_attribute and source.attribute(from_attribute) is not None:
            from_index = slot_of(source, from_attribute, int(driven.channel.element.get("fromIndex", -1)))
            commands.append(SetAttribute(source, from_attribute, value, from_index))
    if len(commands) == 1:
        return commands[0]
    return Group(commands, label or f"set {name}")
