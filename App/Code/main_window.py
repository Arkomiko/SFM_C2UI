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

from PySide6.QtCore import QByteArray, QElapsedTimer, QThread, QTimer, Qt, Signal, Slot
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (QDockWidget, QFileDialog, QLabel, QLineEdit, QListWidget,
                               QListWidgetItem, QMainWindow, QMessageBox, QStatusBar,
                               QVBoxLayout, QWidget)

from Core.API.dmx import Time
from Core.API.session import Camera, Dag, FilmClip, Session
from Core.API.dmx import Element
from Core.Code.animation import Evaluator
from Core.Code.editing import UndoStack, channel_index, record_edit
from Core.Code.formats import FormatError, load_dmx, save_dmx
from Core.Code.editing import Group
from Core.Code.motion import TimeSelection
from Core.Code.transform import (apply, apply_direction, invert, matrix_to_quaternion, multiply,
                                 quaternion_from_axis_angle, quaternion_multiply,
                                 quaternion_normalize, translation_of)

from .content_library import ContentLibrary
from .render.scene import Scene, build_scene, build_shot_scene, refresh_shot_scene
from .render.viewport import Viewport
from .settings import Settings
from .ui.inspector import Inspector
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


def _same(a, b) -> bool:
    """Views are made fresh on every access; two are the same when they wrap
    the same element."""
    return a is not None and b is not None and a.element is b.element


