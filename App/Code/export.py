"""
Rendering a session to files: an image sequence or a movie.

The export walks the sequence frame by frame at the chosen rate, evaluates the
session at each moment exactly as playback does, and renders the shot playing
then through its own camera, off screen, at the chosen size.  Frames go to a
folder as numbered images (PNG, JPEG, TGA, BMP) or into a movie: an AVI
carrying Motion JPEG, written here with nothing but the standard library and
Qt's JPEG encoder, or an MP4 (H.264) through Qt Multimedia's recorder - with an
ffmpeg executable as the fallback where that recorder has no encoder.

    settings = ExportSettings(path, width, height, fps, start, end, kind="png")
    result = export(session, library.disk_source(), settings, progress)

Scenes are built once per shot for the run; the map behind them reloads for
each shot, as it does in the editor.  Sound is not exported yet.
"""
from __future__ import annotations

import logging
import math
import shutil
import struct
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

from Core.API.dmx import Time
from Core.API.session import FilmClip, Session
from Core.Code.animation import Evaluator

from .locations import APP_ROOT, USER
from .render.scene import Scene, build_shot_scene, refresh_shot_scene, shot_camera_pose

__all__ = ["ExportSettings", "ExportResult", "export", "frame_times", "lens_samples", "shutter_times",
           "ffmpeg_path", "mp4_available",
           "IMAGE_KINDS", "MOVIE_KINDS", "MjpegAviWriter", "write_tga"]

log = logging.getLogger("c2ui.export")

#: image sequence kinds, in the order the dialog offers them: kind -> (label, extension)
IMAGE_KINDS = {"png": ("PNG images", "png"), "jpg": ("JPEG images", "jpg"),
               "tga": ("Targa images", "tga"), "bmp": ("Windows bitmaps", "bmp")}
#: movie kinds: kind -> (label, extension)
MOVIE_KINDS = {"avi": ("AVI movie (Motion JPEG)", "avi"), "mp4": ("MP4 movie (H.264)", "mp4")}

#: where exports go unless the user picks somewhere else
DEFAULT_FOLDER = USER / "Export"


@dataclass
class ExportSettings:
    """What to render and where."""
    #: a folder for an image sequence, a file for a movie
    path: Path
    width: int = 1280
    height: int = 720
    fps: float = 24.0
    #: the span to render, in sequence time (the timeline's)
    start: Time = Time(0)
    end: Time = Time(0)
    #: one of IMAGE_KINDS or MOVIE_KINDS
    kind: str = "png"
    #: JPEG / movie quality, 1..100
    quality: int = 90
    #: image file stem: <name>_0001.png
    name: str = "frame"
    #: multisample count for the off-screen frame
    samples: int = 4
    #: renders per frame, spread over the camera's shutter (motion blur) and its lens
    #: (depth of field); 1 renders each frame once, sharp and unblurred
    passes: int = 16

    @property
    def is_movie(self) -> bool:
        """True for a single movie file, False for a folder of images."""
        return self.kind in MOVIE_KINDS

    @property
    def extension(self) -> str:
        """The file extension for this kind."""
        return (MOVIE_KINDS.get(self.kind) or IMAGE_KINDS.get(self.kind) or ("", self.kind))[1]

    def check(self) -> Optional[str]:
        """Why the settings cannot be used, or None when they can."""
        if self.kind not in IMAGE_KINDS and self.kind not in MOVIE_KINDS:
            return f"unknown output kind {self.kind!r}"
        if self.width < 16 or self.height < 16 or self.width > 8192 or self.height > 8192:
            return "the frame must be between 16 and 8192 pixels each way"
        if not 1.0 <= self.fps <= 240.0:
            return "the frame rate must be between 1 and 240"
        if not 1 <= self.passes <= 256:
            return "samples per frame must be between 1 and 256"
        if self.end.ticks <= self.start.ticks:
            return "the range is empty"
        if self.kind == "mp4" and not mp4_available():
            return "no H.264 encoder: Qt Multimedia is missing and there is no ffmpeg in App/Data/bin or on the PATH"
        return None


