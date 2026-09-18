"""
Icon provider.

SVG icons in Assets/icons use ``currentColor`` so a single monochrome asset can be
tinted to match any theme.  ``IconProvider.icon("play", "#dddddd")`` returns a QIcon
with normal/disabled states rendered at several device pixel ratios.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Optional, Tuple

from PySide6.QtCore import QByteArray, QRectF, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

from . import paths

log = logging.getLogger("c2ui.icons")

_SIZES = (16, 20, 24, 32, 48)


class IconProvider:
    def __init__(self, search_dirs: Optional[list[Path]] = None) -> None:
        self.search_dirs: list[Path] = search_dirs or [paths.ICONS_DIR]
        self._svg_cache: Dict[str, Optional[str]] = {}
        self._icon_cache: Dict[Tuple[str, str], QIcon] = {}
        self.default_color = "#c8c8c8"

    # -- lookup -------------------------------------------------------------------
    def find(self, name: str) -> Optional[Path]:
        for d in self.search_dirs:
            p = d / f"{name}.svg"
            if p.is_file():
                return p
        return None

    def svg_source(self, name: str) -> Optional[str]:
        if name not in self._svg_cache:
            p = self.find(name)
            try:
                self._svg_cache[name] = p.read_text(encoding="utf-8") if p else None
            except OSError:
                self._svg_cache[name] = None
            if self._svg_cache[name] is None:
                log.debug("Icon not found: %s", name)
        return self._svg_cache[name]

    def tinted_svg(self, name: str, color: str) -> Optional[str]:
        src = self.svg_source(name)
        return src.replace("currentColor", color) if src else None

    # -- rendering ----------------------------------------------------------------
    def icon(self, name: str, color: Optional[str] = None) -> QIcon:
        color = color or self.default_color
        key = (name, color)
        if key in self._icon_cache:
            return self._icon_cache[key]
        icon = QIcon()
        svg = self.tinted_svg(name, color)
        if svg:
            renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))
            disabled_svg = self.tinted_svg(name, _with_alpha(color, 0.35))
            disabled = QSvgRenderer(QByteArray(disabled_svg.encode("utf-8"))) if disabled_svg else None
            for size in _SIZES:
                icon.addPixmap(_render(renderer, size), QIcon.Mode.Normal, QIcon.State.Off)
                if disabled:
                    icon.addPixmap(_render(disabled, size), QIcon.Mode.Disabled, QIcon.State.Off)
        self._icon_cache[key] = icon
        return icon

    def pixmap(self, name: str, size: int = 16, color: Optional[str] = None) -> QPixmap:
        return self.icon(name, color).pixmap(size, size)

    def clear_cache(self) -> None:
        self._icon_cache.clear()

    def export_tinted(self, target_dir: Path, color: str) -> int:
        """Write tinted copies of every icon into target_dir (used by QSS url())."""
        target_dir.mkdir(parents=True, exist_ok=True)
        count = 0
        for d in self.search_dirs:
            for svg in d.glob("*.svg"):
                tinted = self.tinted_svg(svg.stem, color)
                if tinted is None:
                    continue
                out = target_dir / svg.name
                if not out.is_file() or out.read_text(encoding="utf-8") != tinted:
                    out.write_text(tinted, encoding="utf-8")
                count += 1
        return count


def _render(renderer: QSvgRenderer, size: int) -> QPixmap:
    pm = QPixmap(size, size)
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(painter, QRectF(0, 0, size, size))
    painter.end()
    return pm


def _with_alpha(color: str, alpha: float) -> str:
    """SVG/CSS rgba() - an 8-digit hex is not portable inside SVG attributes."""
    c = QColor(color)
    return f"rgba({c.red()},{c.green()},{c.blue()},{alpha:.2f})"


_provider: Optional[IconProvider] = None


def get_icon_provider() -> IconProvider:
    global _provider
    if _provider is None:
        _provider = IconProvider()
    return _provider


def icon(name: str, color: Optional[str] = None) -> QIcon:
    return get_icon_provider().icon(name, color)
