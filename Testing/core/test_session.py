"""
Transforms, session views and posing, on documents built in memory.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Core.API.dmx import ARRAY_OFFSET, AttrType, DmxDocument, Element, Time
from Core.API.model import Bone, Mesh, Model
from Core.API.session import (Camera, FilmClip, GameModel, Session, SoundClip, Transform,
                              wrap)
from Core.Code import transform as tf
from Core.Code.pose import skin_matrices
from Core.Code.formats import parse_dmx, serialise_dmx


def _close(a, b, eps=1e-6):
    return len(a) == len(b) and all(abs(x - y) <= eps for x, y in zip(a, b))


# ------------------------------------------------------------------- transform
def test_quaternion_rotates_like_source():
    # 90 degrees about Z takes +X to +Y
    q = (0.0, 0.0, math.sin(math.pi / 4), math.cos(math.pi / 4))
    m = tf.matrix_from((0, 0, 0), q)
    assert _close(tf.apply(m, (1, 0, 0)), (0, 1, 0))


def test_compose_applies_right_then_left():
    move = tf.matrix_from((10, 0, 0), (0, 0, 0, 1))
    turn = tf.matrix_from((0, 0, 0), (0, 0, math.sin(math.pi / 4), math.cos(math.pi / 4)))
    assert _close(tf.apply(tf.multiply(move, turn), (1, 0, 0)), (10, 1, 0))
    assert _close(tf.apply(tf.multiply(turn, move), (1, 0, 0)), (0, 11, 0))


def test_invert_undoes():
    m = tf.matrix_from((3, -2, 5), tf.quaternion_normalize((0.2, 0.4, -0.1, 0.8)))
    p = (1.5, 2.5, -4.0)
    assert _close(tf.apply(tf.invert(m), tf.apply(m, p)), p)
    assert _close(tf.multiply(m, tf.invert(m)), tf.IDENTITY, 1e-9)


def test_quaternion_product_matches_matrix_product():
    a = tf.quaternion_normalize((0.1, 0.7, 0.2, 0.6))
    b = tf.quaternion_normalize((-0.3, 0.2, 0.5, 0.7))
    via_q = tf.matrix_from((0, 0, 0), tf.quaternion_multiply(a, b))
    via_m = tf.multiply(tf.matrix_from((0, 0, 0), a), tf.matrix_from((0, 0, 0), b))
    assert _close(via_q, via_m)


def test_slerp_ends_and_middle():
    a = (0.0, 0.0, 0.0, 1.0)
    b = (0.0, 0.0, math.sin(math.pi / 4), math.cos(math.pi / 4))     # 90 degrees
    assert _close(tf.quaternion_slerp(a, b, 0.0), a)
    assert _close(tf.quaternion_slerp(a, b, 1.0), b)
    mid = tf.quaternion_slerp(a, b, 0.5)                             # 45 degrees
    assert _close(mid, (0.0, 0.0, math.sin(math.pi / 8), math.cos(math.pi / 8)))


def test_angles_follow_source_convention():
    q = tf.quaternion_from_angles(0.0, 90.0, 0.0)                    # yaw about Z
    assert _close(tf.apply(tf.matrix_from((0, 0, 0), q), (1, 0, 0)), (0, 1, 0))


def test_column_major_form_has_translation_last():
    m = tf.matrix_from((1, 2, 3), (0, 0, 0, 1))
    assert tf.to_column_major_4x4(m)[12:15] == (1, 2, 3)


# ------------------------------------------------------------------- session document
def _transform(doc, pos=(0, 0, 0), rot=(0, 0, 0, 1)):
    t = doc.add(Element("DmeTransform", "unnamed"))
    t.set("position", AttrType.VECTOR3, tuple(float(v) for v in pos))
    t.set("orientation", AttrType.QUATERNION, tuple(float(v) for v in rot))
    return t


def _dag(doc, etype, name, pos=(0, 0, 0), rot=(0, 0, 0, 1), children=(), visible=True):
    d = doc.add(Element(etype, name))
    d.set("transform", AttrType.ELEMENT, _transform(doc, pos, rot))
    d.set("shape", AttrType.ELEMENT, None)
    d.set("visible", AttrType.BOOL, visible)
    d.set("children", AttrType.ELEMENT + ARRAY_OFFSET, list(children))
    return d


def _time_frame(doc, start, duration, offset=0, scale=1.0):
    f = doc.add(Element("DmeTimeFrame", "unnamed"))
    f.set("start", AttrType.TIME, Time(start))
    f.set("duration", AttrType.TIME, Time(duration))
    f.set("offset", AttrType.TIME, Time(offset))
    f.set("scale", AttrType.FLOAT, scale)
    return f


def _session():
    doc = DmxDocument(format="sfm_session", format_version=20)
    root = doc.add(Element("DmElement", "session"))
    seq = doc.add(Element("DmeFilmClip", "sequence"))
    root.set("activeClip", AttrType.ELEMENT, seq)
    root.set("clipBin", AttrType.ELEMENT + ARRAY_OFFSET, [seq])
    seq.set("timeFrame", AttrType.ELEMENT, _time_frame(doc, 0, 100000))
    seq.set("mapname", AttrType.STRING, "stage.bsp")

    model = _dag(doc, "DmeGameModel", "scout_GameModel", pos=(0, 0, 0))
    model.set("modelName", AttrType.STRING, "models\\player\\scout.mdl")
    model.set("bones", AttrType.ELEMENT + ARRAY_OFFSET,
              [_transform(doc, (0, 0, 40), (0, 0, 0, 1)), _transform(doc, (0, 0, 10), (0, 0, 0, 1))])
    holder = _dag(doc, "DmeDag", "scout1", pos=(100, 0, 0),
                  rot=(0, 0, math.sin(math.pi / 4), math.cos(math.pi / 4)), children=[model])
    hidden = _dag(doc, "DmeGameModel", "ghost", visible=False)
    hidden.set("modelName", AttrType.STRING, "models/ghost.mdl")
    cam = _dag(doc, "DmeCamera", "camera1", pos=(200, 0, 50))
    cam.set("fieldOfView", AttrType.FLOAT, 60.0)
    scene = _dag(doc, "DmeDag", "scene", children=[holder, hidden, cam])

    shot2 = doc.add(Element("DmeFilmClip", "shot2"))
    shot2.set("timeFrame", AttrType.ELEMENT, _time_frame(doc, 50000, 50000))
    shot1 = doc.add(Element("DmeFilmClip", "shot1"))
    shot1.set("timeFrame", AttrType.ELEMENT, _time_frame(doc, 0, 50000, offset=20000, scale=2.0))
    shot1.set("scene", AttrType.ELEMENT, scene)
    shot1.set("camera", AttrType.ELEMENT, cam)
    track = doc.add(Element("DmeTrack", "Film"))
    track.set("children", AttrType.ELEMENT + ARRAY_OFFSET, [shot2, shot1])     # out of order on purpose
    group = doc.add(Element("DmeTrackGroup", "subClipTrackGroup"))
    group.set("tracks", AttrType.ELEMENT + ARRAY_OFFSET, [track])
    seq.set("subClipTrackGroup", AttrType.ELEMENT, group)

    sound = doc.add(Element("DmeSoundClip", "voice"))
    sound.set("timeFrame", AttrType.ELEMENT, _time_frame(doc, 10000, 5000))
    strack = doc.add(Element("DmeTrack", "Dialog"))
    strack.set("children", AttrType.ELEMENT + ARRAY_OFFSET, [sound])
    sgroup = doc.add(Element("DmeTrackGroup", "Sound"))
    sgroup.set("tracks", AttrType.ELEMENT + ARRAY_OFFSET, [strack])
    seq.set("trackGroups", AttrType.ELEMENT + ARRAY_OFFSET, [sgroup])
    return doc


def test_session_views_reach_the_whole_structure():
    session = Session(_session())
    assert session.is_session
    clip = session.active_clip
    assert isinstance(clip, FilmClip) and clip.name == "sequence"
    assert clip.time_frame.duration == Time(100000) and clip.map_name == "stage.bsp"
    assert [s.name for s in clip.shots] == ["shot1", "shot2"]          # sorted by start
    assert [g.name for g in clip.track_groups] == ["Sound"]
    voice = clip.track_groups[0].tracks[0].clips[0]
    assert isinstance(voice, SoundClip) and voice.time_frame.end == Time(15000)
    assert "1 shots" not in session.summary() and "2 shots" in session.summary()


def test_time_frame_maps_parent_time_into_a_shot():
    shot = Session(_session()).active_clip.shots[0]
    frame = shot.time_frame
    assert frame.to_child_time(Time(0)) == Time(20000)
    assert frame.to_child_time(Time(10000)) == Time(40000)          # scale 2, offset 2 s


def test_scene_walk_composes_world_matrices_and_skips_hidden():
    shot = Session(_session()).active_clip.shots[0]
    models = shot.game_models()
    assert [m.name for m, _w in models] == ["scout_GameModel"]
    model, world = models[0]
    assert isinstance(model, GameModel)
    assert model.model_name == "models/player/scout.mdl"
    # the holder is at x=100 turned 90 degrees, so the model's +X points along +Y
    assert _close(tf.apply(world, (0, 0, 0)), (100, 0, 0))
    assert _close(tf.apply_direction(world, (1, 0, 0)), (0, 1, 0))
    assert [n.name for n, _w in shot.scene.walk(include_hidden=True)].count("ghost") == 1


def test_camera_view():
    shot = Session(_session()).active_clip.shots[0]
    cam = shot.camera
    assert isinstance(cam, Camera) and cam.field_of_view == 60.0
    assert cam.transform.position == (200.0, 0.0, 50.0)


def test_wrap_guesses_by_shape_for_unknown_types():
    doc = DmxDocument()
    odd = _dag(doc, "DmeSomethingNew", "x")
    assert type(wrap(odd)).__name__ == "Dag"
    clip = doc.add(Element("DmeOtherClip", "c"))
    clip.set("timeFrame", AttrType.ELEMENT, _time_frame(doc, 0, 1))
    assert type(wrap(clip)).__name__ == "Clip"


def test_views_write_through_to_the_document():
    doc = _session()
    session = Session(doc)
    frame = session.active_clip.shots[1].time_frame
    frame.start = Time(70000)
    t = session.active_clip.shots[0].game_models()[0][0].bones[0]
    t.position = (1, 2, 3)
    data = serialise_dmx(doc)
    again = Session(parse_dmx(data, "again"))
    assert again.active_clip.shots[1].time_frame.start == Time(70000)
    assert again.active_clip.shots[0].game_models()[0][0].bones[0].position == (1.0, 2.0, 3.0)


# ------------------------------------------------------------------- posing
def _two_bone_model():
    """Root at the origin, child 10 up; the child's pose_to_bone is its inverse."""
    root_bind = tf.matrix_from((0, 0, 0), (0, 0, 0, 1))
    child_bind = tf.matrix_from((0, 0, 10), (0, 0, 0, 1))
    model = Model(bones=[
        Bone("root", -1, (0, 0, 0), (0, 0, 0, 1), tf.invert(root_bind)),
        Bone("child", 0, (0, 0, 10), (0, 0, 0, 1), tf.invert(child_bind)),
    ])
    return model


