"""
The viewport widget: a Renderer inside a QOpenGLWidget with orbit controls.

    left drag        orbit
    middle drag      pan          (also shift + left drag)
    wheel            dolly
    F                frame the model
    W                wireframe
    X / Y / Z        set the up axis

The scene is built off the GL thread (it is pure Python) and handed over with
`set_scene`; the GPU upload happens on the next paint, with the context current.
"""
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from .camera import OrbitCamera
from .renderer import Renderer
from .scene import Scene
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
        self._ready = False

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
        self.renderer.draw(self.camera, int(self.width() * ratio), int(self.height() * ratio))

    # -- input ---------------------------------------------------------------------
    def mousePressEvent(self, event) -> None:
        self._last = event.position().toPoint()
        self.setFocus()
        if event.buttons() & (Qt.LeftButton | Qt.MiddleButton):
            self.camera_taken.emit()

    def mouseMoveEvent(self, event) -> None:
        pos = event.position().toPoint()
        dx, dy = pos.x() - self._last.x(), pos.y() - self._last.y()
        self._last = pos
        buttons = event.buttons()
        if buttons & Qt.MiddleButton or (buttons & Qt.LeftButton and event.modifiers() & Qt.ShiftModifier):
            self.camera.pan(dx, dy, self.height())
        elif buttons & Qt.LeftButton:
            self.camera.orbit(dx, dy)
        else:
            return
        self.update()

    def wheelEvent(self, event) -> None:
        self.camera.dolly(event.angleDelta().y() / 120.0)
        self.camera_taken.emit()
        self.update()

    def keyPressEvent(self, event) -> None:
        key = event.key()
        if key == Qt.Key_F:
            self.frame_scene()
        elif key == Qt.Key_W:
            self.renderer.wireframe = not self.renderer.wireframe
            self.update()
        elif key in (Qt.Key_X, Qt.Key_Y, Qt.Key_Z):
            self.camera.up_axis = {Qt.Key_X: "x", Qt.Key_Y: "y", Qt.Key_Z: "z"}[key]
            self.update()
        else:
            super().keyPressEvent(event)
