"""
Viewport panel (central area, UE5 "Level Viewport" look).

Stage 1: a painted placeholder with a UE5-style overlay toolbar.
Stage 2: the native SFM "Primary Viewport" HWND is embedded here through
QWindow.fromWinId() / the native module (see Core/API).
"""
from __future__ import annotations

import logging
from typing import Any, Optional

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPen, QWindow
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QStackedWidget, QToolButton, QWidget

from Core.API import native

from ...icons import icon as make_icon
from ...localization import tr
from ..base import C2UIPanel, PanelMeta

log = logging.getLogger("c2ui.viewport")


class ViewportCanvas(QWidget):
    def __init__(self, panel: "ViewportPanel") -> None:
        super().__init__(panel)
        self.panel = panel
        self.setObjectName("viewportCanvas")
        self.setMinimumSize(320, 200)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.connected = False
        self.hint_key = "viewport.offline_hint"
        self.bg_top = QColor("#1e2126")
        self.bg_bottom = QColor("#0f1114")
        self.grid = QColor("#2b3038")
        self.grid_major = QColor("#3a404a")
        self.text = QColor("#8a9099")
        self.accent = QColor("#3b9eff")

    def apply_theme(self, theme: Any) -> None:
        tok = theme.tokens
        self.bg_top = QColor(str(tok.get("viewport.bg_top", "#1e2126")))
        self.bg_bottom = QColor(str(tok.get("viewport.bg_bottom", "#0f1114")))
        self.grid = QColor(str(tok.get("viewport.grid", "#2b3038")))
        self.grid_major = QColor(str(tok.get("viewport.grid_major", "#3a404a")))
        self.text = QColor(str(tok.get("text.dim", "#8a9099")))
        self.accent = QColor(str(tok.get("accent", "#3b9eff")))
        self.update()

    def paintEvent(self, _event) -> None:  # noqa: N802
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0.0, self.bg_top)
        grad.setColorAt(1.0, self.bg_bottom)
        p.fillRect(self.rect(), grad)

        # pseudo-perspective floor grid
        horizon = h * 0.42
        cx = w / 2.0
        p.setPen(QPen(self.grid, 1))
        for i in range(-24, 25):
            x_far = cx + i * 22
            x_near = cx + i * 140
            pen = QPen(self.grid_major if i % 4 == 0 else self.grid, 1)
            p.setPen(pen)
            p.drawLine(QPointF(x_far, horizon), QPointF(x_near, h))
        rows = 18
        for r in range(1, rows + 1):
            t = (r / rows) ** 2.2
            y = horizon + (h - horizon) * t
            p.setPen(QPen(self.grid_major if r % 4 == 0 else self.grid, 1))
            p.drawLine(QPointF(0, y), QPointF(w, y))
        p.setPen(QPen(self.grid_major, 1))
        p.drawLine(QPointF(0, horizon), QPointF(w, horizon))

        # centre cross / origin
        p.setPen(QPen(self.accent, 1.5))
        p.drawLine(QPointF(cx - 10, horizon + 40), QPointF(cx + 10, horizon + 40))
        p.drawLine(QPointF(cx, horizon + 30), QPointF(cx, horizon + 50))

        # text
        p.setPen(self.text)
        f = p.font()
        f.setPointSizeF(f.pointSizeF() + 1)
        p.setFont(f)
        key = "viewport.embedded_hint" if self.connected else self.hint_key
        p.drawText(QRectF(0, h * 0.55, w, 40), Qt.AlignmentFlag.AlignCenter, tr(key))
        f.setPointSizeF(f.pointSizeF() - 2)
        p.setFont(f)
        p.drawText(QRectF(12, 8, w - 24, 20), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, tr("viewport.camera_label"))
        p.drawText(QRectF(12, h - 26, w - 24, 20), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                   "SFM  -  " + tr("viewport.stats", fps=24, res="1280x720"))
        p.end()


