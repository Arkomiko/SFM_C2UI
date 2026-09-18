"""
ThemeManager - turns a JSON theme into a live Qt look.

A theme is a JSON file in Themes/ (or the user themes dir)::

    {
      "id": "ue5_dark", "name": "Unreal Dark", "base": null,
      "qss": "base.qss",                     # template, default = Themes/base.qss
      "tokens":  { "bg.window": "#1a1a1a", "accent": "#0070e0", "font.size": 9, ... },
      "palette": { "window": "@{bg.window}", "highlight": "@{accent}", ... }
    }

* "tokens" are substituted into the QSS template wherever @{token.name} appears.
* Missing x.hover / x.pressed / x.disabled / x.alphaNN tokens are derived from x.
* "palette" maps QPalette roles (for widgets that ignore QSS).
* "base" lets a theme inherit and override another one.
* "icons:" becomes a Qt search path pointing at icons tinted with @{icon.color},
  so QSS can say  image: url(icons:chevron_down.svg)
"""
from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QDir, QFileSystemWatcher, QObject, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QApplication

from . import paths
from .icons import get_icon_provider

log = logging.getLogger("c2ui.theme")

_TOKEN_RE = re.compile(r"@\{([a-zA-Z0-9_.\-]+)\}")
_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)

_PALETTE_ROLES = {
    "window": QPalette.ColorRole.Window,
    "windowText": QPalette.ColorRole.WindowText,
    "base": QPalette.ColorRole.Base,
    "alternateBase": QPalette.ColorRole.AlternateBase,
    "text": QPalette.ColorRole.Text,
    "button": QPalette.ColorRole.Button,
    "buttonText": QPalette.ColorRole.ButtonText,
    "brightText": QPalette.ColorRole.BrightText,
    "highlight": QPalette.ColorRole.Highlight,
    "highlightedText": QPalette.ColorRole.HighlightedText,
    "toolTipBase": QPalette.ColorRole.ToolTipBase,
    "toolTipText": QPalette.ColorRole.ToolTipText,
    "link": QPalette.ColorRole.Link,
    "placeholderText": QPalette.ColorRole.PlaceholderText,
    "light": QPalette.ColorRole.Light,
    "midlight": QPalette.ColorRole.Midlight,
    "mid": QPalette.ColorRole.Mid,
    "dark": QPalette.ColorRole.Dark,
    "shadow": QPalette.ColorRole.Shadow,
}


@dataclass
class Theme:
    id: str
    name: str = ""
    author: str = ""
    description: str = ""
    base: Optional[str] = None
    qss: str = "base.qss"
    variant: str = "dark"                      # dark | light  (hint for icons/derivations)
    tokens: Dict[str, Any] = field(default_factory=dict)
    palette: Dict[str, str] = field(default_factory=dict)
    file: Optional[Path] = None

    @classmethod
    def from_file(cls, file: Path) -> "Theme":
        with file.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return cls(
            id=data.get("id", file.stem),
            name=data.get("name", file.stem),
            author=data.get("author", ""),
            description=data.get("description", ""),
            base=data.get("base"),
            qss=data.get("qss", "base.qss"),
            variant=data.get("variant", "dark"),
            tokens=dict(data.get("tokens", {})),
            palette=dict(data.get("palette", {})),
            file=file,
        )

    def merged_over(self, parent: "Theme") -> "Theme":
        tokens = dict(parent.tokens)
        tokens.update(self.tokens)
        palette = dict(parent.palette)
        palette.update(self.palette)
        return Theme(
            id=self.id, name=self.name or parent.name, author=self.author or parent.author,
            description=self.description or parent.description, base=parent.id,
            qss=self.qss if self.qss != "base.qss" else parent.qss, variant=self.variant,
            tokens=tokens, palette=palette, file=self.file,
        )


