"""Registry of panel types.  Built-in panels register on import; plugins may add more."""
from __future__ import annotations

import logging
from typing import Callable, Dict, List, Optional, Type

from PySide6.QtCore import QObject, Signal

from .base import C2UIPanel, PanelMeta

log = logging.getLogger("c2ui.panels")

PanelFactory = Callable[..., C2UIPanel]


class PanelRegistry(QObject):
    registered = Signal(str)
    unregistered = Signal(str)

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._types: Dict[str, Type[C2UIPanel]] = {}
        self._factories: Dict[str, PanelFactory] = {}

    def register(self, panel_cls: Type[C2UIPanel], factory: Optional[PanelFactory] = None) -> None:
        meta = panel_cls.META
        if meta.id in self._types:
            log.warning("Panel '%s' re-registered (was %s)", meta.id, self._types[meta.id].__name__)
        self._types[meta.id] = panel_cls
        self._factories[meta.id] = factory or panel_cls
        log.debug("Panel registered: %s (%s)", meta.id, panel_cls.__name__)
        self.registered.emit(meta.id)

    def unregister(self, panel_id: str) -> None:
        self._types.pop(panel_id, None)
        self._factories.pop(panel_id, None)
        self.unregistered.emit(panel_id)

    def has(self, panel_id: str) -> bool:
        return panel_id in self._types

    def meta(self, panel_id: str) -> Optional[PanelMeta]:
        cls = self._types.get(panel_id)
        return cls.META if cls else None

    def ids(self) -> List[str]:
        return list(self._types.keys())

    def all_meta(self) -> List[PanelMeta]:
        return [cls.META for cls in self._types.values()]

    def create(self, panel_id: str, app, parent=None) -> Optional[C2UIPanel]:
        factory = self._factories.get(panel_id)
        if not factory:
            log.error("Unknown panel id '%s'", panel_id)
            return None
        try:
            return factory(app, parent)
        except Exception:  # noqa: BLE001
            log.exception("Failed to create panel '%s'", panel_id)
            return None


_registry: Optional[PanelRegistry] = None


def get_panel_registry() -> PanelRegistry:
    global _registry
    if _registry is None:
        _registry = PanelRegistry()
    return _registry
