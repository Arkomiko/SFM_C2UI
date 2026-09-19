"""
Camera and matrix maths, checked by hand-computable cases.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from App.Code.render import math3d as m
from App.Code.render.camera import OrbitCamera


def _close(a, b, eps=1e-6):
    return all(abs(x - y) <= eps for x, y in zip(a, b)) and len(a) == len(b)


# ------------------------------------------------------------------- vectors
def test_vector_basics():
    assert m.add((1, 2, 3), (1, 1, 1)) == (2, 3, 4)
    assert m.sub((1, 2, 3), (1, 1, 1)) == (0, 1, 2)
    assert m.dot((1, 0, 0), (0, 1, 0)) == 0
    assert m.cross((1, 0, 0), (0, 1, 0)) == (0, 0, 1)
    assert m.length((3, 4, 0)) == 5
    assert _close(m.normalize((0, 0, 5)), (0, 0, 1))
    assert m.normalize((0, 0, 0)) == (0, 0, 0)


# ------------------------------------------------------------------- matrices
def test_identity_and_translation():
    assert m.multiply(m.IDENTITY, m.IDENTITY) == m.IDENTITY
    t = m.translation((1, 2, 3))
    assert m.transform_point(t, (0, 0, 0)) == (1, 2, 3)
    assert m.transform_direction(t, (1, 0, 0)) == (1, 0, 0)     # directions ignore translation


def test_multiply_applies_right_then_left():
    t = m.translation((10, 0, 0))
    r = m.rotation_axis((0, 0, 1), math.pi / 2)             # x -> y
    p = m.transform_point(m.multiply(t, r), (1, 0, 0))       # rotate, then translate
    assert _close(p, (10, 1, 0))
    p = m.transform_point(m.multiply(r, t), (1, 0, 0))       # translate, then rotate
    assert _close(p, (0, 11, 0))


def test_rotation_is_right_handed():
    r = m.rotation_axis((0, 0, 1), math.pi / 2)
    assert _close(m.transform_point(r, (1, 0, 0)), (0, 1, 0))
    r = m.rotation_axis((1, 0, 0), math.pi / 2)
    assert _close(m.transform_point(r, (0, 1, 0)), (0, 0, 1))


def test_look_at_puts_the_target_ahead():
    view = m.look_at(eye=(0, -10, 0), target=(0, 0, 0), up=(0, 0, 1))
    p = m.transform_point(view, (0, 0, 0))
    assert _close(p, (0, 0, -10))                             # ahead is -Z in view space
    p = m.transform_point(view, (0, 0, 1))
    assert _close(p, (0, 1, -10))                             # up stays up


def test_look_at_works_with_any_up_axis():
    for up, eye in (((0, 1, 0), (0, 0, 5)), ((0, 0, 1), (0, -5, 0)), ((1, 0, 0), (0, -5, 0))):
        view = m.look_at(eye, (0, 0, 0), up)
        top = m.transform_point(view, up)
        centre = m.transform_point(view, (0, 0, 0))
        assert top[1] > centre[1], up                        # the up axis rises on screen


def test_look_at_along_the_up_axis_does_not_degenerate():
    view = m.look_at((0, 0, 10), (0, 0, 0), (0, 0, 1))
    assert all(math.isfinite(v) for v in view)
    assert _close(m.transform_point(view, (0, 0, 0)), (0, 0, -10))


def test_perspective_maps_near_and_far_to_clip_range():
    proj = m.perspective(math.radians(90), 1.0, 1.0, 100.0)
    assert _close(m.transform_point(proj, (0, 0, -1)), (0, 0, -1))
    assert _close(m.transform_point(proj, (0, 0, -100)), (0, 0, 1), 1e-4)
    # at 90 degrees the edge of the view at depth d is at x = d
    assert _close(m.transform_point(proj, (5, 0, -5)), (1, 0, 305 / 495), 1e-6)


def test_inverse_rigid_undoes_a_view():
    view = m.look_at((3, -7, 2), (0, 1, 0), (0, 0, 1))
    inverse = m.inverse_rigid(view)
    p = (1.5, -2.0, 4.0)
    assert _close(m.transform_point(inverse, m.transform_point(view, p)), p, 1e-6)


def test_transpose():
    t = m.transpose(m.translation((1, 2, 3)))
    assert (t[3], t[7], t[11]) == (1, 2, 3)                   # last column became last row
    assert m.transpose(t) == m.translation((1, 2, 3))


# ------------------------------------------------------------------- camera
def test_frame_fits_the_bounds_and_guesses_up():
    cam = OrbitCamera()
    cam.frame(((-10, 0, -10), (10, 80, 10)))
    assert cam.up_axis == "y"
    assert _close(cam.target, (0, 40, 0))
    # the far corner must be inside the field of view
    radius = m.length((10, 40, 10))
    assert cam.distance > radius / math.sin(cam.fov_y / 2)


def test_up_axis_prefers_the_axis_the_model_stands_on():
    # a wide pose: arms span 90 along X, height 71 along Z, feet at z=0
    assert OrbitCamera.guess_up_axis(((-45, -20, -0.2), (45, 15, 71))) == "z"
    # the same shape centred on its origin gives no hint: tallest wins
    assert OrbitCamera.guess_up_axis(((-45, -20, -35), (45, 15, 36))) == "x"
    # a Y-up character with feet at y=0
    assert OrbitCamera.guess_up_axis(((-15, 0, -16), (15, 82, 7))) == "y"


def test_frame_of_nothing_still_gives_a_usable_camera():
    cam = OrbitCamera()
    cam.frame(((0, 0, 0), (0, 0, 0)))
    assert cam.distance > 0 and cam.up_axis == "z"
    assert all(math.isfinite(v) for v in cam.view())


def test_eye_orbits_at_the_set_distance():
    cam = OrbitCamera()
    cam.target = (1, 2, 3)
    cam.distance = 50
    for yaw in (0, 1, 2, 3):
        cam.yaw = yaw
        assert abs(m.length(m.sub(cam.eye(), cam.target)) - 50) < 1e-9


def test_pitch_is_clamped():
    cam = OrbitCamera()
    cam.orbit(0, 100000)
    assert cam.pitch < math.pi / 2
    cam.orbit(0, -100000)
    assert cam.pitch > -math.pi / 2


def test_dolly_moves_closer_and_is_bounded():
    cam = OrbitCamera()
    before = cam.distance
    cam.dolly(1)
    assert cam.distance < before
    cam.dolly(-1000)
    assert cam.distance == cam.max_distance
    cam.dolly(1000)
    assert cam.distance == cam.min_distance


def test_pan_moves_the_target_across_the_view():
    cam = OrbitCamera()
    cam.frame(((-1, -1, -1), (1, 1, 1)))
    before = cam.target
    line = m.normalize(m.sub(before, cam.eye()))
    cam.pan(100, 0, 400)
    moved = m.sub(cam.target, before)
    assert m.length(moved) > 0
    # panning never moves along the line of sight
    assert abs(m.dot(m.normalize(moved), line)) < 1e-6


def test_up_axis_is_respected_by_the_view():
    cam = OrbitCamera()
    cam.up_axis = "y"
    cam.target = (0, 0, 0)
    cam.pitch = 0.0
    view = cam.view()
    top = m.transform_point(view, (0, 1, 0))
    centre = m.transform_point(view, (0, 0, 0))
    assert top[1] > centre[1]


def test_look_from_reproduces_the_eye():
    cam = OrbitCamera()
    cam.up_axis = "z"
    for eye, target in (((100, 0, 40), (0, 0, 40)), ((-30, 50, 90), (10, -5, 20)), ((0, 0, 200), (0, 0, 0))):
        cam.look_from(eye, target, fov_y=1.0)
        assert _close(cam.eye(), eye, 1e-6), (eye, cam.eye())
        assert _close(cam.target, target)
    assert cam.fov_y == 1.0