def test_bind_pose_skins_to_identity():
    for m in skin_matrices(_two_bone_model()):
        assert _close(m, tf.IDENTITY)


def test_posed_bones_move_their_vertices():
    doc = DmxDocument()
    # turn the child bone 90 degrees about Z, keep everything else
    pose = [Transform(_transform(doc, (0, 0, 0), (0, 0, 0, 1))),
            Transform(_transform(doc, (0, 0, 10), (0, 0, math.sin(math.pi / 4), math.cos(math.pi / 4))))]
    skins = skin_matrices(_two_bone_model(), pose)
    assert _close(skins[0], tf.IDENTITY)
    # a bind-pose point 5 units along +X from the child bone ends up along +Y
    assert _close(tf.apply(skins[1], (5, 0, 10)), (0, 5, 10))


def test_short_pose_falls_back_to_bind():
    doc = DmxDocument()
    pose = [Transform(_transform(doc, (0, 0, 3), (0, 0, 0, 1)))]      # root moved up 3
    skins = skin_matrices(_two_bone_model(), pose)
    assert _close(tf.apply(skins[0], (0, 0, 0)), (0, 0, 3))
    assert _close(tf.apply(skins[1], (0, 0, 10)), (0, 0, 13))       # child inherits the move


def test_shot_at_and_the_render_defaults():
    session = Session(_session())
    clip = session.active_clip
    assert clip.shot_at(Time(0)).name == "shot1"
    assert clip.shot_at(Time(49999)).name == "shot1"
    assert clip.shot_at(Time(50000)).name == "shot2"
    assert clip.shot_at(Time(100000)) is None                       # the end is exclusive
    # no settings element: SFM's defaults
    assert session.frame_rate == 24.0 and session.movie_size == (1280, 720)
    doc = session.document
    settings = doc.add(Element("DmElement", "sessionSettings"))
    render = doc.add(Element("DmElement", "renderSettings"))
    render.set("frameRate", AttrType.FLOAT, 30.0)
    movie = doc.add(Element("DmElement", "movieSettings"))
    movie.set("width", AttrType.INT, 1920)
    movie.set("height", AttrType.INT, 1080)
    settings.set("renderSettings", AttrType.ELEMENT, render)
    settings.set("movieSettings", AttrType.ELEMENT, movie)
    session.element.set("settings", AttrType.ELEMENT, settings)
    assert session.frame_rate == 30.0 and session.movie_size == (1920, 1080)


