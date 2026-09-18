"""
Inline notification banner.

Used for the "point C2UI at your SFM installation" notice: C2UI runs perfectly well
without SFM, so this must inform rather than block - no modal dialog on startup.
"""
from __future__ import annotations

from typing import Callable, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QToolButton, QWidget

from ..icons import icon as make_icon
from ..localization import tr


class Banner(QWidget):
    """A dismissible one-line message strip with an optional action button."""

    dismissed = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("banner")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setVisible(False)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 6, 8, 6)
        lay.setSpacing(8)

        self.icon = QLabel(self)
        self.icon.setFixedSize(16, 16)
        self.icon.setScaledContents(True)
        lay.addWidget(self.icon)

        self.text = QLabel(self)
        self.text.setObjectName("bannerText")
        self.text.setWordWrap(True)
        self.text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        lay.addWidget(self.text, 1)

        self.action = QPushButton(self)
        self.action.setObjectName("bannerAction")
        self.action.setCursor(Qt.CursorShape.PointingHandCursor)
        self.action.setVisible(False)
        lay.addWidget(self.action)

        self.close_btn = QToolButton(self)
        self.close_btn.setObjectName("bannerClose")
        self.close_btn.setAutoRaise(True)
        self.close_btn.setToolTip(tr("dock.close"))
        self.close_btn.clicked.connect(self._on_dismiss)
        lay.addWidget(self.close_btn)

        self._icon_name = "info"
        self._action_connected = False
        self._refresh_icons()

    # ------------------------------------------------------------------ api
    def show_message(self, text: str, kind: str = "info", icon: str = "info",
                     action_text: str = "", action: Optional[Callable[[], None]] = None,
                     closable: bool = True) -> None:
        self.text.setText(text)
        self._icon_name = icon
        self.setProperty("kind", kind)          # info | warning | error -> QSS colours
        self.style().unpolish(self)
        self.style().polish(self)
        if self._action_connected:
            self.action.clicked.disconnect()
            self._action_connected = False
        if action is not None and action_text:
            self.action.setText(action_text)
            self.action.clicked.connect(action)
            self._action_connected = True
            self.action.setVisible(True)
        else:
            self.action.setVisible(False)
        self.close_btn.setVisible(closable)
        self._refresh_icons()
        self.setVisible(True)

    def hide_message(self) -> None:
        self.setVisible(False)

    def _on_dismiss(self) -> None:
        self.setVisible(False)
        self.dismissed.emit()

    def _refresh_icons(self) -> None:
        self.icon.setPixmap(make_icon(self._icon_name).pixmap(16, 16))
        self.close_btn.setIcon(make_icon("close"))

    def retheme(self) -> None:
        self._refresh_icons()
