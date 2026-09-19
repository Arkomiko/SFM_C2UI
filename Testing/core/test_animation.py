"""
Channels and logs evaluated over time, on a session built in memory.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Core.API.dmx import ARRAY_OFFSET, AttrType, DmxDocument, Element, Time
from Core.API.session import Channel, FilmClip, Log, Session
from Core.Code.animation import (MODE_OFF, MODE_PASS, MODE_RECORD, Evaluator, interpolate,
                                 sample_log)


def _close(a, b, eps=1e-6):
    return len(a) == len(b) and all(abs(x - y) <= eps for x, y in zip(a, b))


def _log(doc, kind, times, values, log_type="DmeFloatLog", default=None):
    layer = doc.add(Element(log_type + "Layer", "layer"))
    layer.set("times", AttrType.TIME + ARRAY_OFFSET, [Time.from_seconds(t) for t in times])
    layer.set("values", kind + ARRAY_OFFSET, list(values))
    log = doc.add(Element(log_type, "log"))
    log.set("layers", AttrType.ELEMENT + ARRAY_OFFSET, [layer])
    if default is not None:
        log.set("usedefaultvalue", AttrType.BOOL, True)
        log.set("defaultvalue", kind, default)
    return log


def _channel(doc, target, attribute, log, mode=MODE_RECORD, index=-1, source=None, source_attr=""):
    ch = doc.add(Element("DmeChannel", f"{attribute}_channel"))
    ch.set("toElement", AttrType.ELEMENT, target)
    ch.set("toAttribute", AttrType.STRING, attribute)
    ch.set("toIndex", AttrType.INT, index)
    ch.set("fromElement", AttrType.ELEMENT, source)
    ch.set("fromAttribute", AttrType.STRING, source_attr)
    ch.set("fromIndex", AttrType.INT, -1)
    ch.set("mode", AttrType.INT, mode)
    ch.set("log", AttrType.ELEMENT, log)
    return ch


def _frame(doc, start, duration, offset=0.0, scale=1.0):
    f = doc.add(Element("DmeTimeFrame", "unnamed"))
    f.set("start", AttrType.TIME, Time.from_seconds(start))
    f.set("duration", AttrType.TIME, Time.from_seconds(duration))
    f.set("offset", AttrType.TIME, Time.from_seconds(offset))
    f.set("scale", AttrType.FLOAT, scale)
    return f


# ------------------------------------------------------------------- sampling
def test_interpolation_per_type():
    assert interpolate(AttrType.FLOAT, 0.0, 10.0, 0.25) == 2.5
    assert _close(interpolate(AttrType.VECTOR3, (0, 0, 0), (2, 4, 6), 0.5), (1, 2, 3))
    assert interpolate(AttrType.COLOR, (0, 0, 0, 255), (100, 50, 0, 255), 0.5) == (50, 25, 0, 255)
    assert interpolate(AttrType.INT, 1, 9, 0.9) == 1                  # holds
    assert interpolate(AttrType.BOOL, True, False, 0.9) is True
    q = interpolate(AttrType.QUATERNION, (0, 0, 0, 1),
                    (0, 0, math.sin(math.pi / 4), math.cos(math.pi / 4)), 0.5)
    assert _close(q, (0, 0, math.sin(math.pi / 8), math.cos(math.pi / 8)))


def test_log_sampling_clamps_and_blends():
    doc = DmxDocument()
    log = Log(_log(doc, AttrType.FLOAT, [1.0, 2.0, 4.0], [10.0, 20.0, 40.0]))
    assert sample_log(log, Time.from_seconds(0.0)) == (True, 10.0)
    assert sample_log(log, Time.from_seconds(1.5)) == (True, 15.0)
    assert sample_log(log, Time.from_seconds(3.0)) == (True, 30.0)
    assert sample_log(log, Time.from_seconds(9.0)) == (True, 40.0)


def test_empty_log_uses_default_or_nothing():
    doc = DmxDocument()
    assert sample_log(Log(_log(doc, AttrType.FLOAT, [], [])), Time(0)) == (False, None)
    with_default = Log(_log(doc, AttrType.FLOAT, [], [], default=0.5))
    assert sample_log(with_default, Time(0)) == (True, 0.5)


def test_cache_is_used_and_cleared():
    doc = DmxDocument()
    log = Log(_log(doc, AttrType.FLOAT, [0.0, 1.0], [0.0, 1.0]))
    cache = {}
    assert sample_log(log, Time.from_seconds(0.5), cache) == (True, 0.5)
    assert len(cache) == 1
    ev = Evaluator()
    ev._cache.update(cache)
    ev.invalidate()
    assert ev._cache == {}


# ------------------------------------------------------------------- channels
def test_channel_writes_its_target_keeping_the_attribute_type():
    doc = DmxDocument()
    bone = doc.add(Element("DmeTransform", "bone"))
    bone.set("position", AttrType.VECTOR3, (0.0, 0.0, 0.0))
    counter = doc.add(Element("DmElement", "c"))
    counter.set("frame", AttrType.INT, 0)
    ev = Evaluator()
    ev.evaluate_channel(Channel(_channel(doc, bone, "position",
                                         _log(doc, AttrType.VECTOR3, [0, 2], [(0, 0, 0), (2, 0, 0)], "DmeVector3Log"))),
                        Time.from_seconds(1.0))
    assert bone["position"] == (1.0, 0.0, 0.0)
    ev.evaluate_channel(Channel(_channel(doc, counter, "frame",
                                         _log(doc, AttrType.FLOAT, [0, 1], [0.0, 10.0]))),
                        Time.from_seconds(0.55))
    assert counter["frame"] == 6 and counter.attribute("frame").type == AttrType.INT


def test_channel_writes_into_an_array_slot():
    doc = DmxDocument()
    model = doc.add(Element("DmeGameModel", "m"))
    model.set("flexWeights", AttrType.FLOAT + ARRAY_OFFSET, [0.0, 0.0, 0.0])
    ch = _channel(doc, model, "flexWeights", _log(doc, AttrType.FLOAT, [0, 1], [0.0, 1.0]), index=2)
    Evaluator().evaluate_channel(Channel(ch), Time.from_seconds(0.25))
    assert model["flexWeights"] == [0.0, 0.0, 0.25]


def test_modes_off_and_pass():
    doc = DmxDocument()
    target = doc.add(Element("DmElement", "t"))
    target.set("value", AttrType.FLOAT, 0.0)
    control = doc.add(Element("DmElement", "control"))
    control.set("value", AttrType.FLOAT, 7.0)
    log = _log(doc, AttrType.FLOAT, [0, 1], [1.0, 1.0])
    ev = Evaluator()
    assert not ev.evaluate_channel(Channel(_channel(doc, target, "value", log, mode=MODE_OFF)), Time(0))
    assert target["value"] == 0.0
    assert ev.evaluate_channel(Channel(_channel(doc, target, "value", log, mode=MODE_PASS,
                                                source=control, source_attr="value")), Time(0))
    assert target["value"] == 7.0                                     # the log was ignored
    assert ev.evaluate_channel(Channel(_channel(doc, target, "value", log, mode=MODE_RECORD)), Time(0))
    assert target["value"] == 1.0


def test_channel_without_keys_falls_back_to_the_control():
    doc = DmxDocument()
    target = doc.add(Element("DmElement", "t"))
    target.set("value", AttrType.FLOAT, 0.0)
    control = doc.add(Element("DmElement", "control"))
    control.set("value", AttrType.FLOAT, 3.0)
    ch = _channel(doc, target, "value", _log(doc, AttrType.FLOAT, [], []), source=control, source_attr="value")
    assert Evaluator().evaluate_channel(Channel(ch), Time(0))
    assert target["value"] == 3.0


# ------------------------------------------------------------------- clips and time
def _sequence():
    """A 10 s sequence with two shots; shot B starts at 4 s and runs at double speed
    from an offset of 1 s. Its bone rises 0..10 over the clip's local 0..5 s."""
    doc = DmxDocument(format="sfm_session", format_version=20)
    root = doc.add(Element("DmElement", "session"))
    seq = doc.add(Element("DmeFilmClip", "sequence"))
    root.set("activeClip", AttrType.ELEMENT, seq)
    seq.set("timeFrame", AttrType.ELEMENT, _frame(doc, 0, 10))

    def shot(name, start, duration, offset=0.0, scale=1.0):
        s = doc.add(Element("DmeFilmClip", name))
        s.set("timeFrame", AttrType.ELEMENT, _frame(doc, start, duration, offset, scale))
        bone = doc.add(Element("DmeTransform", name + "_bone"))
        bone.set("position", AttrType.VECTOR3, (0.0, 0.0, -1.0))
        channels_clip = doc.add(Element("DmeChannelsClip", name + "_channels"))
        channels_clip.set("timeFrame", AttrType.ELEMENT, _frame(doc, 0, duration))
        channels_clip.set("channels", AttrType.ELEMENT + ARRAY_OFFSET, [
            _channel(doc, bone, "position",
                     _log(doc, AttrType.VECTOR3, [0, 5], [(0, 0, 0), (0, 0, 10)], "DmeVector3Log"))])
        track = doc.add(Element("DmeTrack", "animSetEditorChannels"))
        track.set("children", AttrType.ELEMENT + ARRAY_OFFSET, [channels_clip])
        group = doc.add(Element("DmeTrackGroup", "channelTrackGroup"))
        group.set("tracks", AttrType.ELEMENT + ARRAY_OFFSET, [track])
        s.set("trackGroups", AttrType.ELEMENT + ARRAY_OFFSET, [group])
        return s, bone

    a, bone_a = shot("A", 0, 4)
    b, bone_b = shot("B", 4, 6, offset=1.0, scale=2.0)
    film = doc.add(Element("DmeTrack", "Film"))
    film.set("children", AttrType.ELEMENT + ARRAY_OFFSET, [a, b])
    sub = doc.add(Element("DmeTrackGroup", "subClipTrackGroup"))
    sub.set("tracks", AttrType.ELEMENT + ARRAY_OFFSET, [film])
    seq.set("subClipTrackGroup", AttrType.ELEMENT, sub)
    return Session(doc), bone_a, bone_b


