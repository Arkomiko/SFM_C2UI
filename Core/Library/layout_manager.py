"""
LayoutManager - builds the dock-widget tree of the main window from a JSON layout
and captures it back (including Qt's binary dock state) for user layouts.

layout.json::

    {
      "id": "ue5_default", "name": "Unreal Editor",
      "window":  { "size": [1600, 900], "maximized": true },
      "central": "viewport",
      "docks": [
        { "panel": "outliner",        "area": "right" },
        { "panel": "details",         "split": { "with": "outliner", "orientation": "vertical" } },
        { "panel": "content_browser", "area": "bottom" },
        { "panel": "output_log",      "tabify": "content_browser" },
        { "panel": "timeline",        "split": { "with": "content_browser", "orientation": "horizontal" }, "active": true }
      ],
      "sizes":   { "outliner": [340, 300], "content_browser": [600, 280] },
      "corners": { "top_left": "left", "top_right": "right", "bottom_left": "left", "bottom_right": "right" },
      "state":   null
    }

* "docks" are processed in order; "tabify"/"split" reference panels created earlier.
* "sizes" are [width, height] hints applied through QMainWindow.resizeDocks.
* "state" (optional) is a base64 QMainWindow.saveState() blob written by capture();
  when present it wins over the declarative description (pixel-accurate user layouts).
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QByteArray, QObject, Qt, QTimer, Signal
from PySide6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget

from . import paths
from .panels.base import DOCK_AREAS, C2UIPanel
from .panels.registry import PanelRegistry
from .ui.dock import PanelDock

log = logging.getLogger("c2ui.layout")

_CORNERS = {
    "top_left": Qt.Corner.TopLeftCorner,
    "top_right": Qt.Corner.TopRightCorner,
    "bottom_left": Qt.Corner.BottomLeftCorner,
    "bottom_right": Qt.Corner.BottomRightCorner,
}
_ORIENT = {"horizontal": Qt.Orientation.Horizontal, "vertical": Qt.Orientation.Vertical}


class LayoutManager(QObject):
    layout_applied = Signal(str)
    panel_opened = Signal(str)
    panel_closed = Signal(str)

    def __init__(self, app: Any, window: QMainWindow, registry: PanelRegistry,
                 parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.app = app
        self.window = window
        self.registry = registry
        self._docks: Dict[str, PanelDock] = {}
        self._panels: Dict[str, C2UIPanel] = {}
        self._central_id: Optional[str] = None
        self._central_widget: Optional[QWidget] = None
        self._current: Dict[str, Any] = {}
        self._current_id: str = ""
        self._title_timer = QTimer(self)
        self._title_timer.setSingleShot(True)
        self._title_timer.setInterval(60)
        self._title_timer.timeout.connect(self._refresh_title_bars)
        self._closing = False

        window.setDockNestingEnabled(True)
        window.setDockOptions(
            QMainWindow.DockOption.AnimatedDocks
            | QMainWindow.DockOption.AllowNestedDocks
            | QMainWindow.DockOption.AllowTabbedDocks
            | QMainWindow.DockOption.GroupedDragging
        )
        window.setTabPosition(Qt.DockWidgetArea.AllDockWidgetAreas, QTabWidget.TabPosition.North)

    # ------------------------------------------------------------------ queries
    @property
    def current_layout(self) -> Dict[str, Any]:
        return dict(self._current)

    @property
    def current_id(self) -> str:
        return self._current_id

    @property
    def central_id(self) -> Optional[str]:
        """Panel id shown in the central area (never dockable / closable)."""
        return self._central_id

    def panel(self, panel_id: str) -> Optional[C2UIPanel]:
        return self._panels.get(panel_id)

    def panels(self) -> Dict[str, C2UIPanel]:
        return dict(self._panels)

    def dock(self, panel_id: str) -> Optional[PanelDock]:
        return self._docks.get(panel_id)

    def docks(self) -> Dict[str, PanelDock]:
        return dict(self._docks)

    def is_open(self, panel_id: str) -> bool:
        if panel_id == self._central_id:
            return True
        d = self._docks.get(panel_id)
        return bool(d and not d.isHidden())

    # -------------------------------------------------------------------- apply
    def apply(self, layout: Dict[str, Any], layout_id: str = "") -> bool:
        self._current = dict(layout)
        self._current_id = layout_id or layout.get("id", "")
        self.window.setUpdatesEnabled(False)
        try:
            self._apply_window(layout.get("window", {}))
            self._apply_corners(layout.get("corners", {}))
            self._set_central(layout.get("central"))

            wanted = [d["panel"] for d in layout.get("docks", []) if "panel" in d]
            for pid, dock in list(self._docks.items()):
                if pid not in wanted:
                    dock.hide()

            for entry in layout.get("docks", []):
                self._place_dock(entry)

            self._apply_sizes(layout.get("sizes", {}))

            for entry in layout.get("docks", []):
                if entry.get("active"):
                    d = self._docks.get(entry["panel"])
                    if d:
                        d.raise_()

            state = layout.get("state")
            if state:
                try:
                    self.window.restoreState(QByteArray.fromBase64(state.encode("ascii")))
                except Exception:  # noqa: BLE001
                    log.exception("restoreState failed - keeping declarative layout")

            for pid, st in (layout.get("panel_states") or {}).items():
                p = self._panels.get(pid)
                if p:
                    try:
                        p.restore_state(st)
                    except Exception:  # noqa: BLE001
                        log.exception("Panel '%s' failed to restore state", pid)
        finally:
            self.window.setUpdatesEnabled(True)
        self._title_timer.start()
        log.info("Layout applied: %s", self._current_id or "(unnamed)")
        self.layout_applied.emit(self._current_id)
        return True

    def _apply_window(self, spec: Dict[str, Any]) -> None:
        size = spec.get("size")
        if size and not self.window.isVisible():
            self.window.resize(int(size[0]), int(size[1]))
        if spec.get("maximized") and not self.window.isVisible():
            self.window.setWindowState(self.window.windowState() | Qt.WindowState.WindowMaximized)

    def _apply_corners(self, spec: Dict[str, Any]) -> None:
        for corner, area in spec.items():
            c = _CORNERS.get(corner)
            a = DOCK_AREAS.get(area)
            if c is not None and a is not None:
                self.window.setCorner(c, a)

    def _ensure_central_host(self) -> QVBoxLayout:
        """Central area = optional banner + the actual central panel."""
        host = self.window.centralWidget()
        if host is None or host.objectName() != "centralHost":
            host = QWidget()
            host.setObjectName("centralHost")
            lay = QVBoxLayout(host)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.setSpacing(0)
            banner = getattr(self.window, "banner", None)
            if banner is not None:
                banner.setParent(host)
                lay.addWidget(banner)
            self.window.setCentralWidget(host)
        return host.layout()

    def _set_central(self, panel_id: Optional[str]) -> None:
        lay = self._ensure_central_host()
        if panel_id == self._central_id and self._central_widget is not None:
            return
        if self._central_widget is not None:
            lay.removeWidget(self._central_widget)
            self._central_widget.setParent(None)
            if isinstance(self._central_widget, C2UIPanel):
                self._panels.pop(self._central_widget.panel_id, None)
                self._central_widget.deleteLater()
            self._central_widget = None
        if panel_id:
            panel = self._get_or_create_panel(panel_id)
            if panel is not None:
                lay.addWidget(panel, 1)
                self._central_widget = panel
                self._central_id = panel_id
                return
            log.warning("Central panel '%s' is not registered - showing an empty area", panel_id)
        placeholder = QWidget()
        placeholder.setObjectName("central_placeholder")
        lay.addWidget(placeholder, 1)
        self._central_widget = placeholder
        self._central_id = None

    def _get_or_create_panel(self, panel_id: str) -> Optional[C2UIPanel]:
        panel = self._panels.get(panel_id)
        if panel is None:
            panel = self.registry.create(panel_id, self.app)
            if panel is None:
                return None
            self._panels[panel_id] = panel
            self._wire_panel(panel)
        return panel

    def _wire_panel(self, panel: C2UIPanel) -> None:
        ctx = getattr(self.app, "context", None)
        if ctx is not None:
            panel.selection_changed.connect(lambda items, pid=panel.panel_id: ctx.set_selection(items, pid))

    def _get_or_create_dock(self, panel_id: str) -> Optional[PanelDock]:
        dock = self._docks.get(panel_id)
        if dock is not None:
            return dock
        panel = self._get_or_create_panel(panel_id)
        if panel is None:
            return None
        dock = PanelDock(panel, self.window)
        dock.closed.connect(lambda pid=panel_id: self.panel_closed.emit(pid))
        dock.dockLocationChanged.connect(lambda _a: self._schedule_title_refresh())
        dock.topLevelChanged.connect(lambda _f: self._schedule_title_refresh())
        dock.visibilityChanged.connect(lambda _v: self._schedule_title_refresh())
        self._docks[panel_id] = dock
        return dock

    def _place_dock(self, entry: Dict[str, Any]) -> None:
        pid = entry.get("panel")
        if not pid:
            return
        dock = self._get_or_create_dock(pid)
        if dock is None:
            return
        meta = dock.panel.META
        area = DOCK_AREAS.get(entry.get("area", meta.default_area), Qt.DockWidgetArea.RightDockWidgetArea)
        dock.setAllowedAreas(meta.qt_allowed_areas())

        if entry.get("tabify") in self._docks:
            target = self._docks[entry["tabify"]]
            self.window.addDockWidget(self.window.dockWidgetArea(target) or area, dock)
            self.window.tabifyDockWidget(target, dock)
        elif isinstance(entry.get("split"), dict) and entry["split"].get("with") in self._docks:
            target = self._docks[entry["split"]["with"]]
            orient = _ORIENT.get(entry["split"].get("orientation", "vertical"), Qt.Orientation.Vertical)
            self.window.addDockWidget(self.window.dockWidgetArea(target) or area, dock)
            self.window.splitDockWidget(target, dock, orient)
        else:
            self.window.addDockWidget(area, dock)

        if entry.get("floating"):
            dock.setFloating(True)
            geo = entry.get("geometry")
            if geo and len(geo) == 4:
                dock.setGeometry(*geo)
        dock.show()
        self.panel_opened.emit(pid)

    def _apply_sizes(self, sizes: Dict[str, Any]) -> None:
        h_docks, h_sizes, v_docks, v_sizes = [], [], [], []
        for pid, wh in sizes.items():
            d = self._docks.get(pid)
            if not d or not isinstance(wh, (list, tuple)) or len(wh) != 2:
                continue
            if wh[0]:
                h_docks.append(d)
                h_sizes.append(int(wh[0]))
            if wh[1]:
                v_docks.append(d)
                v_sizes.append(int(wh[1]))
        if h_docks:
            self.window.resizeDocks(h_docks, h_sizes, Qt.Orientation.Horizontal)
        if v_docks:
            self.window.resizeDocks(v_docks, v_sizes, Qt.Orientation.Vertical)

    # ------------------------------------------------------------- title bars
    def _schedule_title_refresh(self) -> None:
        if self._closing:
            return
        try:
            self._title_timer.start()
        except RuntimeError:
            pass       # timer already destroyed during teardown

    def prepare_shutdown(self) -> None:
        self._closing = True

    def _refresh_title_bars(self) -> None:
        if self._closing:
            return
        """Tabified docks use the tab bar as their title (UE5 style); solo docks keep a header."""
        for dock in self._docks.values():
            if dock.isHidden():
                continue
            tabbed = bool(self.window.tabifiedDockWidgets(dock)) and not dock.isFloating()
            dock.set_header_visible(not tabbed)

    # -------------------------------------------------------------- open/close
    def open_panel(self, panel_id: str, area: Optional[str] = None, raise_: bool = True) -> Optional[PanelDock]:
        if panel_id == self._central_id:
            return None
        existing = self._docks.get(panel_id)
        if existing is None:
            meta = self.registry.meta(panel_id)
            entry = {"panel": panel_id, "area": area or (meta.default_area if meta else "right")}
            self._place_dock(entry)
            existing = self._docks.get(panel_id)
        else:
            if self.window.dockWidgetArea(existing) == Qt.DockWidgetArea.NoDockWidgetArea and not existing.isFloating():
                meta = existing.panel.META
                self.window.addDockWidget(DOCK_AREAS.get(area or meta.default_area, Qt.DockWidgetArea.RightDockWidgetArea), existing)
            existing.show()
            self.panel_opened.emit(panel_id)
        if existing and raise_:
            existing.raise_()
        self._title_timer.start()
        return existing

    def close_panel(self, panel_id: str) -> None:
        d = self._docks.get(panel_id)
        if d:
            d.hide()
            self.panel_closed.emit(panel_id)
            self._title_timer.start()

    def toggle_panel(self, panel_id: str) -> None:
        if self.is_open(panel_id) and panel_id != self._central_id:
            self.close_panel(panel_id)
        else:
            self.open_panel(panel_id)

    # ------------------------------------------------------------------ capture
    def capture(self, include_state: bool = True) -> Dict[str, Any]:
        docks: List[Dict[str, Any]] = []
        sizes: Dict[str, List[int]] = {}
        for pid, d in self._docks.items():
            if d.isHidden():
                continue
            area = self.window.dockWidgetArea(d)
            area_name = next((k for k, v in DOCK_AREAS.items() if v == area), d.panel.META.default_area)
            entry: Dict[str, Any] = {"panel": pid, "area": area_name}
            if d.isFloating():
                g = d.geometry()
                entry["floating"] = True
                entry["geometry"] = [g.x(), g.y(), g.width(), g.height()]
            docks.append(entry)
            sizes[pid] = [d.width(), d.height()]
        out: Dict[str, Any] = {
            "id": self._current_id,
            "name": self._current.get("name", self._current_id),
            "window": {"size": [self.window.width(), self.window.height()], "maximized": self.window.isMaximized()},
            "central": self._central_id,
            "corners": self._current.get("corners", {}),
            "docks": docks,
            "sizes": sizes,
            "panel_states": {pid: p.save_state() for pid, p in self._panels.items()},
        }
        if include_state:
            out["state"] = bytes(self.window.saveState().toBase64()).decode("ascii")
        return out

    # --------------------------------------------------------- user layouts
    def user_layout_file(self, workspace_id: str, name: str) -> Path:
        safe = "".join(c for c in name if c.isalnum() or c in "-_ ").strip() or "layout"
        return paths.USER_LAYOUTS_DIR / f"{workspace_id}__{safe}.json"

    def save_user_layout(self, workspace_id: str, name: str = "last") -> Path:
        paths.USER_LAYOUTS_DIR.mkdir(parents=True, exist_ok=True)
        file = self.user_layout_file(workspace_id, name)
        data = self.capture()
        data["name"] = name
        with file.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        log.info("User layout saved: %s", file)
        return file

    def load_user_layout(self, workspace_id: str, name: str = "last") -> Optional[Dict[str, Any]]:
        file = self.user_layout_file(workspace_id, name)
        if not file.is_file():
            return None
        try:
            with file.open("r", encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError) as exc:
            log.warning("User layout %s is invalid (%s) - ignoring it", file.name, exc)
            return None

    def user_layouts(self, workspace_id: str) -> List[str]:
        prefix = f"{workspace_id}__"
        return sorted(p.stem[len(prefix):] for p in paths.USER_LAYOUTS_DIR.glob(f"{prefix}*.json"))

    def delete_user_layout(self, workspace_id: str, name: str) -> None:
        f = self.user_layout_file(workspace_id, name)
        if f.is_file():
            f.unlink()
