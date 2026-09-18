"""
Base classes for dockable editor panels.

A *panel* is the content widget that lives inside a QDockWidget (or the central
area).  Panels are created by the LayoutManager through the PanelRegistry and are
identified by a stable string id ("outliner", "details", ...).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from ..localization import tr

# Dock areas as they appear in layout JSON files.
DOCK_AREAS: Dict[str, Qt.DockWidgetArea] = {
    "left": Qt.DockWidgetArea.LeftDockWidgetArea,
    "right": Qt.DockWidgetArea.RightDockWidgetArea,
    "top": Qt.DockWidgetArea.TopDockWidgetArea,
    "bottom": Qt.DockWidgetArea.BottomDockWidgetArea,
}


@dataclass
class PanelMeta:
    id: str                                  # stable identifier used in layouts
    title_key: str                           # localization key for the title
    icon: str = "panel"                      # icon name in Assets/icons
    category: str = "General"                # grouping in the Window menu
    default_area: str = "right"
    allowed_areas: List[str] = field(default_factory=lambda: ["left", "right", "top", "bottom"])
    singleton: bool = True                   # only one instance allowed
    closable: bool = True
    min_size: tuple[int, int] = (160, 120)
    sfm_lookup: Optional[str] = None         # native SFM window "lookupString" (for embedding)

    def title(self) -> str:
        return tr(self.title_key)

    def qt_allowed_areas(self) -> Qt.DockWidgetArea:
        areas = Qt.DockWidgetArea.NoDockWidgetArea
        for a in self.allowed_areas:
            areas |= DOCK_AREAS.get(a, Qt.DockWidgetArea.NoDockWidgetArea)
        return areas


class C2UIPanel(QWidget):
    """
    Base widget for every panel.  Subclasses override :meth:`build` to create their UI
    and may react to app-wide changes through the on_* hooks.
    """

    META: PanelMeta = PanelMeta(id="panel", title_key="panel.generic")

    title_changed = Signal(str)
    selection_changed = Signal(list)          # panel-local selection -> ContextManager

    def __init__(self, app: Any, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.app = app                        # C2UIApplication (typed loosely to avoid cycles)
        self._unsubscribe: List[Callable[[], None]] = []
        self.setObjectName(f"panel_{self.META.id}")
        self.setMinimumSize(*self.META.min_size)
        self._root = QVBoxLayout(self)
        self._root.setContentsMargins(0, 0, 0, 0)
        self._root.setSpacing(0)
        self.build()

    # -- overridables -------------------------------------------------------------
    def build(self) -> None:
        """Create child widgets; add them to self.root_layout."""

    def on_theme_changed(self, theme: Any) -> None:
        """Theme was (re)applied - refresh custom-painted colours here."""

    def on_language_changed(self, code: str) -> None:
        """Re-translate any text that is not driven by Qt itself."""
        self.title_changed.emit(self.META.title())

    def on_context_changed(self, context_id: str) -> None:
        """Editor mode/context switched (see ContextManager)."""

    def on_sfm_connected(self, connected: bool) -> None:
        """Bridge to SFM came up / went down."""

    def save_state(self) -> Dict[str, Any]:
        """Return JSON-serialisable panel state (persisted with the layout)."""
        return {}

    def restore_state(self, state: Dict[str, Any]) -> None:
        """Restore state produced by save_state."""

    # -- helpers ------------------------------------------------------------------
    def subscribe(self, topic: str, handler: Callable[[Any], None]) -> None:
        """Subscribe to an app event for as long as this panel exists.

        Panels outlive individual layouts but not workspaces, so a raw EventBus
        subscription would keep firing into a deleted widget.
        """
        unsub = self.app.events.subscribe(topic, handler)
        self._unsubscribe.append(unsub)
        self.destroyed.connect(lambda *_a, u=unsub: u())

    @property
    def root_layout(self) -> QVBoxLayout:
        return self._root

    @property
    def panel_id(self) -> str:
        return self.META.id

    def window_title(self) -> str:
        return self.META.title()
