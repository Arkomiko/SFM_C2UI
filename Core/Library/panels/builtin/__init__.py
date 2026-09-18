"""Built-in panels.  Importing this package registers them with the PanelRegistry."""
from ..registry import get_panel_registry
from .content_browser import ContentBrowserPanel
from .details import DetailsPanel
from .outliner import OutlinerPanel
from .output_log import OutputLogPanel
from .place_actors import PlaceActorsPanel
from .timeline import TimelinePanel
from .viewport import ViewportPanel

BUILTIN_PANELS = [
    ViewportPanel,
    OutlinerPanel,
    DetailsPanel,
    ContentBrowserPanel,
    OutputLogPanel,
    TimelinePanel,
    PlaceActorsPanel,
]

_registry = get_panel_registry()
for _cls in BUILTIN_PANELS:
    if not _registry.has(_cls.META.id):
        _registry.register(_cls)

__all__ = ["BUILTIN_PANELS"]
