"""
Output Log panel (UE5 look) - shows C2UI logs now, SFM console output via the
bridge in Stage 3.  The command line sends Python/console commands to SFM.
"""
from __future__ import annotations

import logging
from typing import Any, Dict

from PySide6.QtGui import QColor, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLineEdit, QPlainTextEdit, QToolButton, QWidget

from ...icons import icon as make_icon
from ...localization import tr
from ...logging_setup import get_sink
from ...ui.widgets import SearchField
from ..base import C2UIPanel, PanelMeta

log = logging.getLogger("c2ui.console")

_LEVEL_ORDER = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}


class OutputLogPanel(C2UIPanel):
    META = PanelMeta(id="output_log", title_key="panel.output_log", icon="log", category="Editor",
                     default_area="bottom", min_size=(300, 120), sfm_lookup="Console")

    def build(self) -> None:
        self._min_level = 10
        self._colors = {"DEBUG": QColor("#7c8590"), "INFO": QColor("#c9d1d9"), "WARNING": QColor("#e3b341"),
                        "ERROR": QColor("#f85149"), "CRITICAL": QColor("#ff7b72"), "CMD": QColor("#58a6ff")}

        bar = QWidget(self)
        bar.setObjectName("panelToolbar")
        hl = QHBoxLayout(bar)
        hl.setContentsMargins(6, 4, 6, 4)
        hl.setSpacing(4)
        self.level = QComboBox(bar)
        self.level.addItems([tr("log.all"), tr("log.info"), tr("log.warnings"), tr("log.errors")])
        self.level.currentIndexChanged.connect(self._on_level)
        hl.addWidget(self.level)
        self.search = SearchField(bar)
        self.search.setPlaceholderText(tr("common.search"))
        self.search.setClearButtonEnabled(True)
        self.search.textChanged.connect(lambda _t: self._rebuild())
        hl.addWidget(self.search, 1)
        self.btn_clear = QToolButton(bar)
        self.btn_clear.setAutoRaise(True)
        self.btn_clear.setIcon(make_icon("clear"))
        self.btn_clear.setToolTip(tr("log.clear"))
        self.btn_clear.clicked.connect(self._clear)
        hl.addWidget(self.btn_clear)
        self.root_layout.addWidget(bar)

        self.view = QPlainTextEdit(self)
        self.view.setObjectName("outputLog")
        self.view.setReadOnly(True)
        self.view.setMaximumBlockCount(5000)
        self.view.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.root_layout.addWidget(self.view, 1)

        cmd_row = QWidget(self)
        cmd_row.setObjectName("consoleRow")
        cl = QHBoxLayout(cmd_row)
        cl.setContentsMargins(6, 3, 6, 4)
        cl.setSpacing(4)
        self.prompt = QLineEdit(cmd_row)
        self.prompt.setObjectName("consoleInput")
        self.prompt.setPlaceholderText(tr("log.prompt"))
        self.prompt.returnPressed.connect(self._submit)
        cl.addWidget(self.prompt, 1)
        self.root_layout.addWidget(cmd_row)

        self._cleared_marker = 0        # sink.total at the moment of the last "clear"
        sink = get_sink()
        for level, name, msg in list(sink.backlog):
            self._append(level, name, msg)
        sink.record_emitted.connect(self._append)

    # -- log handling -------------------------------------------------------------
    def _append(self, level: str, name: str, msg: str) -> None:
        if _LEVEL_ORDER.get(level, 20) < self._min_level:
            return
        needle = self.search.text().strip().lower()
        if needle and needle not in msg.lower():
            return
        fmt = QTextCharFormat()
        fmt.setForeground(self._colors.get(level, self._colors["INFO"]))
        cursor = self.view.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(msg + "\n", fmt)
        self.view.setTextCursor(cursor)
        self.view.ensureCursorVisible()

    def _rebuild(self) -> None:
        self.view.clear()
        sink = get_sink()
        # backlog is a bounded deque: convert the absolute marker into a live offset
        skip = max(0, self._cleared_marker - (sink.total - len(sink.backlog)))
        for level, name, msg in list(sink.backlog)[skip:]:
            self._append(level, name, msg)

    def _on_level(self, index: int) -> None:
        self._min_level = (10, 20, 30, 40)[max(0, min(index, 3))]
        self._rebuild()

    def _clear(self) -> None:
        self._cleared_marker = get_sink().total
        self.view.clear()

    def _submit(self) -> None:
        text = self.prompt.text().strip()
        if not text:
            return
        self.prompt.clear()
        self._append("CMD", "console", f"> {text}")
        if not self.app.bridge.connected:
            self._append("WARNING", "console", tr("status.sfm_offline_action"))
            return
        self.app.bridge.call("sfm.exec", {"code": text}, self._on_exec_result)

    def _on_exec_result(self, result: Any, error: Any) -> None:
        if error:
            self._append("ERROR", "sfm", str(error.get("message", error)))
        elif result not in (None, ""):
            self._append("INFO", "sfm", str(result))

    # -- hooks ------------------------------------------------------------------
    def on_theme_changed(self, theme: Any) -> None:
        tok = theme.tokens
        self._colors["INFO"] = QColor(str(tok.get("text", "#c9d1d9")))
        self._colors["DEBUG"] = QColor(str(tok.get("text.dim", "#7c8590")))
        self._colors["WARNING"] = QColor(str(tok.get("warning", "#e3b341")))
        self._colors["ERROR"] = QColor(str(tok.get("error", "#f85149")))
        self._colors["CMD"] = QColor(str(tok.get("accent", "#58a6ff")))
        self.btn_clear.setIcon(make_icon("clear"))
        self._rebuild()

    def on_language_changed(self, code: str) -> None:
        super().on_language_changed(code)
        idx = self.level.currentIndex()
        self.level.blockSignals(True)
        self.level.clear()
        self.level.addItems([tr("log.all"), tr("log.info"), tr("log.warnings"), tr("log.errors")])
        self.level.setCurrentIndex(idx)
        self.level.blockSignals(False)
        self.search.setPlaceholderText(tr("common.search"))
        self.prompt.setPlaceholderText(tr("log.prompt"))
        self.btn_clear.setToolTip(tr("log.clear"))

    def save_state(self) -> Dict[str, Any]:
        return {"level": self.level.currentIndex()}

    def restore_state(self, state: Dict[str, Any]) -> None:
        self.level.setCurrentIndex(int(state.get("level", 0)))
