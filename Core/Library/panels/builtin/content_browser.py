"""
Content Browser panel (UE5 look) - browses the SFM game content on disk.

Left: folder tree rooted at game/ (usermod first).  Right: files of the selected
folder as icon tiles.  Stage 3 adds VPK browsing, thumbnails and drag&drop into
the scene through the bridge.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from PySide6.QtCore import QDir, QModelIndex, QSize, Qt
from PySide6.QtWidgets import (
    QFileSystemModel, QHBoxLayout, QLabel, QListView, QPushButton, QSplitter, QStackedWidget, QToolButton,
    QTreeView, QVBoxLayout, QWidget,
)

from ... import paths
from ...icons import icon as make_icon
from ...localization import tr
from ...ui.widgets import SearchField
from ..base import C2UIPanel, PanelMeta

CONTENT_FILTERS = ["*.dmx", "*.mdl", "*.vtf", "*.vmt", "*.wav", "*.mp3", "*.pcf", "*.bsp", "*.py", "*.txt", "*.cfg"]


class ContentBrowserPanel(C2UIPanel):
    META = PanelMeta(id="content_browser", title_key="panel.content_browser", icon="folder", category="Editor",
                     default_area="bottom", min_size=(300, 140))

    def build(self) -> None:
        bar = QWidget(self)
        bar.setObjectName("panelToolbar")
        hl = QHBoxLayout(bar)
        hl.setContentsMargins(6, 4, 6, 4)
        hl.setSpacing(4)
        self.btn_add = QToolButton(bar)
        self.btn_add.setObjectName("accentButton")
        self.btn_add.setIcon(make_icon("add"))
        self.btn_add.setText(tr("content.add"))
        self.btn_add.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btn_add.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        hl.addWidget(self.btn_add)
        self.btn_import = QToolButton(bar)
        self.btn_import.setAutoRaise(True)
        self.btn_import.setIcon(make_icon("import"))
        self.btn_import.setText(tr("content.import"))
        self.btn_import.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        hl.addWidget(self.btn_import)
        hl.addSpacing(8)
        self.path_label = QLabel(bar)
        self.path_label.setObjectName("breadcrumb")
        hl.addWidget(self.path_label, 1)
        self.search = SearchField(bar)
        self.search.setPlaceholderText(tr("common.search"))
        self.search.setClearButtonEnabled(True)
        self.search.setMaximumWidth(260)
        self.search.textChanged.connect(self._apply_filter)
        hl.addWidget(self.search)
        self.root_layout.addWidget(bar)

        self.splitter = QSplitter(Qt.Orientation.Horizontal, self)
        self.splitter.setObjectName("contentSplitter")

        game = paths.sfm_game_dir()
        root = game if game and game.is_dir() else paths.SDK_ROOT
        self.dir_model = QFileSystemModel(self)
        self.dir_model.setFilter(QDir.Filter.Dirs | QDir.Filter.NoDotAndDotDot)
        self.dir_model.setRootPath(str(root))
        self.tree = QTreeView(self.splitter)
        self.tree.setObjectName("contentTree")
        self.tree.setModel(self.dir_model)
        self.tree.setRootIndex(self.dir_model.index(str(root)))
        self.tree.setHeaderHidden(True)
        for col in (1, 2, 3):
            self.tree.hideColumn(col)
        self.tree.setIndentation(14)
        self.tree.clicked.connect(self._on_dir_clicked)

        self.file_model = QFileSystemModel(self)
        self.file_model.setFilter(QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)
        self.file_model.setNameFilters(CONTENT_FILTERS)
        self.file_model.setNameFilterDisables(False)
        self.file_model.setRootPath(str(root))
        self.files = QListView(self.splitter)
        self.files.setObjectName("contentFiles")
        self.files.setModel(self.file_model)
        self.files.setViewMode(QListView.ViewMode.IconMode)
        self.files.setIconSize(QSize(48, 48))
        self.files.setGridSize(QSize(104, 92))
        self.files.setResizeMode(QListView.ResizeMode.Adjust)
        self.files.setSpacing(6)
        self.files.setUniformItemSizes(True)
        self.files.setWordWrap(True)
        self.files.setSelectionMode(QListView.SelectionMode.ExtendedSelection)
        self.files.selectionModel().selectionChanged.connect(self._on_file_selection)
        self.files.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.files.customContextMenuRequested.connect(self._context_menu)

        self.splitter.addWidget(self.tree)
        self.splitter.addWidget(self.files)
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setSizes([220, 700])

        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.splitter)
        self.stack.addWidget(self._build_empty_state())
        self.root_layout.addWidget(self.stack, 1)

        self.refresh_root()
        self.subscribe("sfm.availability_changed", lambda _a: self.refresh_root())

    def _build_empty_state(self) -> QWidget:
        page = QWidget(self)
        page.setObjectName("emptyState")
        vl = QVBoxLayout(page)
        vl.setContentsMargins(24, 24, 24, 24)
        vl.setSpacing(10)
        vl.addStretch(1)
        self.empty_title = QLabel(tr("content.no_sfm_title"), page)
        self.empty_title.setObjectName("emptyStateTitle")
        self.empty_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vl.addWidget(self.empty_title)
        self.empty_text = QLabel(tr("content.no_sfm_text"), page)
        self.empty_text.setObjectName("emptyStateText")
        self.empty_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_text.setWordWrap(True)
        vl.addWidget(self.empty_text)
        row = QHBoxLayout()
        row.addStretch(1)
        self.empty_button = QPushButton(tr("content.set_sfm_path"), page)
        self.empty_button.setIcon(make_icon("folder_open"))
        self.empty_button.clicked.connect(lambda: self.app.open_preferences("sfm"))
        row.addWidget(self.empty_button)
        row.addStretch(1)
        vl.addLayout(row)
        vl.addStretch(2)
        return page

    def refresh_root(self) -> None:
        """Re-root on the configured SFM install, or show the empty state."""
        game = paths.sfm_game_dir()
        if game is None or not game.is_dir():
            self.stack.setCurrentIndex(1)
            self._current_dir = paths.SDK_ROOT
            self.path_label.setText("")
            return
        self.stack.setCurrentIndex(0)
        self.dir_model.setRootPath(str(game))
        self.tree.setRootIndex(self.dir_model.index(str(game)))
        usermod = paths.sfm_usermod_dir()
        start = usermod if usermod and usermod.is_dir() else game
        self._set_dir(start)
        idx = self.dir_model.index(str(start))
        if idx.isValid():
            self.tree.setCurrentIndex(idx)
            self.tree.expand(idx)

    # -- behaviour ----------------------------------------------------------------
    def _set_dir(self, path: Path) -> None:
        self._current_dir = path
        self.files.setRootIndex(self.file_model.setRootPath(str(path)))
        sfm_root = paths.sfm_root()
        crumbs = str(path)
        if sfm_root is not None:
            try:
                rel = path.relative_to(sfm_root)
                crumbs = " > ".join(rel.parts) if rel.parts else path.name
            except ValueError:
                pass
        self.path_label.setText(crumbs)

    def _on_dir_clicked(self, index: QModelIndex) -> None:
        self._set_dir(Path(self.dir_model.filePath(index)))

    def _apply_filter(self, text: str) -> None:
        text = text.strip()
        self.file_model.setNameFilters([f"*{text}*"] if text else CONTENT_FILTERS)

    def _on_file_selection(self, *_args) -> None:
        payload: List[Dict[str, Any]] = []
        for idx in self.files.selectionModel().selectedIndexes():
            p = Path(self.file_model.filePath(idx))
            payload.append({"name": p.name, "type": "asset", "icon": "file", "path": str(p)})
        self.selection_changed.emit(payload)

    def _context_menu(self, pos) -> None:
        menu = self.app.context.context_menu(self.META.id, self)
        if menu.actions():
            menu.exec(self.files.viewport().mapToGlobal(pos))

    def on_theme_changed(self, theme: Any) -> None:
        self.btn_add.setIcon(make_icon("add"))
        self.btn_import.setIcon(make_icon("import"))

    def on_language_changed(self, code: str) -> None:
        super().on_language_changed(code)
        self.btn_add.setText(tr("content.add"))
        self.btn_import.setText(tr("content.import"))
        self.search.setPlaceholderText(tr("common.search"))
        self.empty_title.setText(tr("content.no_sfm_title"))
        self.empty_text.setText(tr("content.no_sfm_text"))
        self.empty_button.setText(tr("content.set_sfm_path"))

    def save_state(self) -> Dict[str, Any]:
        return {"dir": str(self._current_dir), "splitter": self.splitter.sizes()}

    def restore_state(self, state: Dict[str, Any]) -> None:
        d = state.get("dir")
        if self.stack.currentIndex() == 0 and d and Path(d).is_dir():
            self._set_dir(Path(d))
            idx = self.dir_model.index(d)
            if idx.isValid():
                self.tree.setCurrentIndex(idx)
        if state.get("splitter"):
            self.splitter.setSizes([int(x) for x in state["splitter"]])
