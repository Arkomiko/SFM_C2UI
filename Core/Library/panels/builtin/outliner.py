"""
Outliner panel (UE5 "World Outliner" look) - maps to SFM's Animation Set Editor.

Stage 1 shows a placeholder session tree; Stage 3 fills it from the bridge
(sfm.get_animation_sets / dag hierarchy) and drives the Details panel.
"""
from __future__ import annotations

from typing import Any, Dict, List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QHeaderView, QToolButton, QTreeWidget, QTreeWidgetItem, QWidget

from ...icons import icon as make_icon
from ...localization import tr
from ...ui.widgets import SearchField
from ..base import C2UIPanel, PanelMeta

# (label, type, icon, children)
_PLACEHOLDER_TREE = [
    ("Session", "session", "session", [
        ("shot1", "shot", "clip", [
            ("camera1", "camera", "camera", []),
            ("light1", "light", "light", []),
            ("scout", "model", "model", [
                ("rootTransform", "transform", "transform", []),
                ("Face", "controls", "face", []),
                ("Body", "controls", "bone", []),
            ]),
            ("particle_system1", "particles", "particles", []),
            ("dialog.wav", "sound", "sound", []),
        ]),
    ]),
]


class OutlinerPanel(C2UIPanel):
    META = PanelMeta(id="outliner", title_key="panel.outliner", icon="outliner", category="Editor",
                     default_area="right", sfm_lookup="Animation Set Editor")

    def build(self) -> None:
        bar = QWidget(self)
        bar.setObjectName("panelToolbar")
        hl = QHBoxLayout(bar)
        hl.setContentsMargins(6, 4, 6, 4)
        hl.setSpacing(4)
        self.btn_add = QToolButton(bar)
        self.btn_add.setAutoRaise(True)
        self.btn_add.setIcon(make_icon("add"))
        self.btn_add.setToolTip(tr("outliner.add"))
        self.btn_add.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        hl.addWidget(self.btn_add)
        self.search = SearchField(bar)
        self.search.setPlaceholderText(tr("common.search"))
        self.search.setClearButtonEnabled(True)
        self.search.textChanged.connect(self._filter)
        hl.addWidget(self.search, 1)
        self.btn_filter = QToolButton(bar)
        self.btn_filter.setAutoRaise(True)
        self.btn_filter.setIcon(make_icon("filter"))
        self.btn_filter.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        hl.addWidget(self.btn_filter)
        self.root_layout.addWidget(bar)

        self.tree = QTreeWidget(self)
        self.tree.setObjectName("outlinerTree")
        self.tree.setHeaderLabels([tr("outliner.col_label"), tr("outliner.col_type")])
        self.tree.setAlternatingRowColors(True)
        self.tree.setIndentation(14)
        self.tree.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._context_menu)
        self.tree.itemSelectionChanged.connect(self._on_selection)
        hdr = self.tree.header()
        hdr.setStretchLastSection(False)
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.root_layout.addWidget(self.tree, 1)

        self.set_items(_PLACEHOLDER_TREE)

    # -- data -------------------------------------------------------------------
    def set_items(self, nodes: List[Any]) -> None:
        self.tree.clear()
        self._add_nodes(self.tree.invisibleRootItem(), nodes)
        self.tree.expandAll()

    def _add_nodes(self, parent: QTreeWidgetItem, nodes: List[Any]) -> None:
        for label, ntype, icon_name, children in nodes:
            item = QTreeWidgetItem(parent, [label, tr(f"type.{ntype}")])
            item.setIcon(0, make_icon(icon_name))
            item.setData(0, Qt.ItemDataRole.UserRole, {"name": label, "type": ntype, "icon": icon_name})
            self._add_nodes(item, children)

    def _filter(self, text: str) -> None:
        text = text.lower().strip()

        def visit(item: QTreeWidgetItem) -> bool:
            visible = not text or text in item.text(0).lower()
            child_visible = False
            for i in range(item.childCount()):
                child_visible = visit(item.child(i)) or child_visible
            item.setHidden(not (visible or child_visible))
            return visible or child_visible

        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            visit(root.child(i))

    def _on_selection(self) -> None:
        payload: List[Dict[str, Any]] = []
        for item in self.tree.selectedItems():
            data = item.data(0, Qt.ItemDataRole.UserRole) or {}
            payload.append(dict(data))
        self.selection_changed.emit(payload)

    def _context_menu(self, pos) -> None:
        menu = self.app.context.context_menu(self.META.id, self)
        if menu.actions():
            menu.exec(self.tree.viewport().mapToGlobal(pos))

    # -- hooks ------------------------------------------------------------------
    def on_theme_changed(self, theme: Any) -> None:
        self.btn_add.setIcon(make_icon("add"))
        self.btn_filter.setIcon(make_icon("filter"))
        self._retint(self.tree.invisibleRootItem())

    def _retint(self, item: QTreeWidgetItem) -> None:
        for i in range(item.childCount()):
            child = item.child(i)
            data = child.data(0, Qt.ItemDataRole.UserRole) or {}
            child.setIcon(0, make_icon(data.get("icon", "model")))
            self._retint(child)

    def on_language_changed(self, code: str) -> None:
        super().on_language_changed(code)
        self.tree.setHeaderLabels([tr("outliner.col_label"), tr("outliner.col_type")])
        self.search.setPlaceholderText(tr("common.search"))
        self.btn_add.setToolTip(tr("outliner.add"))
        self.set_items(_PLACEHOLDER_TREE)

    def save_state(self) -> Dict[str, Any]:
        return {"search": self.search.text()}

    def restore_state(self, state: Dict[str, Any]) -> None:
        self.search.setText(str(state.get("search", "")))