@dataclass
class ExportResult:
    """What an export produced."""
    frames: int = 0
    files: List[Path] = field(default_factory=list)
    cancelled: bool = False
    warnings: List[str] = field(default_factory=list)
    seconds: float = 0.0

    @property
    def summary(self) -> str:
        """One line for the status bar."""
        state = "cancelled after" if self.cancelled else "wrote"
        where = self.files[0] if len(self.files) == 1 else (self.files[0].parent if self.files else "")
        return f"export {state} {self.frames} frames to {where} in {self.seconds:.1f} s"


#: how far the lens opens per unit of the camera's aperture, in world units: the
#: radius of the disk the eye is moved over for depth of field
APERTURE_RADIUS = 0.1
#: the golden angle: consecutive samples on the disk never line up
_GOLDEN = 2.399963229728653


def lens_samples(count: int, radius: float) -> List[Tuple[float, float]]:
    """`count` points on a disk of `radius`, evenly spread (a Vogel spiral); one point
    at the centre when there is only one or no radius."""
    if count <= 1 or radius <= 0.0:
        return [(0.0, 0.0)] * max(1, count)
    out = []
    for k in range(count):
        r = radius * math.sqrt((k + 0.5) / count)
        a = k * _GOLDEN
        out.append((r * math.cos(a), r * math.sin(a)))
    return out


def shutter_times(moment: Time, shutter: Time, count: int, start: Time, end: Time) -> List[Time]:
    """`count` moments spread over the shutter centred on `moment`, kept inside
    [start, end) so a frame never samples the neighbouring shot."""
    if count <= 1 or shutter.ticks <= 0:
        return [moment] * max(1, count)
    out = []
    for k in range(count):
        offset = shutter.ticks * ((k + 0.5) / count - 0.5)
        ticks = moment.ticks + round(offset)
        out.append(Time(min(max(ticks, start.ticks), end.ticks - 1)))
    return out


def frame_times(start: Time, end: Time, fps: float) -> List[Time]:
    """The moments rendered for a span at a rate: `start`, then every 1 / fps
    seconds, up to but not including `end` - a 2 s clip at 24 fps is 48 frames."""
    if end.ticks <= start.ticks or fps <= 0:
        return []
    count = max(1, round((end.ticks - start.ticks) / Time.PER_SECOND * fps))
    return [Time(start.ticks + round(n * Time.PER_SECOND / fps)) for n in range(count)]


def ffmpeg_path() -> Optional[str]:
    """An ffmpeg executable: `App/Data/bin/ffmpeg(.exe)` first, then the PATH; None when absent."""
    for candidate in (APP_ROOT / "Data" / "bin" / "ffmpeg.exe", APP_ROOT / "Data" / "bin" / "ffmpeg"):
        if candidate.is_file():
            return str(candidate)
    return shutil.which("ffmpeg")


def _qt_recorder_available() -> bool:
    """True when Qt Multimedia can take frames straight into a recorder (Qt 6.8+)."""
    try:
        from PySide6.QtMultimedia import QVideoFrameInput  # noqa: F401
    except ImportError:
        return False
    return True


def mp4_available() -> bool:
    """True when an MP4 can be written: Qt's recorder, or an ffmpeg executable."""
    return _qt_recorder_available() or ffmpeg_path() is not None


# ---------------------------------------------------------------------------
#  Writers: a folder of images, an AVI, an ffmpeg pipe
# ---------------------------------------------------------------------------
def write_tga(path: Path, width: int, height: int, rgb: bytes) -> None:
    """A 24-bit uncompressed Targa from top-row-first RGB bytes."""
    header = struct.pack("<BBBHHBHHHHBB", 0, 0, 2, 0, 0, 0, 0, 0, width, height, 24, 0x20)  # 0x20: top-left origin
    rows = bytearray(len(rgb))
    rows[0::3] = rgb[2::3]                       # Targa stores BGR
    rows[1::3] = rgb[1::3]
    rows[2::3] = rgb[0::3]
    path.write_bytes(header + bytes(rows))


