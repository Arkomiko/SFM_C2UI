"""The graph editor: the selected element's animation as curves over time.

One curve per component of every log that drives the element (X/Y/Z of a
position, pitch/yaw/roll of a rotation, a float's value).  Keys are
squares on the curve; drag them in time and value, rubber-band to select
several, double-click a curve to add a key, Delete removes.  The time
axis is the timeline's own, so both scroll and zoom together.  Each log
has its own value range (a position in units, a rotation in degrees, both
filling the height), so nothing is flattened by a neighbour's scale; the
value grid is labelled for the curve being worked on.  The wheel zooms
values, Home fits them.

Every change goes out as one command through `edited`; the window pushes
it on the undo stack.  While a drag is in progress the change is applied
as a preview and taken back before the real command is emitted.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional, Set, Tuple

from PySide6.QtCore import QPointF, QRect, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QWidget

from Core.API.dmx import AttrType, Time
from Core.API.session import Log
from Core.Code.animation import _layer_keys
from Core.Code.editing import Command, top_layer
from Core.Code.keys import (component_value, delete_keys, insert_key, key_count, move_keys,
                            with_component)

from .timeline import HEADER_W, RULER_H, Timeline

__all__ = ["Curve", "GraphEditor"]

BG = QColor("#1b1e23")
HEADER_BG = QColor("#23272d")
RULER_BG = QColor("#262a30")
GRID = QColor(255, 255, 255, 18)
ZERO = QColor(255, 255, 255, 50)
TEXT = QColor("#c9d1d9")
DIM = QColor("#7d8590")
CURSOR = QColor("#ff5c5c")
KEY = QColor("#e6f0f8")
KEY_SEL = QColor("#ffd166")
BAND = QColor(102, 192, 244, 40)
COLOURS = {"X": QColor("#ff6b6b"), "Y": QColor("#7ddb7d"), "Z": QColor("#6fb6ff"), "W": QColor("#d29bff"),
           "pitch": QColor("#ff6b6b"), "yaw": QColor("#7ddb7d"), "roll": QColor("#6fb6ff"),
           "R": QColor("#ff6b6b"), "G": QColor("#7ddb7d"), "B": QColor("#6fb6ff"), "A": QColor("#d0d0d0"),
           "value": QColor("#ffc857")}
KEY_HALF = 3.5


@dataclass
class Curve:
    """One line on the graph: a component of a log, with the mapping between
    the session's time (the x axis) and the log's own clip time."""
    log: Log
    kind: int
    component: int
    label: str
    to_log: Callable[[Time], Time]      # session time -> log time
    to_session: Callable[[Time], Time]  # log time -> session time
    colour: QColor = None
    low: float = -1.0                   # value range shown; curves of one log share theirs
    high: float = 1.0

    def __post_init__(self) -> None:
        if self.colour is None:
            self.colour = COLOURS.get(self.label, COLOURS["value"])

    def keys(self) -> Tuple[List[Time], List[float]]:
        """Key times in session time, key values of this component."""
        layer = top_layer(self.log)
        if layer is None:
            return [], []
        times = layer.get("times") or []
        values = layer.get("values") or []
        n = min(len(times), len(values))
        return ([self.to_session(t) for t in times[:n]],
                [component_value(self.kind, v, self.component) for v in values[:n]])

    def value_at(self, session_time: Time) -> Optional[float]:
        """The curve's value at a session time, or None outside its keys."""
        layer = top_layer(self.log)
        keys = _layer_keys(layer) if layer is not None else None
        if keys is None:
            return None
        return component_value(self.kind, keys.sample(self.to_log(session_time)), self.component)