def test_material_overlay_and_fades():
    session = Session(_session())
    doc = session.document
    shot1 = session.active_clip.shots[0]
    overlay = doc.add(Element("DmeMaterialOverlayFXClip", "materialOverlay"))
    overlay.set("material", AttrType.STRING, "titles\meet_the_team\mtt_group_e.vmt")
    overlay.set("overlaycolor", AttrType.COLOR, (255, 128, 0, 64))
    overlay.set("fullscreen", AttrType.BOOL, False)
    overlay.set("left", AttrType.FLOAT, 0.25)
    overlay.set("top", AttrType.FLOAT, 0.0)
    overlay.set("width", AttrType.FLOAT, 0.5)
    overlay.set("height", AttrType.FLOAT, 1.0)
    shot1.element.set("materialOverlay", AttrType.ELEMENT, overlay)
    shot1.element.set("fadeIn", AttrType.TIME, Time(10000))
    shot1.element.set("fadeOut", AttrType.TIME, Time(5000))
    view = shot1.material_overlay
    assert view is not None and view.material == "titles/meet_the_team/mtt_group_e"
    assert view.color == (1.0, 128 / 255.0, 0.0, 64 / 255.0) and not view.fullscreen
    assert view.rect == (0.25, 0.0, 0.5, 1.0)
    # shot1 runs 0..50000 on the sequence; its own offset and scale do not shift the fades
    assert shot1.fade_at(Time(0)) == 1.0
    assert abs(shot1.fade_at(Time(5000)) - 0.5) < 1e-9
    assert shot1.fade_at(Time(10000)) == 0.0 and shot1.fade_at(Time(30000)) == 0.0
    assert abs(shot1.fade_at(Time(47500)) - 0.5) < 1e-9
    assert shot1.fade_at(Time(50000)) == 1.0
    assert session.active_clip.shots[1].fade_at(Time(50000)) == 0.0   # no fades set


