"""
PanelDock - a QDockWidget hosting a C2UIPanel with a UE5-style header.

The header (DockTitleBar) shows the panel icon, title and float/close buttons.
When the dock is part of a tab group the LayoutManager hides the header so the
tab bar acts as the title, exactly like Unreal's tab wells.
"""
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QEvent, Signal
from PySide6.QtWidgets import QDockWidget, QHBoxLayout, QLabel, QSizePolicy, QToolButton, QWidget

from ..icons import icon as make_icon
from ..localization import tr
from ..panels.base import C2UIPanel


class DockTitleBar(QWidget):
    def __init__(self, dock: "PanelDock") -> None:
        super().__init__(dock)
        self.setObjectName("dockTitleBar")
        self._dock = dock
        lay = QHBoxLayout(self)
        lay.setContentsMargins(8, 0, 4, 0)
        lay.setSpacing(6)

        self.icon_label = QLabel(self)
        self.icon_label.setObjectName("dockTitleIcon")
        self.icon_label.setFixedSize(16, 16)
        self.icon_label.setScaledContents(True)
        lay.addWidget(self.icon_label)

        self.title_label = QLabel(self)
        self.title_label.setObjectName("dockTitleText")
        self.title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        lay.addWidget(self.title_label, 1)

        self.float_btn = QToolButton(self)
        self.float_btn.setObjectName("dockFloatButton")
        self.float_btn.setAutoRaise(True)
        self.float_btn.setToolTip(tr("dock.float"))
        self.float_btn.clicked.connect(lambda: dock.setFloating(not dock.isFloating()))
        lay.addWidget(self.float_btn)

        self.close_btn = QToolButton(self)
        self.close_btn.setObjectName("dockCloseButton")
        self.close_btn.setAutoRaise(True)
        self.close_btn.setToolTip(tr("dock.close"))
        self.close_btn.clicked.connect(dock.close)
        lay.addWidget(self.close_btn)

        self.setFixedHeight(26)
        self.refresh()

    def refresh(self) -> None:
        meta = self._dock.panel.META
        self.icon_label.setPixmap(make_icon(meta.icon).pixmap(16, 16))
        self.title_label.setText(meta.title())
        self.float_btn.setIcon(make_icon("dock_float"))
        self.close_btn.setIcon(make_icon("close"))
        self.close_btn.setVisible(meta.closable)

    def mouseDoubleClickEvent(self, event) -> None:  # noqa: N802
        self._dock.setFloating(not self._dock.isFloating())
        event.accept()


class PanelDock(QDockWidget):
    closed = Signal()

    def __init__(self, panel: C2UIPanel, parent: Optional[QWidget] = None) -> None:
        super().__init__(panel.META.title(), parent)
        self.panel = panel
        self.setObjectName(f"dock_{panel.META.id}")
        self.setWidget(panel)
        features = QDockWidget.DockWidgetFeature.DockWidgetMovable | QDockWidget.DockWidgetFeature.DockWidgetFloatable
        if panel.META.closable:
            features |= QDockWidget.DockWidgetFeature.DockWidgetClosable
        self.setFeatures(features)
        self._header = DockTitleBar(self)
        self._blank = QWidget(self)
        self._blank.setObjectName("dockTitleHidden")
        self._blank.setFixedHeight(0)
        self.setTitleBarWidget(self._header)
        panel.title_changed.connect(self._on_title_changed)

    def set_header_visible(self, visible: bool) -> None:
        target = self._header if visible else self._blank
        if self.titleBarWidget() is not target:
            self.setTitleBarWidget(target)

    def retranslate(self) -> None:
        self._on_title_changed(self.panel.META.title())

    def _on_title_changed(self, title: str) -> None:
        self.setWindowTitle(title)
        self._header.refresh()

    def closeEvent(self, event: QEvent) -> None:  # noqa: N802
        event.ignore()          # never destroy - the LayoutManager hides and re-shows docks
        self.hide()
        self.closed.emit()

    def changeEvent(self, event: QEvent) -> None:  # noqa: N802
        if event.type() == QEvent.Type.StyleChange:
            self._header.refresh()
        super().changeEvent(event)
