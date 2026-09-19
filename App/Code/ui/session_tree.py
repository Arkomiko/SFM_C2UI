"""
The session as a tree: sequence, shots, each shot's scene graph and
animation sets. Selecting a shot shows it in the viewport; selecting a node
inside a shot frames it.
"""
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

from Core.API.session import AnimationSet, Camera, Dag, FilmClip, GameModel, Session

__all__ = ["SessionTree"]

ROLE_KIND = Qt.UserRole
ROLE_VIEW = Qt.UserRole + 1


class SessionTree(QTreeWidget):
    shot_selected = Signal(object)          # FilmClip
    node_selected = Signal(object, object)  # FilmClip, Dag (or None)
    element_selected = Signal(object)       # the Element behind whatever was picked

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setHeaderLabels(["Element", "Type"])
        self.setColumnWidth(0, 260)
        self.setAlternatingRowColors(True)
        self.setUniformRowHeights(True)
        self.currentItemChanged.connect(self._changed)
        self._session: Optional[Session] = None

    # -- filling -------------------------------------------------------------------
    def set_session(self, session: Optional[Session]) -> None:
        self.clear()
        self._session = session
        if session is None:
            return
        clip = session.active_clip
        if clip is None:
            return
        top = self._item(self, clip.name or "sequence", clip.element.type, "clip", clip)
        for shot in clip.shots:
            frame = shot.time_frame
            label = f"{shot.name}   {frame.start.seconds:.2f}s + {frame.duration.seconds:.2f}s"
            item = self._item(top, label, "DmeFilmClip", "shot", shot)
            scene = shot.scene
            if scene is not None:
                scene_item = self._item(item, "Scene", "DmeDag", "scene", (shot, scene))
                self._fill_dag(scene_item, shot, scene, depth=0)
            sets = shot.animation_sets
            if sets:
                sets_item = self._item(item, f"Animation Sets ({len(sets)})", "", "sets", shot)
                for aset in sets:
                    target = aset.game_model or aset.camera
                    kind = target.element.type if target is not None else "DmeAnimationSet"
                    self._item(sets_item, aset.name, kind, "animset", (shot, aset))
            if shot.camera is not None:
                self._item(item, f"Camera: {shot.camera.name}", "DmeCamera", "node",
                           (shot, shot.camera))
        top.setExpanded(True)
        if top.childCount():
            top.child(0).setExpanded(True)

    def _fill_dag(self, parent: QTreeWidgetItem, shot: FilmClip, dag: Dag, depth: int) -> None:
        if depth > 32:
            return
        for child in dag.children:
            label = child.name
            if isinstance(child, GameModel):
                label = f"{child.name}   [{child.model_name.rsplit('/', 1)[-1]}]"
            item = self._item(parent, label, child.element.type, "node", (shot, child))
            if not child.visible:
                item.setForeground(0, Qt.gray)
            self._fill_dag(item, shot, child, depth + 1)

    @staticmethod
    def _item(parent, label: str, kind: str, role: str, payload) -> QTreeWidgetItem:
        item = QTreeWidgetItem(parent, [label, kind])
        item.setData(0, ROLE_KIND, role)
        item.setData(0, ROLE_VIEW, payload)
        return item

    # -- selection -----------------------------------------------------------------
    def _changed(self, current: Optional[QTreeWidgetItem], _previous) -> None:
        if current is None:
            return
        role = current.data(0, ROLE_KIND)
        payload = current.data(0, ROLE_VIEW)
        picked = payload[1] if isinstance(payload, tuple) else payload
        if picked is not None and hasattr(picked, "element"):
            self.element_selected.emit(picked.element)
        if role == "shot":
            self.shot_selected.emit(payload)
        elif role in ("node", "scene"):
            shot, node = payload
            self.node_selected.emit(shot, node)
        elif role == "animset":
            shot, aset = payload
            self.node_selected.emit(shot, aset.game_model or aset.camera)
        elif role == "sets":
            self.shot_selected.emit(payload)

    def select_element(self, element) -> bool:
        """Make the item for a session element current; False when none shows it."""
        stack = [self.topLevelItem(i) for i in range(self.topLevelItemCount())]
        while stack:
            item = stack.pop()
            payload = item.data(0, ROLE_VIEW)
            picked = payload[1] if isinstance(payload, tuple) else payload
            if picked is not None and getattr(picked, "element", None) is element:
                self.setCurrentItem(item)
                self.scrollToItem(item)
                return True
            stack.extend(item.child(i) for i in range(item.childCount()))
        return False

    def select_shot(self, shot: FilmClip) -> None:
        root = self.topLevelItem(0)
        if root is None:
            return
        for i in range(root.childCount()):
            item = root.child(i)
            if item.data(0, ROLE_KIND) == "shot" and item.data(0, ROLE_VIEW) == shot:
                self.setCurrentItem(item)
                return