class MainWindow(QMainWindow):
    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.settings = settings
        self.library = ContentLibrary()
        self.session: Optional[Session] = None
        self.session_path: Optional[Path] = None
        self.current_shot: Optional[FilmClip] = None
        self._loader: Optional[_SceneLoader] = None
        self.evaluator = Evaluator()
        self.undo = UndoStack()
        self.undo.changed.append(self._undo_changed)
        self._channel_index: dict = {}
        self._channel_index_shot: Optional[FilmClip] = None
        #: the dag the manipulator acts on, with its world and parent-world matrices
        self.selected: Optional[Dag] = None
        self._selected_world = None
        self._selected_parent = None
        self._drag_start = None
        #: whether the viewport keeps looking through the shot's camera as time moves
        self.follow_camera = True
        self._play_timer = QTimer(self)
        self._play_timer.setInterval(1000 // 60)
        self._play_timer.timeout.connect(self._tick)
        self._play_clock = QElapsedTimer()
        self._play_from = Time(0)
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
        self.inspector = Inspector()
        self.inspector_dock = self._dock("Element", self.inspector, Qt.RightDockWidgetArea)
        self.timeline = Timeline()
        self.timeline_dock = self._dock("Timeline", self.timeline, Qt.BottomDockWidgetArea)
        self.resizeDocks([self.browser_dock, self.tree_dock], [300, 380], Qt.Horizontal)
        self.resizeDocks([self.tree_dock, self.inspector_dock], [420, 320], Qt.Vertical)
        self.resizeDocks([self.timeline_dock], [200], Qt.Vertical)

        self._menus()

        self.search.textChanged.connect(self._search)
        self.results.itemActivated.connect(self._open_item)
        self.results.currentItemChanged.connect(lambda cur, _prev: self._open_item(cur))
        self.viewport.failed.connect(self._viewport_failed)
        self.viewport.camera_taken.connect(self._camera_taken)
        self.viewport.picked.connect(self._picked)
        self.viewport.manipulate_begin.connect(self._manipulate_begin)
        self.viewport.manipulated.connect(self._manipulated)
        self.viewport.manipulate_end.connect(self._manipulate_end)
        self.viewport.scene_ready.connect(self.statusBar().showMessage)
        self.tree.shot_selected.connect(self.show_shot)
        self.tree.node_selected.connect(self._node_selected)
        self.tree.element_selected.connect(self.inspector.set_element)
        self.inspector.edited.connect(self._inspector_edited)
        self.inspector.navigate.connect(self.inspector.set_element)
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
        self.save_action = QAction("&Save", self)
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.triggered.connect(self.save_session)
        file_menu.addAction(self.save_action)
        save_as = QAction("Save &As...", self)
        save_as.setShortcut(QKeySequence.SaveAs)
        save_as.triggered.connect(self.save_session_as)
        file_menu.addAction(save_as)
        close_action = QAction("&Close Session", self)
        close_action.triggered.connect(self.close_session)
        file_menu.addAction(close_action)
        file_menu.addSeparator()
        quit_action = QAction("&Quit", self)
        quit_action.setShortcut(QKeySequence.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        edit_menu = bar.addMenu("&Edit")
        self.undo_action = QAction("&Undo", self)
        self.undo_action.setShortcut(QKeySequence.Undo)
        self.undo_action.triggered.connect(self.undo_edit)
        edit_menu.addAction(self.undo_action)
        self.redo_action = QAction("&Redo", self)
        self.redo_action.setShortcuts([QKeySequence.Redo, QKeySequence("Ctrl+Shift+Z")])
        self.redo_action.triggered.connect(self.redo_edit)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        self.motion_action = QAction("&Motion Editor (edit over the time selection)", self)
        self.motion_action.setCheckable(True)
        self.motion_action.setShortcut("M")
        self.motion_action.toggled.connect(self._motion_toggled)
        edit_menu.addAction(self.motion_action)
        clear_selection = QAction("Clear &Time Selection", self)
        clear_selection.setShortcut("Ctrl+Shift+A")
        clear_selection.triggered.connect(lambda: self.timeline.clear_selection())
        edit_menu.addAction(clear_selection)
        self._undo_changed()

        view_menu = bar.addMenu("&View")
        for dock in (self.browser_dock, self.tree_dock, self.inspector_dock, self.timeline_dock):
            view_menu.addAction(dock.toggleViewAction())
        view_menu.addSeparator()
        frame = QAction("&Frame Selection", self)
        frame.setShortcut("F")
        frame.triggered.connect(self.frame_selection)
        view_menu.addAction(frame)
        frame_all = QAction("Frame &All", self)
        frame_all.setShortcut("Shift+F")
        frame_all.triggered.connect(self.viewport.frame_scene)
        view_menu.addAction(frame_all)
        shot_cam = QAction("Shot &Camera", self)
        shot_cam.setShortcut("C")
        shot_cam.triggered.connect(self.use_shot_camera)
        view_menu.addAction(shot_cam)

        play_menu = bar.addMenu("&Playback")
        play = QAction("&Play / Pause", self)
        play.setShortcut("Space")
        play.triggered.connect(self.toggle_play)
        play_menu.addAction(play)
        stop = QAction("&Stop", self)
        stop.setShortcut("Escape")
        stop.triggered.connect(self.stop)
        play_menu.addAction(stop)
        home = QAction("Go to &Start", self)
        home.setShortcut("Ctrl+Home")
        home.triggered.connect(lambda: self.timeline.set_time(Time(0)))
        play_menu.addAction(home)

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
        if not self._confirm_discard():
            return False
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
        self.undo.clear()
        self.evaluator.invalidate()
        self._channel_index = {}
        self._channel_index_shot = None
        self.inspector.set_element(None)
        self.settings.set("session.last_folder", str(path.parent))
        self.tree.set_session(session)
        self.timeline.set_session(session)
        self.setWindowTitle(f"C2UI - {path.name}")
        self.statusBar().showMessage(session.summary())
        shots = session.active_clip.shots if session.active_clip else []
        first = next((s for s in shots if s.scene is not None), shots[0] if shots else None)
        if first is not None:
            self.tree.select_shot(first)
            self.timeline.set_time(first.time_frame.start, emit=False)
            self.show_shot(first)
        return True

    def close_session(self) -> None:
        if not self._confirm_discard():
            return
        self._play_timer.stop()
        self.undo.clear()
        self.inspector.set_element(None)
        self.session = None
        self.session_path = None
        self.current_shot = None
        self.tree.set_session(None)
        self.timeline.set_session(None)
        self.viewport.set_scene(None)
        self.setWindowTitle(f"C2UI - {self.library.state.title}" if self.library.ready else "C2UI")

    # -- saving and editing --------------------------------------------------------
    def save_session(self) -> bool:
        if self.session is None:
            return False
        if self.session_path is None:
            return self.save_session_as()
        return self._save_to(self.session_path)

    def save_session_as(self) -> bool:
        if self.session is None:
            return False
        start = str(self.session_path) if self.session_path else self.sessions_folder()
        path, _filter = QFileDialog.getSaveFileName(self, "Save Session As", start,
                                                    "Source Filmmaker sessions (*.dmx)")
        if not path:
            return False
        if not path.lower().endswith(".dmx"):
            path += ".dmx"
        return self._save_to(Path(path))

    def _save_to(self, path: Path) -> bool:
        try:
            save_dmx(self.session.document, path)
        except (OSError, FormatError) as exc:
            QMessageBox.critical(self, "C2UI", f"Could not save {path.name}:\n{exc}")
            return False
        self.session_path = path
        self.undo.mark_clean()
        self.statusBar().showMessage(f"saved {path}")
        return True

    def _confirm_discard(self) -> bool:
        """True when it is fine to drop the open session."""
        if self.session is None or not self.undo.dirty:
            return True
        answer = QMessageBox.question(
            self, "C2UI", f"Save changes to {self.session_path.name if self.session_path else 'the session'}?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Save)
        if answer == QMessageBox.Save:
            return self.save_session()
        return answer == QMessageBox.Discard

    def _undo_changed(self) -> None:
        self.undo_action.setEnabled(self.undo.can_undo)
        self.undo_action.setText(f"&Undo {self.undo.undo_label}" if self.undo.can_undo else "&Undo")
        self.redo_action.setEnabled(self.undo.can_redo)
        self.redo_action.setText(f"&Redo {self.undo.redo_label}" if self.undo.can_redo else "&Redo")
        title = "C2UI"
        if self.session_path is not None:
            title += f" - {self.session_path.name}"
        elif self.library.ready:
            title += f" - {self.library.state.title}"
        if self.undo.dirty:
            title += " *"
        self.setWindowTitle(title)

    def undo_edit(self) -> None:
        if self.undo.undo() is not None:
            self._after_edit()

    def redo_edit(self) -> None:
        if self.undo.redo() is not None:
            self._after_edit()

    def _after_edit(self) -> None:
        """Bring the scene and panels up to date after the document changed."""
        self.evaluator.invalidate()
        if self.session is not None and self.session.active_clip is not None:
            self.evaluator.evaluate(self.session.active_clip, self.timeline.time)
        self._refresh_pose()
        self.inspector.refresh()

    def _shot_time(self, shot: FilmClip) -> Time:
        return shot.time_frame.to_child_time(self.timeline.time)

    def _motion_toggled(self, on: bool) -> None:
        self.statusBar().showMessage("motion editor: edits spread over the time selection" if on
                                     else "graph editor: edits key at the cursor")

    def _selection_for(self, shot: FilmClip) -> Optional[TimeSelection]:
        """The time selection to edit over, in the shot's time, or None to key at the cursor."""
        if not self.motion_action.isChecked():
            return None
        selection = self.timeline.selection
        if selection is None or not selection.enabled:
            selection = TimeSelection()                  # the whole clip, as SFM with no selection
        return selection.mapped(shot.time_frame)

    def _inspector_edited(self, element: Element, name: str, index: int, value) -> None:
        if name == "name":
            old = element.name
            from Core.Code.editing import Command

            class Rename(Command):
                label = "rename"

                def apply(self_inner) -> None:
                    element.name = value

                def revert(self_inner) -> None:
                    element.name = old
            self.undo.push(Rename())
            self.tree.set_session(self.session)
            return
        shot = self.current_shot
        if shot is not None and not _same(self._channel_index_shot, shot):
            self._channel_index = channel_index(shot)
            self._channel_index_shot = shot
        try:
            if shot is not None:
                command = record_edit(self._channel_index, element, name, value, self._shot_time(shot), index,
                                      selection=self._selection_for(shot))
            else:
                from Core.Code.editing import SetAttribute
                command = SetAttribute(element, name, value, index)
        except KeyError as exc:
            self.statusBar().showMessage(str(exc))
            return
        self.undo.push(command)
        self._after_edit()

    def show_shot(self, shot: FilmClip) -> None:
        if _same(shot, self.current_shot):
            return
        self.current_shot = shot
        self.timeline.select_clip(shot)
        source = self.library.disk_source()
        self._start_load(lambda: build_shot_scene(source, shot), shot.name)

    def _timeline_shot(self, shot: FilmClip) -> None:
        self.tree.select_shot(shot)
        self.show_shot(shot)

    def _node_selected(self, shot: FilmClip, node: Optional[Dag]) -> None:
        if not _same(shot, self.current_shot):
            self.show_shot(shot)
            self.selected = node
            return
        self.selected = node
        self._place_manipulator()

    def _place_manipulator(self) -> None:
        """Put the manipulator on the selected node, in its own frame."""
        node = self.selected
        shot = self.current_shot
        if node is None or shot is None or shot.scene is None or node.transform is None:
            self.viewport.manipulator.hide()
            self.viewport.update()
            return
        world = None
        for candidate, m, _visible in shot.scene.walk_visibility():
            if candidate.element is node.element:
                world = m
                break
        if world is None:
            self.viewport.manipulator.hide()
            self.viewport.update()
            return
        self._selected_world = world
        self._selected_parent = multiply(world, invert(node.local_matrix()))
        self.viewport.manipulator.place(translation_of(world), matrix_to_quaternion(world))
        self.viewport.update()

    def frame_selection(self) -> None:
        scene = self.viewport.scene
        node = self.selected
        if scene is None or node is None:
            self.viewport.frame_scene()
            return
        wanted = {n.element for n, _m in node.walk(include_hidden=True)}
        boxes = [i.bounds() for i in scene.instances
                 if i.source is not None and i.source.element in wanted]
        boxes = [b for b in boxes if b[0] != b[1]]
        if boxes:
            lo = tuple(min(b[0][a] for b in boxes) for a in range(3))
            hi = tuple(max(b[1][a] for b in boxes) for a in range(3))
            self.viewport.camera.frame((lo, hi), guess_up=False)
        elif self._selected_world is not None:
            o = translation_of(self._selected_world)
            self.viewport.camera.frame(((o[0] - 10, o[1] - 10, o[2] - 10), (o[0] + 10, o[1] + 10, o[2] + 10)), guess_up=False)
        self.follow_camera = False
        self.viewport.update()

    def _picked(self, instance) -> None:
        if instance is None or instance.source is None:
            self.selected = None
            self.viewport.manipulator.hide()
            self.viewport.update()
            return
        if not self.tree.select_element(instance.source.element):
            self.selected = instance.source
            self._place_manipulator()

    # -- manipulating --------------------------------------------------------------
    def _manipulate_begin(self) -> None:
        node = self.selected
        if node is None or node.transform is None:
            return
        t = node.transform
        self._drag_start = (t.position, t.orientation)

    def _manipulated(self, delta) -> None:
        node = self.selected
        if node is None or node.transform is None or self._drag_start is None or self._selected_parent is None:
            return
        start_position, start_orientation = self._drag_start
        transform = node.transform
        parent_inverse = invert(self._selected_parent)
        if isinstance(delta[0], (int, float)):
            origin = translation_of(self._selected_world)
            world_position = (origin[0] + delta[0], origin[1] + delta[1], origin[2] + delta[2])
            transform.position = apply(parent_inverse, world_position)
        else:
            axis, angle = delta
            world_rotation = matrix_to_quaternion(self._selected_world)
            turned = quaternion_multiply(quaternion_from_axis_angle(axis, angle), world_rotation)
            parent_rotation = matrix_to_quaternion(parent_inverse)
            transform.orientation = quaternion_normalize(quaternion_multiply(parent_rotation, turned))
        self._refresh_pose_only()

    def _manipulate_end(self) -> None:
        node = self.selected
        if node is None or node.transform is None or self._drag_start is None:
            return
        transform = node.transform
        start_position, start_orientation = self._drag_start
        final_position, final_orientation = transform.position, transform.orientation
        self._drag_start = None
        # restore, then apply through the undo stack as one recorded edit
        transform.position = start_position
        transform.orientation = start_orientation
        shot = self.current_shot
        commands = []
        if final_position != start_position:
            commands.append(self._edit_command(transform.element, "position", final_position, shot))
        if final_orientation != start_orientation:
            commands.append(self._edit_command(transform.element, "orientation", final_orientation, shot))
        if commands:
            self.undo.push(Group(commands, f"move {node.name}") if len(commands) > 1 else commands[0])
            self._after_edit()
        self._place_manipulator()

    def _edit_command(self, element: Element, name: str, value, shot: Optional[FilmClip]):
        if shot is not None:
            if not _same(self._channel_index_shot, shot):
                self._channel_index = channel_index(shot)
                self._channel_index_shot = shot
            return record_edit(self._channel_index, element, name, value, self._shot_time(shot),
                               selection=self._selection_for(shot))
        from Core.Code.editing import SetAttribute
        return SetAttribute(element, name, value)

    def _refresh_pose_only(self) -> None:
        """Re-pose from the elements as they are, without evaluating (a drag in progress)."""
        scene = self.viewport.scene
        shot = self.current_shot
        if scene is not None and shot is not None and scene.up_axis:
            refresh_shot_scene(scene, shot)
        self.viewport.update()

    def use_shot_camera(self) -> None:
        shot = self.current_shot
        if shot is not None and shot.camera is not None:
            self.follow_camera = True
            self._look_through(shot, shot.camera)

    def _camera_taken(self) -> None:
        self.follow_camera = False

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

    # -- time ----------------------------------------------------------------------
    def _time_changed(self, time: Time) -> None:
        session = self.session
        if session is None or session.active_clip is None:
            return
        clip = session.active_clip
        self.evaluator.evaluate(clip, time)
        shot = self._shot_at(time)
        if shot is not None and not _same(shot, self.current_shot):
            self.tree.select_shot(shot)
            self.show_shot(shot)
            return
        self._refresh_pose()
        if not self._play_timer.isActive():
            self.statusBar().showMessage(
                f"time {time.seconds:.3f} s   {self.evaluator.channels_run} channels")

    def _shot_at(self, time: Time) -> Optional[FilmClip]:
        clip = self.session.active_clip if self.session else None
        if clip is None:
            return None
        for shot in clip.shots:
            frame = shot.time_frame
            if frame.start.ticks <= time.ticks < frame.end.ticks:
                return shot
        return None

    def _refresh_pose(self) -> None:
        scene = self.viewport.scene
        shot = self.current_shot
        if scene is None or shot is None or not scene.up_axis:
            return
        refresh_shot_scene(scene, shot)
        if self.follow_camera and shot.camera is not None:
            self._look_through(shot, shot.camera)
        if self.selected is not None and self._drag_start is None:
            self._place_manipulator()
        self.viewport.update()

    def toggle_play(self) -> None:
        if self._play_timer.isActive():
            self._play_timer.stop()
            self.statusBar().showMessage(f"paused at {self.timeline.time.seconds:.3f} s")
        elif self.session is not None:
            self._play_from = self.timeline.time
            self._play_clock.start()
            self._play_timer.start()

    def stop(self) -> None:
        if self._play_timer.isActive():
            self._play_timer.stop()
            self.timeline.set_time(self._play_from)

    def _tick(self) -> None:
        elapsed = self._play_clock.elapsed() / 1000.0
        time = Time(self._play_from.ticks + round(elapsed * Time.PER_SECOND))
        clip = self.session.active_clip if self.session else None
        if clip is not None and time.ticks >= clip.time_frame.duration.ticks:
            self._play_timer.stop()
            time = clip.time_frame.duration
        self.timeline.set_time(time)

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
        if shot is not None and scene.up_axis:
            # the scene was built from the session as saved; bring it to the cursor
            self.evaluator.evaluate(self.session.active_clip, self.timeline.time)
            refresh_shot_scene(scene, shot)
        through_camera = shot is not None and scene.up_axis and shot.camera is not None
        self.viewport.set_scene(scene, frame=not through_camera)
        if through_camera:
            self.follow_camera = True
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
        if not self._confirm_discard():
            event.ignore()
            return
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
