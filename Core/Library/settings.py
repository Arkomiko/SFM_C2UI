"""
User settings (JSON) with dotted-key access and defaults.

    settings.get("ui.language", "en")
    settings.set("ui.theme", "ue5_dark")      # persisted automatically (debounced)

Writes are coalesced through a short timer so a burst of changes (e.g. dragging a
slider in Preferences) costs one disk write instead of dozens.
"""
from __future__ import annotations

import atexit
import copy
import json
import logging
from pathlib import Path
from typing import Any, Dict

from PySide6.QtCore import QObject, QTimer, Signal

from . import paths

log = logging.getLogger("c2ui.settings")

SAVE_DELAY_MS = 400

DEFAULTS: Dict[str, Any] = {
    "ui": {
        "language": "en",
        "theme": "ue5_dark",
        "workspace": "UnrealEditor",
        "font_scale": 1.0,
        "restore_last_layout": True,
        "show_sfm_banner": True,        # hide the "point me at SFM" banner once dismissed
    },
    "sfm": {
        "root": "",                     # SFM install folder ("" = auto-detect)
        "exe": "",                      # explicit sfm.exe override (rarely needed)
        "launch_args": [],
        "auto_launch": False,           # launch sfm.exe when C2UI starts
        "auto_connect": True,           # try to connect to the in-process agent
        "agent_port": 41794,
        "connect_timeout_sec": 2.0,
        "auto_install_agent": True,     # write the sfm_init.py hook before launching
        "embed_viewport_on_connect": True,
        "sync_theme": True,             # push the C2UI theme into SFM's own Qt widgets
        "viewport_lookup": "Primary Viewport",
        "auto_dismiss_startup_dialogs": True,
    },
    "plugins": {
        "disabled": [],
    },
    "dev": {
        "hot_reload_themes": True,
        "log_level": "INFO",
    },
}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = copy.deepcopy(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


class Settings(QObject):
    changed = Signal(str, object)   # (dotted key, new value)

    def __init__(self, file: Path | None = None, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._file = file or paths.USER_SETTINGS_FILE
        self._data: Dict[str, Any] = copy.deepcopy(DEFAULTS)
        self._dirty = False
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(SAVE_DELAY_MS)
        self._timer.timeout.connect(self.flush)
        self.load()
        atexit.register(self.flush)

    # -- persistence ------------------------------------------------------------
    def load(self) -> None:
        if not self._file.is_file():
            return
        try:
            with self._file.open("r", encoding="utf-8") as fh:
                user = json.load(fh)
            self._data = _deep_merge(DEFAULTS, user)
            log.debug("Settings loaded from %s", self._file)
        except (OSError, ValueError) as exc:
            log.warning("Settings file %s is invalid (%s) - using defaults", self._file.name, exc)

    def flush(self) -> None:
        """Write pending changes to disk now."""
        if not self._dirty:
            return
        self._dirty = False
        try:
            self._file.parent.mkdir(parents=True, exist_ok=True)
            tmp = self._file.with_suffix(".json.tmp")
            with tmp.open("w", encoding="utf-8") as fh:
                json.dump(self._data, fh, indent=2, ensure_ascii=False)
            tmp.replace(self._file)     # atomic: never leave a truncated settings file
        except OSError:
            log.exception("Failed to save settings to %s", self._file)

    save = flush        # backwards-compatible alias

    # -- access -----------------------------------------------------------------
    def get(self, key: str, default: Any = None) -> Any:
        node: Any = self._data
        for part in key.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node

    def set(self, key: str, value: Any, save: bool = True) -> None:
        parts = key.split(".")
        node = self._data
        for part in parts[:-1]:
            nxt = node.get(part)
            if not isinstance(nxt, dict):
                nxt = {}
                node[part] = nxt
            node = nxt
        if node.get(parts[-1]) == value:
            return
        node[parts[-1]] = value
        self._dirty = True
        if save:
            self._timer.start()
        self.changed.emit(key, value)

    def as_dict(self) -> Dict[str, Any]:
        return copy.deepcopy(self._data)
