"""
WorkspaceManager - discovers workspaces under Workspaces/ and activates them.

A workspace is a folder with a workspace.json that bundles everything that defines
an editor "personality" (Unreal Editor, UWP, After Effects, ...)::

    Workspaces/UnrealEditor/
        workspace.json      -> { id, name_key, icon, theme, layout, contexts, menu, toolbar, locale_overrides }
        layout.json         -> LayoutManager format
        contexts.json       -> ContextManager format
        menu.json           -> { "menus": [ { "title_key": "menu.file", "items": [ "file.new", "-", ... ] } ] }
        toolbar.json        -> { "toolbars": [ { "id": "main", "area": "top", "items": [ ... ] } ] }

Activation order: locale overrides -> theme -> context presets -> menus/toolbars -> layout.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QObject, Signal

from . import paths
from .localization import tr

log = logging.getLogger("c2ui.workspace")


@dataclass
class Workspace:
    id: str
    dir: Path
    name: str = ""
    name_key: str = ""
    description: str = ""
    icon: str = "workspace"
    theme: str = "ue5_dark"
    layout: str = "layout.json"
    contexts: str = "contexts.json"
    menu: str = "menu.json"
    toolbar: str = "toolbar.json"
    locale_overrides: Dict[str, Any] = field(default_factory=dict)
    experimental: bool = False

    @classmethod
    def from_dir(cls, d: Path) -> "Workspace":
        with (d / "workspace.json").open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return cls(
            id=data.get("id", d.name),
            dir=d,
            name=data.get("name", d.name),
            name_key=data.get("name_key", ""),
            description=data.get("description", ""),
            icon=data.get("icon", "workspace"),
            theme=data.get("theme", "ue5_dark"),
            layout=data.get("layout", "layout.json"),
            contexts=data.get("contexts", "contexts.json"),
            menu=data.get("menu", "menu.json"),
            toolbar=data.get("toolbar", "toolbar.json"),
            locale_overrides=dict(data.get("locale_overrides", {})),
            experimental=bool(data.get("experimental", False)),
        )

    def display_name(self) -> str:
        return tr(self.name_key) if self.name_key else self.name

    def read_json(self, rel: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        file = self.dir / rel
        if not file.is_file():
            if default is None:
                log.warning("Workspace '%s': missing %s", self.id, rel)
            return dict(default or {})
        try:
            with file.open("r", encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError) as exc:
            log.warning("Workspace '%s': %s is invalid (%s)", self.id, rel, exc)
            return dict(default or {})


class WorkspaceManager(QObject):
    workspace_changed = Signal(object)      # Workspace
    workspaces_discovered = Signal(list)

    def __init__(self, app: Any, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.app = app
        self._workspaces: Dict[str, Workspace] = {}
        self._current: Optional[Workspace] = None

    # ---------------------------------------------------------------- discovery
    def discover(self) -> List[Workspace]:
        self._workspaces.clear()
        if paths.WORKSPACES_DIR.is_dir():
            for d in sorted(paths.WORKSPACES_DIR.iterdir()):
                if not (d / "workspace.json").is_file():
                    continue
                try:
                    ws = Workspace.from_dir(d)
                    self._workspaces[ws.id] = ws
                except Exception:  # noqa: BLE001
                    log.exception("Bad workspace in %s", d)
        result = list(self._workspaces.values())
        log.info("Workspaces: %s", ", ".join(w.id for w in result) or "(none)")
        self.workspaces_discovered.emit(result)
        return result

    def all(self) -> List[Workspace]:
        return list(self._workspaces.values())

    def get(self, workspace_id: str) -> Optional[Workspace]:
        return self._workspaces.get(workspace_id)

    @property
    def current(self) -> Optional[Workspace]:
        return self._current

    # --------------------------------------------------------------- activation
    def activate(self, workspace_id: str, theme_override: Optional[str] = None,
                 restore_user_layout: bool = True) -> bool:
        if not self._workspaces:
            self.discover()
        ws = self._workspaces.get(workspace_id)
        if ws is None:
            log.error("Workspace '%s' not found", workspace_id)
            if not self._workspaces:
                return False
            ws = next(iter(self._workspaces.values()))
            log.warning("Falling back to workspace '%s'", ws.id)

        app = self.app
        if self._current is not None and self._current.id != ws.id and app.settings.get("ui.restore_last_layout", True):
            try:
                app.layout.save_user_layout(self._current.id, "last")
            except Exception:  # noqa: BLE001
                log.exception("Could not save layout of previous workspace")

        log.info("Activating workspace '%s'", ws.id)
        app.locale.set_overrides(ws.locale_overrides)

        theme_id = theme_override or ws.theme
        if not app.theme.apply(theme_id) and theme_id != ws.theme:
            app.theme.apply(ws.theme)

        app.context.load_presets(ws.read_json(ws.contexts, {"contexts": []}))
        app.window.build_menus(ws.read_json(ws.menu, {"menus": []}))
        app.window.build_toolbars(ws.read_json(ws.toolbar, {"toolbars": []}))

        default_layout = ws.read_json(ws.layout, {"docks": []})
        layout = None
        if restore_user_layout and app.settings.get("ui.restore_last_layout", True):
            layout = app.layout.load_user_layout(ws.id, "last")
            if layout is not None and not self._layout_is_usable(layout, default_layout):
                log.warning("Saved layout for '%s' is stale - falling back to the workspace default", ws.id)
                layout = None
        if layout is None:
            layout = default_layout
        app.layout.apply(layout, layout.get("id", f"{ws.id}_default"))

        self._current = ws
        app.settings.set("ui.workspace", ws.id)
        self.workspace_changed.emit(ws)
        return True

    def _layout_is_usable(self, layout: Dict[str, Any], default: Dict[str, Any]) -> bool:
        """A user layout is discarded when it no longer matches the available panels.

        Without this a single corrupt/outdated file would permanently leave the user
        without a central panel (no viewport) on every start.
        """
        registry = self.app.panels
        central = layout.get("central")
        if central is not None and not registry.has(central):
            return False
        if default.get("central") is not None and central is None:
            return False
        return any(registry.has(d.get("panel")) for d in layout.get("docks", []) if isinstance(d, dict))

    def reset_layout(self) -> None:
        if not self._current:
            return
        ws = self._current
        self.app.layout.apply(ws.read_json(ws.layout, {"docks": []}), f"{ws.id}_default")
        self.app.layout.delete_user_layout(ws.id, "last")

    def save_layout(self, name: str = "last") -> Optional[Path]:
        if not self._current:
            return None
        return self.app.layout.save_user_layout(self._current.id, name)

    def load_layout(self, name: str) -> bool:
        if not self._current:
            return False
        data = self.app.layout.load_user_layout(self._current.id, name)
        if data is None:
            return False
        self.app.layout.apply(data, data.get("id", name))
        return True

    def default_layout(self) -> Dict[str, Any]:
        if not self._current:
            return {"docks": []}
        return self._current.read_json(self._current.layout, {"docks": []})
