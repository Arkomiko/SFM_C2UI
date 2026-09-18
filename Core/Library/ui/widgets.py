"""Small reusable widgets shared by panels."""
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QLineEdit, QWidget

from ..icons import icon as make_icon


class SearchField(QLineEdit):
    """QLineEdit with a leading, theme-tinted search icon and a clear button."""

    def __init__(self, parent: Optional[QWidget] = None, icon_name: str = "search") -> None:
        super().__init__(parent)
        self.setObjectName("searchField")
        self._icon_name = icon_name
        self.setClearButtonEnabled(True)
        self._lead = self.addAction(make_icon(icon_name), QLineEdit.ActionPosition.LeadingPosition)

    def changeEvent(self, event: QEvent) -> None:  # noqa: N802
        if event.type() in (QEvent.Type.StyleChange, QEvent.Type.PaletteChange):
            self._lead.setIcon(make_icon(self._icon_name))
        super().changeEvent(event)
