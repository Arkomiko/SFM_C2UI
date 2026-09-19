"""
The motion editor's time selection: weights, offsets over a log, undo.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Core.API.dmx import ARRAY_OFFSET, AttrType, DmxDocument, Element, Time
from Core.API.session import Log
from Core.Code.animation import Evaluator, sample_log
from Core.Code.editing import UndoStack, channel_index, record_edit, top_layer
from Core.Code.motion import (INFINITE, INTERP_EASE_INOUT, INTERP_LINEAR, OffsetOverSelection,
                              TimeSelection, offset_between, offset_value, weight_curve)

s = Time.from_seconds


def _log(doc, times, values, kind=AttrType.FLOAT, name="DmeFloatLog"):
    layer = doc.add(Element(name + "Layer", "layer"))
    layer.set("times", AttrType.TIME + ARRAY_OFFSET, [s(t) for t in times])
    layer.set("values", kind + ARRAY_OFFSET, list(values))
    log = doc.add(Element(name, "log"))
    log.set("layers", AttrType.ELEMENT + ARRAY_OFFSET, [layer])
    return Log(log)


# ------------------------------------------------------------------- weights
def test_weight_is_full_in_the_hold_and_fades_in_the_falloff():
    sel = TimeSelection(s(1), s(2), s(3), s(4), INTERP_LINEAR, INTERP_LINEAR)
    assert sel.weight(s(0.5)) == 0.0 and sel.weight(s(4.5)) == 0.0
    assert sel.weight(s(2)) == 1.0 and sel.weight(s(2.5)) == 1.0 and sel.weight(s(3)) == 1.0
    assert abs(sel.weight(s(1.5)) - 0.5) < 1e-9 and abs(sel.weight(s(3.75)) - 0.25) < 1e-9
    assert weight_curve(0.5, INTERP_EASE_INOUT) == 0.5 and weight_curve(0.25, INTERP_EASE_INOUT) < 0.25


def test_infinite_selection_weights_everything():
    sel = TimeSelection()
    assert sel.is_infinite and sel.weight(s(-1000)) == 1.0 and sel.weight(s(1e5)) == 1.0


def test_selection_round_trips_through_an_element_and_maps_into_a_clip():
    doc = DmxDocument()
    e = doc.add(Element("DmeTimeSelection", "ts"))
    TimeSelection(s(1), s(2), s(3), s(4), 6, 4, True).write(e)
    e.set("resampleinterval", AttrType.TIME, s(0.02))              # sessions store it as a time
    back = TimeSelection.from_element(e)
    assert (back.falloff_left, back.hold_right, back.interpolator_left, back.enabled) == (s(1), s(3), 6, True)
    assert back.resample_interval == 0.02
    frame = doc.add(Element("DmeTimeFrame", "f"))
    frame.set("start", AttrType.TIME, s(10)); frame.set("duration", AttrType.TIME, s(5))
    frame.set("offset", AttrType.TIME, s(1)); frame.set("scale", AttrType.FLOAT, 1.0)
    from Core.API.session import TimeFrame
    mapped = TimeSelection(s(11), s(12), s(13), INFINITE, 6, 6).mapped(TimeFrame(frame))
    assert (mapped.falloff_left, mapped.hold_left, mapped.hold_right, mapped.falloff_right) == (s(2), s(3), s(4), INFINITE)


# ------------------------------------------------------------------- offsets
def test_offsets_by_type():
    assert offset_value(AttrType.FLOAT, 1.0, 4.0, 0.5) == 3.0
    assert offset_value(AttrType.VECTOR3, (0, 0, 0), (2, 4, 6), 0.5) == (1, 2, 3)
    assert offset_value(AttrType.INT, 1, 3, 1.0) == 4
    q = offset_value(AttrType.QUATERNION, (0, 0, 0, 1), (0, 0, math.sin(math.pi / 4), math.cos(math.pi / 4)), 0.5)
    assert abs(q[2] - math.sin(math.pi / 8)) < 1e-9
    assert offset_between(AttrType.VECTOR3, (1, 1, 1), (2, 3, 4)) == (1, 2, 3)
    assert offset_between(AttrType.FLOAT, 2.0, 5.0) == 3.0


def test_offset_over_selection_moves_the_hold_fades_the_falloff_and_spares_the_rest():
    doc = DmxDocument()
    log = _log(doc, [0, 1, 2, 3, 4, 5], [0.0] * 6)
    sel = TimeSelection(s(1), s(2), s(3), s(4), INTERP_LINEAR, INTERP_LINEAR, resample_interval=0.5)
    stack = UndoStack()
    stack.push(OffsetOverSelection(log, AttrType.FLOAT, sel, 10.0))
    layer = top_layer(log)
    keyed = dict(zip([t.seconds for t in layer["times"]], layer["values"]))
    assert keyed[0] == 0.0 and keyed[5] == 0.0                    # outside: untouched
    assert keyed[1] == 0.0 and keyed[4] == 0.0                    # the falloff edges: nothing yet
    assert keyed[2] == 10.0 and keyed[3] == 10.0                  # the hold: everything
    assert abs(keyed[1.5] - 5.0) < 1e-9 and abs(keyed[3.5] - 5.0) < 1e-9   # resampled falloff
    assert sample_log(log, s(2.5)) == (True, 10.0)
    stack.undo()
    assert [t.seconds for t in top_layer(log)["times"]] == [0, 1, 2, 3, 4, 5]
    assert top_layer(log)["values"] == [0.0] * 6


def test_offset_over_an_infinite_selection_moves_every_key():
    doc = DmxDocument()
    log = _log(doc, [0, 1, 2], [1.0, 2.0, 3.0])
    OffsetOverSelection(log, AttrType.FLOAT, TimeSelection(), -1.0).apply()
    assert top_layer(log)["values"] == [0.0, 1.0, 2.0]
    assert len(top_layer(log)["times"]) == 3                      # no edges to add


def test_record_edit_with_a_selection_spreads_the_change():
    from core.test_editing import _shot
    shot, bone, control, log = _shot()                              # keys at 0 s and 4 s (clip time)
    index = channel_index(shot)
    # shot time 2 s is clip time 3 s; hold 1..3 s of shot time, no falloff
    sel = TimeSelection(s(1), s(1), s(3), s(3), INTERP_LINEAR, INTERP_LINEAR)
    stack = UndoStack()
    stack.push(record_edit(index, bone, "position", (5.0, 0.0, 20.0), s(2), selection=sel))
    ev = Evaluator()
    ev.evaluate(shot, s(2))
    assert bone["position"] == (5.0, 0.0, 20.0)                     # the edit at the cursor
    ev.evaluate(shot, s(1.5))                                       # inside the hold: same offset
    assert abs(bone["position"][0] - 5.0) < 1e-9
    ev.evaluate(shot, s(0.0))                                       # outside: the original curve
    assert abs(bone["position"][0]) < 1e-9
    assert control["valuePosition"] == (5.0, 0.0, 20.0)
    stack.undo()
    ev.invalidate(); ev.evaluate(shot, s(2))
    assert abs(bone["position"][0]) < 1e-9
