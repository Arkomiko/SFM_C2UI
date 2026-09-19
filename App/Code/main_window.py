"""
The editor window at this stage: a content browser beside a viewport.

Deliberately plain - one default look, no docking, no workspaces yet. What it
proves is the whole path from "where is Source Filmmaker?" to a textured model
on screen, inside the application folder, without touching sfm.exe.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QByteArray, QThread, Qt, Signal, Slot
from PySide6.QtWidgets import (QFileDialog, QLabel, QLineEdit, QListWidget,
                               QListWidgetItem, QMainWindow, QMessageBox, QSplitter,
                               QStatusBar, QVBoxLayout, QWidget)

from Core.Code.formats import FormatError

from .content_library import ContentLibrary
from .render.scene import Scene, build_scene
from .render.viewport import Viewport
from .settings import Settings

log = logging.getLogger("c2ui.window")

__all__ = ["MainWindow"]


class _SceneLoader(QThread):
    """Builds a scene off the UI thread; the GPU upload waits for the viewport."""
    done = Signal(object, str)          # Scene or None, error text

    def __init__(self, library: ContentLibrary, rel: str, parent=None) -> None:
        super().__init__(parent)
        self.source = library.disk_source()          # the index is not thread-safe
        self.rel = rel

    def run(self) -> None:
        try:
            self.done.emit(build_scene(self.source, self.rel), "")
        except FormatError as exc:
            self.done.emit(None, str(exc))
        except Exception as exc:                        # noqa: BLE001 - shown, not hidden
            log.exception("scene build failed for %s", self.rel)
            self.done.emit(None, f"{type(exc).__name__}: {exc}")


class MainWindow(QMainWindow):
    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.settings = settings
        self.library = ContentLibrary()
        self._loader: Optional[_SceneLoader] = None
        self.setWindowTitle("C2UI")
        self.resize(1280, 800)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Find a model...")
        self.search.setClearButtonEnabled(True)
        self.results = QListWidget()
        self.results.setAlternatingRowColors(True)
        self.info = QLabel("")
        self.info.setWordWrap(True)
        self.viewport = Viewport()

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(6, 6, 6, 6)
        left_layout.addWidget(self.search)
        left_layout.addWidget(self.results, 1)
        left_layout.addWidget(self.info)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(self.viewport)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([320, 960])
        self.setCentralWidget(splitter)
        self.setStatusBar(QStatusBar())

        self.search.textChanged.connect(self._search)
        self.results.itemActivated.connect(self._open_item)
        self.results.currentItemChanged.connect(lambda cur, _prev: self._open_item(cur))
        self.viewport.failed.connect(self._viewport_failed)
        self.viewport.scene_ready.connect(self.statusBar().showMessage)

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
        if self._loader is not None and self._loader.isRunning():
            self._loader.done.disconnect()
            self._loader.finished.connect(self._loader.deleteLater)
        self.statusBar().showMessage(f"loading {rel}...")
        self._loader = _SceneLoader(self.library, rel, self)
        self._loader.done.connect(self._scene_built)
        self._loader.start()

    @Slot(object, str)
    def _scene_built(self, scene: Optional[Scene], error: str) -> None:
        if scene is None:
            self.statusBar().showMessage(error)
            self.info.setText(error)
            return
        self.viewport.set_scene(scene)
        lines = [scene.model.summary()]
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
