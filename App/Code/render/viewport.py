"""
The viewport widget: a Renderer inside a QOpenGLWidget with orbit controls.

    left drag        orbit; on a manipulator axis, move or rotate the target
    left click       pick what is under the pointer
    middle drag      pan          (also shift + left drag)
    wheel            dolly
    F                frame the model
    W                wireframe
    T / R            manipulator: move / rotate
    X / Y / Z        set the up axis

The scene is built off the GL thread (it is pure Python) and handed over with
`set_scene`; the GPU upload happens on the next paint, with the context current.
"""
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QPoint, Qt, Signal
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
    fmt = QSurfaceFormat()
    fmt.setVersion(3, 3)
    fmt.setProfile(QSurfaceFormat.CoreProfile)
    fmt.setDepthBufferSize(24)
    fmt.setSamples(4)
    return fmt


class Viewport(QOpenGLWidget):
    #: emitted with a human-readable message when the GL side fails
    failed = Signal(str)
    #: emitted after a scene is uploaded, with the scene summary
    scene_ready = Signal(str)
    #: emitted when the user takes hold of the camera
    camera_taken = Signal()
    #: emitted with the instance under a click (or None for empty space)
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

    # -- scene ---------------------------------------------------------------------
    def set_scene(self, scene: Optional[Scene], frame: bool = True) -> None:
        self._pending = scene
        self._pending_frame = frame
        self._scene_changed = True
        self.update()

    @property
    def scene(self) -> Optional[Scene]:
        return self.renderer.scene

    def frame_scene(self) -> None:
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

    # -- input ---------------------------------------------------------------------
    def mousePressEvent(self, event) -> None:
        pos = event.position().toPoint()
        self._last = pos
        self._press = pos
        self._dragged = False
        self.setFocus()
        if event.button() == Qt.LeftButton and not (event.modifiers() & Qt.ShiftModifier):
            axis = self.manipulator.hit(pos.x(), pos.y(), self.project, self._manipulator_size())
            if axis is not None:
                self.manipulator.begin(axis, pos.x(), pos.y(), self.project)
                self.manipulate_begin.emit()
                self.update()
                return
        if event.buttons() & (Qt.LeftButton | Qt.MiddleButton):
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
        if buttons & Qt.MiddleButton or (buttons & Qt.LeftButton and event.modifiers() & Qt.ShiftModifier):
            self.camera.pan(dx, dy, self.height())
        elif buttons & Qt.LeftButton:
            self.camera.orbit(dx, dy)
        else:
            return
        self.update()

    def mouseReleaseEvent(self, event) -> None:
        if self.manipulator.active is not None:
            self.manipulator.end()
            self.manipulate_end.emit()
            self.update()
            return
        if event.button() == Qt.LeftButton and not self._dragged:
            pos = event.position().toPoint()
            self.picked.emit(self.pick(pos.x(), pos.y()))

    def wheelEvent(self, event) -> None:
        self.camera.dolly(event.angleDelta().y() / 120.0)
        self.camera_taken.emit()
        self.update()

    def keyPressEvent(self, event) -> None:
        key = event.key()
        if key == Qt.Key_W:
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
