"""
ContextManager - actions, editor contexts (modes), shortcuts, context menus, selection.

Terminology
-----------
* **Action**   - a named command ("file.save", "transport.play").  Registered once by
                 code (core or plugins) and referenced by id from JSON (menus, toolbars,
                 context presets, shortcuts).
* **Context**  - an editor mode such as *Animation*, *Motion Editor*, *Graph Editor*,
                 *Render*.  A context preset decides which panels are visible, what the
                 mode toolbar shows, which shortcut overrides apply and which context
                 menus panels get.  Presets are defined per workspace in contexts.json.
* **Selection** - the current selection shared between panels (e.g. an Outliner item
                 drives the Details panel).

contexts.json::

    {
      "default": "animation",
      "shortcuts": { "file.save": "Ctrl+S" },
      "menus": { "outliner": ["sel.rename", "-", "sel.delete"] },
      "contexts": [
        { "id": "animation", "name_key": "context.animation", "icon": "mode_animation",
          "shortcut": "F1", "show_panels": ["timeline"], "hide_panels": [],
          "toolbar": ["transport.play", "transport.stop"],
          "shortcuts": {}, "menus": {} }
      ]
    }
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import QAction, QActionGroup, QKeySequence
from PySide6.QtWidgets import QMenu, QWidget

from .icons import icon as make_icon
from .localization import tr

log = logging.getLogger("c2ui.context")


@dataclass
class ActionDef:
    id: str
    text_key: str
    icon: str = ""
    shortcut: str = ""
    tooltip_key: str = ""
    checkable: bool = False
    checked: bool = False
    category: str = "General"
    callback: Optional[Callable[..., Any]] = None
    enabled: bool = True


@dataclass
class ContextPreset:
    id: str
    name_key: str
    icon: str = "mode_generic"
    shortcut: str = ""
    show_panels: List[str] = field(default_factory=list)
    hide_panels: List[str] = field(default_factory=list)
    toolbar: List[str] = field(default_factory=list)
    shortcuts: Dict[str, str] = field(default_factory=dict)
    menus: Dict[str, List[str]] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ContextPreset":
        return cls(
            id=d["id"],
            name_key=d.get("name_key", f"context.{d['id']}"),
            icon=d.get("icon", "mode_generic"),
            shortcut=d.get("shortcut", ""),
            show_panels=list(d.get("show_panels", [])),
            hide_panels=list(d.get("hide_panels", [])),
            toolbar=list(d.get("toolbar", [])),
            shortcuts=dict(d.get("shortcuts", {})),
            menus={k: list(v) for k, v in d.get("menus", {}).items()},
        )

    def name(self) -> str:
        return tr(self.name_key)


class ContextManager(QObject):
    context_changed = Signal(str)               # new context id
    selection_changed = Signal(list, str)       # items, source panel id
    action_registered = Signal(str)
    presets_loaded = Signal()

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._defs: Dict[str, ActionDef] = {}
        self._actions: Dict[str, QAction] = {}
        self._presets: Dict[str, ContextPreset] = {}
        self._preset_order: List[str] = []
        self._global_shortcuts: Dict[str, str] = {}
        self._global_menus: Dict[str, List[str]] = {}
        self._current: Optional[str] = None
        self._default: Optional[str] = None
        self._selection: List[Any] = []
        self._selection_source: str = ""
        self._host: Optional[QWidget] = None
        self._mode_group = QActionGroup(self)
        self._mode_group.setExclusive(True)

    # ------------------------------------------------------------------ actions
    def register_action(self, d: ActionDef) -> QAction:
        act = self._actions.get(d.id)
        if act is None:
            act = QAction(self._host or self)
            act.setObjectName(d.id)
            self._actions[d.id] = act
            if self._host is not None:
                self._host.addAction(act)
        self._defs[d.id] = d
        act.setText(tr(d.text_key))
        if d.tooltip_key:
            act.setToolTip(tr(d.tooltip_key))
            act.setStatusTip(tr(d.tooltip_key))
        if d.icon:
            act.setProperty("c2ui_icon", d.icon)
            act.setIcon(make_icon(d.icon))
        act.setCheckable(d.checkable)
        if d.checkable:
            act.setChecked(d.checked)
        act.setEnabled(d.enabled)
        act.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        if act.property("c2ui_connected"):
            try:
                act.triggered.disconnect()
            except (RuntimeError, TypeError):
                pass
            act.setProperty("c2ui_connected", False)
        if d.callback:
            act.setProperty("c2ui_connected", True)
            if d.checkable:
                act.triggered.connect(lambda checked=False, cb=d.callback: cb(checked))
            else:
                act.triggered.connect(lambda _checked=False, cb=d.callback: cb())
        self._apply_shortcut(d.id)
        self.action_registered.emit(d.id)
        return act

    def register_actions(self, defs: List[ActionDef]) -> None:
        for d in defs:
            self.register_action(d)

    def action(self, action_id: str) -> Optional[QAction]:
        return self._actions.get(action_id)

    def actions(self) -> Dict[str, QAction]:
        return dict(self._actions)

    def action_defs(self) -> Dict[str, ActionDef]:
        return dict(self._defs)

    def trigger(self, action_id: str) -> bool:
        act = self._actions.get(action_id)
        if act is None or not act.isEnabled():
            log.warning("Action '%s' not available", action_id)
            return False
        act.trigger()
        return True

    def set_enabled(self, action_id: str, enabled: bool) -> None:
        act = self._actions.get(action_id)
        if act:
            act.setEnabled(enabled)

    def attach_host(self, host: QWidget) -> None:
        """Make shortcuts work application-wide by parenting actions to the main window."""
        self._host = host
        for act in self._actions.values():
            act.setParent(host)
            host.addAction(act)

    def refresh_icons(self) -> None:
        """Re-render every action icon in the new theme colour (no menu rebuild)."""
        for aid, d in self._defs.items():
            if d.icon:
                self._actions[aid].setIcon(make_icon(d.icon))

    def retranslate(self) -> None:
        for aid, d in self._defs.items():
            act = self._actions[aid]
            act.setText(tr(d.text_key))
            if d.tooltip_key:
                act.setToolTip(tr(d.tooltip_key))
        for pid, preset in self._presets.items():
            mode_act = self._actions.get(f"context.{pid}")
            if mode_act:
                mode_act.setText(preset.name())

    # ---------------------------------------------------------------- shortcuts
    def _apply_shortcut(self, action_id: str) -> None:
        act = self._actions.get(action_id)
        d = self._defs.get(action_id)
        if not act or not d:
            return
        seq = d.shortcut
        seq = self._global_shortcuts.get(action_id, seq)
        if self._current and self._current in self._presets:
            seq = self._presets[self._current].shortcuts.get(action_id, seq)
        act.setShortcut(QKeySequence(seq) if seq else QKeySequence())

    def _apply_all_shortcuts(self) -> None:
        for aid in self._actions:
            self._apply_shortcut(aid)

    def set_user_shortcut(self, action_id: str, sequence: str) -> None:
        self._global_shortcuts[action_id] = sequence
        self._apply_shortcut(action_id)

    # ------------------------------------------------------------------ presets
    def load_presets(self, data: Dict[str, Any]) -> None:
        # Drop mode-switch actions of the previous workspace.
        for pid in list(self._presets):
            self._remove_action(f"context.{pid}")
        self._presets.clear()
        self._preset_order.clear()
        self._global_shortcuts = dict(data.get("shortcuts", {}))
        self._global_menus = {k: list(v) for k, v in data.get("menus", {}).items()}
        for raw in data.get("contexts", []):
            try:
                preset = ContextPreset.from_dict(raw)
            except Exception:  # noqa: BLE001
                log.exception("Bad context preset: %r", raw)
                continue
            self._presets[preset.id] = preset
            self._preset_order.append(preset.id)
            act = self.register_action(ActionDef(
                id=f"context.{preset.id}", text_key=preset.name_key, icon=preset.icon,
                shortcut=preset.shortcut, checkable=True, category="Modes",
                callback=lambda _checked=False, pid=preset.id: self.set_context(pid),
            ))
            self._mode_group.addAction(act)
        self._default = data.get("default") or (self._preset_order[0] if self._preset_order else None)
        self.presets_loaded.emit()
        if self._default:
            self.set_context(self._default, force=True)
        else:
            self._apply_all_shortcuts()

    def _remove_action(self, action_id: str) -> None:
        act = self._actions.pop(action_id, None)
        self._defs.pop(action_id, None)
        if act:
            self._mode_group.removeAction(act)
            if self._host:
                self._host.removeAction(act)
            act.deleteLater()

    def presets(self) -> List[ContextPreset]:
        return [self._presets[p] for p in self._preset_order]

    def preset(self, context_id: str) -> Optional[ContextPreset]:
        return self._presets.get(context_id)

    @property
    def current(self) -> Optional[str]:
        return self._current

    def current_preset(self) -> Optional[ContextPreset]:
        return self._presets.get(self._current) if self._current else None

    def set_context(self, context_id: str, force: bool = False) -> bool:
        if context_id not in self._presets:
            log.warning("Unknown context '%s'", context_id)
            return False
        if context_id == self._current and not force:
            return True
        self._current = context_id
        self._apply_all_shortcuts()
        mode_act = self._actions.get(f"context.{context_id}")
        if mode_act and not mode_act.isChecked():
            mode_act.setChecked(True)
        log.info("Context -> %s", context_id)
        self.context_changed.emit(context_id)
        return True

    # ------------------------------------------------------------- context menus
    def menu_items(self, panel_id: str) -> List[str]:
        items = list(self._global_menus.get(panel_id, []))
        preset = self.current_preset()
        if preset and panel_id in preset.menus:
            extra = preset.menus[panel_id]
            if extra and extra[0] == "@replace":
                items = list(extra[1:])
            else:
                if items and extra:
                    items.append("-")
                items.extend(extra)
        return items

    def build_menu(self, items: List[str], parent: Optional[QWidget] = None, title: str = "") -> QMenu:
        """Build a QMenu from action ids; "-" is a separator, "sub:Title" opens a submenu
        described by a nested list."""
        menu = QMenu(title, parent)
        self.populate_menu(menu, items)
        return menu

    def populate_menu(self, menu: QMenu, items: List[Any]) -> None:
        for item in items:
            if item == "-":
                menu.addSeparator()
            elif isinstance(item, dict):                 # {"title_key": "...", "items": [...]}
                sub = menu.addMenu(tr(item.get("title_key", "menu.more")))
                if item.get("icon"):
                    sub.setIcon(make_icon(item["icon"]))
                self.populate_menu(sub, item.get("items", []))
            else:
                act = self._actions.get(item)
                if act is not None:
                    menu.addAction(act)
                else:
                    ph = menu.addAction(item)
                    ph.setEnabled(False)
                    log.debug("Menu references unknown action '%s'", item)

    def context_menu(self, panel_id: str, parent: Optional[QWidget] = None) -> QMenu:
        return self.build_menu(self.menu_items(panel_id), parent)

    # ---------------------------------------------------------------- selection
    def set_selection(self, items: List[Any], source: str = "") -> None:
        self._selection = list(items)
        self._selection_source = source
        self.selection_changed.emit(self._selection, source)

    @property
    def selection(self) -> List[Any]:
        return list(self._selection)

    @property
    def selection_source(self) -> str:
        return self._selection_source
