"""
Timeline / Sequencer panel (UE5 "Sequencer" look) - maps to SFM's Timeline
(Clip Editor / Motion Editor / Graph Editor).

Stage 1: custom-painted ruler, tracks, clips and a draggable playhead with
placeholder data.  Stage 3 binds it to sfm shots/clips and the transport.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QFontMetrics, QMouseEvent, QPainter, QPen, QWheelEvent
from PySide6.QtWidgets import QLabel, QSizePolicy, QSpinBox, QToolBar, QWidget

from ...icons import icon as make_icon
from ...localization import tr
from ..base import C2UIPanel, PanelMeta


@dataclass
class Clip:
    name: str
    start: int
    length: int
    color: str = ""


@dataclass
class Track:
    name: str
    icon: str = "clip"
    clips: List[Clip] = field(default_factory=list)


_PLACEHOLDER_TRACKS = [
    Track("Camera", "camera", [Clip("shot1", 0, 240)]),
    Track("scout", "model", [Clip("idle", 0, 96, "#3f6f9f"), Clip("walk", 110, 130, "#3f6f9f")]),
    Track("light1", "light", [Clip("key light", 0, 240, "#8a7a2c")]),
    Track("dialog.wav", "sound", [Clip("dialog", 24, 160, "#3f8f5f")]),
    Track("particle_system1", "particles", [Clip("smoke", 60, 100, "#8f4f8f")]),
]


class TimelineView(QWidget):
    frame_changed = Signal(int)
    clip_selected = Signal(object)

    HEADER_W = 170
    RULER_H = 24
    ROW_H = 24

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("timelineView")
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tracks: List[Track] = list(_PLACEHOLDER_TRACKS)
        self.fps = 24
        self.frame = 0
        self.range_end = 240
        self.px_per_frame = 4.0
        self.scroll_x = 0.0
        self._drag_playhead = False
        self._pan_last: Optional[QPointF] = None
        self._selected: Optional[Clip] = None
        self.c: Dict[str, QColor] = {}
        self.apply_theme(None)

    # -- theme ----------------------------------------------------------------------
    def apply_theme(self, theme: Any) -> None:
        tok = theme.tokens if theme else {}
        get = lambda k, d: QColor(str(tok.get(k, d)))  # noqa: E731
        self.c = {
            "bg": get("timeline.bg", "#181a1e"),
            "header": get("timeline.header_bg", "#1f2227"),
            "row": get("timeline.row", "#1c1f24"),
            "row_alt": get("timeline.row_alt", "#202329"),
            "ruler": get("timeline.ruler_bg", "#14161a"),
            "grid": get("timeline.grid", "#2a2e35"),
            "grid_major": get("timeline.grid_major", "#3a3f48"),
            "text": get("text", "#d0d4d8"),
            "text_dim": get("text.dim", "#8a9099"),
            "clip": get("timeline.clip", "#3f6f9f"),
            "clip_border": get("timeline.clip_border", "#6aa5e0"),
            "playhead": get("timeline.playhead", "#ff4d4d"),
            "accent": get("accent", "#3b9eff"),
            "border": get("border", "#2c3038"),
            "range": get("timeline.range", "#2d3340"),
        }
        self.update()

    # -- helpers --------------------------------------------------------------------
    def x_of(self, frame: float) -> float:
        return self.HEADER_W + frame * self.px_per_frame - self.scroll_x

    def frame_at(self, x: float) -> int:
        return int(round((x - self.HEADER_W + self.scroll_x) / self.px_per_frame))

    def set_frame(self, frame: int, emit: bool = True) -> None:
        frame = max(0, min(self.range_end, frame))
        if frame != self.frame:
            self.frame = frame
            self.update()
            if emit:
                self.frame_changed.emit(frame)

    def set_tracks(self, tracks: List[Track]) -> None:
        self.tracks = tracks
        self.range_end = max([c.start + c.length for t in tracks for c in t.clips] + [1])
        self.update()

    # -- painting -------------------------------------------------------------------
    def paintEvent(self, _e) -> None:  # noqa: N802
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        w, h = self.width(), self.height()
        p.fillRect(self.rect(), self.c["bg"])

        # rows
        y = self.RULER_H
        for i, track in enumerate(self.tracks):
            row = QRectF(0, y, w, self.ROW_H)
            p.fillRect(row, self.c["row_alt"] if i % 2 else self.c["row"])
            y += self.ROW_H

        # range background + vertical grid in track area
        p.setClipRect(QRectF(self.HEADER_W, 0, w - self.HEADER_W, h))
        p.fillRect(QRectF(self.x_of(0), self.RULER_H, self.range_end * self.px_per_frame, h), self.c["range"].darker(115))
        step = self._grid_step()
        first = max(0, int((self.scroll_x / self.px_per_frame) // step) * step)
        f = first
        while self.x_of(f) < w:
            x = int(self.x_of(f))
            major = (f % (step * 4) == 0)
            p.setPen(QPen(self.c["grid_major"] if major else self.c["grid"], 1))
            p.drawLine(x, self.RULER_H, x, h)
            f += step

        # clips
        y = self.RULER_H
        for track in self.tracks:
            for clip in track.clips:
                r = QRectF(self.x_of(clip.start), y + 3, clip.length * self.px_per_frame, self.ROW_H - 6)
                color = QColor(clip.color) if clip.color else self.c["clip"]
                p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
                p.setPen(QPen(self.c["accent"] if clip is self._selected else color.lighter(140), 1))
                p.setBrush(color if clip is not self._selected else color.lighter(120))
                p.drawRoundedRect(r, 3, 3)
                p.setRenderHint(QPainter.RenderHint.Antialiasing, False)
                p.setPen(self.c["text"])
                p.drawText(r.adjusted(6, 0, -4, 0), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, clip.name)
            y += self.ROW_H

        # ruler
        p.setClipping(False)
        p.fillRect(QRectF(0, 0, w, self.RULER_H), self.c["ruler"])
        p.setClipRect(QRectF(self.HEADER_W, 0, w - self.HEADER_W, self.RULER_H))
        fm = QFontMetrics(p.font())
        f = first
        while self.x_of(f) < w:
            x = int(self.x_of(f))
            major = (f % (step * 4) == 0)
            p.setPen(QPen(self.c["text_dim"] if major else self.c["grid_major"], 1))
            p.drawLine(x, self.RULER_H - (12 if major else 6), x, self.RULER_H)
            if major:
                p.setPen(self.c["text_dim"])
                p.drawText(x + 3, fm.ascent() + 2, self._label(f))
            f += step
        p.setClipping(False)

        # header column
        p.fillRect(QRectF(0, 0, self.HEADER_W, h), self.c["header"])
        p.setPen(QPen(self.c["border"], 1))
        p.drawLine(self.HEADER_W, 0, self.HEADER_W, h)
        p.drawLine(0, self.RULER_H, w, self.RULER_H)
        y = self.RULER_H
        for track in self.tracks:
            make_icon(track.icon).paint(p, int(8), int(y + 4), 16, 16)
            p.setPen(self.c["text"])
            p.drawText(QRectF(30, y, self.HEADER_W - 34, self.ROW_H), Qt.AlignmentFlag.AlignVCenter, track.name)
            p.setPen(QPen(self.c["border"], 1))
            p.drawLine(0, int(y + self.ROW_H), w, int(y + self.ROW_H))
            y += self.ROW_H
        p.setPen(self.c["text_dim"])
        p.drawText(QRectF(8, 0, self.HEADER_W - 12, self.RULER_H), Qt.AlignmentFlag.AlignVCenter,
                   self._label(self.frame) + f"   {self.fps} fps")

        # playhead
        x = self.x_of(self.frame)
        if x >= self.HEADER_W:
            p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            p.setPen(QPen(self.c["playhead"], 1.5))
            p.drawLine(QPointF(x, 0), QPointF(x, h))
            p.setBrush(self.c["playhead"])
            p.drawPolygon([QPointF(x - 6, 0), QPointF(x + 6, 0), QPointF(x, 9)])
        p.end()

    def _grid_step(self) -> int:
        for s in (1, 2, 5, 10, 24, 48, 120, 240, 600):
            if s * self.px_per_frame >= 28:
                return s
        return 1200

    def _label(self, frame: int) -> str:
        secs, fr = divmod(int(frame), self.fps)
        m, s = divmod(secs, 60)
        return f"{m:02d}:{s:02d}:{fr:02d}"

    # -- interaction ----------------------------------------------------------------
    def mousePressEvent(self, e: QMouseEvent) -> None:  # noqa: N802
        pos = e.position()
        if e.button() == Qt.MouseButton.MiddleButton:
            self._pan_last = pos
            return
        if e.button() == Qt.MouseButton.LeftButton and pos.x() >= self.HEADER_W:
            if pos.y() <= self.RULER_H:
                self._drag_playhead = True
                self.set_frame(self.frame_at(pos.x()))
            else:
                self._select_clip_at(pos)
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:  # noqa: N802
        pos = e.position()
        if self._pan_last is not None:
            self.scroll_x = max(0.0, self.scroll_x - (pos.x() - self._pan_last.x()))
            self._pan_last = pos
            self.update()
        elif self._drag_playhead:
            self.set_frame(self.frame_at(pos.x()))
        super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:  # noqa: N802
        self._drag_playhead = False
        self._pan_last = None
        super().mouseReleaseEvent(e)

    def wheelEvent(self, e: QWheelEvent) -> None:  # noqa: N802
        delta = e.angleDelta().y()
        if e.modifiers() & Qt.KeyboardModifier.ControlModifier:
            anchor_frame = self.frame_at(e.position().x())
            self.px_per_frame = max(0.5, min(60.0, self.px_per_frame * (1.15 if delta > 0 else 1 / 1.15)))
            self.scroll_x = max(0.0, anchor_frame * self.px_per_frame - (e.position().x() - self.HEADER_W))
        else:
            self.scroll_x = max(0.0, self.scroll_x - delta * 0.5)
        self.update()
        e.accept()

    def _select_clip_at(self, pos: QPointF) -> None:
        row = int((pos.y() - self.RULER_H) // self.ROW_H)
        frame = self.frame_at(pos.x())
        self._selected = None
        if 0 <= row < len(self.tracks):
            for clip in self.tracks[row].clips:
                if clip.start <= frame <= clip.start + clip.length:
                    self._selected = clip
                    break
        self.clip_selected.emit(self._selected)
        self.update()


class TimelinePanel(C2UIPanel):
    META = PanelMeta(id="timeline", title_key="panel.timeline", icon="timeline", category="Editor",
                     default_area="bottom", min_size=(400, 160), sfm_lookup="Timestrip")

    def build(self) -> None:
        self.toolbar = QToolBar(self)
        self.toolbar.setObjectName("timelineToolbar")
        self.toolbar.setIconSize(self.toolbar.iconSize().boundedTo(self.toolbar.iconSize()))
        self.toolbar.setMovable(False)
        ctx = self.app.context
        for aid in ("transport.to_start", "transport.prev_frame", "transport.play_pause", "transport.stop",
                    "transport.next_frame", "transport.to_end"):
            act = ctx.action(aid)
            if act:
                self.toolbar.addAction(act)
        self.toolbar.addSeparator()
        self.frame_box = QSpinBox(self.toolbar)
        self.frame_box.setObjectName("frameBox")
        self.frame_box.setRange(0, 1_000_000)
        self.frame_box.setPrefix(tr("timeline.frame_prefix"))
        self.frame_box.valueChanged.connect(lambda v: self.view.set_frame(v, emit=False))
        self.toolbar.addWidget(self.frame_box)
        spacer = QWidget(self.toolbar)
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(spacer)
        self.mode_label = QLabel(self.toolbar)
        self.mode_label.setObjectName("timelineMode")
        self.toolbar.addWidget(self.mode_label)
        self.root_layout.addWidget(self.toolbar)

        self.view = TimelineView(self)
        self.view.frame_changed.connect(self._on_frame)
        self.view.clip_selected.connect(self._on_clip)
        self.root_layout.addWidget(self.view, 1)

        self._suppress = False        # ignore our own set_frame echo coming back as an event
        self.subscribe("sfm.state_changed", self._on_sfm_state)

    def _on_frame(self, frame: int) -> None:
        self.frame_box.blockSignals(True)
        self.frame_box.setValue(frame)
        self.frame_box.blockSignals(False)
        if self.app.bridge.connected and not self._suppress:
            self.app.sfm_call("sfm.set_frame", {"frame": frame})

    def _on_sfm_state(self, payload: dict) -> None:
        state = (payload or {}).get("state", payload) or {}
        fps = state.get("fps")
        if fps:
            self.view.fps = int(round(fps))
        frame = state.get("frame")
        if frame is not None and frame != self.view.frame:
            self._suppress = True
            self.view.set_frame(int(frame), emit=False)
            self.frame_box.blockSignals(True)
            self.frame_box.setValue(int(frame))
            self.frame_box.blockSignals(False)
            self._suppress = False
        play = self.app.context.action("transport.play_pause")
        if play is not None:
            from ...icons import icon as _icon
            play.setIcon(_icon("pause" if state.get("playing") else "play"))

    def _on_clip(self, clip: Optional[Clip]) -> None:
        self.selection_changed.emit([{"name": clip.name, "type": "clip", "icon": "clip"}] if clip else [])

    def on_theme_changed(self, theme: Any) -> None:
        self.view.apply_theme(theme)

    def on_context_changed(self, context_id: str) -> None:
        preset = self.app.context.preset(context_id)
        self.mode_label.setText(preset.name() if preset else "")

    def on_language_changed(self, code: str) -> None:
        super().on_language_changed(code)
        self.frame_box.setPrefix(tr("timeline.frame_prefix"))
        self.on_context_changed(self.app.context.current or "")
