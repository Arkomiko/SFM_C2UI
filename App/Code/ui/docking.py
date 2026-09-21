"""
Docking the way Unreal Engine 5 and Visual Studio do it.

Drag a panel by its title and it lifts off as a floating window that
follows the pointer. An overlay appears over the editor with a compass of
drop targets - dock to the left, right, top, bottom, or as a tab - both for
the whole window and, when the pointer is over another panel, for that
panel. Hovering a target shows a translucent preview of the space the
panel would take, animated into place; releasing there docks it.

Only the chrome is replaced: each panel keeps its widget, and Qt's own
save/restore of the layout keeps working.

    Docking(main_window)             # once; every QDockWidget gets the title bar
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from PySide6.QtCore import (Property, QEasingCurve, QEvent, QObject, QPoint, QPropertyAnimation,
                            QRect, Qt, Signal)
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QPen
from PySide6.QtWidgets import (QApplication, QDockWidget, QHBoxLayout, QLabel, QMainWindow,
                               QToolButton, QWidget)

__all__ = ["Docking", "DockTitleBar", "DockOverlay"]

# targets
LEFT, RIGHT, TOP, BOTTOM, CENTER = "left", "right", "top", "bottom", "center"
TARGETS = (LEFT, RIGHT, TOP, BOTTOM, CENTER)
AREAS = {LEFT: Qt.LeftDockWidgetArea, RIGHT: Qt.RightDockWidgetArea,
         TOP: Qt.TopDockWidgetArea, BOTTOM: Qt.BottomDockWidgetArea}

BUTTON = 36
GAP = 4
PREVIEW = QColor(102, 192, 244, 70)
PREVIEW_EDGE = QColor(102, 192, 244, 200)
PLATE = QColor(28, 33, 40, 235)
PLATE_HOT = QColor(102, 192, 244, 255)
ICON = QColor(210, 220, 230)
ICON_HOT = QColor(14, 20, 27)
TITLE_BG = QColor("#262b33")
TITLE_FG = QColor("#c9d1d9")


# ---------------------------------------------------------------------------
#  Title bar
# ---------------------------------------------------------------------------
class DockTitleBar(QWidget):
    """A dock's own title bar: the drag handle, float and close."""

    drag_started = Signal(QDockWidget, QPoint)
    drag_moved = Signal(QPoint)
    drag_finished = Signal(QPoint)
    drag_cancelled = Signal()

    def __init__(self, dock: QDockWidget) -> None:
        super().__init__(dock)
        self.dock = dock
        self.setFixedHeight(24)
        self.setCursor(Qt.OpenHandCursor)
        self._press: Optional[QPoint] = None
        self._dragging = False
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 2, 0)
        layout.setSpacing(2)
        self.label = QLabel(dock.windowTitle())
        self.label.setStyleSheet(f"color: {TITLE_FG.name()}; font-weight: 600;")
        layout.addWidget(self.label, 1)
        self.float_button = QToolButton()
        self.float_button.setText("▫")
        self.float_button.setToolTip("Float")
        self.float_button.setAutoRaise(True)
        self.float_button.setFixedSize(20, 20)
        self.float_button.clicked.connect(lambda: dock.setFloating(not dock.isFloating()))
        layout.addWidget(self.float_button)
        self.close_button = QToolButton()
        self.close_button.setText("✕")
        self.close_button.setToolTip("Close")
        self.close_button.setAutoRaise(True)
        self.close_button.setFixedSize(20, 20)
        self.close_button.clicked.connect(dock.close)
        layout.addWidget(self.close_button)
        dock.windowTitleChanged.connect(self.label.setText)
        self.setStyleSheet(f"DockTitleBar {{ background: {TITLE_BG.name()}; }} "
                           f"QToolButton {{ color: {TITLE_FG.name()}; border: none; }} "
                           f"QToolButton:hover {{ background: #3a4150; }}")

    def paintEvent(self, event) -> None:
        p = QPainter(self)
        p.fillRect(self.rect(), TITLE_BG)
        p.setPen(QPen(QColor(255, 255, 255, 18), 1))
        p.drawLine(0, self.height() - 1, self.width(), self.height() - 1)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._press = event.globalPosition().toPoint()
            self._dragging = False

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._press is None:
            return
        pos = event.globalPosition().toPoint()
        if not self._dragging:
            if (pos - self._press).manhattanLength() < QApplication.startDragDistance():
                return
            self._dragging = True
            self.setCursor(Qt.ClosedHandCursor)
            self.drag_started.emit(self.dock, pos)
        self.drag_moved.emit(pos)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self._dragging:
            self.drag_finished.emit(event.globalPosition().toPoint())
        self._dragging = False
        self._press = None
        self.setCursor(Qt.OpenHandCursor)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.dock.setFloating(not self.dock.isFloating())

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Escape and self._dragging:
            self._dragging = False
            self._press = None
            self.drag_cancelled.emit()
        else:
            super().keyPressEvent(event)


