"""
C2UIMainWindow - the editor shell: menu bar, tool bars, status bar and the dock area
managed by the LayoutManager.

Menus and tool bars are declared in workspace JSON and reference action ids.  A few
dynamic placeholders are expanded at runtime:

    "@panels"      - toggle entries for every registered panel
    "@workspaces"  - workspace switcher
    "@themes"      - theme switcher
    "@languages"   - language switcher
    "@layouts"     - saved user layouts
    "@contexts"    - editor modes (mode buttons in tool bars)
    "-"            - separator            "->" - expanding spacer (tool bars only)
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QActionGroup, QCloseEvent
from PySide6.QtWidgets import (
    QInputDialog, QLabel, QMainWindow, QMenu, QMenuBar, QSizePolicy, QStatusBar, QToolBar, QWidget,
)

from ..icons import icon as make_icon
from ..localization import tr
from .banner import Banner

log = logging.getLogger("c2ui.window")

_TB_AREAS = {
    "top": Qt.ToolBarArea.TopToolBarArea,
    "bottom": Qt.ToolBarArea.BottomToolBarArea,
    "left": Qt.ToolBarArea.LeftToolBarArea,
    "right": Qt.ToolBarArea.RightToolBarArea,
}


class C2UIMainWindow(QMainWindow):
    def __init__(self, app: Any) -> None:
        super().__init__()
        self.app = app
        self.setObjectName("C2UIMainWindow")
        self.setWindowTitle("SFM - C2UI")
        self.setWindowIcon(make_icon("c2ui_logo", "#3b9eff"))
        self.setMinimumSize(960, 600)
        self._menu_spec: Dict[str, Any] = {"menus": []}
        self._toolbar_spec: Dict[str, Any] = {"toolbars": []}
        self._toolbars: List[QToolBar] = []
        self.banner = Banner(self)
        self._build_status_bar()

    # ------------------------------------------------------------- accessors
    @property
    def toolbar_spec(self) -> Dict[str, Any]:
        return self._toolbar_spec

    @property
    def menu_spec(self) -> Dict[str, Any]:
        return self._menu_spec

    # ---------------------------------------------------------------- menus
    def build_menus(self, spec: Dict[str, Any]) -> None:
        self._menu_spec = spec or {"menus": []}
        bar: QMenuBar = self.menuBar()
        bar.clear()
        for m in self._menu_spec.get("menus", []):
            menu = bar.addMenu(tr(m.get("title_key", "menu.untitled")))
            menu.setObjectName(f"menu_{m.get('id', m.get('title_key', ''))}")
            self._fill_menu(menu, m.get("items", []))

    def _fill_menu(self, menu: QMenu, items: List[Any]) -> None:
        ctx = self.app.context
        for item in items:
            if item == "-":
                menu.addSeparator()
            elif isinstance(item, dict):
                sub = menu.addMenu(tr(item.get("title_key", "menu.more")))
                if item.get("icon"):
                    sub.setIcon(make_icon(item["icon"]))
                self._fill_menu(sub, item.get("items", []))
            elif isinstance(item, str) and item.startswith("@"):
                self._add_dynamic(menu, item)
            else:
                act = ctx.action(item)
                if act is not None:
                    menu.addAction(act)
                else:
                    ph = menu.addAction(item)
                    ph.setEnabled(False)
                    log.debug("Menu references unknown action '%s'", item)

    def _add_dynamic(self, menu: QMenu, token: str) -> None:
        builders = {
            "@panels": (tr("menu.panels"), "panel", self._populate_panels),
            "@workspaces": (tr("menu.workspaces"), "workspace", self._populate_workspaces),
            "@themes": (tr("menu.themes"), "theme", self._populate_themes),
            "@languages": (tr("menu.languages"), "language", self._populate_languages),
            "@layouts": (tr("menu.layouts"), "layout", self._populate_layouts),
            "@contexts": (tr("menu.modes"), "mode_generic", self._populate_contexts),
        }
        entry = builders.get(token)
        if entry is None:
            log.warning("Unknown dynamic menu token %s", token)
            return
        title, icon_name, populate = entry
        sub = menu.addMenu(make_icon(icon_name), title)
        sub.aboutToShow.connect(lambda s=sub, p=populate: (s.clear(), p(s)))
        populate(sub)

    # -- dynamic menu content -----------------------------------------------------
    def _populate_panels(self, menu: QMenu) -> None:
        layout = self.app.layout
        by_cat: Dict[str, list] = {}
        for meta in self.app.panels.all_meta():
            by_cat.setdefault(meta.category, []).append(meta)
        first = True
        for cat in sorted(by_cat):
            if not first:
                menu.addSeparator()
            first = False
            for meta in sorted(by_cat[cat], key=lambda m: m.title()):
                act = QAction(make_icon(meta.icon), meta.title(), menu)
                act.setCheckable(True)
                act.setChecked(layout.is_open(meta.id))
                act.setEnabled(meta.id != layout.central_id)
                act.triggered.connect(lambda _c=False, pid=meta.id: layout.toggle_panel(pid))
                menu.addAction(act)

    def _populate_workspaces(self, menu: QMenu) -> None:
        wm = self.app.workspace
        group = QActionGroup(menu)
        for ws in wm.all():
            act = QAction(make_icon(ws.icon), ws.display_name(), menu)
            act.setCheckable(True)
            act.setChecked(wm.current is not None and wm.current.id == ws.id)
            act.triggered.connect(lambda _c=False, wid=ws.id: self.app.switch_workspace(wid))
            group.addAction(act)
            menu.addAction(act)

    def _populate_themes(self, menu: QMenu) -> None:
        tm = self.app.theme
        group = QActionGroup(menu)
        for theme in sorted(tm.available(), key=lambda t: t.name):
            act = QAction(theme.name, menu)
            act.setCheckable(True)
            act.setChecked(tm.current is not None and tm.current.id == theme.id)
            act.triggered.connect(lambda _c=False, tid=theme.id: self.app.switch_theme(tid))
            group.addAction(act)
            menu.addAction(act)

    def _populate_languages(self, menu: QMenu) -> None:
        lm = self.app.locale
        group = QActionGroup(menu)
        for loc in lm.available():
            act = QAction(f"{loc['native_name']}  ({loc['code']})", menu)
            act.setCheckable(True)
            act.setChecked(lm.language == loc["code"])
            act.triggered.connect(lambda _c=False, code=loc["code"]: self.app.switch_language(code))
            group.addAction(act)
            menu.addAction(act)

    def _populate_layouts(self, menu: QMenu) -> None:
        wm = self.app.workspace
        if wm.current is None:
            return
        names = [n for n in self.app.layout.user_layouts(wm.current.id) if n != "last"]
        for name in names:
            act = QAction(name, menu)
            act.triggered.connect(lambda _c=False, n=name: wm.load_layout(n))
            menu.addAction(act)
        if names:
            menu.addSeparator()
        save = QAction(make_icon("save"), tr("window.save_layout_as"), menu)
        save.triggered.connect(self.save_layout_as)
        menu.addAction(save)
        reset = QAction(make_icon("reset"), tr("window.reset_layout"), menu)
        reset.triggered.connect(wm.reset_layout)
        menu.addAction(reset)

    def _populate_contexts(self, menu: QMenu) -> None:
        ctx = self.app.context
        for preset in ctx.presets():
            act = ctx.action(f"context.{preset.id}")
            if act:
                menu.addAction(act)

    # ------------------------------------------------------------- tool bars
    def build_toolbars(self, spec: Dict[str, Any]) -> None:
        self._toolbar_spec = spec or {"toolbars": []}
        for tb in self._toolbars:
            self.removeToolBar(tb)
            tb.deleteLater()
        self._toolbars.clear()
        ctx = self.app.context
        for t in self._toolbar_spec.get("toolbars", []):
            tb = QToolBar(tr(t.get("title_key", "toolbar.main")), self)
            tb.setObjectName(f"toolbar_{t.get('id', 'main')}")
            tb.setMovable(bool(t.get("movable", False)))
            tb.setIconSize(QSize(int(t.get("icon_size", 18)), int(t.get("icon_size", 18))))
            tb.setToolButtonStyle(
                Qt.ToolButtonStyle.ToolButtonTextBesideIcon if t.get("text") else Qt.ToolButtonStyle.ToolButtonIconOnly
            )
            for item in t.get("items", []):
                if item == "-":
                    tb.addSeparator()
                elif item == "->":
                    spacer = QWidget(tb)
                    spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
                    spacer.setObjectName("toolbarSpacer")
                    tb.addWidget(spacer)
                elif item == "@contexts":
                    for preset in ctx.presets():
                        act = ctx.action(f"context.{preset.id}")
                        if act:
                            tb.addAction(act)
                elif isinstance(item, str) and item.startswith("@"):
                    menu = QMenu(tb)
                    self._add_dynamic(menu, item)
                    if menu.actions():
                        tb.addAction(menu.actions()[0])
                else:
                    act = ctx.action(item)
                    if act is not None:
                        tb.addAction(act)
                    else:
                        log.debug("Toolbar references unknown action '%s'", item)
            self.addToolBar(_TB_AREAS.get(t.get("area", "top"), Qt.ToolBarArea.TopToolBarArea), tb)
            self._toolbars.append(tb)

    # ------------------------------------------------------------- status bar
    def _build_status_bar(self) -> None:
        sb: QStatusBar = self.statusBar()
        sb.setObjectName("statusBar")
        sb.setSizeGripEnabled(False)
        self.status_context = QLabel(sb)
        self.status_context.setObjectName("statusContext")
        self.status_sfm = QLabel(sb)
        self.status_sfm.setObjectName("statusSfm")
        self.status_workspace = QLabel(sb)
        self.status_workspace.setObjectName("statusWorkspace")
        sb.addPermanentWidget(self.status_context)
        sb.addPermanentWidget(self.status_workspace)
        sb.addPermanentWidget(self.status_sfm)
        self.set_sfm_status(False)
        self.show_message(tr("status.ready"))

    def show_message(self, text: str, timeout_ms: int = 4000) -> None:
        self.statusBar().showMessage(text, timeout_ms)

    def set_sfm_status(self, connected: bool, detail: str = "") -> None:
        key = "status.sfm_connected" if connected else "status.sfm_offline"
        self.status_sfm.setText(f"  {tr(key)}{('  ' + detail) if detail else ''}  ")
        self.status_sfm.setProperty("state", "online" if connected else "offline")
        self.status_sfm.style().unpolish(self.status_sfm)
        self.status_sfm.style().polish(self.status_sfm)

    def set_context_status(self, text: str) -> None:
        self.status_context.setText(f"  {text}  ")

    def set_workspace_status(self, text: str) -> None:
        self.status_workspace.setText(f"  {text}  ")

    # ------------------------------------------------------------------ misc
    def retheme(self) -> None:
        """Re-tint chrome that owns its own icons after a theme change."""
        self.banner.retheme()
        for tb in self._toolbars:
            for act in tb.actions():
                icon_name = act.property("c2ui_icon")
                if icon_name:
                    act.setIcon(make_icon(icon_name))

    def retranslate(self) -> None:
        self.build_menus(self._menu_spec)
        self.build_toolbars(self._toolbar_spec)
        for dock in self.app.layout.docks().values():
            dock.retranslate()
        for panel in self.app.layout.panels().values():
            panel.on_language_changed(self.app.locale.language)
        ws = self.app.workspace.current
        if ws:
            self.set_workspace_status(ws.display_name())
        preset = self.app.context.current_preset()
        if preset:
            self.set_context_status(preset.name())
        self.set_sfm_status(self.app.bridge.connected)

    def save_layout_as(self) -> None:
        name, ok = QInputDialog.getText(self, tr("window.save_layout_as"), tr("window.layout_name"))
        if ok and name.strip():
            self.app.workspace.save_layout(name.strip())
            self.show_message(tr("status.layout_saved", name=name.strip()))

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        try:
            self.app.shutdown()
        except Exception:  # noqa: BLE001
            log.exception("Error during shutdown")
        super().closeEvent(event)
