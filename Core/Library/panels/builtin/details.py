"""
Details panel (UE5 "Details" look) - maps to SFM's Element Viewer / attribute editor.

Shows the properties of the current selection (ContextManager.selection).  Stage 1
renders a generic Transform + Info set; Stage 3 pulls real DmElement attributes.
"""
from __future__ import annotations

from typing import Any, Dict, List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDoubleSpinBox, QFormLayout, QFrame, QHBoxLayout, QLabel, QLineEdit, QScrollArea, QSizePolicy, QToolButton,
    QVBoxLayout, QWidget,
)

from ...icons import icon as make_icon
from ...localization import tr
from ...ui.widgets import SearchField
from ..base import C2UIPanel, PanelMeta


class Section(QWidget):
    """Collapsible property group like Unreal's category headers."""

    def __init__(self, title: str, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("detailsSection")
        vl = QVBoxLayout(self)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.setSpacing(0)
        self.header = QToolButton(self)
        self.header.setObjectName("detailsSectionHeader")
        self.header.setText(title)
        self.header.setCheckable(True)
        self.header.setChecked(True)
        self.header.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.header.setArrowType(Qt.ArrowType.DownArrow)
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.header.toggled.connect(self._toggle)
        vl.addWidget(self.header)
        self.body = QWidget(self)
        self.body.setObjectName("detailsSectionBody")
        self.form = QFormLayout(self.body)
        self.form.setContentsMargins(12, 4, 8, 6)
        self.form.setHorizontalSpacing(12)
        self.form.setVerticalSpacing(4)
        self.form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        vl.addWidget(self.body)

    def _toggle(self, on: bool) -> None:
        self.body.setVisible(on)
        self.header.setArrowType(Qt.ArrowType.DownArrow if on else Qt.ArrowType.RightArrow)

    def add_row(self, label: str, widget: QWidget) -> None:
        self.form.addRow(label, widget)


def _vec3(parent: QWidget, values=(0.0, 0.0, 0.0), suffix: str = "") -> QWidget:
    w = QWidget(parent)
    hl = QHBoxLayout(w)
    hl.setContentsMargins(0, 0, 0, 0)
    hl.setSpacing(4)
    for axis, val, color in zip("XYZ", values, ("#d0413b", "#5aa83a", "#3b7dd8")):
        tag = QLabel(axis, w)
        tag.setObjectName("axisTag")
        tag.setStyleSheet(f"color:{color}; font-weight:bold;")
        sb = QDoubleSpinBox(w)
        sb.setRange(-1e6, 1e6)
        sb.setDecimals(3)
        sb.setValue(val)
        sb.setSuffix(suffix)
        sb.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        sb.setMinimumWidth(36)                      # keep narrow docks usable
        hl.addWidget(tag)
        hl.addWidget(sb, 1)
    return w


class DetailsPanel(C2UIPanel):
    META = PanelMeta(id="details", title_key="panel.details", icon="details", category="Editor",
                     default_area="right", sfm_lookup="Element Viewer")

    def build(self) -> None:
        top = QWidget(self)
        top.setObjectName("panelToolbar")
        hl = QHBoxLayout(top)
        hl.setContentsMargins(6, 4, 6, 4)
        hl.setSpacing(6)
        self.icon = QLabel(top)
        self.icon.setFixedSize(16, 16)
        self.icon.setScaledContents(True)
        hl.addWidget(self.icon)
        self.name = QLineEdit(top)
        self.name.setObjectName("detailsName")
        self.name.setReadOnly(True)
        hl.addWidget(self.name, 1)
        self.type_label = QLabel(top)
        self.type_label.setObjectName("detailsType")
        hl.addWidget(self.type_label)
        self.root_layout.addWidget(top)

        self.search = SearchField(self)
        self.search.setPlaceholderText(tr("details.search"))
        self.search.setClearButtonEnabled(True)
        wrap = QWidget(self)
        wl = QHBoxLayout(wrap)
        wl.setContentsMargins(6, 0, 6, 4)
        wl.addWidget(self.search)
        self.root_layout.addWidget(wrap)

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.content = QWidget(self.scroll)
        self.content.setObjectName("detailsContent")
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(1)
        self.content_layout.addStretch(1)
        self.scroll.setWidget(self.content)
        self.root_layout.addWidget(self.scroll, 1)

        self.empty = QLabel(tr("details.nothing_selected"), self.content)
        self.empty.setObjectName("detailsEmpty")
        self.empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.insertWidget(0, self.empty)

        self._sections: List[Section] = []
        self.app.context.selection_changed.connect(self._on_selection)

    def _clear(self) -> None:
        for s in self._sections:
            self.content_layout.removeWidget(s)
            s.deleteLater()
        self._sections.clear()

    def _add_section(self, title: str) -> Section:
        s = Section(title, self.content)
        self.content_layout.insertWidget(self.content_layout.count() - 1, s)
        s.show()
        self._sections.append(s)
        return s

    def _on_selection(self, items: List[Dict[str, Any]], source: str) -> None:
        self._clear()
        if not items:
            self.empty.show()
            self.name.setText("")
            self.type_label.setText("")
            self.icon.clear()
            return
        self.empty.hide()
        first = items[0]
        name = first.get("name", "?")
        if len(items) > 1:
            name = tr("details.multiple", n=len(items))
        self.name.setText(name)
        self.type_label.setText(tr(f"type.{first.get('type', 'element')}"))
        self.icon.setPixmap(make_icon(first.get("icon", "model")).pixmap(16, 16))

        tf = self._add_section(tr("details.transform"))
        tf.add_row(tr("details.location"), _vec3(tf.body))
        tf.add_row(tr("details.rotation"), _vec3(tf.body, suffix="°"))
        tf.add_row(tr("details.scale"), _vec3(tf.body, (1.0, 1.0, 1.0)))

        info = self._add_section(tr("details.info"))
        for key in ("name", "type"):
            le = QLineEdit(str(first.get(key, "")), info.body)
            le.setReadOnly(True)
            info.add_row(tr(f"details.{key}"), le)
        src = QLineEdit(source or "-", info.body)
        src.setReadOnly(True)
        info.add_row(tr("details.source"), src)

    def on_language_changed(self, code: str) -> None:
        super().on_language_changed(code)
        self.search.setPlaceholderText(tr("details.search"))
        self.empty.setText(tr("details.nothing_selected"))
        self._on_selection(self.app.context.selection, self.app.context.selection_source)
