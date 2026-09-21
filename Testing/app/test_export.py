"""
Export without a GPU: frame timing, the settings' checks, the Targa and AVI writers.
"""
import struct
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from App.Code.export import (ExportSettings, IMAGE_KINDS, MOVIE_KINDS, MjpegAviWriter,
                             frame_times, write_tga)
from Core.API.dmx import Time


def test_frame_times_cover_the_span_at_the_rate():
    times = frame_times(Time(0), Time(20000), 24.0)                 # 2 s at 24 fps
    assert len(times) == 48
    assert times[0] == Time(0) and times[1].ticks == round(10000 / 24)
    assert times[-1].ticks < 20000                                   # the end is not rendered
    # a span that is not a whole number of frames rounds to the nearest count
    assert len(frame_times(Time(0), Time(10000), 30.0)) == 30
    assert len(frame_times(Time(5000), Time(5100), 24.0)) == 1       # never fewer than one
    assert frame_times(Time(5000), Time(5000), 24.0) == []
    assert frame_times(Time(5000), Time(0), 24.0) == []


def test_settings_check_names_the_problem():
    good = ExportSettings(Path("x"), 1280, 720, 24.0, Time(0), Time(10000), kind="png")
    assert good.check() is None and not good.is_movie and good.extension == "png"
    movie = ExportSettings(Path("x.avi"), 1280, 720, 24.0, Time(0), Time(10000), kind="avi")
    assert movie.check() is None and movie.is_movie and movie.extension == "avi"
    assert "kind" in ExportSettings(Path("x"), kind="gif", end=Time(1)).check()
    assert "pixels" in ExportSettings(Path("x"), width=8, end=Time(1)).check()
    assert "rate" in ExportSettings(Path("x"), fps=0.5, end=Time(1)).check()
    assert "empty" in ExportSettings(Path("x"), start=Time(5), end=Time(5)).check()
    assert set(IMAGE_KINDS) == {"png", "jpg", "tga", "bmp"} and set(MOVIE_KINDS) == {"avi", "mp4"}


def test_tga_is_24_bit_top_left_bgr():
    folder = Path(tempfile.mkdtemp(prefix="c2ui_tga_"))
    path = folder / "f.tga"
    write_tga(path, 2, 1, bytes([255, 0, 0, 0, 0, 255]))              # red, blue
    data = path.read_bytes()
    assert len(data) == 18 + 6
    assert data[2] == 2 and struct.unpack_from("<HH", data, 12) == (2, 1) and data[16] == 24 and data[17] == 0x20
    assert data[18:24] == bytes([0, 0, 255, 255, 0, 0])               # BGR


def _walk_avi(data: bytes):
    """(frames in movi, index entries, avih total frames, stream fourccs)."""
    assert data[:4] == b"RIFF" and data[8:12] == b"AVI "
    assert struct.unpack_from("<I", data, 4)[0] == len(data) - 8
    pos, frames, idx, total, fourccs = 12, 0, 0, None, []
    while pos + 8 <= len(data):
        fourcc, size = data[pos:pos + 4], struct.unpack_from("<I", data, pos + 4)[0]
        if fourcc == b"LIST":
            kind = data[pos + 8:pos + 12]
            if kind == b"movi":
                q, end = pos + 12, pos + 8 + size
                while q + 8 <= end:
                    cc, sz = data[q:q + 4], struct.unpack_from("<I", data, q + 4)[0]
                    frames += cc == b"00dc"
                    q += 8 + sz + (sz & 1)
                pos = end
                continue
            pos += 12                                             # descend into hdrl / strl
            continue
        if fourcc == b"avih":
            total = struct.unpack_from("<I", data, pos + 8 + 16)[0]
        elif fourcc == b"strh":
            fourccs.append((data[pos + 8:pos + 12], data[pos + 12:pos + 16]))
        elif fourcc == b"idx1":
            idx = size // 16
        pos += 8 + size + (size & 1)
    return frames, idx, total, fourccs


def test_avi_writer_lays_out_a_valid_riff():
    folder = Path(tempfile.mkdtemp(prefix="c2ui_avi_"))
    path = folder / "m.avi"
    writer = MjpegAviWriter(path, 320, 240, 24.0)
    for size in (101, 200, 57):                                       # odd sizes get a pad byte
        writer.add(b"\xff\xd8" + bytes(size - 4) + b"\xff\xd9")
    writer.close()
    data = path.read_bytes()
    frames, idx, total, fourccs = _walk_avi(data)
    assert frames == 3 and idx == 3 and total == 3
    assert fourccs == [(b"vids", b"MJPG")]
    assert len(data) % 2 == 0
    # the index offsets point at the chunks, relative to the movi list's fourcc
    movi = data.index(b"movi")
    idx_at = data.index(b"idx1") + 8
    for n in range(3):
        _cc, _flags, offset, size = struct.unpack_from("<4sIII", data, idx_at + 16 * n)
        chunk = movi + offset                                          # the first chunk sits at offset 4
        assert data[chunk:chunk + 4] == b"00dc" and struct.unpack_from("<I", data, chunk + 4)[0] == size


def test_samples_spread_over_the_shutter_and_the_lens():
    from App.Code.export import lens_samples, shutter_times
    # one sample, or a closed shutter: the frame's own moment
    assert shutter_times(Time(5000), Time(208), 1, Time(0), Time(10000)) == [Time(5000)]
    assert shutter_times(Time(5000), Time(0), 4, Time(0), Time(10000)) == [Time(5000)] * 4
    # four samples centred on the moment, inside the shutter, never past the clip's end
    times = shutter_times(Time(5000), Time(208), 4, Time(0), Time(10000))
    assert times[0].ticks < 5000 < times[-1].ticks and max(t.ticks for t in times) - min(t.ticks for t in times) < 208
    assert max(t.ticks for t in shutter_times(Time(9999), Time(2000), 4, Time(0), Time(10000))) == 9999
    # the lens: the centre alone, or points on the disk within the radius, all different
    assert lens_samples(1, 0.8) == [(0.0, 0.0)]
    assert lens_samples(4, 0.0) == [(0.0, 0.0)] * 4
    points = lens_samples(16, 0.8)
    assert len(set(points)) == 16 and all(x * x + y * y <= 0.8 * 0.8 + 1e-9 for x, y in points)
    assert "samples per frame" in ExportSettings(Path("x"), end=Time(1), passes=0).check()


def test_avi_writer_interleaves_a_sound_stream():
    from array import array
    from Core.Code.sound import Mix
    folder = Path(tempfile.mkdtemp(prefix="c2ui_avi_"))
    path = folder / "m.avi"
    # 3 frames at 10 fps with 8 kHz stereo: 800 frames of sound per video frame
    mix = Mix(8000, 2, array("h", range(0, 3 * 800 * 2)))
    writer = MjpegAviWriter(path, 64, 48, 10.0, mix)
    for _ in range(3):
        writer.add(b"\xff\xd8" + bytes(96) + b"\xff\xd9")
    writer.close()
    data = path.read_bytes()
    frames, idx, total, fourccs = _walk_avi(data)
    assert frames == 3 and idx == 6 and total == 3
    assert fourccs == [(b"vids", b"MJPG"), (b"auds", b"\x01\x00\x00\x00")]
    assert data.count(b"01wb") == 3 + 3                                # three chunks, three index entries
    # the first sound chunk holds the first 800 stereo frames, verbatim
    at = data.index(b"01wb") + 8
    assert struct.unpack_from("<4h", data, at) == (0, 1, 2, 3)
    assert struct.unpack_from("<I", data, at - 4)[0] == 800 * 2 * 2
