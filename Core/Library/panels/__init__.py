"""Panel system: base class, metadata and the registry of available panels."""
from .base import C2UIPanel, PanelMeta
from .registry import PanelRegistry, get_panel_registry

__all__ = ["C2UIPanel", "PanelMeta", "PanelRegistry", "get_panel_registry"]
