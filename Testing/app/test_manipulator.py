"""
The manipulator with a fake orthographic projector: hits, drags, rotations.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from App.Code.render.manipulator import MOVE, ROTATE, Manipulator


def project(point):
    """An orthographic camera looking down -Y: x right, z up, depth = -y."""
    x, y, z = point
    return (100 + x * 4, 100 - z * 4, -y)


def test_lines_cover_the_axes_and_rings_when_rotating():
    m = Manipulator()
    assert m.lines(10) == []
    m.place((0, 0, 0))
    assert len(m.lines(10)) == 9                       # 3 axes with 2 arrow strokes each
    m.mode = ROTATE
    assert len(m.lines(10)) == 9 + 3 * 32
    assert m.lines(10)[0][0] == (0, 0, 0) and m.lines(10)[0][1] == (10, 0, 0)


def test_hit_finds_the_nearest_axis_and_nothing_far_away():
    m = Manipulator()
    m.place((0, 0, 0))
    size = 10.0
    assert m.hit(100 + 20, 100 + 3, project, size) == 0         # along +X on screen
    assert m.hit(100 - 2, 100 - 25, project, size) == 2         # along +Z (up on screen)
    assert m.hit(100 + 20, 100 - 20, project, size) is None     # off both
    assert m.hit(300, 300, project, size) is None


def test_move_drag_follows_the_axis_in_world_units():
    m = Manipulator()
    m.place((0, 0, 0))
    size = 10.0
    m.begin(0, 120, 100, project)
    delta = m.drag(140, 100, project, size)                     # 20 px = half the 40 px axis
    assert tuple(round(v, 6) for v in delta) == (5.0, 0.0, 0.0)
    delta = m.drag(140, 130, project, size)                     # sideways motion is ignored
    assert tuple(round(v, 6) for v in delta) == (5.0, 0.0, 0.0)
    m.begin(2, 100, 80, project)
    delta = m.drag(100, 40, project, size)                      # 40 px up = a full axis
    assert tuple(round(v, 6) for v in delta) == (0.0, 0.0, 10.0)
    m.end()
    assert m.active is None


def test_rotation_axes_follow_the_placed_frame():
    m = Manipulator()
    quarter = (0, 0, math.sin(math.pi / 4), math.cos(math.pi / 4))   # 90 degrees about Z
    m.place((0, 0, 0), quarter)
    x, y, z = m.axes
    assert tuple(round(v, 6) for v in x) == (0.0, 1.0, 0.0)
    assert tuple(round(v, 6) for v in y) == (-1.0, 0.0, 0.0)
    assert tuple(round(v, 6) for v in z) == (0.0, 0.0, 1.0)


def test_rotate_drag_gives_an_angle_about_the_axis():
    m = Manipulator()
    m.mode = ROTATE
    m.place((0, 0, 0))
    m.begin(1, 140, 100, project)                                # on the Y ring, to the right of the origin
    axis, angle = m.drag(100, 60, project, 10.0)                 # a quarter turn on screen
    assert axis == (0, 1, 0)
    assert abs(abs(angle) - math.pi / 2) < 1e-6


def test_hide_clears_everything():
    m = Manipulator()
    m.place((1, 2, 3))
    m.begin(0, 0, 0, project)
    m.hide()
    assert not m.visible and m.active is None and m.drag(5, 5, project, 1.0) is None
