"""
The editor window: a viewport in the middle, the content browser on the
left, the session tree on the right and the timeline along the bottom.

Deliberately plain - one default look, plain dock widgets, no workspaces yet.
What it proves is the whole path from "where is Source Filmmaker?" to a
session's shot on screen, inside the application folder, without sfm.exe.
"""
from __future__ import annotations

import logging
import math
from pathlib import Path
from typing import Callable, Optional

from PySide6.QtCore import QByteArray, QThread, Qt, Signal, Slot
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (QDockWidget, QFileDialog, QLabel, QLineEdit, QListWidget,
                               QListWidgetItem, QMainWindow, QMessageBox, QStatusBar,
                               QVBoxLayout, QWidget)

from Core.API.dmx import Time
from Core.API.session import Camera, Dag, FilmClip, Session
from Core.Code.formats import FormatError, load_dmx
from Core.Code.transform import apply, apply_direction

from .content_library import ContentLibrary
from .render.scene import Scene, build_scene, build_shot_scene
from .render.viewport import Viewport
from .settings import Settings
from .ui.session_tree import SessionTree
from .ui.timeline import Timeline

log = logging.getLogger("c2ui.window")

__all__ = ["MainWindow"]


class _SceneLoader(QThread):
    """Runs a scene builder off the UI thread; the GPU upload waits for the viewport."""
    done = Signal(object, str)          # Scene or None, error text

    def __init__(self, build: Callable[[], Scene], label: str, parent=None) -> None:
        super().__init__(parent)
        self.build = build
        self.label = label

    def run(self) -> None:
        try:
            self.done.emit(self.build(), "")
        except FormatError as exc:
            self.done.emit(None, str(exc))
        except Exception as exc:                        # noqa: BLE001 - shown, not hidden
            log.exception("scene build failed for %s", self.label)
            self.done.emit(None, f"{type(exc).__name__}: {exc}")


