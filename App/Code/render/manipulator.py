"""
The manipulator: three axes at a point in the world that can be dragged.

It knows nothing about sessions or OpenGL. Given a way to project world
points to the screen, it draws itself as line segments, says which axis a
pixel is on, and turns a mouse drag into a translation along that axis or a
rotation about it. The window decides what the result is applied to.

    m = Manipulator()
    m.place(origin, rotation)           # world position, optional local frame
    m.lines(scale)                       # segments for the overlay
    axis = m.hit(px, py, project)        # 0, 1, 2 or None
    m.begin(axis, px, py, project)
    delta = m.drag(px, py, project)      # Vec3 (move) or (axis_dir, angle) (rotate)
"""
from __future__ import annotations

import math
from typing import Callable, List, Optional, Tuple

from Core.Code.transform import quaternion_to_matrix

__all__ = ["Manipulator", "MOVE", "ROTATE"]

Vec3 = Tuple[float, float, float]
Project = Callable[[Vec3], Optional[Tuple[float, float, float]]]   # world -> (sx, sy, depth) or None

MOVE = "move"
ROTATE = "rotate"

AXIS_COLOURS = ((0.95, 0.25, 0.25, 1.0), (0.35, 0.85, 0.35, 1.0), (0.35, 0.55, 0.95, 1.0))
ACTIVE_COLOUR = (1.0, 0.9, 0.2, 1.0)
PICK_DISTANCE = 10.0


