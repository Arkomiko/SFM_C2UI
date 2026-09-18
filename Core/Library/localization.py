"""
Localization (i18n).

Locale files live in Locales/<code>.json and may be nested::

    { "_meta": {"name": "English", "native_name": "English"},
      "menu": { "file": "File", "edit": "Edit" } }

Usage::

    from Core.Library.localization import tr
    tr("menu.file")                    -> "File"
    tr("status.sfm_launched", pid=42)  -> formats "{pid}" into the string

Missing keys fall back to English, then to the key itself, so the UI never breaks.
Workspaces may ship "locale_overrides" that are layered on top.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QObject, Signal

from . import paths

log = logging.getLogger("c2ui.i18n")

FALLBACK_LANGUAGE = "en"


def _flatten(node: Dict[str, Any], prefix: str = "") -> Dict[str, str]:
    out: Dict[str, str] = {}
    for k, v in node.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(_flatten(v, key))
        else:
            out[key] = str(v)
    return out


class LocaleManager(QObject):
    language_changed = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._language = FALLBACK_LANGUAGE
        self._meta: Dict[str, Dict[str, Any]] = {}
        self._available_cache: Optional[List[Dict[str, Any]]] = None
        self._overrides_raw: Dict[str, Any] = {}
        self._overrides: Dict[str, str] = {}
        self._fallback: Dict[str, str] = self._load_file(FALLBACK_LANGUAGE)
        self._strings: Dict[str, str] = dict(self._fallback)

    # -- discovery ----------------------------------------------------------------
    def available(self, refresh: bool = False) -> List[Dict[str, Any]]:
        """Return [{code, name, native_name}] for every locale file found (cached)."""
        if self._available_cache is not None and not refresh:
            return self._available_cache
        result = []
        for file in sorted(paths.LOCALES_DIR.glob("*.json")):
            code = file.stem
            meta = self._meta.get(code) or self._read_meta(file)
            result.append({
                "code": code,
                "name": meta.get("name", code),
                "native_name": meta.get("native_name", code),
            })
        self._available_cache = result
        return result

    def _read_meta(self, file: Path) -> Dict[str, Any]:
        try:
            with file.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            meta = data.get("_meta", {})
            self._meta[file.stem] = meta
            return meta
        except Exception:  # noqa: BLE001
            return {}

    def _load_file(self, code: str) -> Dict[str, str]:
        file = paths.LOCALES_DIR / f"{code}.json"
        if not file.is_file():
            log.warning("Locale file not found: %s", file)
            return {}
        try:
            with file.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            self._meta[code] = data.pop("_meta", {})
            return _flatten(data)
        except (OSError, ValueError) as exc:
            log.warning("Locale file %s is invalid (%s)", file.name, exc)
            return {}

    # -- state ----------------------------------------------------------------------
    @property
    def language(self) -> str:
        return self._language

    def set_language(self, code: str) -> bool:
        strings = dict(self._fallback) if code == FALLBACK_LANGUAGE else self._load_file(code)
        if not strings and code != FALLBACK_LANGUAGE:
            return False
        self._language = code
        self._strings = strings
        self.set_overrides(self._overrides_raw)
        log.info("Language set to '%s' (%d strings)", code, len(strings))
        self.language_changed.emit(code)
        return True

    def set_overrides(self, overrides: Optional[Dict[str, Any]]) -> None:
        """Workspace-level overrides: {"en": {...}, "ru": {...}}."""
        self._overrides_raw = overrides or {}
        lang_block = self._overrides_raw.get(self._language)
        self._overrides = _flatten(lang_block) if isinstance(lang_block, dict) else {}

    # -- lookup ---------------------------------------------------------------------
    def tr(self, key: str, **kwargs: Any) -> str:
        text = self._overrides.get(key) or self._strings.get(key) or self._fallback.get(key) or key
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, IndexError, ValueError):
                pass
        return text


_instance: Optional[LocaleManager] = None


def get_locale_manager() -> LocaleManager:
    global _instance
    if _instance is None:
        _instance = LocaleManager()
    return _instance


def tr(key: str, **kwargs: Any) -> str:
    """Module-level shortcut used all over the UI code."""
    return get_locale_manager().tr(key, **kwargs)