class MjpegAviWriter:
    """An AVI of Motion JPEG frames: each frame is one JPEG in a `00dc` chunk,
    with the `idx1` index players need to seek.  Plain RIFF, no dependencies;
    the AVI 1.0 layout holds up to 2 GB."""

    def __init__(self, path: Path, width: int, height: int, fps: float) -> None:
        self.path = path
        self.width, self.height, self.fps = width, height, fps
        self._file = open(path, "wb")
        self._index: List[Tuple[int, int]] = []     # (offset from movi start, size) per frame
        self._largest = 0
        self._file.write(self._headers(0, 0))
        self._movi_start = self._file.tell()
        self._file.write(b"LIST" + struct.pack("<I", 0) + b"movi")

    def add(self, jpeg: bytes) -> None:
        """Append one frame."""
        offset = self._file.tell() - (self._movi_start + 8)
        padded = jpeg + (b"\0" if len(jpeg) & 1 else b"")
        self._file.write(b"00dc" + struct.pack("<I", len(jpeg)) + padded)
        self._index.append((offset, len(jpeg)))
        self._largest = max(self._largest, len(jpeg))

    def close(self) -> None:
        """Write the index and the final sizes."""
        f = self._file
        movi_end = f.tell()
        f.write(b"idx1" + struct.pack("<I", 16 * len(self._index)))
        for offset, size in self._index:
            f.write(b"00dc" + struct.pack("<III", 0x10, offset, size))    # AVIIF_KEYFRAME
        end = f.tell()
        f.seek(self._movi_start + 4)
        f.write(struct.pack("<I", movi_end - self._movi_start - 8))
        f.seek(0)
        f.write(self._headers(len(self._index), end - 8))
        f.close()

    def _headers(self, frames: int, riff_size: int) -> bytes:
        """The RIFF header and the `hdrl` list, sized for `frames` frames."""
        rate = max(1, round(self.fps * 1000))
        scale = 1000
        us_per_frame = round(1_000_000 / self.fps) if self.fps else 0
        avih = struct.pack("<IIIIIIIIIIIIII", us_per_frame, self._largest * max(1, round(self.fps)), 0,
                           0x10, frames, 0, 1, self._largest, self.width, self.height, 0, 0, 0, 0)
        strh = (b"vids" + b"MJPG" + struct.pack("<IHHIIIIIIII", 0, 0, 0, 0, scale, rate, 0, frames,
                                                 self._largest, 0xFFFFFFFF, 0)
                + struct.pack("<hhhh", 0, 0, self.width, self.height))
        strf = struct.pack("<IiiHHIIiiII", 40, self.width, self.height, 1, 24, 0x47504A4D,   # 'MJPG'
                           self.width * self.height * 3, 0, 0, 0, 0)
        strl = _list(b"strl", _chunk(b"strh", strh) + _chunk(b"strf", strf))
        hdrl = _list(b"hdrl", _chunk(b"avih", avih) + strl)
        return b"RIFF" + struct.pack("<I", riff_size) + b"AVI " + hdrl


def _chunk(fourcc: bytes, data: bytes) -> bytes:
    return fourcc + struct.pack("<I", len(data)) + data + (b"\0" if len(data) & 1 else b"")


def _list(fourcc: bytes, data: bytes) -> bytes:
    return b"LIST" + struct.pack("<I", len(data) + 4) + fourcc + data