class GraphEditor(QWidget):
    """Curves of the selected logs over time, with key editing."""
    time_changed = Signal(object)       # Time: the ruler was clicked or dragged
    edited = Signal(object)             # Command: push it
    previewed = Signal()                # the logs changed under a drag: re-pose

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMinimumHeight(120)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self._timeline: Optional[Timeline] = None
        self._origin = 0.0
        self._scale = 60.0
        self._time = Time(0)
        self.curves: List[Curve] = []
        self.selected: Set[Tuple[int, int]] = set()     # (curve index, key index)
        self._drag: Optional[str] = None
        self._press = QPointF()
        self._last = QPointF()
        self._band: Optional[QRectF] = None
        self._preview: Optional[Command] = None
        self._drag_dt = 0
        self._drag_dy = 0.0
        self._font = QFont(self.font())
        self._font.setPointSizeF(max(7.5, self.font().pointSizeF() - 1))

    # -- data ------------------------------------------------------------------------
    def follow(self, timeline: Timeline) -> None:
        """Share the timeline's time axis."""
        self._timeline = timeline
        timeline.view_changed.connect(self._sync)
        self._sync()

    def _sync(self) -> None:
        if self._timeline is not None:
            self._origin = self._timeline.origin
            self._scale = self._timeline.scale
        self.update()

    def set_curves(self, curves: List[Curve]) -> None:
        """Show these curves."""
        self.curves = list(curves)
        self.selected = set()
        self.fit_values()

    def set_time(self, time: Time) -> None:
        """Move the time cursor."""
        self._time = time
        self.update()

    def refresh(self) -> None:
        """The logs changed elsewhere (undo, another edit): drop stale selections."""
        self.selected = {(c, k) for c, k in self.selected
                         if c < len(self.curves) and k < key_count(self.curves[c].log)}
        self.update()

    def fit_values(self) -> None:
        """Each log's curves fill the height together."""
        groups = {}
        for curve in self.curves:
            groups.setdefault(id(curve.log), []).append(curve)
        for group in groups.values():
            lo, hi = None, None
            for curve in group:
                _times, values = curve.keys()
                for v in values:
                    lo = v if lo is None else min(lo, v)
                    hi = v if hi is None else max(hi, v)
            if lo is None:
                lo, hi = -1.0, 1.0
            if hi - lo < 1e-6:
                lo, hi = lo - 1.0, hi + 1.0
            pad = (hi - lo) * 0.12
            for curve in group:
                curve.low, curve.high = lo - pad, hi + pad
        self.update()

    def _active(self) -> Optional[Curve]:
        """The curve the value grid is labelled for: the one being edited, else the first."""
        if self.selected:
            c = min(self.selected)[0]
            if c < len(self.curves):
                return self.curves[c]
        return self.curves[0] if self.curves else None

    # -- geometry ----------------------------------------------------------------------
    def _x(self, seconds: float) -> float:
        return HEADER_W + (seconds - self._origin) * self._scale

    def _seconds(self, x: float) -> float:
        return self._origin + (x - HEADER_W) / self._scale

    def _y(self, value: float, curve: Curve) -> float:
        h = self.height() - RULER_H
        return RULER_H + (curve.high - value) / (curve.high - curve.low) * h

    def _value(self, y: float, curve: Curve) -> float:
        h = max(1, self.height() - RULER_H)
        return curve.high - (y - RULER_H) / h * (curve.high - curve.low)

    def _per_pixel(self, curve: Curve) -> float:
        return (curve.high - curve.low) / max(1, self.height() - RULER_H)

    def _key_points(self, index: int) -> List[Tuple[QPointF, int]]:
        curve = self.curves[index]
        times, values = curve.keys()
        return [(QPointF(self._x(t.seconds), self._y(v, curve)), i) for i, (t, v) in enumerate(zip(times, values))]

    def _key_at(self, pos: QPointF) -> Optional[Tuple[int, int]]:
        best, best_d = None, 8.0 ** 2
        for c in range(len(self.curves)):
            for point, k in self._key_points(c):
                d = (point.x() - pos.x()) ** 2 + (point.y() - pos.y()) ** 2
                if d < best_d:
                    best, best_d = (c, k), d
        return best

    def _curve_at(self, pos: QPointF) -> Optional[int]:
        """The curve passing within a few pixels of `pos`."""
        seconds = self._seconds(pos.x())
        best, best_d = None, 6.0
        for c, curve in enumerate(self.curves):
            v = curve.value_at(Time.from_seconds(seconds))
            if v is None:
                continue
            d = abs(self._y(v, curve) - pos.y())
            if d < best_d:
                best, best_d = c, d
        return best

    # -- painting ----------------------------------------------------------------------
    def paintEvent(self, event) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        p.fillRect(0, 0, w, h, BG)
        p.setFont(self._font)
        self._paint_grid(p, w, h)
        p.setClipRect(QRect(HEADER_W, RULER_H, w - HEADER_W, h - RULER_H))
        for c, curve in enumerate(self.curves):
            self._paint_curve(p, c, curve)
        # the cursor
        x = round(self._x(self._time.seconds))
        if x >= HEADER_W:
            p.setPen(QPen(CURSOR, 1))
            p.drawLine(x, RULER_H, x, h)
        if self._band is not None:
            p.fillRect(self._band, BAND)
            p.setPen(QPen(QColor("#66c0f4"), 1))
            p.drawRect(self._band)
        p.setClipping(False)
        self._paint_header(p, h)
        p.end()

    def _paint_grid(self, p: QPainter, w: int, h: int) -> None:
        p.fillRect(0, 0, w, RULER_H, RULER_BG)
        # time
        step = self._timeline.tick_step() if self._timeline is not None else 1.0
        first = int(self._origin // step)
        last = int(self._seconds(w) // step) + 1
        for i in range(first, last + 1):
            seconds = i * step
            x = round(self._x(seconds))
            if x < HEADER_W:
                continue
            p.setPen(GRID)
            p.drawLine(x, RULER_H, x, h)
            p.setPen(DIM)
            p.drawLine(x, RULER_H - 6, x, RULER_H)
            p.setPen(TEXT)
            p.drawText(x + 3, RULER_H - 8, f"{seconds:g}s")
        # value, for the active curve
        curve = self._active()
        if curve is None:
            return
        span = curve.high - curve.low
        vstep = _nice_step(span / max(2, (h - RULER_H) / 40))
        v = (curve.low // vstep) * vstep
        while v <= curve.high:
            y = round(self._y(v, curve))
            if RULER_H < y < h:
                p.setPen(ZERO if abs(v) < vstep * 1e-6 else GRID)
                p.drawLine(HEADER_W, y, w, y)
                p.setPen(curve.colour if abs(v) < vstep * 1e-6 else DIM)
                p.drawText(QRectF(4, y - 8, HEADER_W - 8, 16), Qt.AlignRight | Qt.AlignVCenter, f"{v:g}")
            v += vstep

    def _paint_curve(self, p: QPainter, index: int, curve: Curve) -> None:
        times, values = curve.keys()
        if not times:
            return
        path = QPainterPath()
        smooth = curve.kind == AttrType.QUATERNION
        stepped = curve.kind in (AttrType.BOOL, AttrType.INT)
        x0, y0 = self._x(times[0].seconds), self._y(values[0], curve)
        path.moveTo(min(x0, HEADER_W), y0)               # flat before the first key
        path.lineTo(x0, y0)
        for i in range(1, len(times)):
            x1, y1 = self._x(times[i].seconds), self._y(values[i], curve)
            if x1 < HEADER_W - 2 and x0 < HEADER_W - 2:
                x0, y0 = x1, y1
                path.moveTo(x1, y1)
                continue
            if stepped:
                path.lineTo(x1, y0)
                path.lineTo(x1, y1)
            elif smooth and x1 - x0 > 6:
                for s in range(1, 5):                    # a slerp is not straight in angles
                    t = Time(round(times[i - 1].ticks + (times[i].ticks - times[i - 1].ticks) * s / 5))
                    v = curve.value_at(t)
                    if v is not None:
                        path.lineTo(self._x(t.seconds), self._y(v, curve))
                path.lineTo(x1, y1)
            else:
                path.lineTo(x1, y1)
            x0, y0 = x1, y1
            if x0 > self.width():
                break
        path.lineTo(max(x0, self.width()), y0)           # and flat after the last
        p.setPen(QPen(curve.colour, 1.4))
        p.drawPath(path)
        # keys, only those on screen; where they crowd (a key every frame) a tick stands in for the square
        last_square = -1e9
        for point, k in self._key_points(index):
            if point.x() < HEADER_W - KEY_HALF or point.x() > self.width() + KEY_HALF:
                continue
            chosen = (index, k) in self.selected
            if not chosen and point.x() - last_square < 3.5 * KEY_HALF:
                p.setPen(QPen(curve.colour, 1))
                p.drawLine(QPointF(point.x(), point.y() - 2), QPointF(point.x(), point.y() + 2))
                continue
            last_square = point.x()
            p.setPen(QPen(KEY_SEL if chosen else curve.colour, 1))
            p.setBrush(KEY_SEL if chosen else KEY)
            size = KEY_HALF + (1 if chosen else 0)
            p.drawRect(QRectF(point.x() - size, point.y() - size, size * 2, size * 2))

    def _paint_header(self, p: QPainter, h: int) -> None:
        p.fillRect(0, 0, HEADER_W, RULER_H, HEADER_BG)
        p.setPen(TEXT)
        p.drawText(QRectF(8, 0, HEADER_W - 16, RULER_H), Qt.AlignVCenter | Qt.AlignLeft,
                   f"{self._time.seconds:8.3f} s")
        # the legend with each curve's value at the cursor
        y = RULER_H + 6
        for curve in self.curves:
            v = curve.value_at(self._time)
            p.setPen(curve.colour)
            p.drawText(QRectF(8, y, HEADER_W - 16, 16), Qt.AlignVCenter | Qt.AlignLeft,
                       f"{curve.label}  {v:.3f}" if v is not None else curve.label)
            y += 16
            if y > h - 16:
                break

    # -- mouse -------------------------------------------------------------------------
    def mousePressEvent(self, event) -> None:
        pos = event.position()
        self._press = self._last = pos
        if event.button() == Qt.MiddleButton:
            self._drag = "pan"
            return
        if event.button() != Qt.LeftButton:
            return
        if pos.y() < RULER_H or pos.x() < HEADER_W:
            self._drag = "scrub"
            self._scrub(pos.x())
            return
        hit = self._key_at(pos)
        if hit is not None:
            if event.modifiers() & Qt.ShiftModifier:
                self.selected ^= {hit}
            elif hit not in self.selected:
                self.selected = {hit}
            self._drag = "keys" if hit in self.selected else None
            self._drag_dt, self._drag_dy = 0, 0.0
            self.update()
            return
        if not event.modifiers() & Qt.ShiftModifier:
            self.selected = set()
        self._drag = "band"
        self._band = QRectF(pos, pos)
        self.update()

    def mouseMoveEvent(self, event) -> None:
        pos = event.position()
        if self._drag == "scrub":
            self._scrub(pos.x())
        elif self._drag == "pan":
            dy = pos.y() - self._last.y()
            for curve in self.curves:
                dv = dy * self._per_pixel(curve)
                curve.low += dv
                curve.high += dv
            self.update()
        elif self._drag == "band":
            self._band = QRectF(self._press, pos).normalized()
            self.update()
        elif self._drag == "keys":
            dt = round((pos.x() - self._press.x()) / self._scale * Time.PER_SECOND)
            dy = -(pos.y() - self._press.y())
            if event.modifiers() & Qt.ControlModifier:
                dt = 0                                    # value only
            if event.modifiers() & Qt.AltModifier:
                dy = 0.0                                  # time only
            self._apply_preview(dt, dy)
        self._last = pos

    def mouseReleaseEvent(self, event) -> None:
        drag, self._drag = self._drag, None
        if drag == "band" and self._band is not None:
            band = self._band
            self._band = None
            for c in range(len(self.curves)):
                for point, k in self._key_points(c):
                    if band.contains(point):
                        self.selected.add((c, k))
            self.update()
        elif drag == "keys":
            self._finish_drag()

    def mouseDoubleClickEvent(self, event) -> None:
        pos = event.position()
        if event.button() != Qt.LeftButton or pos.y() < RULER_H or pos.x() < HEADER_W:
            return
        c = self._curve_at(pos)
        if c is None:
            return
        curve = self.curves[c]
        at = curve.to_log(Time.from_seconds(self._seconds(pos.x())))
        command = insert_key(curve.log, at)
        if command is not None:
            self.edited.emit(command)

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            self.delete_selected()
        elif event.key() == Qt.Key_Home:
            self.fit_values()
        elif event.key() == Qt.Key_A and event.modifiers() & Qt.ControlModifier:
            self.selected = {(c, k) for c in range(len(self.curves)) for k in range(key_count(self.curves[c].log))}
            self.update()
        else:
            super().keyPressEvent(event)

    def wheelEvent(self, event) -> None:
        delta = event.angleDelta().y() / 120.0
        if event.modifiers() & Qt.ControlModifier and self._timeline is not None:
            self._timeline.wheelEvent(event)             # zoom time through the shared axis
            return
        factor = 1.15 ** (-delta)
        for curve in self.curves:
            centre = self._value(event.position().y(), curve)
            curve.low = centre - (centre - curve.low) * factor
            curve.high = centre + (curve.high - centre) * factor
        self.update()

    # -- edits -------------------------------------------------------------------------
    def _scrub(self, x: float) -> None:
        seconds = max(0.0, self._seconds(max(x, HEADER_W)))
        self.time_changed.emit(Time.from_seconds(seconds))

    def _by_curve(self) -> List[Tuple[int, List[int]]]:
        out = {}
        for c, k in self.selected:
            out.setdefault(c, []).append(k)
        return sorted(out.items())

    def _commands(self, dt: int, dy: float, label: str) -> List[Command]:
        """One command per curve: `dt` session ticks, `dy` pixels in each curve's own scale."""
        commands = []
        for c, keys in self._by_curve():
            curve = self.curves[c]
            dv = dy * self._per_pixel(curve)
            # session-time delta becomes log-time delta through the clip's scale
            zero = curve.to_log(Time(0)).ticks
            log_dt = curve.to_log(Time(dt)).ticks - zero
            change = (lambda v, curve=curve: with_component(
                curve.kind, v, curve.component, component_value(curve.kind, v, curve.component) + dv))
            command = move_keys(curve.log, keys, log_dt, change if dv else None, label)
            if command is not None:
                commands.append(command)
        return commands

    def _apply_preview(self, dt: int, dy: float) -> None:
        if self._preview is not None:
            self._preview.revert()
            self._preview = None
        self._drag_dt, self._drag_dy = dt, dy
        commands = self._commands(dt, dy, "move keys")
        if commands:
            from Core.Code.editing import Group
            self._preview = Group(commands, "move keys") if len(commands) > 1 else commands[0]
            self._preview.apply()
        self.previewed.emit()
        self.update()

    def _finish_drag(self) -> None:
        if self._preview is not None:
            self._preview.revert()
            self._preview = None
        dt, dy = self._drag_dt, self._drag_dy
        self._drag_dt, self._drag_dy = 0, 0.0
        if dt == 0 and dy == 0.0:
            self.previewed.emit()
            return
        commands = self._commands(dt, dy, "move keys")
        # the moved keys keep their selection at their new places
        moved = []
        for c, keys in self._by_curve():
            curve = self.curves[c]
            times, _values = curve.keys()
            for k in keys:
                if k < len(times):
                    moved.append((c, Time(times[k].ticks + dt)))
        if commands:
            from Core.Code.editing import Group
            self.edited.emit(Group(commands, "move keys") if len(commands) > 1 else commands[0])
            self.selected = set()
            for c, at in moved:
                times, _values = self.curves[c].keys()
                for k, t in enumerate(times):
                    if t.ticks == at.ticks:
                        self.selected.add((c, k))
                        break
        self.update()

    def delete_selected(self) -> None:
        """Delete the selected keys as one undoable command."""
        commands = []
        for c, keys in self._by_curve():
            command = delete_keys(self.curves[c].log, keys)
            if command is not None:
                commands.append(command)
        if commands:
            from Core.Code.editing import Group
            self.selected = set()
            self.edited.emit(Group(commands, "delete keys") if len(commands) > 1 else commands[0])


def _nice_step(raw: float) -> float:
    """A grid step near `raw` that reads well: 1, 2, 5 x 10^n."""
    if raw <= 0:
        return 1.0
    import math
    power = 10.0 ** math.floor(math.log10(raw))
    for m in (1, 2, 5, 10):
        if m * power >= raw:
            return m * power
    return 10 * power