def test_sound_clips_wav_and_mix():
    import struct
    from array import array
    from Core.Code.sound import active_sound_clips, mix_sequence, parse_wav, sound_path
    assert sound_path("#vo" + chr(92) + "monologues" + chr(92) + "engineer.wav") == "sound/vo/monologues/engineer.wav"
    assert sound_path("*)music/x.wav") == "sound/music/x.wav" and sound_path("") == ""
    # a 16-bit mono wave of 100 frames at 8 kHz, a ramp, plus a stray chunk before the data
    frames = array("h", range(0, 1000, 10))
    fmt = struct.pack("<HHIIHH", 1, 1, 8000, 16000, 2, 16)
    data = frames.tobytes()
    wav = (b"RIFF" + struct.pack("<I", 4 + 8 + len(fmt) + 8 + 5 + 8 + len(data)) + b"WAVE"
           + b"fmt " + struct.pack("<I", len(fmt)) + fmt + b"LIST" + struct.pack("<I", 5) + b"abcde\0"
           + b"data" + struct.pack("<I", len(data)) + data)
    wave = parse_wav(wav, "ramp.wav")
    assert wave.rate == 8000 and wave.channels == 1 and wave.frames == 100 and list(wave.samples[:3]) == [0, 10, 20]
    eight = b"RIFF" + struct.pack("<I", 36 + 4) + b"WAVE" + b"fmt " + struct.pack("<I", 16) + struct.pack("<HHIIHH", 1, 1, 8000, 8000, 1, 8) + b"data" + struct.pack("<I", 4) + bytes([128, 255, 0, 128])
    assert list(parse_wav(eight).samples) == [0, 127 << 8, -128 << 8, 0]

    # a session whose sequence has one sound clip on an unmuted track and one on a muted track
    session = Session(_session())
    doc = session.document
    seq = session.active_clip
    def sound_clip(name, start, duration, offset=0):
        clip = doc.add(Element("DmeSoundClip", name))
        clip.set("timeFrame", AttrType.ELEMENT, _time_frame(doc, start, duration, offset=offset))
        sound = doc.add(Element("DmeGameSound", "sound"))
        sound.set("soundname", AttrType.STRING, "#tools\\ramp.wav")
        sound.set("volume", AttrType.FLOAT, 1.0)
        clip.set("sound", AttrType.ELEMENT, sound)
        return clip
    live = doc.add(Element("DmeTrack", "mix"))
    live.set("children", AttrType.ELEMENT + ARRAY_OFFSET, [sound_clip("a", 10000, 5000, offset=25)])
    live.set("mute", AttrType.BOOL, False)
    muted = doc.add(Element("DmeTrack", "voice"))
    muted.set("children", AttrType.ELEMENT + ARRAY_OFFSET, [sound_clip("b", 0, 5000)])
    muted.set("mute", AttrType.BOOL, True)
    group = seq.track_groups[0]
    group.element.set("tracks", AttrType.ELEMENT + ARRAY_OFFSET, [live.element if hasattr(live, "element") else live, muted])
    placed = active_sound_clips(seq)
    assert [(p.clip.name, p.path, p.start.ticks, p.offset.ticks) for p in placed] == [("a", "sound/tools/ramp.wav", 10000, 25)]

    class _Source:
        def read_bytes(self, rel):
            return wav if rel == "sound/tools/ramp.wav" else None
    mix = mix_sequence(session, _Source(), rate=8000, start=Time(0), end=Time(20000))
    assert mix.rate == 8000 and mix.channels == 2 and mix.frames == 16000 and not mix.warnings
    # silence before the clip; at the clip's start the sound plays from its offset (25 ticks = 0.0025 s = frame 20 = value 200)
    assert mix.samples[0] == 0 and mix.samples[7999 * 2] == 0
    assert mix.samples[8000 * 2] == 200 and mix.samples[8000 * 2 + 1] == 200
    assert mix.samples[8010 * 2] == 300
    # past the sound's end (100 frames) the clip is silent again
    assert mix.samples[8200 * 2] == 0
    # the slice of a span past the mix is padded with silence and the wav is a valid file
    assert len(mix.slice(Time(19000), Time(21000))) == 1600 * 2 * 2          # 0.2 s of stereo 16-bit
    assert parse_wav(mix.wav_bytes()).frames == 16000
