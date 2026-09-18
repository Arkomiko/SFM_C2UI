"""
Place Actors panel (UE5 "Place Actors" look) - a palette of things that can be
added to the SFM session: models, lights, cameras, particles, sounds, ...

Stage 1: static palette.  Stage 3: double-click / drag creates the element via
the bridge (sfm.create_*).
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QHBoxLayout, QListWidget, QListWidgetItem, QToolButton, QWidget

from ...icons import icon as make_icon
from ...localization import tr
from ...ui.widgets import SearchField
from ..base import C2UIPanel, PanelMeta

# (category key, [(item key, icon, sfm create method)])
_PALETTE: List[Tuple[str, List[Tuple[str, str, str]]]] = [
    ("place.basic", [("place.model", "model", "sfm.create_model"), ("place.camera", "camera", "sfm.create_camera"),
                     ("place.sound", "sound", "sfm.create_sound"), ("place.particles", "particles", "sfm.create_particles")]),
    ("place.lights", [("place.light_spot", "light", "sfm.create_light"), ("place.light_point", "light", "sfm.create_light"),
                      ("place.light_volumetric", "light", "sfm.create_light")]),
    ("place.clips", [("place.shot", "clip", "sfm.create_shot"), ("place.sound_clip", "sound", "sfm.create_sound_clip"),
                     ("place.color_clip", "color", "sfm.create_color_clip")]),
]


class PlaceActorsPanel(C2UIPanel):
    META = PanelMeta(id="place_actors", title_key="panel.place_actors", icon="add_cube", category="Editor",
                     default_area="left", min_size=(180, 200))

    def build(self) -> None:
        bar = QWidget(self)
        bar.setObjectName("panelToolbar")
        hl = QHBoxLayout(bar)
        hl.setContentsMargins(6, 4, 6, 4)
        self.search = SearchField(bar)
        self.search.setPlaceholderText(tr("common.search"))
        self.search.setClearButtonEnabled(True)
        self.search.textChanged.connect(self._filter)
        hl.addWidget(self.search, 1)
        self.root_layout.addWidget(bar)

        self.tabs = QWidget(self)
        self.tabs.setObjectName("placeCategories")
        tl = QHBoxLayout(self.tabs)
        tl.setContentsMargins(6, 0, 6, 2)
        tl.setSpacing(2)
        self._cat_buttons: List[QToolButton] = []
        for i, (cat_key, _items) in enumerate(_PALETTE):
            b = QToolButton(self.tabs)
            b.setObjectName("categoryTab")
            b.setText(tr(cat_key))
            b.setCheckable(True)
            b.setChecked(i == 0)
            b.setAutoExclusive(True)
            b.clicked.connect(lambda _c=False, idx=i: self._show_category(idx))
            tl.addWidget(b)
            self._cat_buttons.append(b)
        tl.addStretch(1)
        self.root_layout.addWidget(self.tabs)

        self.list = QListWidget(self)
        self.list.setObjectName("placeList")
        self.list.setIconSize(QSize(20, 20))
        self.list.setSpacing(1)
        self.list.setDragEnabled(True)
        self.list.itemDoubleClicked.connect(self._create)
        self.root_layout.addWidget(self.list, 1)
        self._show_category(0)

    def _show_category(self, idx: int) -> None:
        self._category = idx
        self.list.clear()
        for key, icon_name, method in _PALETTE[idx][1]:
            item = QListWidgetItem(make_icon(icon_name), tr(key))
            item.setData(Qt.ItemDataRole.UserRole, {"key": key, "icon": icon_name, "method": method})
            self.list.addItem(item)
        self._filter(self.search.text())

    def _filter(self, text: str) -> None:
        text = text.lower().strip()
        for i in range(self.list.count()):
            it = self.list.item(i)
            it.setHidden(bool(text) and text not in it.text().lower())

    def _create(self, item: QListWidgetItem) -> None:
        data: Dict[str, Any] = item.data(Qt.ItemDataRole.UserRole) or {}
        self.app.sfm_call(data.get("method", "sfm.noop"), {"kind": data.get("key")})

    def on_theme_changed(self, theme: Any) -> None:
        self._show_category(self._category)

    def on_language_changed(self, code: str) -> None:
        super().on_language_changed(code)
        self.search.setPlaceholderText(tr("common.search"))
        for b, (cat_key, _i) in zip(self._cat_buttons, _PALETTE):
            b.setText(tr(cat_key))
        self._show_category(self._category)
