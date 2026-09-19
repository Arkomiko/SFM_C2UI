"""
Undo, keys and recording an edit at a time.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Core.API.dmx import ARRAY_OFFSET, AttrType, DmxDocument, Element, Time
from Core.API.session import FilmClip, Log
from Core.Code.animation import Evaluator
from Core.Code.editing import (Group, SetAttribute, SetKey, UndoStack, channel_index, record_edit,
                               remove_key, set_key, top_layer)


def _log(doc, times, values):
    layer = doc.add(Element("DmeFloatLogLayer", "layer"))
    layer.set("times", AttrType.TIME + ARRAY_OFFSET, [Time.from_seconds(t) for t in times])
    layer.set("values", AttrType.FLOAT + ARRAY_OFFSET, list(values))
    log = doc.add(Element("DmeFloatLog", "log"))
    log.set("layers", AttrType.ELEMENT + ARRAY_OFFSET, [layer])
    return log


# ------------------------------------------------------------------- undo
def test_set_attribute_applies_and_reverts():
    doc = DmxDocument()
    e = doc.add(Element("DmElement", "e"))
    e.set("x", AttrType.FLOAT, 1.0)
    e.set("list", AttrType.FLOAT + ARRAY_OFFSET, [0.0, 0.0])
    stack = UndoStack()
    stack.push(SetAttribute(e, "x", 2.0))
    stack.push(SetAttribute(e, "list", 5.0, index=1))
    assert e["x"] == 2.0 and e["list"] == [0.0, 5.0] and stack.dirty
    assert stack.undo_label == "set list"
    stack.undo()
    assert e["list"] == [0.0, 0.0]
    stack.undo()
    assert e["x"] == 1.0 and not stack.dirty and not stack.can_undo
    stack.redo(); stack.redo()
    assert e["x"] == 2.0 and e["list"] == [0.0, 5.0] and not stack.can_redo


def test_a_new_push_forgets_the_redo_branch_and_clean_tracks_saves():
    doc = DmxDocument()
    e = doc.add(Element("DmElement", "e"))
    e.set("x", AttrType.INT, 0)
    stack = UndoStack()
    stack.push(SetAttribute(e, "x", 1))
    stack.undo()
    stack.push(SetAttribute(e, "x", 2))
    assert not stack.can_redo and e["x"] == 2
    stack.mark_clean()
    assert not stack.dirty
    stack.undo()
    assert stack.dirty                                  # differs from what was saved
    stack.redo()
    assert not stack.dirty


def test_unknown_attribute_is_refused():
    e = Element("DmElement", "e")
    try:
        SetAttribute(e, "nothing", 1)
    except KeyError:
        return
    raise AssertionError("set an attribute that does not exist")


def test_changed_callbacks_fire():
    doc = DmxDocument()
    e = doc.add(Element("DmElement", "e"))
    e.set("x", AttrType.INT, 0)
    stack = UndoStack()
    calls = []
    stack.changed.append(lambda: calls.append(1))
    stack.push(SetAttribute(e, "x", 1)); stack.undo(); stack.redo(); stack.mark_clean()
    assert len(calls) == 4


# ------------------------------------------------------------------- keys
def test_set_key_inserts_in_order_and_replaces():
    doc = DmxDocument()
    log = Log(_log(doc, [0.0, 2.0], [0.0, 20.0]))
    assert set_key(log, Time.from_seconds(1.0), 10.0)
    layer = top_layer(log)
    assert [t.seconds for t in layer["times"]] == [0.0, 1.0, 2.0] and layer["values"] == [0.0, 10.0, 20.0]
    set_key(log, Time.from_seconds(1.0), 11.0)
    assert layer["values"] == [0.0, 11.0, 20.0]
    assert remove_key(log, Time.from_seconds(1.0)) and not remove_key(log, Time.from_seconds(1.0))
    assert layer["values"] == [0.0, 20.0]


def test_set_key_command_reverts_to_absence_or_the_old_value():
    doc = DmxDocument()
    log = Log(_log(doc, [0.0, 2.0], [0.0, 20.0]))
    stack = UndoStack()
    stack.push(SetKey(log, Time.from_seconds(1.0), 10.0))
    stack.push(SetKey(log, Time.from_seconds(2.0), 99.0))
    assert top_layer(log)["values"] == [0.0, 10.0, 99.0]
    stack.undo()
    assert top_layer(log)["values"] == [0.0, 10.0, 20.0]
    stack.undo()
    assert top_layer(log)["values"] == [0.0, 20.0]


# ------------------------------------------------------------------- recording
def _shot():
    doc = DmxDocument()
    bone = doc.add(Element("DmeTransform", "bone"))
    bone.set("position", AttrType.VECTOR3, (0.0, 0.0, 0.0))
    control = doc.add(Element("DmeTransformControl", "ctl"))
    control.set("valuePosition", AttrType.VECTOR3, (0.0, 0.0, 0.0))
    layer = doc.add(Element("DmeVector3LogLayer", "l"))
    layer.set("times", AttrType.TIME + ARRAY_OFFSET, [Time.from_seconds(0.0), Time.from_seconds(4.0)])
    layer.set("values", AttrType.VECTOR3 + ARRAY_OFFSET, [(0.0, 0.0, 0.0), (0.0, 0.0, 40.0)])
    log = doc.add(Element("DmeVector3Log", "log"))
    log.set("layers", AttrType.ELEMENT + ARRAY_OFFSET, [layer])
    ch = doc.add(Element("DmeChannel", "ch"))
    ch.set("toElement", AttrType.ELEMENT, bone); ch.set("toAttribute", AttrType.STRING, "position")
    ch.set("toIndex", AttrType.INT, 0)                # SFM writes 0 for scalars too
    ch.set("fromElement", AttrType.ELEMENT, control); ch.set("fromAttribute", AttrType.STRING, "valuePosition")
    ch.set("fromIndex", AttrType.INT, 0)
    ch.set("mode", AttrType.INT, 3); ch.set("log", AttrType.ELEMENT, log)
    cclip = doc.add(Element("DmeChannelsClip", "channels"))
    frame = doc.add(Element("DmeTimeFrame", "f"))
    frame.set("start", AttrType.TIME, Time(0)); frame.set("duration", AttrType.TIME, Time.from_seconds(4))
    frame.set("offset", AttrType.TIME, Time.from_seconds(1.0)); frame.set("scale", AttrType.FLOAT, 1.0)
    cclip.set("timeFrame", AttrType.ELEMENT, frame)
    cclip.set("channels", AttrType.ELEMENT + ARRAY_OFFSET, [ch])
    track = doc.add(Element("DmeTrack", "t")); track.set("children", AttrType.ELEMENT + ARRAY_OFFSET, [cclip])
    group = doc.add(Element("DmeTrackGroup", "g")); group.set("tracks", AttrType.ELEMENT + ARRAY_OFFSET, [track])
    shot = doc.add(Element("DmeFilmClip", "shot"))
    sframe = doc.add(Element("DmeTimeFrame", "sf"))
    sframe.set("start", AttrType.TIME, Time(0)); sframe.set("duration", AttrType.TIME, Time.from_seconds(4))
    shot.set("timeFrame", AttrType.ELEMENT, sframe)
    shot.set("trackGroups", AttrType.ELEMENT + ARRAY_OFFSET, [group])
    return FilmClip(shot), bone, control, log


def test_recording_writes_the_attribute_the_key_and_the_control():
    shot, bone, control, log = _shot()
    index = channel_index(shot)
    assert (id(bone), "position", -1) in index
    stack = UndoStack()
    command = record_edit(index, bone, "position", (5.0, 0.0, 0.0), Time.from_seconds(2.0))
    stack.push(command)
    assert isinstance(command, Group)
    assert bone["position"] == (5.0, 0.0, 0.0) and control["valuePosition"] == (5.0, 0.0, 0.0)
    # the key sits at the channel clip's local time: 2 s + 1 s offset
    layer = top_layer(Log(log))
    assert [t.seconds for t in layer["times"]] == [0.0, 3.0, 4.0]
    assert layer["values"][1] == (5.0, 0.0, 0.0)
    stack.undo()
    assert bone["position"] == (0.0, 0.0, 0.0) and len(layer["times"]) == 2


def test_a_recorded_edit_survives_re_evaluation():
    shot, bone, _control, _log = _shot()
    stack = UndoStack()
    stack.push(record_edit(channel_index(shot), bone, "position", (5.0, 0.0, 0.0), Time.from_seconds(2.0)))
    ev = Evaluator()
    ev.evaluate(shot, Time.from_seconds(2.0))
    assert bone["position"] == (5.0, 0.0, 0.0)
    ev.evaluate(shot, Time.from_seconds(2.5))                     # clip 3.5 s: halfway to the 4 s key
    assert abs(bone["position"][2] - 20.0) < 1e-6 and abs(bone["position"][0] - 2.5) < 1e-6


def test_an_undriven_attribute_is_a_plain_set():
    shot, bone, _c, _l = _shot()
    bone.set("scale", AttrType.FLOAT, 1.0)
    command = record_edit(channel_index(shot), bone, "scale", 2.0, Time(0))
    assert isinstance(command, SetAttribute)


def test_a_group_that_fails_midway_leaves_nothing_applied():
    doc = DmxDocument()
    e = doc.add(Element("DmElement", "e"))
    e.set("x", AttrType.INT, 0)
    e.set("v", AttrType.VECTOR3, (0.0, 0.0, 0.0))
    bad = SetAttribute(e, "v", 1.0, index=0)            # a slot on a scalar: cannot apply
    group = Group([SetAttribute(e, "x", 5), bad])
    stack = UndoStack()
    try:
        stack.push(group)
    except TypeError:
        pass
    assert e["x"] == 0 and not stack.can_undo and not stack.dirty
