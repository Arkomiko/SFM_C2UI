"""
The viewport widget: a Renderer inside a QOpenGLWidget with SFM's controls.

    right drag             look around from where the camera is
    right + W A S D        fly forward / left / back / right (Z or Q down, X or E up;
                           Shift faster, Ctrl slower)
    middle drag            pan
    Alt + left drag        orbit the target
    wheel                  dolly
    left click             pick the bone under the pointer (instance, then bone)
    left drag on an axis   move or rotate along the manipulator
    F3                     wireframe
    T / R                  manipulator: move / rotate
    X / Y / Z              set the up axis

`F` (frame the selection) and the playback keys are the window's shortcuts.

The scene is built off the GL thread (it is pure Python) and handed over with
`set_scene`; the GPU upload happens on the next paint, with the context current.
"""
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QElapsedTimer, QPoint, Qt, QTimer, Signal
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtOpenGL import QOpenGLFramebufferObject, QOpenGLFramebufferObjectFormat
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from .camera import OrbitCamera
from .manipulator import MOVE, ROTATE, Manipulator
from .math3d import multiply, transform_point
from .renderer import Renderer
from .scene import Scene, SceneInstance
from .shaders import ShaderError

__all__ = ["Viewport", "gl_format"]


def gl_format() -> QSurfaceFormat:
    """The GL 3.3 core surface format the viewport needs."""
    fmt = QSurfaceFormat()
    fmt.setVersion(3, 3)
    fmt.setProfile(QSurfaceFormat.CoreProfile)
    fmt.setDepthBufferSize(24)
    fmt.setSamples(4)
    return fmt