# ---------------------------------------------------------------------------
#  Overlay: compass, targets, preview
# ---------------------------------------------------------------------------
class DockOverlay(QWidget):
    """A transparent layer over the main window showing where a dock can go."""

    def __init__(self, main: QMainWindow) -> None:
        super().__init__(main)
        self.main = main
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.hide()
        #: (kind, target dock or None, name) -> rect in overlay coordinates
        self.buttons: Dict[Tuple[str, Optional[QDockWidget], str], QRect] = {}
        self.hot: Optional[Tuple[str, Optional[QDockWidget], str]] = None
        self.hover_dock: Optional[QDockWidget] = None
        self.dragged: Optional[QDockWidget] = None
        self._preview = QRect()
        self._preview_target = QRect()
        self._animation = QPropertyAnimation(self, b"preview", self)
        self._animation.setDuration(140)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)

    # the preview rectangle is animated through this property
    def _get_preview(self) -> QRect:
        return self._preview

    def _set_preview(self, rect: QRect) -> None:
        self._preview = rect
        self.update()

    preview = Property(QRect, _get_preview, _set_preview)

    def begin(self, dragged: QDockWidget) -> None:
        """Start showing drop targets for `dragged`."""
        self.dragged = dragged
        self.setGeometry(self.main.rect())
        self.hot = None
        self.hover_dock = None
        self._preview = QRect()
        self._preview_target = QRect()
        self._layout_buttons()
        self.show()
        self.raise_()

    def end(self) -> None:
        """Hide the overlay."""
        self._animation.stop()
        self.hide()
        self.dragged = None
        self.hot = None
        self.hover_dock = None
        self.buttons = {}

    # -- geometry ----------------------------------------------------------------------
    def _dock_rect(self, dock: QDockWidget) -> QRect:
        return QRect(dock.mapTo(self.main, QPoint(0, 0)), dock.size())

    def _compass(self, centre: QPoint, kind: str, target: Optional[QDockWidget], with_center: bool) -> None:
        step = BUTTON + GAP
        places = {LEFT: (-step, 0), RIGHT: (step, 0), TOP: (0, -step), BOTTOM: (0, step), CENTER: (0, 0)}
        for name, (dx, dy) in places.items():
            if name == CENTER and not with_center:
                continue
            rect = QRect(centre.x() + dx - BUTTON // 2, centre.y() + dy - BUTTON // 2, BUTTON, BUTTON)
            self.buttons[(kind, target, name)] = rect

    def _layout_buttons(self) -> None:
        self.buttons = {}
        area = self.rect()
        margin = BUTTON // 2 + 12
        # the window's edges
        self.buttons[("window", None, LEFT)] = QRect(margin - BUTTON // 2, area.center().y() - BUTTON // 2, BUTTON, BUTTON)
        self.buttons[("window", None, RIGHT)] = QRect(area.right() - margin - BUTTON // 2, area.center().y() - BUTTON // 2, BUTTON, BUTTON)
        self.buttons[("window", None, TOP)] = QRect(area.center().x() - BUTTON // 2, margin - BUTTON // 2, BUTTON, BUTTON)
        self.buttons[("window", None, BOTTOM)] = QRect(area.center().x() - BUTTON // 2, area.bottom() - margin - BUTTON // 2, BUTTON, BUTTON)
        if self.hover_dock is not None and self.hover_dock is not self.dragged:
            self._compass(self._dock_rect(self.hover_dock).center(), "dock", self.hover_dock, True)

    def set_hover_dock(self, dock: Optional[QDockWidget]) -> None:
        """Show the targets around this dock, or the window edges."""
        if dock is self.hover_dock:
            return
        self.hover_dock = dock
        self._layout_buttons()
        self.update()

    def hit(self, local: QPoint) -> Optional[Tuple[str, Optional[QDockWidget], str]]:
        """The drop target under `local`, or None."""
        for key, rect in self.buttons.items():
            if rect.contains(local):
                return key
        return None

    def preview_for(self, key: Optional[Tuple[str, Optional[QDockWidget], str]]) -> QRect:
        """Where the dragged dock would land for a target."""
        if key is None or self.dragged is None:
            return QRect()
        kind, target, name = key
        if kind == "window":
            area = self.rect()
            w = max(120, min(area.width() // 3, self.dragged.width() or 300))
            h = max(100, min(area.height() // 3, self.dragged.height() or 220))
            if name == LEFT:
                return QRect(area.left(), area.top(), w, area.height())
            if name == RIGHT:
                return QRect(area.right() - w, area.top(), w, area.height())
            if name == TOP:
                return QRect(area.left(), area.top(), area.width(), h)
            return QRect(area.left(), area.bottom() - h, area.width(), h)
        if target is None:
            return QRect()
        r = self._dock_rect(target)
        if name == CENTER:
            return r
        if name == LEFT:
            return QRect(r.left(), r.top(), r.width() // 2, r.height())
        if name == RIGHT:
            return QRect(r.center().x(), r.top(), r.width() - r.width() // 2, r.height())
        if name == TOP:
            return QRect(r.left(), r.top(), r.width(), r.height() // 2)
        return QRect(r.left(), r.center().y(), r.width(), r.height() - r.height() // 2)

    def set_hot(self, key) -> None:
        """Highlight one target."""
        if key == self.hot:
            return
        self.hot = key
        target = self.preview_for(key)
        if target.isNull():
            self._animation.stop()
            self._preview = QRect()
            self.update()
            return
        self._animation.stop()
        self._animation.setStartValue(self._preview if not self._preview.isNull() else target.adjusted(
            target.width() // 4, target.height() // 4, -target.width() // 4, -target.height() // 4))
        self._animation.setEndValue(target)
        self._animation.start()
        self._preview_target = target

    # -- painting ----------------------------------------------------------------------
    def paintEvent(self, event) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        if not self._preview.isNull():
            p.fillRect(self._preview, PREVIEW)
            p.setPen(QPen(PREVIEW_EDGE, 2))
            p.drawRect(self._preview.adjusted(1, 1, -1, -1))
        for key, rect in self.buttons.items():
            hot = key == self.hot
            self._paint_button(p, rect, key[2], hot)

    @staticmethod
    def _paint_button(p: QPainter, rect: QRect, name: str, hot: bool) -> None:
        p.setPen(QPen(PLATE_HOT if hot else QColor(90, 100, 115), 1))
        p.setBrush(PLATE_HOT if hot else PLATE)
        p.drawRoundedRect(rect, 5, 5)
        ink = ICON_HOT if hot else ICON
        p.setPen(QPen(ink, 1.5))
        inner = rect.adjusted(8, 8, -8, -8)
        p.setBrush(Qt.NoBrush)
        p.drawRect(inner)                          # the window
        p.setBrush(ink)
        if name == LEFT:
            p.drawRect(QRect(inner.left(), inner.top(), inner.width() // 2, inner.height()))
        elif name == RIGHT:
            p.drawRect(QRect(inner.center().x(), inner.top(), inner.width() - inner.width() // 2, inner.height()))
        elif name == TOP:
            p.drawRect(QRect(inner.left(), inner.top(), inner.width(), inner.height() // 2))
        elif name == BOTTOM:
            p.drawRect(QRect(inner.left(), inner.center().y(), inner.width(), inner.height() - inner.height() // 2))
        else:                                       # a tab
            p.drawRect(QRect(inner.left(), inner.top(), inner.width() // 2, 4))


# ---------------------------------------------------------------------------
#  The controller
# ---------------------------------------------------------------------------
class Docking(QObject):
    """Installs the title bars on a main window's docks and runs drags."""

    def __init__(self, main: QMainWindow) -> None:
        super().__init__(main)
        self.main = main
        self.overlay = DockOverlay(main)
        self.dragged: Optional[QDockWidget] = None
        self._grab_offset = QPoint()
        self._was_floating = False
        main.installEventFilter(self)
        app = QApplication.instance()
        if app is not None:
            app.installEventFilter(self)
        for dock in main.findChildren(QDockWidget):
            self.attach(dock)

    def attach(self, dock: QDockWidget) -> None:
        """Give a dock the custom title bar."""
        if isinstance(dock.titleBarWidget(), DockTitleBar):
            return
        bar = DockTitleBar(dock)
        dock.setTitleBarWidget(bar)
        bar.drag_started.connect(self._start)
        bar.drag_moved.connect(self._move)
        bar.drag_finished.connect(self._finish)
        bar.drag_cancelled.connect(self._cancel)

    def docks(self) -> List[QDockWidget]:
        """Every visible dock widget."""
        return [d for d in self.main.findChildren(QDockWidget) if d.isVisible()]

    # -- the drag ------------------------------------------------------------------------
    def _start(self, dock: QDockWidget, global_pos: QPoint) -> None:
        self.dragged = dock
        self._was_floating = dock.isFloating()
        if not dock.isFloating():
            size = dock.size()
            dock.setFloating(True)
            dock.resize(size)
        self._grab_offset = QPoint(min(dock.width() // 2, 120), 12)
        dock.move(global_pos - self._grab_offset)
        self.overlay.begin(dock)
        self._move(global_pos)

    def _move(self, global_pos: QPoint) -> None:
        dock = self.dragged
        if dock is None:
            return
        dock.move(global_pos - self._grab_offset)
        local = self.main.mapFromGlobal(global_pos)
        under = None
        for other in self.docks():
            if other is dock or other.isFloating():
                continue
            if QRect(other.mapTo(self.main, QPoint(0, 0)), other.size()).contains(local):
                under = other
                break
        self.overlay.set_hover_dock(under)
        self.overlay.set_hot(self.overlay.hit(local))

    def _finish(self, global_pos: QPoint) -> None:
        dock = self.dragged
        if dock is None:
            return
        key = self.overlay.hot
        self.overlay.end()
        self.dragged = None
        if key is None:
            return                                  # stays floating where it was dropped
        self.dock_to(dock, key)

    def _cancel(self) -> None:
        dock = self.dragged
        self.overlay.end()
        self.dragged = None
        if dock is not None and not self._was_floating:
            dock.setFloating(False)

    def dock_to(self, dock: QDockWidget, key: Tuple[str, Optional[QDockWidget], str]) -> None:
        """Put `dock` where a target says."""
        kind, target, name = key
        dock.setFloating(False)
        if kind == "window" or target is None:
            self.main.addDockWidget(AREAS.get(name, Qt.LeftDockWidgetArea), dock)
            return
        area = self.main.dockWidgetArea(target)
        if name == CENTER:
            self.main.addDockWidget(area, dock)
            self.main.tabifyDockWidget(target, dock)
            dock.raise_()
            return
        orientation = Qt.Horizontal if name in (LEFT, RIGHT) else Qt.Vertical
        self.main.addDockWidget(area, dock)
        self.main.splitDockWidget(target, dock, orientation)          # dock after the target
        if name in (LEFT, TOP):
            self.main.splitDockWidget(dock, target, orientation)      # ...then the target after the dock

    # -- keep the overlay over everything ------------------------------------------------
    def eventFilter(self, watched, event) -> bool:
        if watched is self.main and event.type() == QEvent.Resize and self.overlay.isVisible():
            self.overlay.setGeometry(self.main.rect())
        elif (self.dragged is not None and event.type() in (QEvent.KeyPress, QEvent.ShortcutOverride)
              and event.key() == Qt.Key_Escape):
            bar = self.dragged.titleBarWidget()
            if isinstance(bar, DockTitleBar):
                bar._dragging = False
                bar._press = None
            self._cancel()
            return True
        return False
