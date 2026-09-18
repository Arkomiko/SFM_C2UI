"""
Preferences dialog.

The most important page is **Source Filmmaker**: C2UI is a standalone shell, so the
user has to tell it where SFM lives before any SFM-backed feature can work.  The
path field validates live and shows exactly why a folder is not accepted.
"""
from __future__ import annotations

import logging
from typing import Any, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QFileDialog, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton, QSpinBox, QStackedWidget, QVBoxLayout, QWidget,
)

from Core.Library import paths

from ..icons import icon as make_icon
from ..localization import tr

log = logging.getLogger("c2ui.prefs")


class PreferencesDialog(QDialog):
    def __init__(self, app: Any, parent: Optional[QWidget] = None, page: str = "sfm") -> None:
        super().__init__(parent)
        self.app = app
        self.setObjectName("preferencesDialog")
        self.setWindowTitle(tr("prefs.title"))
        self.setMinimumSize(680, 440)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        self.nav = QListWidget(self)
        self.nav.setObjectName("prefsNav")
        self.nav.setFixedWidth(170)
        self.pages = QStackedWidget(self)
        self.pages.setObjectName("prefsPages")

        self._add_page("sfm", tr("prefs.page.sfm"), "launch", self._build_sfm_page())
        self._add_page("appearance", tr("prefs.page.appearance"), "theme", self._build_appearance_page())
        self._add_page("advanced", tr("prefs.page.advanced"), "settings", self._build_advanced_page())

        self.nav.currentRowChanged.connect(self.pages.setCurrentIndex)
        body.addWidget(self.nav)
        body.addWidget(self.pages, 1)
        root.addLayout(body, 1)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close, self)
        buttons.rejected.connect(self.accept)
        buttons.accepted.connect(self.accept)
        wrap = QWidget(self)
        wrap.setObjectName("prefsFooter")
        wl = QHBoxLayout(wrap)
        wl.setContentsMargins(12, 8, 12, 10)
        wl.addStretch(1)
        wl.addWidget(buttons)
        root.addWidget(wrap)

        self.select_page(page)
        self._refresh_sfm_status()

    # ------------------------------------------------------------------ pages
    def _add_page(self, key: str, title: str, icon: str, widget: QWidget) -> None:
        item = QListWidgetItem(make_icon(icon), title)
        item.setData(Qt.ItemDataRole.UserRole, key)
        self.nav.addItem(item)
        self.pages.addWidget(widget)

    def select_page(self, key: str) -> None:
        for i in range(self.nav.count()):
            if self.nav.item(i).data(Qt.ItemDataRole.UserRole) == key:
                self.nav.setCurrentRow(i)
                return
        self.nav.setCurrentRow(0)

    def _page(self, title: str) -> tuple[QWidget, QFormLayout]:
        page = QWidget(self)
        page.setObjectName("prefsPage")
        vl = QVBoxLayout(page)
        vl.setContentsMargins(18, 16, 18, 16)
        vl.setSpacing(10)
        heading = QLabel(title, page)
        heading.setObjectName("prefsHeading")
        vl.addWidget(heading)
        form = QFormLayout()
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(8)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        vl.addLayout(form)
        vl.addStretch(1)
        return page, form

    # ------------------------------------------------------------ SFM page
    def _build_sfm_page(self) -> QWidget:
        page, form = self._page(tr("prefs.page.sfm"))
        s = self.app.settings

        row = QWidget(page)
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(6)
        self.sfm_path = QLineEdit(str(s.get("sfm.root", "") or ""), row)
        self.sfm_path.setMinimumWidth(320)
        self.sfm_path.setPlaceholderText(tr("prefs.sfm.placeholder"))
        self.sfm_path.editingFinished.connect(self._apply_sfm_path)
        rl.addWidget(self.sfm_path, 1)
        browse = QPushButton(tr("prefs.browse"), row)
        browse.setIcon(make_icon("folder_open"))
        browse.clicked.connect(self._browse_sfm)
        rl.addWidget(browse)
        detect = QPushButton(tr("prefs.sfm.detect"), row)
        detect.setIcon(make_icon("search"))
        detect.clicked.connect(self._detect_sfm)
        rl.addWidget(detect)
        form.addRow(tr("prefs.sfm.path"), row)

        self.sfm_status = QLabel(page)
        self.sfm_status.setObjectName("prefsStatus")
        self.sfm_status.setWordWrap(True)
        form.addRow(self.sfm_status)          # single-widget row spans both columns

        self.sfm_hint = QLabel(tr("prefs.sfm.hint"), page)
        self.sfm_hint.setObjectName("prefsHint")
        self.sfm_hint.setWordWrap(True)
        form.addRow(self.sfm_hint)

        self.cb_auto_launch = self._checkbox(form, "sfm.auto_launch", tr("prefs.sfm.auto_launch"))
        self.cb_auto_connect = self._checkbox(form, "sfm.auto_connect", tr("prefs.sfm.auto_connect"))
        self.cb_auto_agent = self._checkbox(form, "sfm.auto_install_agent", tr("prefs.sfm.auto_install_agent"))
        self.cb_embed = self._checkbox(form, "sfm.embed_viewport_on_connect", tr("prefs.sfm.embed"))
        self.cb_sync_theme = self._checkbox(form, "sfm.sync_theme", tr("prefs.sfm.sync_theme"))
        self.cb_dismiss = self._checkbox(form, "sfm.auto_dismiss_startup_dialogs", tr("prefs.sfm.dismiss_dialogs"))

        port = QSpinBox(page)
        port.setRange(1024, 65535)
        port.setValue(int(s.get("sfm.agent_port", 41794)))
        port.valueChanged.connect(lambda v: s.set("sfm.agent_port", int(v)))
        form.addRow(tr("prefs.sfm.port"), port)

        args = QLineEdit(" ".join(s.get("sfm.launch_args", []) or []), page)
        args.setPlaceholderText("-w 1280 -h 720")
        args.editingFinished.connect(lambda: s.set("sfm.launch_args", args.text().split()))
        form.addRow(tr("prefs.sfm.launch_args"), args)
        return page

    def _checkbox(self, form: QFormLayout, key: str, label: str) -> QCheckBox:
        s = self.app.settings
        cb = QCheckBox(label)
        cb.setChecked(bool(s.get(key, False)))
        cb.toggled.connect(lambda v, k=key: s.set(k, bool(v)))
        form.addRow(cb)
        return cb

    # ------------------------------------------------------ appearance page
    def _build_appearance_page(self) -> QWidget:
        page, form = self._page(tr("prefs.page.appearance"))
        s = self.app.settings

        theme = QComboBox(page)
        for t in sorted(self.app.theme.available(), key=lambda x: x.name):
            theme.addItem(t.name, t.id)
        current = self.app.theme.current
        if current:
            idx = theme.findData(current.id)
            if idx >= 0:
                theme.setCurrentIndex(idx)
        theme.currentIndexChanged.connect(lambda: self.app.switch_theme(theme.currentData()))
        form.addRow(tr("prefs.appearance.theme"), theme)

        lang = QComboBox(page)
        for loc in self.app.locale.available():
            lang.addItem(f"{loc['native_name']} ({loc['code']})", loc["code"])
        idx = lang.findData(self.app.locale.language)
        if idx >= 0:
            lang.setCurrentIndex(idx)
        lang.currentIndexChanged.connect(lambda: self.app.switch_language(lang.currentData()))
        form.addRow(tr("prefs.appearance.language"), lang)

        ws = QComboBox(page)
        for w in self.app.workspace.all():
            ws.addItem(w.display_name(), w.id)
        cur_ws = self.app.workspace.current
        if cur_ws:
            idx = ws.findData(cur_ws.id)
            if idx >= 0:
                ws.setCurrentIndex(idx)
        ws.currentIndexChanged.connect(lambda: self.app.switch_workspace(ws.currentData()))
        form.addRow(tr("prefs.appearance.workspace"), ws)

        scale = QDoubleSpinBox(page)
        scale.setRange(0.75, 2.0)
        scale.setSingleStep(0.05)
        scale.setDecimals(2)
        scale.setValue(float(s.get("ui.font_scale", 1.0)))
        scale.valueChanged.connect(self._apply_font_scale)
        form.addRow(tr("prefs.appearance.font_scale"), scale)

        self._checkbox(form, "ui.restore_last_layout", tr("prefs.appearance.restore_layout"))
        self._checkbox(form, "dev.hot_reload_themes", tr("prefs.appearance.hot_reload"))
        return page

    def _apply_font_scale(self, value: float) -> None:
        self.app.settings.set("ui.font_scale", float(value))
        self.app.theme.set_font_scale(float(value))

    # -------------------------------------------------------- advanced page
    def _build_advanced_page(self) -> QWidget:
        page, form = self._page(tr("prefs.page.advanced"))
        s = self.app.settings

        level = QComboBox(page)
        level.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        level.setCurrentText(str(s.get("dev.log_level", "INFO")))
        level.currentTextChanged.connect(lambda v: s.set("dev.log_level", v))
        form.addRow(tr("prefs.advanced.log_level"), level)

        for label, value in ((tr("prefs.advanced.user_dir"), paths.USER_DIR),
                             (tr("prefs.advanced.sdk_dir"), paths.SDK_ROOT)):
            field = QLineEdit(str(value), page)
            field.setReadOnly(True)
            form.addRow(label, field)

        open_dir = QPushButton(tr("prefs.advanced.open_user_dir"), page)
        open_dir.setIcon(make_icon("folder_open"))
        open_dir.clicked.connect(self._open_user_dir)
        form.addRow(open_dir)
        return page

    def _open_user_dir(self) -> None:
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices
        paths.ensure_user_dirs()
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(paths.USER_DIR)))

    # --------------------------------------------------------------- SFM path
    def _browse_sfm(self) -> None:
        start = self.sfm_path.text() or str(paths.SDK_ROOT)
        chosen = QFileDialog.getExistingDirectory(self, tr("prefs.sfm.choose"), start)
        if chosen:
            self.sfm_path.setText(chosen)
            self._apply_sfm_path()

    def _detect_sfm(self) -> None:
        found = paths.detect_sfm_root(force=True)
        if found is None:
            self.sfm_status.setText(tr("prefs.sfm.not_detected"))
            self.sfm_status.setProperty("state", "bad")
        else:
            self.sfm_path.setText(str(found))
            self._apply_sfm_path()
            return
        self._restyle(self.sfm_status)

    def _apply_sfm_path(self) -> None:
        text = self.sfm_path.text().strip()
        ok, result = self.app.sfm.set_path(text)
        if ok and text:
            self.sfm_path.setText(result)      # normalised (accepts sfm.exe or game/)
        elif not ok:
            self.sfm_status.setText(tr("prefs.sfm.invalid", reason=result))
            self.sfm_status.setProperty("state", "bad")
            self._restyle(self.sfm_status)
            return
        self._refresh_sfm_status()

    def _refresh_sfm_status(self) -> None:
        if self.app.sfm.available:
            self.sfm_status.setText(tr("prefs.sfm.ok", path=str(self.app.sfm.root)))
            self.sfm_status.setProperty("state", "good")
        else:
            self.sfm_status.setText(tr("prefs.sfm.missing"))
            self.sfm_status.setProperty("state", "bad")
        self._restyle(self.sfm_status)

    @staticmethod
    def _restyle(w: QWidget) -> None:
        w.style().unpolish(w)
        w.style().polish(w)
