"""
The element inspector: every attribute of the selected element, editable.

Values are shown as text in the datamodel's own spelling ("1 2 3" for a
vector, "0.5" for a time in seconds, "1"/"0" for a bool) and parsed back
the same way. Editing emits `edited`; the window decides how to apply it -
through the undo stack, and as a key when the attribute is animated.
Element references show as links; double-clicking one navigates to it.
"""
from __future__ import annotations

import uuid
from typing import Any, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QAbstractItemView, QTreeWidget, QTreeWidgetItem

from Core.API.dmx import ARRAY_OFFSET, AttrType, Element, Time, is_array, type_name

__all__ = ["Inspector", "parse_value", "format_value"]

ROLE_ATTR = Qt.UserRole
ROLE_INDEX = Qt.UserRole + 1
ROLE_ELEMENT = Qt.UserRole + 2

_EDITABLE = {AttrType.INT, AttrType.FLOAT, AttrType.BOOL, AttrType.STRING, AttrType.TIME,
             AttrType.COLOR, AttrType.VECTOR2, AttrType.VECTOR3, AttrType.VECTOR4,
             AttrType.QANGLE, AttrType.QUATERNION}


def format_value(kind: int, value: Any) -> str:
    """A value as the inspector shows it."""
    if value is None:
        return ""
    if isinstance(value, Element):
        return f"→ {value.type} {value.name!r}"
    if isinstance(value, uuid.UUID):
        return f"→ external {value}"
    if kind == AttrType.BOOL:
        return "1" if value else "0"
    if kind == AttrType.TIME:
        return f"{value.seconds:g}" if isinstance(value, Time) else str(value)
    if kind == AttrType.FLOAT:
        return f"{value:g}"
    if kind == AttrType.BINARY:
        return f"{len(value)} bytes"
    if isinstance(value, (tuple, list)):
        return " ".join(f"{v:g}" if isinstance(v, float) else str(v) for v in value)
    return str(value)


def parse_value(kind: int, text: str) -> Any:
    """The text back into a value of the attribute's type; raises ValueError."""
    text = text.strip()
    if kind == AttrType.INT:
        return int(float(text))
    if kind == AttrType.FLOAT:
        return float(text)
    if kind == AttrType.BOOL:
        return text.lower() in ("1", "true", "yes", "on")
    if kind == AttrType.STRING:
        return text
    if kind == AttrType.TIME:
        return Time.from_seconds(float(text))
    if kind == AttrType.COLOR:
        parts = [int(float(p)) for p in text.replace(",", " ").split()]
        if len(parts) != 4:
            raise ValueError("a colour needs four numbers")
        return tuple(max(0, min(255, p)) for p in parts)
    counts = {AttrType.VECTOR2: 2, AttrType.VECTOR3: 3, AttrType.VECTOR4: 4,
              AttrType.QANGLE: 3, AttrType.QUATERNION: 4}
    if kind in counts:
        parts = [float(p) for p in text.replace(",", " ").split()]
        if len(parts) != counts[kind]:
            raise ValueError(f"{type_name(kind)} needs {counts[kind]} numbers")
        return tuple(parts)
    raise ValueError(f"{type_name(kind)} cannot be edited as text")


class Inspector(QTreeWidget):
    #: element, attribute name, array index (-1 for a scalar), new value
    """Attributes of one element, editable in place."""
    edited = Signal(object, str, int, object)
    #: an element reference was activated
    navigate = Signal(object)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setHeaderLabels(["Attribute", "Value", "Type"])
        self.setColumnWidth(0, 170)
        self.setColumnWidth(1, 220)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        self.itemChanged.connect(self._changed)
        self.itemDoubleClicked.connect(self._double_clicked)
        self._element: Optional[Element] = None
        self._filling = False

    @property
    def element(self) -> Optional[Element]:
        """The element shown, or None."""
        return self._element

    def set_element(self, element: Optional[Element]) -> None:
        """Show this element's attributes."""
        self._filling = True
        self.clear()
        self._element = element
        if element is not None:
            head = QTreeWidgetItem(self, ["element", f"{element.type} {element.name!r}", str(element.id)])
            head.setFlags(head.flags() & ~Qt.ItemIsEditable)
            name_item = QTreeWidgetItem(self, ["name", element.name, "string"])
            name_item.setData(0, ROLE_ATTR, "name")
            name_item.setData(0, ROLE_INDEX, -2)
            name_item.setFlags(name_item.flags() | Qt.ItemIsEditable)
            for attr in element:
                self._add_attribute(attr)
        self._filling = False

    def refresh(self) -> None:
        """Re-read every value; keeps the expansion state."""
        element = self._element
        if element is None:
            return
        expanded = {self.topLevelItem(i).text(0) for i in range(self.topLevelItemCount())
                    if self.topLevelItem(i).isExpanded()}
        self.set_element(element)
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            if item.text(0) in expanded:
                item.setExpanded(True)

    def _add_attribute(self, attr) -> None:
        if is_array(attr.type):
            base = attr.type - ARRAY_OFFSET
            item = QTreeWidgetItem(self, [attr.name, f"[{len(attr.value)}]", attr.type_name])
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            limit = 200
            for i, value in enumerate(attr.value[:limit]):
                child = QTreeWidgetItem(item, [str(i), format_value(base, value), type_name(base)])
                self._decorate(child, attr.name, i, base, value)
            if len(attr.value) > limit:
                QTreeWidgetItem(item, ["…", f"{len(attr.value) - limit} more", ""])
            return
        item = QTreeWidgetItem(self, [attr.name, format_value(attr.type, attr.value), attr.type_name])
        self._decorate(item, attr.name, -1, attr.type, attr.value)

    @staticmethod
    def _decorate(item: QTreeWidgetItem, name: str, index: int, kind: int, value: Any) -> None:
        item.setData(0, ROLE_ATTR, name)
        item.setData(0, ROLE_INDEX, index)
        if isinstance(value, Element):
            item.setData(0, ROLE_ELEMENT, value)
            item.setForeground(1, Qt.blue)
        if kind in _EDITABLE and not isinstance(value, Element):
            item.setFlags(item.flags() | Qt.ItemIsEditable)
        else:
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    def _changed(self, item: QTreeWidgetItem, column: int) -> None:
        if self._filling or column != 1 or self._element is None:
            return
        name = item.data(0, ROLE_ATTR)
        index = item.data(0, ROLE_INDEX)
        if name is None:
            return
        if index == -2:
            self.edited.emit(self._element, "name", -1, item.text(1))
            return
        attr = self._element.attribute(name)
        if attr is None:
            return
        kind = attr.type - ARRAY_OFFSET if is_array(attr.type) else attr.type
        try:
            value = parse_value(kind, item.text(1))
        except ValueError:
            self._filling = True
            current = attr.value[index] if index >= 0 else attr.value
            item.setText(1, format_value(kind, current))
            self._filling = False
            return
        self.edited.emit(self._element, name, index, value)

    def _double_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        target = item.data(0, ROLE_ELEMENT)
        if isinstance(target, Element):
            self.navigate.emit(target)