class ViewportPanel(C2UIPanel):
    META = PanelMeta(
        id="viewport", title_key="panel.viewport", icon="viewport", category="Editor",
        default_area="left", closable=False, min_size=(320, 240), sfm_lookup="Primary Viewport",
    )

    def build(self) -> None:
        header = QWidget(self)
        header.setObjectName("viewportHeader")
        header.setFixedHeight(28)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(6, 2, 6, 2)
        hl.setSpacing(4)

        def btn(icon_name: str, text_key: str, menu: bool = True) -> QToolButton:
            b = QToolButton(header)
            b.setObjectName("viewportToolButton")
            b.setAutoRaise(True)
            b.setProperty("icon_name", icon_name)
            b.setIcon(make_icon(icon_name))
            b.setText(tr(text_key))
            b.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
            if menu:
                b.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
            hl.addWidget(b)
            return b

        self.btn_menu = btn("menu", "viewport.menu", menu=False)
        self.btn_menu.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.btn_persp = btn("camera", "viewport.perspective")
        self.btn_lit = btn("lit", "viewport.lit")
        self.btn_show = btn("eye", "viewport.show")
        hl.addStretch(1)
        self.lbl_speed = QLabel(tr("viewport.camera_speed", speed=4), header)
        self.lbl_speed.setObjectName("viewportInfoLabel")
        hl.addWidget(self.lbl_speed)
        self.btn_max = btn("maximize", "viewport.maximize", menu=False)
        self.btn_max.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.root_layout.addWidget(header)

        self.stack = QStackedWidget(self)
        self.stack.setObjectName("viewportStack")
        self.canvas = ViewportCanvas(self)
        self.stack.addWidget(self.canvas)
        self.root_layout.addWidget(self.stack, 1)

        self._foreign: Optional[QWindow] = None
        self._container: Optional[QWidget] = None
        self._hwnd = 0
        # The foreign window belongs to another process which may move/resize it on its
        # own (e.g. after a style change); this guard snaps it back to the container.
        self._guard = QTimer(self)
        self._guard.setInterval(700)
        self._guard.timeout.connect(self._guard_geometry)
        session = getattr(self.app, "sfm", None)
        if session is not None:
            session.viewport_ready.connect(self.embed_hwnd)
            session.viewport_released.connect(self.release)
            session.availability_changed.connect(self._on_sfm_availability)
            self._on_sfm_availability(session.available)

    def _on_sfm_availability(self, available: bool) -> None:
        self.canvas.hint_key = "viewport.offline_hint" if available else "viewport.no_sfm_hint"
        self.canvas.update()

    # -- native viewport embedding ----------------------------------------------------
    @property
    def embedded(self) -> bool:
        return self._container is not None

    def embed_hwnd(self, hwnd: int) -> None:
        """Wrap a foreign HWND (the detached SFM viewport) into this panel."""
        self.release()
        if not hwnd or not native.is_window(hwnd):
            log.warning("embed_hwnd: invalid hwnd %r", hwnd)
            return
        try:
            self._foreign = QWindow.fromWinId(int(hwnd))
            self._container = QWidget.createWindowContainer(self._foreign, self.stack)
            self._container.setObjectName("viewportContainer")
            self._container.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            self._container.setMinimumSize(64, 64)
            self.stack.addWidget(self._container)
            self.stack.setCurrentWidget(self._container)
            self._hwnd = int(hwnd)
            self._guard.start()
            log.info("SFM viewport embedded (hwnd=%d)", hwnd)
            self.canvas.connected = True
        except Exception:  # noqa: BLE001
            log.exception("Failed to embed hwnd %r", hwnd)
            self.release()

    def release(self) -> None:
        """Detach the foreign window again (it becomes a top-level window of SFM)."""
        if self._container is None and self._foreign is None:
            return
        self._guard.stop()
        self._hwnd = 0
        hwnd = 0
        try:
            if self._foreign is not None:
                hwnd = int(self._foreign.winId())
        except (RuntimeError, ValueError, TypeError):
            hwnd = 0
        # Qt may already have destroyed these C++ objects (panel teardown, stack reset):
        # releasing must always finish so the SFM window is handed back.
        try:
            self.stack.setCurrentWidget(self.canvas)
            if self._container is not None:
                self.stack.removeWidget(self._container)
                self._container.setParent(None)
                self._container.deleteLater()
        except (RuntimeError, TypeError):
            log.debug("Viewport container was already destroyed", exc_info=True)
        if self._foreign is not None:
            try:
                self._foreign.setParent(None)
            except (RuntimeError, TypeError):
                pass
            self._foreign = None
        self._container = None
        if hwnd and native.is_window(hwnd):
            native.set_parent(hwnd, None)      # give the HWND back to its own process' desktop
        log.info("SFM viewport released")

    MIN_EMBED_SIZE = 32

    def _guard_geometry(self) -> None:
        if not self._hwnd or self._container is None:
            return
        if not native.is_window(self._hwnd):
            log.warning("Embedded SFM viewport window vanished")
            self.release()
            return
        try:
            self._sync_container_geometry()
        except (RuntimeError, TypeError):
            log.debug("Viewport container gone while syncing geometry", exc_info=True)
            self.release()

    def _sync_container_geometry(self) -> None:
        # Never resize while the container is hidden or collapsed: a 0x0 MoveWindow
        # would shrink SFM's own viewport window and it would not come back.
        if not self._container.isVisible():
            return
        w, h = self._container.width(), self._container.height()
        if w < self.MIN_EMBED_SIZE or h < self.MIN_EMBED_SIZE:
            return
        x, y, cw, ch = native.window_rect(self._hwnd)
        top_left = self._container.mapToGlobal(self._container.rect().topLeft())
        if (cw, ch) != (w, h) or abs(x - top_left.x()) > 1 or abs(y - top_left.y()) > 1:
            native.move_window(self._hwnd, 0, 0, w, h)

    def on_theme_changed(self, theme: Any) -> None:
        self.canvas.apply_theme(theme)
        for b in (self.btn_menu, self.btn_persp, self.btn_lit, self.btn_show, self.btn_max):
            b.setIcon(make_icon(b.property("icon_name")))

    def on_language_changed(self, code: str) -> None:
        super().on_language_changed(code)
        self.btn_persp.setText(tr("viewport.perspective"))
        self.btn_lit.setText(tr("viewport.lit"))
        self.btn_show.setText(tr("viewport.show"))
        self.lbl_speed.setText(tr("viewport.camera_speed", speed=4))
        self.canvas.update()

    def on_sfm_connected(self, connected: bool) -> None:
        self.canvas.connected = connected
        if not connected:
            self.release()
        self.canvas.update()