class Viewport(QOpenGLWidget):
    #: emitted with a human-readable message when the GL side fails
    """The 3D view: renders a Scene, handles the SFM camera and picking."""
    failed = Signal(str)
    #: emitted after a scene is uploaded, with the scene summary
    scene_ready = Signal(str)
    #: emitted when the user takes hold of the camera
    camera_taken = Signal()
    #: emitted with (instance, bone index) under a click, or (None, -1) for empty space;
    #: the bone is the one weighting the nearest vertex, -1 when the model has none
    picked = Signal(object)
    #: manipulator drags: begin, a delta (Vec3 or (axis, angle)), end
    manipulate_begin = Signal()
    manipulated = Signal(object)
    manipulate_end = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setFormat(gl_format())
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMinimumSize(200, 150)
        self.camera = OrbitCamera()
        self.renderer = Renderer()
        self._pending: Optional[Scene] = None
        self._pending_frame = False
        self._scene_changed = False
        self._last = QPoint()
        self._press = QPoint()
        self._dragged = False
        self._ready = False
        self.manipulator = Manipulator()
        self._pick_fbo: Optional[QOpenGLFramebufferObject] = None
        #: manipulator size in pixels
        self.manipulator_pixels = 90
        # SFM's flight: keys held while the right button is down move the camera
        self._keys_down: set = set()
        self._fly_timer = QTimer(self)
        self._fly_timer.setInterval(16)
        self._fly_timer.timeout.connect(self._fly_tick)
        self._fly_clock = QElapsedTimer()
        self._looking = False

    # -- scene ---------------------------------------------------------------------
    def set_scene(self, scene: Optional[Scene], frame: bool = True) -> None:
        """Show `scene` on the next paint, framing it when `frame` is set."""
        self._pending = scene
        self._pending_frame = frame
        self._scene_changed = True
        self.update()

    @property
    def scene(self) -> Optional[Scene]:
        """The scene on screen, or None."""
        return self.renderer.scene

    def frame_scene(self) -> None:
        """Fit the camera to the whole scene."""
        scene = self.renderer.scene
        if scene is not None:
            self._frame(scene)
            self.update()

    def _frame(self, scene: Scene) -> None:
        """Fit the scene; a session says which way is up, a lone model does not."""
        if scene.up_axis:
            self.camera.up_axis = scene.up_axis
            self.camera.frame(scene.bounds, guess_up=False)
        else:
            self.camera.frame(scene.bounds)

    # -- GL ------------------------------------------------------------------------
    def initializeGL(self) -> None:
        try:
            self.renderer.initialize()
            self._ready = True
        except ShaderError as exc:
            self.failed.emit(f"shader failed to build:\n{exc}")
        # free GPU objects while the context still exists
        self.context().aboutToBeDestroyed.connect(self._release)

    def _release(self) -> None:
        self.makeCurrent()
        self.renderer.release()
        self._ready = False
        self.doneCurrent()

    def paintGL(self) -> None:
        if not self._ready:
            return
        if self._scene_changed:
            self._scene_changed = False
            scene, self._pending = self._pending, None
            self.renderer.set_scene(scene)
            if scene is not None and self._pending_frame:
                self._frame(scene)
            self._pending_frame = False
            if self.renderer.errors:
                self.failed.emit("\n".join(self.renderer.errors))
                self.renderer.errors.clear()
            if scene is not None:
                self.scene_ready.emit(scene.summary())
        ratio = self.devicePixelRatioF()
        self.renderer.overlay_lines = self.manipulator.lines(self._manipulator_size())
        self.renderer.draw(self.camera, int(self.width() * ratio), int(self.height() * ratio))

    # -- projection and picking ------------------------------------------------------
    def _view_proj(self):
        return multiply(self.camera.projection(self.width() / max(1, self.height())), self.camera.view())

    def project(self, point):
        """World point to (x, y, depth) in widget pixels, or None when behind."""
        vp = self._view_proj()
        x, y, z = point
        w = vp[3] * x + vp[7] * y + vp[11] * z + vp[15]
        if w <= 1e-6:
            return None
        nx, ny, nz = transform_point(vp, point)
        return ((nx * 0.5 + 0.5) * self.width(), (0.5 - ny * 0.5) * self.height(), nz)

    def _manipulator_size(self) -> float:
        """A world length that shows as about `manipulator_pixels` on screen."""
        import math
        o = self.manipulator.origin
        eye = self.camera.eye()
        distance = math.dist(o, eye)
        per_pixel = 2.0 * distance * math.tan(self.camera.fov_y / 2.0) / max(1, self.height())
        return max(1e-3, per_pixel * self.manipulator_pixels)

    def pick(self, x: int, y: int) -> Optional[SceneInstance]:
        """The instance under a widget pixel, from an id pass into an offscreen buffer."""
        if not self._ready or self.renderer.scene is None:
            return None
        ratio = self.devicePixelRatioF()
        width, height = max(1, int(self.width() * ratio)), max(1, int(self.height() * ratio))
        self.makeCurrent()
        try:
            if self._pick_fbo is None or self._pick_fbo.size().width() != width or self._pick_fbo.size().height() != height:
                fmt = QOpenGLFramebufferObjectFormat()
                fmt.setAttachment(QOpenGLFramebufferObject.CombinedDepthStencil)
                self._pick_fbo = QOpenGLFramebufferObject(width, height, fmt)
            self._pick_fbo.bind()
            self.renderer.draw_ids(self.camera, width, height)
            found = self.renderer.instance_at(int(x * ratio), int(y * ratio), width, height)
            self._pick_fbo.release()
            # back to the widget's own framebuffer
            from OpenGL import GL
            GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.defaultFramebufferObject())
        finally:
            self.doneCurrent()
        return found

    def pick_bone(self, instance: SceneInstance, x: int, y: int) -> int:
        """The bone weighting the vertex nearest the pixel, on the CPU from the posed
        skinning matrices; -1 when the model has no bones or nothing projects."""
        if not instance.bones:
            return -1
        best, best_d = -1, 24.0 ** 2                      # within 24 px, else it is not that bone
        world = instance.world
        bones = instance.bones
        for item in instance.loaded.items:
            mesh = item.mesh
            pos, idx, wgt = mesh.positions, mesh.bone_indices, mesh.bone_weights
            n = len(pos) // 3
            if len(idx) < n * 3 or len(wgt) < n * 3:
                continue
            for v in range(0, n, 2):                      # every other vertex is plenty
                px, py, pz = pos[3 * v], pos[3 * v + 1], pos[3 * v + 2]
                sx = sy = sz = 0.0
                heaviest, heaviest_w = -1, 0.0
                for k in range(3):
                    w = wgt[3 * v + k]
                    if w <= 0.0:
                        continue
                    b = idx[3 * v + k]
                    if b >= len(bones):
                        continue
                    m = bones[b]
                    sx += w * (m[0] * px + m[1] * py + m[2] * pz + m[3])
                    sy += w * (m[4] * px + m[5] * py + m[6] * pz + m[7])
                    sz += w * (m[8] * px + m[9] * py + m[10] * pz + m[11])
                    if w > heaviest_w:
                        heaviest, heaviest_w = b, w
                if heaviest < 0:
                    continue
                wx = world[0] * sx + world[4] * sy + world[8] * sz + world[12]
                wy = world[1] * sx + world[5] * sy + world[9] * sz + world[13]
                wz = world[2] * sx + world[6] * sy + world[10] * sz + world[14]
                screen = self.project((wx, wy, wz))
                if screen is None:
                    continue
                d = (screen[0] - x) ** 2 + (screen[1] - y) ** 2
                if d < best_d:
                    best, best_d = heaviest, d
        return best

    # -- input: SFM's scheme -------------------------------------------------------
    #   left click      select what is under the cursor (a bone of a model)
    #   left drag       the manipulator, when the press lands on it
    #   right drag      look around from where the camera is; hold it and fly with
    #                   W A S D (forward, left, back, right), Z / X (down, up),
    #                   Shift faster, Ctrl slower
    #   middle drag     pan;  Alt + left drag  orbit the target;  wheel  dolly
    def mousePressEvent(self, event) -> None:
        pos = event.position().toPoint()
        self._last = pos
        self._press = pos
        self._dragged = False
        self.setFocus()
        if event.button() == Qt.LeftButton and not (event.modifiers() & Qt.AltModifier):
            axis = self.manipulator.hit(pos.x(), pos.y(), self.project, self._manipulator_size())
            if axis is not None:
                self.manipulator.begin(axis, pos.x(), pos.y(), self.project)
                self.manipulate_begin.emit()
                self.update()
                return
        if event.button() == Qt.RightButton:
            self._looking = True
            self._fly_clock.start()
            self._fly_timer.start()
            self.camera_taken.emit()
        elif event.button() == Qt.MiddleButton or (event.button() == Qt.LeftButton and event.modifiers() & Qt.AltModifier):
            self.camera_taken.emit()

    def mouseMoveEvent(self, event) -> None:
        pos = event.position().toPoint()
        dx, dy = pos.x() - self._last.x(), pos.y() - self._last.y()
        self._last = pos
        if (pos - self._press).manhattanLength() > 3:
            self._dragged = True
        buttons = event.buttons()
        if self.manipulator.active is not None and buttons & Qt.LeftButton:
            delta = self.manipulator.drag(pos.x(), pos.y(), self.project, self._manipulator_size())
            if delta is not None:
                self.manipulated.emit(delta)
            self.update()
            return
        if buttons & Qt.RightButton:
            self.camera.look(dx, dy)
        elif buttons & Qt.MiddleButton:
            self.camera.pan(dx, dy, self.height())
        elif buttons & Qt.LeftButton and event.modifiers() & Qt.AltModifier:
            self.camera.orbit(dx, dy)
        else:
            return
        self.update()

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.RightButton:
            self._looking = False
            if not self._keys_down:
                self._fly_timer.stop()
        if self.manipulator.active is not None:
            self.manipulator.end()
            self.manipulate_end.emit()
            self.update()
            return
        if event.button() == Qt.LeftButton and not self._dragged and not (event.modifiers() & Qt.AltModifier):
            pos = event.position().toPoint()
            instance = self.pick(pos.x(), pos.y())
            bone = self.pick_bone(instance, pos.x(), pos.y()) if instance is not None else -1
            self.picked.emit((instance, bone))

    def wheelEvent(self, event) -> None:
        self.camera.dolly(event.angleDelta().y() / 120.0)
        self.camera_taken.emit()
        self.update()

    def _fly_tick(self) -> None:
        """Move while the right button is held and flight keys are down."""
        seconds = self._fly_clock.restart() / 1000.0
        if not self._looking or not self._keys_down:
            return
        keys = self._keys_down
        forward = (Qt.Key_W in keys) - (Qt.Key_S in keys)
        right = (Qt.Key_D in keys) - (Qt.Key_A in keys)
        up = (Qt.Key_X in keys or Qt.Key_E in keys) - (Qt.Key_Z in keys or Qt.Key_Q in keys)
        if not (forward or right or up):
            return
        speed = self.camera.distance * 1.5                # units per second, scaled to the scene
        if Qt.Key_Shift in keys:
            speed *= 4.0
        if Qt.Key_Control in keys:
            speed *= 0.25
        step = speed * min(seconds, 0.1)
        self.camera.fly(forward * step, right * step, up * step)
        self.update()

    def keyReleaseEvent(self, event) -> None:
        self._keys_down.discard(event.key())
        if not self._keys_down and not self._looking:
            self._fly_timer.stop()
        super().keyReleaseEvent(event)

    def keyPressEvent(self, event) -> None:
        key = event.key()
        self._keys_down.add(key)
        if self._looking:
            if not self._fly_timer.isActive():
                self._fly_clock.start()
                self._fly_timer.start()
            return                                        # flight keys never reach the shortcuts
        if key == Qt.Key_F3:
            self.renderer.wireframe = not self.renderer.wireframe
            self.update()
        elif key == Qt.Key_T:
            self.manipulator.mode = MOVE
            self.update()
        elif key == Qt.Key_R:
            self.manipulator.mode = ROTATE
            self.update()
        elif key in (Qt.Key_X, Qt.Key_Y, Qt.Key_Z):
            self.camera.up_axis = {Qt.Key_X: "x", Qt.Key_Y: "y", Qt.Key_Z: "z"}[key]
            self.update()
        else:
            super().keyPressEvent(event)
