"""
Plugin loader for Core/Scripts.

Each plugin is a folder with a plugin.json manifest and a Python package::

    Core/Scripts/my_plugin/
        plugin.json    {"id": "my_plugin", "name": "...", "version": "0.1.0", "enabled": true}
        __init__.py    def register(api): ...      def unregister(api): ...   (optional)

Plugins receive a PluginAPI facade - the supported surface for scripts.
"""
from __future__ import annotations

import importlib
import importlib.util
import json
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List, Optional

from . import paths
from .context_manager import ActionDef
from .localization import tr

log = logging.getLogger("c2ui.plugins")


@dataclass
class PluginInfo:
    id: str
    dir: Path
    name: str = ""
    version: str = "0.0.0"
    author: str = ""
    description: str = ""
    enabled: bool = True
    entry: str = "__init__.py"
    module: Optional[ModuleType] = None
    error: str = ""
    actions: List[str] = field(default_factory=list)


class PluginAPI:
    """What a plugin is allowed to touch.  Keep this stable - scripts depend on it."""

    def __init__(self, app: Any, info: PluginInfo) -> None:
        self.app = app
        self.info = info
        self.log = logging.getLogger(f"plugin.{info.id}")
        self.events = app.events
        self.bridge = app.bridge
        self.settings = app.settings
        self.tr = tr

    def register_action(self, action_id: str, text: str, callback, icon: str = "", shortcut: str = "",
                        checkable: bool = False, category: str = "Plugins"):
        d = ActionDef(id=action_id, text_key=text, icon=icon, shortcut=shortcut, checkable=checkable,
                      category=category, callback=callback)
        self.info.actions.append(action_id)
        return self.app.context.register_action(d)

    def register_panel(self, panel_cls) -> None:
        self.app.panels.register(panel_cls)

    def open_panel(self, panel_id: str) -> None:
        self.app.layout.open_panel(panel_id)

    def add_menu_action(self, menu_title: str, action_id: str) -> None:
        """Append an already registered action to a top-level menu (created if missing)."""
        act = self.app.context.action(action_id)
        if act is None:
            self.log.warning("add_menu_action: unknown action %s", action_id)
            return
        bar = self.app.window.menuBar()
        for top in bar.actions():
            menu = top.menu()
            if menu is not None and menu.title().replace("&", "") == menu_title:
                menu.addAction(act)
                return
        bar.addMenu(menu_title).addAction(act)

    def status(self, text: str) -> None:
        self.app.window.show_message(text)

    def sfm_call(self, method: str, params: Optional[Dict[str, Any]] = None, timeout_ms: int = 5000) -> Any:
        return self.bridge.call_sync(method, params, timeout_ms)


class PluginLoader:
    def __init__(self, app: Any) -> None:
        self.app = app
        self.plugins: Dict[str, PluginInfo] = {}

    def discover(self) -> List[PluginInfo]:
        self.plugins.clear()
        root = paths.SCRIPTS_DIR
        if not root.is_dir():
            return []
        for d in sorted(root.iterdir()):
            manifest = d / "plugin.json"
            if not d.is_dir() or not manifest.is_file():
                continue
            try:
                with manifest.open("r", encoding="utf-8") as fh:
                    m = json.load(fh)
                info = PluginInfo(id=m.get("id", d.name), dir=d, name=m.get("name", d.name),
                                  version=m.get("version", "0.0.0"), author=m.get("author", ""),
                                  description=m.get("description", ""), enabled=bool(m.get("enabled", True)),
                                  entry=m.get("entry", "__init__.py"))
                self.plugins[info.id] = info
            except Exception as exc:  # noqa: BLE001
                log.exception("Bad plugin manifest %s", manifest)
                self.plugins[d.name] = PluginInfo(id=d.name, dir=d, enabled=False, error=str(exc))
        return list(self.plugins.values())

    def load_all(self) -> None:
        disabled = set(self.app.settings.get("plugins.disabled", []) or [])
        for info in self.plugins.values():
            if not info.enabled or info.id in disabled:
                log.info("Plugin '%s' disabled", info.id)
                continue
            self.load(info)

    def load(self, info: PluginInfo) -> bool:
        entry = info.dir / info.entry
        if not entry.is_file():
            info.error = f"entry not found: {entry.name}"
            log.error("Plugin '%s': %s", info.id, info.error)
            return False
        mod_name = f"c2ui_plugins.{info.id}"
        try:
            spec = importlib.util.spec_from_file_location(mod_name, entry, submodule_search_locations=[str(info.dir)])
            module = importlib.util.module_from_spec(spec)          # type: ignore[arg-type]
            sys.modules[mod_name] = module
            spec.loader.exec_module(module)                          # type: ignore[union-attr]
            info.module = module
            if hasattr(module, "register"):
                module.register(PluginAPI(self.app, info))
            log.info("Plugin loaded: %s v%s", info.name or info.id, info.version)
            return True
        except Exception as exc:  # noqa: BLE001
            info.error = str(exc)
            log.exception("Plugin '%s' failed to load", info.id)
            return False

    def unload_all(self) -> None:
        for info in self.plugins.values():
            if info.module and hasattr(info.module, "unregister"):
                try:
                    info.module.unregister(PluginAPI(self.app, info))
                except Exception:  # noqa: BLE001
                    log.exception("Plugin '%s' failed to unregister", info.id)
