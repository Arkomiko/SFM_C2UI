"""Graph-editor key edits: move, insert, delete, per-component values, undo."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Core.API.dmx import ARRAY_OFFSET, AttrType, DmxDocument, Element, Time
from Core.API.session import Log, TimeFrame
from Core.Code.animation import sample_log
from Core.Code.editing import UndoStack, top_layer
from Core.Code.keys import (component_value, components, delete_keys, insert_key, key_count,
                            move_keys, with_component)
from Core.Code.transform import angles_from_quaternion, quaternion_from_angles


def s(seconds):
    return Time.from_seconds(seconds)


def _log(doc, times, values, kind=AttrType.FLOAT, curvetypes=None):
    layer = doc.add(Element("DmeFloatLogLayer", "layer"))
    layer.set("times", AttrType.TIME + ARRAY_OFFSET, [s(t) for t in times])
    if curvetypes is not None:
        layer.set("curvetypes", AttrType.INT + ARRAY_OFFSET, list(curvetypes))
    layer.set("values", kind + ARRAY_OFFSET, list(values))
    log = doc.add(Element("DmeFloatLog", "log"))
    log.set("layers", AttrType.ELEMENT + ARRAY_OFFSET, [layer])
    return Log(log)


def _times(log):
    return [round(t.seconds, 4) for t in top_layer(log)["times"]]


# ------------------------------------------------------------------- components
def test_components_per_value_type():
    assert components(AttrType.FLOAT) == ["value"]
    assert components(AttrType.VECTOR3) == ["X", "Y", "Z"]
    assert components(AttrType.QUATERNION) == ["pitch", "yaw", "roll"]
    assert components(AttrType.COLOR) == ["R", "G", "B", "A"]
    assert components(AttrType.ELEMENT) == []


def test_component_round_trip_for_vectors_and_rotations():
    v = (1.0, 2.0, 3.0)
    assert component_value(AttrType.VECTOR3, v, 1) == 2.0
    assert with_component(AttrType.VECTOR3, v, 1, 9.5) == (1.0, 9.5, 3.0)
    q = quaternion_from_angles(10.0, 20.0, 30.0)
    assert abs(component_value(AttrType.QUATERNION, q, 1) - 20.0) < 1e-6
    turned = with_component(AttrType.QUATERNION, q, 1, 50.0)
    assert all(abs(a - b) < 1e-6 for a, b in zip(angles_from_quaternion(turned), (10.0, 50.0, 30.0)))
    assert with_component(AttrType.INT, 3, 0, 4.6) == 5
    assert with_component(AttrType.BOOL, False, 0, 0.7) is True


def test_angles_from_quaternion_inverts_quaternion_from_angles():
    for angles in ((0, 0, 0), (10, 20, 30), (-45, 170, -100), (89, 10, 5), (-30, -179, 60)):
        back = angles_from_quaternion(quaternion_from_angles(*angles))
        assert all(abs(a - b) < 1e-6 for a, b in zip(angles, back)), (angles, back)


# ------------------------------------------------------------------- moving
def test_move_keys_shifts_time_and_value_and_undoes():
    doc = DmxDocument()
    log = _log(doc, [0, 1, 2, 3], [0.0, 10.0, 20.0, 30.0])
    stack = UndoStack()
    command = move_keys(log, [1, 2], s(0.5).ticks, lambda v: v + 5.0)
    stack.push(command)
    assert _times(log) == [0, 1.5, 2.5, 3]
    assert top_layer(log)["values"] == [0.0, 15.0, 25.0, 30.0]
    assert stack.undo_label == "move keys"
    stack.undo()
    assert _times(log) == [0, 1, 2, 3] and top_layer(log)["values"] == [0.0, 10.0, 20.0, 30.0]
    stack.redo()
    assert _times(log) == [0, 1.5, 2.5, 3]


def test_moved_keys_pass_others_and_stay_sorted():
    doc = DmxDocument()
    log = _log(doc, [0, 1, 2, 3], [0.0, 10.0, 20.0, 30.0])
    move_keys(log, [1], s(1.5).ticks).apply()                 # key at 1 goes to 2.5, past the key at 2
    assert _times(log) == [0, 2, 2.5, 3]
    assert top_layer(log)["values"] == [0.0, 20.0, 10.0, 30.0]


def test_a_moved_key_landing_on_another_replaces_it():
    doc = DmxDocument()
    log = _log(doc, [0, 1, 2], [0.0, 10.0, 20.0])
    move_keys(log, [1], s(1).ticks).apply()
    assert _times(log) == [0, 2] and top_layer(log)["values"] == [0.0, 10.0]


def test_curvetypes_follow_their_keys():
    doc = DmxDocument()
    log = _log(doc, [0, 1, 2], [0.0, 10.0, 20.0], curvetypes=[1, 2, 3])
    move_keys(log, [2], -s(1.5).ticks).apply()                # 2 -> 0.5, between the first two
    assert _times(log) == [0, 0.5, 1]
    assert top_layer(log)["curvetypes"] == [1, 3, 2]
    # SFM's empty array stays empty
    log2 = _log(doc, [0, 1], [0.0, 1.0], curvetypes=[])
    move_keys(log2, [1], s(1).ticks).apply()
    assert top_layer(log2)["curvetypes"] == []


def test_move_ignores_bad_indices_and_returns_none_for_nothing():
    doc = DmxDocument()
    log = _log(doc, [0, 1], [0.0, 1.0])
    assert move_keys(log, [7], 100) is None
    assert move_keys(log, [], 100) is None


# ------------------------------------------------------------------- inserting and deleting
def test_insert_key_samples_the_curve_and_keeps_the_shape():
    doc = DmxDocument()
    log = _log(doc, [0, 2], [0.0, 20.0])
    stack = UndoStack()
    stack.push(insert_key(log, s(1)))
    assert _times(log) == [0, 1, 2] and top_layer(log)["values"] == [0.0, 10.0, 20.0]
    assert sample_log(log, s(0.5))[1] == 5.0
    stack.push(insert_key(log, s(1), 99.0))                  # an explicit value replaces
    assert top_layer(log)["values"] == [0.0, 99.0, 20.0]
    stack.undo()
    assert top_layer(log)["values"] == [0.0, 10.0, 20.0]
    stack.undo()
    assert _times(log) == [0, 2]


def test_delete_keys_keeps_at_least_one():
    doc = DmxDocument()
    log = _log(doc, [0, 1, 2], [0.0, 10.0, 20.0])
    stack = UndoStack()
    stack.push(delete_keys(log, [0, 2]))
    assert _times(log) == [1] and top_layer(log)["values"] == [10.0]
    assert delete_keys(log, [0]) is None
    stack.undo()
    assert key_count(log) == 3


# ------------------------------------------------------------------- time frames
def test_to_parent_time_inverts_to_child_time():
    doc = DmxDocument()
    frame = TimeFrame(doc.add(Element("DmeTimeFrame", "f")))
    frame.element.set("start", AttrType.TIME, s(10))
    frame.element.set("offset", AttrType.TIME, s(2))
    frame.element.set("scale", AttrType.FLOAT, 0.5)
    child = frame.to_child_time(s(14))
    assert child.ticks == s(4).ticks                          # (14 - 10) * 0.5 + 2
    assert frame.to_parent_time(child).ticks == s(14).ticks