class MainWindow(QMainWindow):
    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.settings = settings
        self.library = ContentLibrary()
        self.session: Optional[Session] = None
        self.session_path: Optional[Path] = None
        self.current_shot: Optional[FilmClip] = None
        self._loader: Optional[_SceneLoader] = None
        self.setWindowTitle("C2UI")
        self.resize(1400, 860)

        self.viewport = Viewport()
        self.setCentralWidget(self.viewport)
        self.setStatusBar(QStatusBar())

        # content browser
        self.search = QLineEdit()
        self.search.setPlaceholderText("Find a model...")
        self.search.setClearButtonEnabled(True)
        self.results = QListWidget()
        self.results.setAlternatingRowColors(True)
        self.info = QLabel("")
        self.info.setWordWrap(True)
        browser = QWidget()
        layout = QVBoxLayout(browser)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.addWidget(self.search)
        layout.addWidget(self.results, 1)
        layout.addWidget(self.info)
        self.browser_dock = self._dock("Content", browser, Qt.LeftDockWidgetArea)

        # session
        self.tree = SessionTree()
        self.tree_dock = self._dock("Session", self.tree, Qt.RightDockWidgetArea)
        self.timeline = Timeline()
        self.timeline_dock = self._dock("Timeline", self.timeline, Qt.BottomDockWidgetArea)
        self.resizeDocks([self.browser_dock, self.tree_dock], [300, 340], Qt.Horizontal)
        self.resizeDocks([self.timeline_dock], [200], Qt.Vertical)

        self._menus()

        self.search.textChanged.connect(self._search)
        self.results.itemActivated.connect(self._open_item)
        self.results.currentItemChanged.connect(lambda cur, _prev: self._open_item(cur))
        self.viewport.failed.connect(self._viewport_failed)
        self.viewport.scene_ready.connect(self.statusBar().showMessage)
        self.tree.shot_selected.connect(self.show_shot)
        self.tree.node_selected.connect(self._node_selected)
        self.timeline.shot_selected.connect(self._timeline_shot)
        self.timeline.time_changed.connect(self._time_changed)

    def _dock(self, title: str, widget: QWidget, area) -> QDockWidget:
        dock = QDockWidget(title, self)
        dock.setObjectName(title)
        dock.setWidget(widget)
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.addDockWidget(area, dock)
        return dock

    def _menus(self) -> None:
        bar = self.menuBar()
        file_menu = bar.addMenu("&File")
        open_action = QAction("&Open Session...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_session_dialog)
        file_menu.addAction(open_action)
        close_action = QAction("&Close Session", self)
        close_action.triggered.connect(self.close_session)
        file_menu.addAction(close_action)
        file_menu.addSeparator()
        quit_action = QAction("&Quit", self)
        quit_action.setShortcut(QKeySequence.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        view_menu = bar.addMenu("&View")
        for dock in (self.browser_dock, self.tree_dock, self.timeline_dock):
            view_menu.addAction(dock.toggleViewAction())
        view_menu.addSeparator()
        frame = QAction("&Frame Scene", self)
        frame.setShortcut("F")
        frame.triggered.connect(self.viewport.frame_scene)
        view_menu.addAction(frame)
        shot_cam = QAction("Shot &Camera", self)
        shot_cam.setShortcut("C")
        shot_cam.triggered.connect(self.use_shot_camera)
        view_menu.addAction(shot_cam)

    # -- content -------------------------------------------------------------------
    def open_content(self) -> bool:
        """Mount the installation, asking for it when it cannot be found."""
        stored = self.settings.get("content.sfm_path") or None
        state = self.library.open("sfm", path=stored, progress=self._progress)
        if not state.ready:
            chosen = QFileDialog.getExistingDirectory(
                self, "Where is Source Filmmaker installed?",
                stored or str(Path.home()))
            if not chosen:
                self.statusBar().showMessage(state.detail or "no content mounted")
                return False
            state = self.library.open("sfm", path=chosen, progress=self._progress)
            if not state.ready:
                QMessageBox.warning(self, "C2UI", state.detail or "That folder is not a Source Filmmaker installation.")
                return False
            self.settings.set("content.sfm_path", chosen)
            self.settings.save()
        self.statusBar().showMessage(state.summary())
        self.setWindowTitle(f"C2UI - {state.title}")
        self._search("")
        return True

    def _progress(self, phase: str, count: int) -> None:
        self.statusBar().showMessage(f"{phase}: {count}")

    @Slot(str)
    def _search(self, text: str) -> None:
        if not self.library.ready:
            return
        self.results.clear()
        entries = (self.library.search(text, kind="model", limit=500) if text.strip()
                   else self.library.page(kind="model", limit=500))
        for entry in entries:
            item = QListWidgetItem(entry.rel)
            item.setData(Qt.UserRole, entry.rel)
            self.results.addItem(item)
        self.info.setText(f"{self.results.count()} models")

    def _open_item(self, item: Optional[QListWidgetItem]) -> None:
        if item is None:
            return
        rel = item.data(Qt.UserRole)
        source = self.library.disk_source()
        self.current_shot = None
        self._start_load(lambda: build_scene(source, rel), rel)

    # -- sessions ------------------------------------------------------------------
    def sessions_folder(self) -> str:
        root = self.library.state.root
        if root is not None:
            for candidate in (root / "game" / "usermod" / "elements" / "sessions",
                              root / "game" / "usermod" / "elements", root / "game"):
                if candidate.is_dir():
                    return str(candidate)
        return str(Path.home())

    def open_session_dialog(self) -> None:
        path, _filter = QFileDialog.getOpenFileName(
            self, "Open Session", self.settings.get("session.last_folder") or self.sessions_folder(),
            "Source Filmmaker sessions (*.dmx);;All files (*)")
        if path:
            self.open_session(Path(path))

    def open_session(self, path: Path) -> bool:
        self.statusBar().showMessage(f"reading {path.name}...")
        try:
            session = Session(load_dmx(path))
        except (FormatError, OSError, ValueError) as exc:
            QMessageBox.warning(self, "C2UI", f"Could not open {path.name}:\n{exc}")
            self.statusBar().showMessage(str(exc))
            return False
        if not session.is_session:
            QMessageBox.warning(self, "C2UI", f"{path.name} is a DMX file but not a session "
                                              f"(format {session.document.format}).")
            return False
        self.session = session
        self.session_path = path
        self.current_shot = None
        self.settings.set("session.last_folder", str(path.parent))
        self.tree.set_session(session)
        self.timeline.set_session(session)
        self.setWindowTitle(f"C2UI - {path.name}")
        self.statusBar().showMessage(session.summary())
        shots = session.active_clip.shots if session.active_clip else []
        first = next((s for s in shots if s.scene is not None), shots[0] if shots else None)
        if first is not None:
            self.tree.select_shot(first)
            self.show_shot(first)
        return True

    def close_session(self) -> None:
        self.session = None
        self.session_path = None
        self.current_shot = None
        self.tree.set_session(None)
        self.timeline.set_session(None)
        self.viewport.set_scene(None)
        self.setWindowTitle(f"C2UI - {self.library.state.title}" if self.library.ready else "C2UI")

    def show_shot(self, shot: FilmClip) -> None:
        if shot is self.current_shot:
            return
        self.current_shot = shot
        self.timeline.select_clip(shot)
        source = self.library.disk_source()
        self._start_load(lambda: build_shot_scene(source, shot), shot.name)

    def _timeline_shot(self, shot: FilmClip) -> None:
        self.tree.select_shot(shot)
        self.show_shot(shot)

    def _node_selected(self, shot: FilmClip, node: Optional[Dag]) -> None:
        if shot is not self.current_shot:
            self.show_shot(shot)
            return
        scene = self.viewport.scene
        if scene is None or node is None:
            return
        if isinstance(node, Camera):
            self._look_through(shot, node)
            return
        wanted = {n.element for n, _m in node.walk(include_hidden=True)}
        boxes = [i.bounds() for i in scene.instances
                 if i.source is not None and i.source.element in wanted]
        boxes = [b for b in boxes if b[0] != b[1]]
        if boxes:
            lo = tuple(min(b[0][a] for b in boxes) for a in range(3))
            hi = tuple(max(b[1][a] for b in boxes) for a in range(3))
            self.viewport.camera.frame((lo, hi), guess_up=False)
            self.viewport.update()

    def use_shot_camera(self) -> None:
        shot = self.current_shot
        if shot is not None and shot.camera is not None:
            self._look_through(shot, shot.camera)

    def _look_through(self, shot: FilmClip, camera: Camera) -> None:
        """Put the orbit camera where a session camera is, looking along its +X."""
        world = camera.local_matrix()
        if shot.scene is not None:
            for node, m in shot.scene.walk(include_hidden=True):
                if node.element is camera.element:
                    world = m
                    break
        eye = apply(world, (0.0, 0.0, 0.0))
        forward = apply_direction(world, (1.0, 0.0, 0.0))
        target = tuple(eye[i] + forward[i] * camera.focal_distance for i in range(3))
        # SFM's field of view is horizontal; the orbit camera's is vertical
        aspect = self.viewport.width() / max(1, self.viewport.height())
        fov_y = 2 * math.atan(math.tan(math.radians(camera.field_of_view) / 2) / max(aspect, 1e-3))
        self.viewport.camera.up_axis = "z"
        self.viewport.camera.look_from(eye, target, fov_y=fov_y)
        self.viewport.update()

    def _time_changed(self, time: Time) -> None:
        self.statusBar().showMessage(f"time {time.seconds:.3f} s")

    # -- loading -------------------------------------------------------------------
    def _start_load(self, build: Callable[[], Scene], label: str) -> None:
        if self._loader is not None and self._loader.isRunning():
            # let it finish on its own; its result is ignored (see _scene_built)
            self._loader.finished.connect(self._loader.deleteLater)
        self.statusBar().showMessage(f"loading {label}...")
        self._loader = _SceneLoader(build, label, self)
        self._loader.done.connect(self._scene_built)
        self._loader.start()

    @Slot(object, str)
    def _scene_built(self, scene: Optional[Scene], error: str) -> None:
        if self.sender() is not self._loader:
            return                                   # a superseded request
        if scene is None:
            self.statusBar().showMessage(error)
            self.info.setText(error)
            return
        shot = self.current_shot
        through_camera = shot is not None and scene.up_axis and shot.camera is not None
        self.viewport.set_scene(scene, frame=not through_camera)
        if through_camera:
            self._look_through(shot, shot.camera)
        lines = [scene.model.summary() if scene.model is not None else scene.summary()]
        if scene.warnings:
            lines.append(f"{len(scene.warnings)} warnings:")
            lines.extend(f"  {w}" for w in scene.warnings[:5])
        self.info.setText("\n".join(lines))

    def _viewport_failed(self, message: str) -> None:
        log.error("viewport: %s", message)
        QMessageBox.critical(self, "C2UI viewport", message)

    # -- lifecycle -----------------------------------------------------------------
    def closeEvent(self, event) -> None:
        self.settings.set("window.geometry", bytes(self.saveGeometry().toBase64()).decode("ascii"))
        self.settings.set("window.state", bytes(self.saveState().toBase64()).decode("ascii"))
        try:
            self.settings.save()
        except OSError:
            log.exception("settings could not be saved")
        self.library.close()
        super().closeEvent(event)

    def restore_geometry(self) -> None:
        raw = self.settings.get("window.geometry")
        if raw:
            self.restoreGeometry(QByteArray.fromBase64(raw.encode("ascii")))
        raw = self.settings.get("window.state")
        if raw:
            self.restoreState(QByteArray.fromBase64(raw.encode("ascii")))