class ThemeManager(QObject):
    theme_changed = Signal(object)          # Theme
    themes_discovered = Signal(list)        # List[Theme] (metadata only)

    def __init__(self, app: QApplication, hot_reload: bool = True, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._app = app
        self._current: Optional[Theme] = None
        self._search_dirs: List[Path] = [paths.THEMES_DIR, paths.USER_THEMES_DIR]
        self._font_scale = 1.0
        self._icon_color: Optional[str] = None      # last exported tint
        self._watcher: Optional[QFileSystemWatcher] = None
        self._reload_timer = QTimer(self)
        self._reload_timer.setSingleShot(True)
        self._reload_timer.setInterval(150)
        self._reload_timer.timeout.connect(self._hot_reload)
        if hot_reload:
            self._watcher = QFileSystemWatcher(self)
            self._watcher.fileChanged.connect(lambda _p: self._reload_timer.start())

    # -- discovery ------------------------------------------------------------------
    def available(self) -> List[Theme]:
        found: Dict[str, Theme] = {}
        for d in self._search_dirs:
            if not d.is_dir():
                continue
            for file in sorted(d.glob("*.json")):
                try:
                    found_theme = Theme.from_file(file)
                except (OSError, ValueError, KeyError) as exc:
                    log.warning("Skipping invalid theme file %s (%s)", file.name, exc)
                    continue
                found[found_theme.id] = found_theme
        themes = list(found.values())
        self.themes_discovered.emit(themes)
        return themes

    def find_file(self, theme_id: str) -> Optional[Path]:
        for d in self._search_dirs:
            p = d / f"{theme_id}.json"
            if p.is_file():
                return p
        for t in self.available():           # id may differ from file name
            if t.id == theme_id and t.file:
                return t.file
        return None

    def load(self, theme_id: str, _depth: int = 0) -> Optional[Theme]:
        file = self.find_file(theme_id)
        if not file:
            log.error("Theme '%s' not found", theme_id)
            return None
        try:
            theme = Theme.from_file(file)
        except (OSError, ValueError, KeyError) as exc:
            log.warning("Theme '%s' could not be read (%s)", theme_id, exc)
            return None
        if theme.base and _depth < 8:
            parent = self.load(theme.base, _depth + 1)
            if parent:
                theme = theme.merged_over(parent)
        return theme

    # -- state ------------------------------------------------------------------------
    @property
    def current(self) -> Optional[Theme]:
        return self._current

    def set_font_scale(self, scale: float) -> None:
        self._font_scale = max(0.5, min(3.0, scale))
        if self._current:
            self.apply(self._current.id)

    def token(self, name: str, default: Any = None) -> Any:
        if not self._current:
            return default
        return self._resolve_token(self._current.tokens, name, default)

    def color(self, name: str, default: str = "#ff00ff") -> QColor:
        return QColor(str(self.token(name, default)))

    # -- apply ------------------------------------------------------------------------
    def apply(self, theme_id: str) -> bool:
        theme = self.load(theme_id)
        if theme is None:
            return False
        try:
            qss = self.build_qss(theme)
        except Exception:  # noqa: BLE001
            log.exception("Failed to build QSS for theme '%s'", theme_id)
            return False

        self._export_icons(theme)
        self._apply_font(theme)
        self._apply_palette(theme)
        self._app.setStyleSheet(qss)
        self._current = theme
        self._watch(theme)
        log.info("Theme applied: %s (%s)", theme.name, theme.id)
        self.theme_changed.emit(theme)
        return True

    def reapply(self) -> None:
        if self._current:
            self.apply(self._current.id)

    # -- building ---------------------------------------------------------------------
    def qss_template_path(self, theme: Theme) -> Path:
        candidates = []
        if theme.file:
            candidates.append(theme.file.parent / theme.qss)
        candidates += [d / theme.qss for d in self._search_dirs]
        for c in candidates:
            if c.is_file():
                return c
        raise FileNotFoundError(f"QSS template '{theme.qss}' not found for theme {theme.id}")

    def build_qss(self, theme: Theme) -> str:
        template = self.qss_template_path(theme).read_text(encoding="utf-8")
        template = _COMMENT_RE.sub("", template)          # comments may mention @{...} literally
        tokens = dict(theme.tokens)
        tokens.setdefault("font.size", 9)
        tokens["font.size"] = round(float(tokens["font.size"]) * self._font_scale, 1)
        missing: set[str] = set()

        def _sub(m: re.Match[str]) -> str:
            name = m.group(1)
            value = self._resolve_token(tokens, name, None)
            if value is None:
                missing.add(name)
                return "#ff00ff"
            return str(value)

        # Two passes so tokens may reference other tokens.
        qss = _TOKEN_RE.sub(_sub, template)
        qss = _TOKEN_RE.sub(_sub, qss)
        if missing:
            log.warning("Theme '%s': unresolved tokens: %s", theme.id, ", ".join(sorted(missing)))
        return qss

    def _resolve_token(self, tokens: Dict[str, Any], name: str, default: Any) -> Any:
        if name in tokens:
            value = tokens[name]
            if isinstance(value, str) and _TOKEN_RE.search(value):
                return _TOKEN_RE.sub(lambda m: str(self._resolve_token(tokens, m.group(1), "#ff00ff")), value)
            return value
        # derived states: foo.hover / foo.pressed / foo.disabled / foo.alpha50
        for suffix, fn in (
            (".hover", lambda c: _adjust(c, 1.18)),
            (".pressed", lambda c: _adjust(c, 0.85)),
            (".disabled", lambda c: _with_alpha(c, 0.4)),
        ):
            if name.endswith(suffix):
                base = self._resolve_token(tokens, name[: -len(suffix)], None)
                if base is not None:
                    return fn(str(base))
        m = re.match(r"^(.*)\.alpha(\d{1,3})$", name)
        if m:
            base = self._resolve_token(tokens, m.group(1), None)
            if base is not None:
                return _with_alpha(str(base), int(m.group(2)) / 100.0)
        return default

    def _apply_palette(self, theme: Theme) -> None:
        pal = QPalette(self._app.style().standardPalette())
        for key, raw in theme.palette.items():
            role = _PALETTE_ROLES.get(key)
            if role is None:
                continue
            value = _TOKEN_RE.sub(lambda m: str(self._resolve_token(theme.tokens, m.group(1), "#ff00ff")), str(raw))
            color = QColor(value)
            if color.isValid():
                pal.setColor(role, color)
                if key in ("text", "windowText", "buttonText"):
                    pal.setColor(QPalette.ColorGroup.Disabled, role, _qcolor_alpha(color, 0.4))
        self._app.setPalette(pal)

    def _apply_font(self, theme: Theme) -> None:
        family = str(theme.tokens.get("font.family", "Segoe UI"))
        size = float(theme.tokens.get("font.size", 9)) * self._font_scale
        font = QFont(family)
        font.setPointSizeF(size)
        self._app.setFont(font)

    def _export_icons(self, theme: Theme) -> None:
        color = str(self._resolve_token(theme.tokens, "icon.color", "#c8c8c8"))
        target = paths.USER_CACHE_DIR / "icons" / theme.id
        QDir.setSearchPaths("icons", [str(target)])
        if color == self._icon_color and target.is_dir():
            return                      # same tint - the cached SVGs are still valid
        try:
            n = get_icon_provider().export_tinted(target, color)
            log.debug("Exported %d tinted icons to %s", n, target)
        except OSError:
            log.exception("Icon export failed")
        provider = get_icon_provider()
        provider.default_color = color
        provider.clear_cache()
        self._icon_color = color

    # -- hot reload -------------------------------------------------------------------
    def _watch(self, theme: Theme) -> None:
        if not self._watcher:
            return
        files = self._watcher.files()
        if files:
            self._watcher.removePaths(files)
        to_watch = []
        if theme.file:
            to_watch.append(str(theme.file))
        try:
            to_watch.append(str(self.qss_template_path(theme)))
        except FileNotFoundError:
            pass
        if theme.base:
            base_file = self.find_file(theme.base)
            if base_file:
                to_watch.append(str(base_file))
        self._watcher.addPaths(to_watch)

    def _hot_reload(self) -> None:
        if self._current:
            log.info("Theme file changed - reloading '%s'", self._current.id)
            self.apply(self._current.id)


# -- colour helpers ----------------------------------------------------------------------
def _adjust(hex_color: str, factor: float) -> str:
    c = QColor(hex_color)
    if not c.isValid():
        return hex_color
    h, s, v, a = c.getHsvF()
    v = max(0.0, min(1.0, v * factor))
    if factor > 1 and v >= 0.999:          # already white-ish: brighten via saturation drop
        s = max(0.0, s - 0.15)
    out = QColor.fromHsvF(h if h >= 0 else 0, s, v, a)
    return out.name(QColor.NameFormat.HexArgb if a < 1 else QColor.NameFormat.HexRgb)


def _with_alpha(hex_color: str, alpha: float) -> str:
    c = QColor(hex_color)
    c.setAlphaF(alpha)
    return c.name(QColor.NameFormat.HexArgb)


def _qcolor_alpha(c: QColor, alpha: float) -> QColor:
    out = QColor(c)
    out.setAlphaF(alpha)
    return out
