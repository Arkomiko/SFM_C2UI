"""
The timeline: the sequence's shots on the film track, the sound and other
track groups under it, and a time cursor.

Drawn by hand rather than assembled from widgets: a timeline is one picture
that scrolls and zooms as a whole. Time runs along X in the sequence's own
time; each clip is a rectangle from its start to its end.

    left drag on the ruler or empty space   move the time cursor
    shift + left drag on the ruler          make a time selection (its hold)
    drag a selection edge on the ruler      move that edge (inner: hold, outer: falloff)
    left click on a clip                    select it (a shot is shown in the viewport)
    wheel                                   zoom about the cursor
    middle drag / shift + wheel             scroll
    Home                                    fit the whole sequence
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen
from PySide6.QtWidgets import QWidget

from Core.API.dmx import Time
from Core.API.session import Clip, FilmClip, Session, SoundClip
from Core.Code.motion import INFINITE, TimeSelection

__all__ = ["Timeline"]

RULER_H = 24
ROW_H = 22
HEADER_W = 150
GROUP_H = 18

BG = QColor("#1f2227")
RULER_BG = QColor("#262a30")
HEADER_BG = QColor("#23272d")
GRID = QColor(255, 255, 255, 18)
TEXT = QColor("#c9d1d9")
DIM = QColor("#7d8590")
FILM = QColor("#3b6ea5")
FILM_SEL = QColor("#66c0f4")
SOUND = QColor("#4a8a5c")
OTHER = QColor("#6b5e9a")
CURSOR = QColor("#ff5c5c")
HOLD = QColor(255, 200, 80, 60)
FALLOFF = QColor(255, 200, 80, 28)
EDGE = QColor("#ffc850")
EDGE_GRAB = 6


@dataclass
class _Row:
    label: str
    clips: List[Clip]
    kind: str            # "film", "sound", "other", "group"
    y: int


class Timeline(QWidget):
    time_changed = Signal(object)        # Time
    shot_selected = Signal(object)       # FilmClip
    selection_changed = Signal(object)   # TimeSelection

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMinimumHeight(RULER_H + ROW_H * 3)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self._session: Optional[Session] = None
        self._rows: List[_Row] = []
        self._duration = 10.0            # seconds shown in total
        self._scale = 60.0               # pixels per second
        self._origin = 0.0               # seconds at the left edge of the track area
        self._time = Time(0)
        self._selected: Optional[Clip] = None
        self._drag: Optional[str] = None
        self._drag_last = QPointF()
        self.selection: Optional[TimeSelection] = None
        self._drag_edge: Optional[str] = None
        self._drag_anchor = 0.0
        self._font = QFont(self.font())
        self._font.setPointSizeF(max(7.5, self.font().pointSizeF() - 1))

    # -- data ------------------------------------------------------------------------
    def set_session(self, session: Optional[Session]) -> None:
        self._session = session
        self._rows = []
        self._selected = None
        self._time = Time(0)
        self.selection = None
        if session is not None and session.settings is not None:
            element = session.settings.get("timeSelection")
            if element is not None:
                self.selection = TimeSelection.from_element(element)
        if session is not None and session.active_clip is not None:
            clip = session.active_clip
            self._duration = max(0.001, clip.time_frame.duration.seconds)
            y = RULER_H
            self._rows.append(_Row("Film", clip.shots, "film", y))
            y += ROW_H
            for group in clip.track_groups:
                self._rows.append(_Row(group.name, [], "group", y))
                y += GROUP_H
                for track in group.tracks:
                    kind = "sound" if any(isinstance(c, SoundClip) for c in track.clips) else "other"
                    self._rows.append(_Row(track.name, track.clips, kind, y))
                    y += ROW_H
            self.setMinimumHeight(min(y, RULER_H + ROW_H * 12))
        self.fit()

    @property
    def time(self) -> Time:
        return self._time

    def set_time(self, time: Time, emit: bool = True) -> None:
        ticks = max(0, min(time.ticks, int(self._duration * Time.PER_SECOND)))
        if ticks == self._time.ticks:
            return
        self._time = Time(ticks)
        self.update()
        if emit:
            self.time_changed.emit(self._time)

    def select_clip(self, clip: Optional[Clip]) -> None:
        self._selected = clip
        self.update()

    # -- time selection ----------------------------------------------------------------
    def set_selection(self, selection: Optional[TimeSelection], write: bool = True) -> None:
        self.selection = selection
        if write and self._session is not None and self._session.settings is not None:
            element = self._session.settings.get("timeSelection")
            if element is not None and selection is not None:
                selection.write(element)
        self.selection_changed.emit(selection)
        self.update()

    def clear_selection(self) -> None:
        self.set_selection(TimeSelection(enabled=False))

    def _edges(self):
        """(name, seconds) of the finite selection edges."""
        sel = self.selection
        if sel is None or not sel.enabled:
            return []
        out = []
        for name, t in (("falloff_left", sel.falloff_left), ("hold_left", sel.hold_left),
                        ("hold_right", sel.hold_right), ("falloff_right", sel.falloff_right)):
            if abs(t.ticks) < INFINITE.ticks:
                out.append((name, t.seconds))
        return out

    def _edge_at(self, x: float) -> Optional[str]:
        best = None
        best_distance = EDGE_GRAB
        for name, seconds in self._edges():
            distance = abs(self._x(seconds) - x)
            if distance < best_distance:
                best, best_distance = name, distance
        return best

    def fit(self) -> None:
        width = max(50, self.width() - HEADER_W - 8)
        self._scale = width / self._duration
        self._origin = 0.0
        self.update()

    # -- geometry ----------------------------------------------------------------------
    def _x(self, seconds: float) -> float:
        return HEADER_W + (seconds - self._origin) * self._scale

    def _seconds(self, x: float) -> float:
        return self._origin + (x - HEADER_W) / self._scale

    def _clip_rect(self, clip: Clip, row: _Row) -> QRectF:
        frame = clip.time_frame
        x0 = self._x(frame.start.seconds)
        x1 = self._x(frame.end.seconds)
        return QRectF(x0, row.y + 2, max(2.0, x1 - x0), ROW_H - 4)

    def _clip_at(self, pos: QPointF) -> Tuple[Optional[Clip], Optional[_Row]]:
        for row in self._rows:
            if row.kind == "group" or not (row.y <= pos.y() < row.y + ROW_H):
                continue
            for clip in row.clips:
                if self._clip_rect(clip, row).contains(pos):
                    return clip, row
        return None, None

    # -- painting ----------------------------------------------------------------------
    def paintEvent(self, event) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, False)
        p.setFont(self._font)
        w, h = self.width(), self.height()
        p.fillRect(0, 0, w, h, BG)
        if self._session is None:
            p.setPen(DIM)
            p.drawText(self.rect(), Qt.AlignCenter, "No session open")
            return

        self._paint_ruler(p, w)
        self._paint_selection(p, w, h)
        p.setClipRect(0, RULER_H, w, h - RULER_H)
        for row in self._rows:
            self._paint_row(p, row, w)
        p.setClipping(False)
        # the time cursor
        x = round(self._x(self._time.seconds))
        if HEADER_W <= x <= w:
            p.setPen(QPen(CURSOR, 1))
            p.drawLine(x, 0, x, h)
            p.setBrush(CURSOR)
            p.drawPolygon([QPointF(x - 5, 0), QPointF(x + 5, 0), QPointF(x, 8)])

    def _paint_ruler(self, p: QPainter, w: int) -> None:
        p.fillRect(0, 0, w, RULER_H, RULER_BG)
        p.fillRect(0, 0, HEADER_W, RULER_H, HEADER_BG)
        p.setPen(TEXT)
        p.drawText(QRectF(8, 0, HEADER_W - 16, RULER_H), Qt.AlignVCenter | Qt.AlignLeft,
                   f"{self._time.seconds:8.3f} s")
        step = self._tick_step()
        first = int(self._origin // step)
        last = int(self._seconds(w) // step) + 1
        metrics = QFontMetrics(self._font)
        for i in range(first, last + 1):
            seconds = i * step
            x = round(self._x(seconds))
            if x < HEADER_W:
                continue
            p.setPen(DIM)
            p.drawLine(x, RULER_H - 8, x, RULER_H)
            p.setPen(GRID)
            p.drawLine(x, RULER_H, x, self.height())
            label = f"{seconds:g}s"
            p.setPen(TEXT)
            p.drawText(x + 3, RULER_H - 10, label)
            # minor ticks
            p.setPen(DIM)
            for k in range(1, 5):
                mx = round(self._x(seconds + step * k / 5))
                if mx > HEADER_W:
                    p.drawLine(mx, RULER_H - 3, mx, RULER_H)

    def _paint_selection(self, p: QPainter, w: int, h: int) -> None:
        sel = self.selection
        if sel is None or not sel.enabled:
            return

        def x_of(t: Time, fallback: float) -> float:
            return fallback if abs(t.ticks) >= INFINITE.ticks else self._x(t.seconds)

        fl = x_of(sel.falloff_left, HEADER_W)
        hl = x_of(sel.hold_left, HEADER_W)
        hr = x_of(sel.hold_right, w)
        fr = x_of(sel.falloff_right, w)
        left = max(HEADER_W, fl)
        p.fillRect(QRectF(left, 0, max(0.0, min(w, fr) - left), h), FALLOFF)
        p.fillRect(QRectF(max(HEADER_W, hl), 0, max(0.0, min(w, hr) - max(HEADER_W, hl)), h), HOLD)
        p.setPen(QPen(EDGE, 1))
        for _name, seconds in self._edges():
            x = round(self._x(seconds))
            if HEADER_W <= x <= w:
                p.drawLine(x, 0, x, h)
                p.setBrush(EDGE)
                p.drawPolygon([QPointF(x - 4, RULER_H), QPointF(x + 4, RULER_H), QPointF(x, RULER_H - 6)])

    def _tick_step(self) -> float:
        """Seconds between labelled ticks, chosen so labels do not collide."""
        for step in (0.1, 0.25, 0.5, 1, 2, 5, 10, 15, 30, 60, 120, 300):
            if step * self._scale >= 70:
                return step
        return 600

    def _paint_row(self, p: QPainter, row: _Row, w: int) -> None:
        height = GROUP_H if row.kind == "group" else ROW_H
        p.fillRect(0, row.y, HEADER_W, height, HEADER_BG)
        p.setPen(GRID)
        p.drawLine(0, row.y + height, w, row.y + height)
        p.setPen(TEXT if row.kind != "group" else DIM)
        p.drawText(QRectF(8 + (0 if row.kind in ("film", "group") else 10), row.y, HEADER_W - 12, height),
                   Qt.AlignVCenter | Qt.AlignLeft, row.label)
        if row.kind == "group":
            return
        colour = {"film": FILM, "sound": SOUND}.get(row.kind, OTHER)
        for clip in row.clips:
            rect = self._clip_rect(clip, row)
            if rect.right() < HEADER_W or rect.left() > w:
                continue
            selected = self._selected is not None and clip == self._selected
            fill = FILM_SEL if (selected and row.kind == "film") else colour.lighter(130 if selected else 100)
            p.fillRect(rect, fill)
            p.setPen(QPen(fill.darker(160), 1))
            p.drawRect(rect.adjusted(0, 0, -1, -1))
            if rect.width() > 24:
                p.setPen(QColor("#0b1016") if selected else TEXT)
                text_rect = rect.adjusted(4, 0, -4, 0)
                p.setClipRect(text_rect)
                p.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, clip.name)
                p.setClipRect(0, RULER_H, w, self.height() - RULER_H)

    # -- input -------------------------------------------------------------------------
    def mousePressEvent(self, event) -> None:
        pos = event.position()
        self._drag_last = pos
        if event.button() == Qt.MiddleButton:
            self._drag = "pan"
            return
        if event.button() != Qt.LeftButton or self._session is None:
            return
        if pos.x() < HEADER_W:
            return
        if pos.y() < RULER_H:
            edge = self._edge_at(pos.x())
            if edge is not None:
                self._drag = "edge"
                self._drag_edge = edge
                return
            if event.modifiers() & Qt.ShiftModifier:
                self._drag = "select"
                self._drag_anchor = self._seconds(pos.x())
                t = Time.from_seconds(self._drag_anchor)
                self.set_selection(TimeSelection(t, t, t, t, enabled=True), write=False)
                return
        clip, row = self._clip_at(pos)
        if clip is not None and pos.y() >= RULER_H:
            self._selected = clip
            self.update()
            if row is not None and row.kind == "film" and isinstance(clip, FilmClip):
                self.shot_selected.emit(clip)
            return
        self._drag = "scrub"
        self.set_time(Time.from_seconds(self._seconds(pos.x())))

    def mouseMoveEvent(self, event) -> None:
        pos = event.position()
        if self._drag == "scrub":
            self.set_time(Time.from_seconds(self._seconds(pos.x())))
        elif self._drag == "select" and self.selection is not None:
            a, b = sorted((self._drag_anchor, max(0.0, self._seconds(pos.x()))))
            sel = self.selection
            sel.falloff_left = sel.hold_left = Time.from_seconds(a)
            sel.hold_right = sel.falloff_right = Time.from_seconds(b)
            self.update()
        elif self._drag == "edge" and self.selection is not None:
            self._move_edge(self._drag_edge, max(0.0, self._seconds(pos.x())))
        elif self._drag == "pan":
            self._origin -= (pos.x() - self._drag_last.x()) / self._scale
            self._origin = max(0.0, self._origin)
            self.update()
        self._drag_last = pos

    def mouseReleaseEvent(self, event) -> None:
        if self._drag in ("select", "edge") and self.selection is not None:
            self.set_selection(self.selection)          # write it to the session
        self._drag = None
        self._drag_edge = None

    def _move_edge(self, edge: str, seconds: float) -> None:
        sel = self.selection
        t = Time.from_seconds(seconds)
        if edge == "falloff_left":
            sel.falloff_left = Time(min(t.ticks, sel.hold_left.ticks))
        elif edge == "hold_left":
            sel.hold_left = Time(min(max(t.ticks, sel.falloff_left.ticks), sel.hold_right.ticks))
        elif edge == "hold_right":
            sel.hold_right = Time(max(min(t.ticks, sel.falloff_right.ticks), sel.hold_left.ticks))
        elif edge == "falloff_right":
            sel.falloff_right = Time(max(t.ticks, sel.hold_right.ticks))
        self.update()

    def wheelEvent(self, event) -> None:
        delta = event.angleDelta().y() / 120.0
        if event.modifiers() & Qt.ShiftModifier:
            self._origin = max(0.0, self._origin - delta * 40 / self._scale)
        else:
            anchor = self._seconds(event.position().x())
            self._scale = min(5000.0, max(2.0, self._scale * (1.15 ** delta)))
            self._origin = max(0.0, anchor - (event.position().x() - HEADER_W) / self._scale)
        self.update()

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Home:
            self.fit()
        else:
            super().keyPressEvent(event)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