def test_only_the_shot_under_the_cursor_is_evaluated():
    session, bone_a, bone_b = _sequence()
    ev = Evaluator()
    ev.evaluate(session.active_clip, Time.from_seconds(2.0))
    assert _close(bone_a["position"], (0, 0, 4))
    assert bone_b["position"] == (0.0, 0.0, -1.0)                    # untouched
    assert ev.channels_run == 1


def test_shot_time_goes_through_offset_and_scale():
    session, _a, bone_b = _sequence()
    # sequence 5 s -> shot B local (5 - 4) * 2 + 1 = 3 s -> height 6
    Evaluator().evaluate(session.active_clip, Time.from_seconds(5.0))
    assert _close(bone_b["position"], (0, 0, 6))


def test_time_between_shots_touches_nothing():
    session, bone_a, bone_b = _sequence()
    ev = Evaluator()
    ev.evaluate(session.active_clip, Time.from_seconds(10.5))
    assert bone_a["position"] == (0.0, 0.0, -1.0) and bone_b["position"] == (0.0, 0.0, -1.0)
    assert ev.channels_run == 0


def test_evaluated_session_saves_the_new_values():
    from Core.Code.formats import parse_dmx, serialise_dmx
    session, bone_a, _b = _sequence()
    Evaluator().evaluate(session.active_clip, Time.from_seconds(1.0))
    again = parse_dmx(serialise_dmx(session.document), "again")
    saved = again.by_id(bone_a.id)
    assert _close(saved["position"], (0, 0, 2))
