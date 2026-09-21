"""
User settings: one JSON file under App/User/Settings.

Kept deliberately small. Values are plain JSON types, keys are dotted names,
and a write goes through a temporary file so a crash mid-save cannot leave
half a file behind. Nothing here lives outside the application folder.

    settings = Settings.load()
    settings.get("content.sfm_path")
    settings.set("content.sfm_path", r"D:\\Steam\\...\\SourceFilmmaker")
    settings.save()
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

from . import locations

__all__ = ["Settings", "DEFAULTS"]

DEFAULTS: Dict[str, Any] = {
    "content.source": "sfm",
    "content.sfm_path": "",
    "viewport.up_axis": "auto",
    "window.geometry": "",
}


class Settings:
    """User settings: a JSON file under App/User/Settings."""
    FILE_NAME = "settings.json"

    def __init__(self, path: Optional[Path] = None, values: Optional[Dict[str, Any]] = None) -> None:
        self.path = Path(path) if path else locations.SETTINGS / self.FILE_NAME
        self.values: Dict[str, Any] = dict(DEFAULTS)
        if values:
            self.values.update(values)
        self.dirty = False

    @classmethod
    def load(cls, path: Optional[Path] = None) -> "Settings":
        """Read settings, falling back to defaults on any error."""
        settings = cls(path)
        try:
            raw = json.loads(settings.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return settings
        except (OSError, ValueError):
            # unreadable settings are treated as absent, not as a reason to fail
            return settings
        if isinstance(raw, dict):
            settings.values.update({k: v for k, v in raw.items() if isinstance(k, str)})
        return settings

    def get(self, key: str, default: Any = None) -> Any:
        """A value, else its default."""
        return self.values.get(key, DEFAULTS.get(key, default))

    def set(self, key: str, value: Any) -> None:
        """Change a value and mark the settings dirty."""
        if self.values.get(key) != value:
            self.values[key] = value
            self.dirty = True

    def save(self) -> bool:
        """Write if anything changed.  Returns whether a write happened."""
        if not self.dirty:
            return False
        self.path.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(self.values, indent=2, ensure_ascii=False, sort_keys=True)
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, prefix=".settings-", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(text)
            os.replace(tmp, self.path)
        except OSError:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise
        self.dirty = False
        return True