class _QtMovieWriter:
    """Frames handed to Qt Multimedia's recorder, which encodes H.264 into an MP4
    with the platform's encoder.  The recorder works asynchronously; this waits on
    its signals by pumping events, so the export stays one straight loop."""

    def __init__(self, path: Path, width: int, height: int, fps: float, quality: int) -> None:
        from PySide6.QtCore import QSize, QUrl
        from PySide6.QtMultimedia import QMediaCaptureSession, QMediaFormat, QMediaRecorder, QVideoFrameInput

        self.path = path
        self.fps = fps
        self.index = 0
        self.error = ""
        self.session = QMediaCaptureSession()
        self.input = QVideoFrameInput()
        self.session.setVideoFrameInput(self.input)
        self.recorder = QMediaRecorder()
        self.session.setRecorder(self.recorder)
        media = QMediaFormat(QMediaFormat.MPEG4)
        media.setVideoCodec(QMediaFormat.VideoCodec.H264)
        self.recorder.setMediaFormat(media)
        levels = (QMediaRecorder.VeryLowQuality, QMediaRecorder.LowQuality, QMediaRecorder.NormalQuality,
                  QMediaRecorder.HighQuality, QMediaRecorder.VeryHighQuality)
        self.recorder.setQuality(levels[min(4, max(0, (quality - 1) // 20))])
        self.recorder.setVideoFrameRate(fps)
        self.recorder.setVideoResolution(QSize(width, height))
        self.recorder.setOutputLocation(QUrl.fromLocalFile(str(path.resolve())))   # relative paths are refused
        self.recorder.errorOccurred.connect(self._failed)
        self.recorder.record()

    def _failed(self, _error, message: str) -> None:
        self.error = self.error or message

    def add(self, image) -> None:
        """Queue one frame, stamped at its time; waits while the encoder catches up."""
        from PySide6.QtGui import QImage
        from PySide6.QtMultimedia import QVideoFrame
        frame = QVideoFrame(image.convertToFormat(QImage.Format_RGBA8888))
        frame.setStartTime(round(self.index * 1_000_000 / self.fps))
        frame.setEndTime(round((self.index + 1) * 1_000_000 / self.fps))
        self.index += 1
        for _attempt in range(3000):                    # 30 s at most
            if self.error:
                raise RuntimeError(f"MP4 encoder: {self.error}")
            if self.input.sendVideoFrame(frame):
                return
            _pump(10)
        raise RuntimeError("MP4 encoder stopped taking frames")

    def close(self) -> Optional[str]:
        """Stop the recorder and wait for the file to be finished."""
        from PySide6.QtMultimedia import QMediaRecorder
        self.recorder.stop()
        for _attempt in range(3000):
            if self.recorder.recorderState() == QMediaRecorder.StoppedState:
                break
            _pump(10)
        _pump(50)                                        # let the last write settle
        if self.error:
            return f"MP4 encoder: {self.error}"
        if not self.path.is_file() or self.path.stat().st_size == 0:
            return "MP4 encoder wrote nothing"
        return None


def _pump(milliseconds: int) -> None:
    """Run the event loop for a moment so Qt's recorder can work."""
    from PySide6.QtCore import QCoreApplication, QEventLoop, QTimer
    loop = QEventLoop()
    QTimer.singleShot(milliseconds, loop.quit)
    loop.exec()
    QCoreApplication.processEvents()


class _FfmpegWriter:
    """Raw RGB frames piped into ffmpeg, which writes H.264 in an MP4."""

    def __init__(self, path: Path, width: int, height: int, fps: float, quality: int) -> None:
        exe = ffmpeg_path()
        if exe is None:
            raise RuntimeError("ffmpeg not found")
        crf = round(35 - quality * 0.2)                        # 100 -> 15 (near lossless), 50 -> 25
        self.process = subprocess.Popen(
            [exe, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
             "-s", f"{width}x{height}", "-r", f"{fps:g}", "-i", "-",
             "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-pix_fmt", "yuv420p",
             "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", str(path)],
            stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    def add(self, rgb: bytes) -> None:
        """Pipe one frame."""
        assert self.process.stdin is not None
        self.process.stdin.write(rgb)

    def close(self) -> Optional[str]:
        """Finish the file; returns ffmpeg's complaint, if any."""
        assert self.process.stdin is not None
        self.process.stdin.close()
        _out, err = self.process.communicate()
        if self.process.returncode:
            return err.decode("utf-8", "replace").strip() or f"ffmpeg exited with {self.process.returncode}"
        return None


# ---------------------------------------------------------------------------
#  The export
# ---------------------------------------------------------------------------
class _Offscreen:
    """A GL 3.3 context of its own with a multisampled frame to draw into."""

    def __init__(self, width: int, height: int, samples: int) -> None:
        from PySide6.QtGui import QOffscreenSurface, QOpenGLContext
        from PySide6.QtOpenGL import QOpenGLFramebufferObject, QOpenGLFramebufferObjectFormat

        from .render.viewport import gl_format
        fmt = gl_format()
        self.context = QOpenGLContext()
        self.context.setFormat(fmt)
        if not self.context.create():
            raise RuntimeError("no OpenGL 3.3 context for the export")
        self.surface = QOffscreenSurface()
        self.surface.setFormat(fmt)
        self.surface.create()
        if not self.context.makeCurrent(self.surface):
            raise RuntimeError("the export context cannot be made current")
        fbo_format = QOpenGLFramebufferObjectFormat()
        fbo_format.setAttachment(QOpenGLFramebufferObject.CombinedDepthStencil)
        fbo_format.setSamples(samples)
        self.fbo = QOpenGLFramebufferObject(width, height, fbo_format)
        if not self.fbo.isValid() or not self.fbo.bind():
            raise RuntimeError(f"no {width}x{height} frame buffer for the export")

    def bind(self) -> None:
        """Make the context current and the frame the draw target again: a progress
        callback may have let the viewport paint, and resolving an image unbinds."""
        if not self.context.makeCurrent(self.surface):
            raise RuntimeError("the export context cannot be made current")
        self.fbo.bind()

    def image(self):
        """The frame as a QImage, multisampling resolved, top row first."""
        return self.fbo.toImage()

    def release(self) -> None:
        """Drop the frame buffer and the context."""
        self.context.makeCurrent(self.surface)
        self.fbo.release()
        self.fbo = None
        self.context.doneCurrent()
        self.surface.destroy()


def export(session: Session, source, settings: ExportSettings,
           progress: Optional[Callable[[int, int], bool]] = None) -> ExportResult:
    """Render the session's active sequence over `settings`' span.  `progress`
    is told (frames done, frames in all) after every frame and stops the export
    by returning False.  The elements are left evaluated at the last frame; the
    caller re-evaluates at its own time.  Needs a Qt application object."""
    import time as clock

    from PySide6.QtCore import QBuffer, QIODevice
    from PySide6.QtGui import QImage

    from .render.camera import OrbitCamera
    from .render.renderer import Renderer

    problem = settings.check()
    if problem:
        raise ValueError(problem)
    clip = session.active_clip
    if clip is None:
        raise ValueError("the session has no active sequence")
    times = frame_times(settings.start, settings.end, settings.fps)
    result = ExportResult()
    started = clock.perf_counter()

    if settings.is_movie:
        settings.path.parent.mkdir(parents=True, exist_ok=True)
    else:
        settings.path.mkdir(parents=True, exist_ok=True)
    writer = None
    if settings.kind == "avi":
        writer = MjpegAviWriter(settings.path, settings.width, settings.height, settings.fps)
    elif settings.kind == "mp4":
        if _qt_recorder_available():
            writer = _QtMovieWriter(settings.path, settings.width, settings.height, settings.fps, settings.quality)
        else:
            writer = _FfmpegWriter(settings.path, settings.width, settings.height, settings.fps, settings.quality)

    screen = _Offscreen(settings.width, settings.height, settings.samples)
    renderer = Renderer()
    renderer.initialize()
    renderer.background = (0.0, 0.0, 0.0, 1.0)         # a movie has no editor grey behind it
    evaluator = Evaluator()
    camera = OrbitCamera()
    camera.up_axis = "z"
    scenes: Dict[int, Scene] = {}
    current: Optional[FilmClip] = None
    scene: Optional[Scene] = None
    digits = max(4, len(str(len(times))))
    try:
        for index, moment in enumerate(times):
            evaluator.evaluate(clip, moment)
            shot = clip.shot_at(moment)
            if shot is None:
                scene = None
                renderer.set_scene(None)
                current = None
            elif current is None or shot.element is not current.element:
                scene = scenes.get(id(shot.element))
                if scene is None:
                    scene = build_shot_scene(source, shot, clip.map_name)
                    scenes[id(shot.element)] = scene
                    for warning in scene.warnings:
                        result.warnings.append(f"{shot.name}: {warning}")
                renderer.set_scene(scene)
                current = shot
            screen.bind()
            if scene is None or shot is None:
                renderer.draw(camera, settings.width, settings.height)
            else:
                # several renders per frame: the shutter open for motion blur, the eye moved
                # over the lens for depth of field, each sample evaluated at its own moment
                shot_camera = shot.camera
                passes = settings.passes if shot_camera is not None else 1
                shutter = shot_camera.shutter_speed if shot_camera is not None else Time(0)
                radius = shot_camera.aperture * APERTURE_RADIUS if shot_camera is not None else 0.0
                moments = shutter_times(moment, shutter, passes, shot.time_frame.start, shot.time_frame.end)
                lens = lens_samples(passes, radius)
                renderer.begin_frame(settings.width, settings.height)
                for sample, (at, (dx, dy)) in enumerate(zip(moments, lens)):
                    if passes > 1 or sample == 0:
                        if at.ticks != moment.ticks or sample > 0:
                            evaluator.evaluate(clip, at)
                        refresh_shot_scene(scene, shot)
                    scene.fade = shot.fade_at(moment)
                    if shot_camera is not None:
                        eye, target, fov = shot_camera_pose(shot, shot_camera, settings.width / settings.height)
                        camera.look_from(eye, target, fov_y=fov)
                        if dx or dy:
                            _forward, right, up = camera.screen_axes()
                            eye = tuple(eye[i] + right[i] * dx + up[i] * dy for i in range(3))
                            camera.look_from(eye, target, fov_y=fov)
                    else:
                        camera.frame(scene.bounds, guess_up=False)
                    screen.bind()
                    renderer.draw_sample(camera, settings.width, settings.height, 1.0 / passes)
                renderer.finish_frame(settings.width, settings.height)
            image = screen.image().convertToFormat(QImage.Format_RGB888)
            if settings.is_movie:
                if settings.kind == "avi":
                    buffer = QBuffer()
                    buffer.open(QIODevice.WriteOnly)
                    image.save(buffer, "JPG", settings.quality)
                    writer.add(bytes(buffer.data()))
                elif isinstance(writer, _QtMovieWriter):
                    writer.add(image)
                else:
                    writer.add(_rgb_bytes(image))
            else:
                path = settings.path / f"{settings.name}_{index + 1:0{digits}d}.{settings.extension}"
                if settings.kind == "tga":
                    write_tga(path, image.width(), image.height(), _rgb_bytes(image))
                elif not image.save(str(path), settings.kind.upper(), settings.quality if settings.kind == "jpg" else -1):
                    raise RuntimeError(f"cannot write {path}")
                result.files.append(path)
            result.frames = index + 1
            if progress is not None and not progress(index + 1, len(times)):
                result.cancelled = True
                break
    finally:
        renderer.release()
        screen.release()
        if writer is not None:
            complaint = writer.close()
            if complaint:
                result.warnings.append(complaint)
            result.files.append(settings.path)
    result.seconds = clock.perf_counter() - started
    log.info(result.summary)
    return result


def _rgb_bytes(image) -> bytes:
    """Tightly packed RGB rows of a Format_RGB888 image."""
    width, height = image.width(), image.height()
    stride = image.bytesPerLine()
    raw = bytes(image.constBits())
    if stride == width * 3:
        return raw
    return b"".join(raw[y * stride:y * stride + width * 3] for y in range(height))