class Manipulator:
    """The move/rotate gizmo: three axes, one active while dragging."""
    def __init__(self) -> None:
        self.mode = MOVE
        self.origin: Vec3 = (0.0, 0.0, 0.0)
        self.axes: List[Vec3] = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]
        self.visible = False
        self.active: Optional[int] = None
        self._start: Optional[Tuple[float, float]] = None
        self._start_origin_px: Optional[Tuple[float, float]] = None
        self._start_angle = 0.0
        self._accumulated_angle = 0.0

    # -- placement -------------------------------------------------------------------
    def place(self, origin: Vec3, rotation: Optional[Tuple[float, float, float, float]] = None) -> None:
        """Put the gizmo at `origin`, aligned to `rotation` or world axes."""
        self.origin = tuple(origin)
        if rotation is None:
            self.axes = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]
        else:
            m = quaternion_to_matrix(rotation)
            self.axes = [(m[0], m[3], m[6]), (m[1], m[4], m[7]), (m[2], m[5], m[8])]
        self.visible = True

    def hide(self) -> None:
        """Hide and stop any drag."""
        self.visible = False
        self.active = None
        self._start = None

    # -- drawing ---------------------------------------------------------------------
    def lines(self, size: float):
        """Segments to draw: the three axes; rings around them when rotating."""
        if not self.visible:
            return []
        out = []
        o = self.origin
        for i, axis in enumerate(self.axes):
            colour = ACTIVE_COLOUR if i == self.active else AXIS_COLOURS[i]
            end = (o[0] + axis[0] * size, o[1] + axis[1] * size, o[2] + axis[2] * size)
            out.append((o, end, colour))
            # an arrow head as two short strokes
            for other in (self.axes[(i + 1) % 3], self.axes[(i + 2) % 3]):
                tip = (end[0] - axis[0] * size * 0.15 + other[0] * size * 0.06,
                       end[1] - axis[1] * size * 0.15 + other[1] * size * 0.06,
                       end[2] - axis[2] * size * 0.15 + other[2] * size * 0.06)
                out.append((end, tip, colour))
            if self.mode == ROTATE:
                out.extend(self._ring(i, size * 0.8, colour))
        return out

    def _ring(self, axis_index: int, radius: float, colour, segments: int = 32):
        u = self.axes[(axis_index + 1) % 3]
        v = self.axes[(axis_index + 2) % 3]
        o = self.origin
        points = []
        for k in range(segments + 1):
            a = 2 * math.pi * k / segments
            c, s = math.cos(a) * radius, math.sin(a) * radius
            points.append((o[0] + u[0] * c + v[0] * s, o[1] + u[1] * c + v[1] * s, o[2] + u[2] * c + v[2] * s))
        return [(points[k], points[k + 1], colour) for k in range(segments)]

    # -- picking ---------------------------------------------------------------------
    def hit(self, px: float, py: float, project: Project, size: float) -> Optional[int]:
        """Which axis (0, 1, 2) the pixel is on, nearest wins, or None."""
        if not self.visible:
            return None
        o = project(self.origin)
        if o is None:
            return None
        best = None
        best_distance = PICK_DISTANCE
        for i, axis in enumerate(self.axes):
            if self.mode == ROTATE:
                distance = self._ring_distance(i, px, py, project, size * 0.8)
            else:
                end = project((self.origin[0] + axis[0] * size, self.origin[1] + axis[1] * size,
                               self.origin[2] + axis[2] * size))
                if end is None:
                    continue
                distance = _segment_distance(px, py, o[0], o[1], end[0], end[1])
            if distance < best_distance:
                best_distance = distance
                best = i
        return best

    def _ring_distance(self, axis_index: int, px: float, py: float, project: Project, radius: float) -> float:
        best = float("inf")
        ring = self._ring(axis_index, radius, None)
        for a, b, _c in ring:
            pa, pb = project(a), project(b)
            if pa is None or pb is None:
                continue
            best = min(best, _segment_distance(px, py, pa[0], pa[1], pb[0], pb[1]))
        return best

    # -- dragging --------------------------------------------------------------------
    def begin(self, axis: int, px: float, py: float, project: Project) -> None:
        """Start dragging along `axis` from screen point (px, py)."""
        self.active = axis
        self._start = (px, py)
        o = project(self.origin)
        self._start_origin_px = (o[0], o[1]) if o is not None else (px, py)
        self._start_angle = math.atan2(py - self._start_origin_px[1], px - self._start_origin_px[0])
        self._accumulated_angle = 0.0

    def drag(self, px: float, py: float, project: Project, size: float):
        """Since `begin`: a world translation (move) or (axis, angle) (rotate)."""
        if self.active is None or self._start is None:
            return None
        axis = self.axes[self.active]
        if self.mode == MOVE:
            o = project(self.origin)
            e = project((self.origin[0] + axis[0] * size, self.origin[1] + axis[1] * size,
                         self.origin[2] + axis[2] * size))
            if o is None or e is None:
                return None
            dx, dy = e[0] - o[0], e[1] - o[1]
            length_sq = dx * dx + dy * dy
            if length_sq < 1e-6:
                return None
            mx, my = px - self._start[0], py - self._start[1]
            t = (mx * dx + my * dy) / length_sq * size
            return (axis[0] * t, axis[1] * t, axis[2] * t)
        ox, oy = self._start_origin_px
        angle = math.atan2(py - oy, px - ox) - self._start_angle
        # screen y points down, so a counter-clockwise drag on screen is clockwise in the world
        angle = -angle
        # an axis pointing away from the viewer turns the other way
        o = project(self.origin)
        tip = project((self.origin[0] + axis[0], self.origin[1] + axis[1], self.origin[2] + axis[2]))
        if o is not None and tip is not None and tip[2] > o[2]:
            angle = -angle
        return (axis, angle)

    def end(self) -> None:
        """Finish the drag."""
        self.active = None
        self._start = None


def _segment_distance(px: float, py: float, x0: float, y0: float, x1: float, y1: float) -> float:
    dx, dy = x1 - x0, y1 - y0
    length_sq = dx * dx + dy * dy
    if length_sq < 1e-9:
        return math.hypot(px - x0, py - y0)
    t = max(0.0, min(1.0, ((px - x0) * dx + (py - y0) * dy) / length_sq))
    return math.hypot(px - (x0 + dx * t), py - (y0 + dy * t))
