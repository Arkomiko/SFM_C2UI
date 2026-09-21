"""
Just enough linear algebra for a viewport.

Matrices are 4x4, column-major, flat tuples of 16 floats - the layout OpenGL
takes without transposing. Vectors are 3-tuples. Everything is pure Python so
the camera can be tested without a GPU or numpy; the renderer only needs to
hand the result to a uniform.

    mvp = multiply(projection, view)
    look = look_at(eye, target, up)
"""
from __future__ import annotations

import math
from typing import Tuple

__all__ = [
    "Vec3", "Mat4", "IDENTITY",
    "add", "sub", "scale", "dot", "cross", "length", "normalize",
    "multiply", "transform_point", "transform_direction", "transpose",
    "perspective", "orthographic", "look_at", "translation", "rotation_axis",
    "inverse_rigid",
]

Vec3 = Tuple[float, float, float]
Mat4 = Tuple[float, ...]

IDENTITY: Mat4 = (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)


# ---------------------------------------------------------------------------
#  Vectors
# ---------------------------------------------------------------------------
def add(a: Vec3, b: Vec3) -> Vec3:
    """a + b"""
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


def sub(a: Vec3, b: Vec3) -> Vec3:
    """a - b"""
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]


def scale(a: Vec3, s: float) -> Vec3:
    """a * s"""
    return a[0] * s, a[1] * s, a[2] * s


def dot(a: Vec3, b: Vec3) -> float:
    """Dot product."""
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec3, b: Vec3) -> Vec3:
    """Cross product."""
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def length(a: Vec3) -> float:
    """Euclidean length."""
    return math.sqrt(dot(a, a))


def normalize(a: Vec3) -> Vec3:
    """Unit vector; zero for a zero input."""
    n = length(a)
    return (a[0] / n, a[1] / n, a[2] / n) if n > 1e-12 else (0.0, 0.0, 0.0)


# ---------------------------------------------------------------------------
#  Matrices (column-major: element (row r, column c) is at index c*4 + r)
# ---------------------------------------------------------------------------
def multiply(a: Mat4, b: Mat4) -> Mat4:
    """`a` applied after `b`, as in OpenGL's ``P * V * M``."""
    out = [0.0] * 16
    for c in range(4):
        for r in range(4):
            out[c * 4 + r] = (a[r] * b[c * 4] + a[4 + r] * b[c * 4 + 1]
                              + a[8 + r] * b[c * 4 + 2] + a[12 + r] * b[c * 4 + 3])
    return tuple(out)


def transpose(m: Mat4) -> Mat4:
    """Transpose a column-major 4x4."""
    return tuple(m[r * 4 + c] for c in range(4) for r in range(4))


def transform_point(m: Mat4, p: Vec3) -> Vec3:
    """Transform a point, dividing by w."""
    x, y, z = p
    w = m[3] * x + m[7] * y + m[11] * z + m[15]
    w = w if abs(w) > 1e-12 else 1.0
    return ((m[0] * x + m[4] * y + m[8] * z + m[12]) / w,
            (m[1] * x + m[5] * y + m[9] * z + m[13]) / w,
            (m[2] * x + m[6] * y + m[10] * z + m[14]) / w)


def transform_direction(m: Mat4, d: Vec3) -> Vec3:
    """Transform a direction (no translation)."""
    x, y, z = d
    return (m[0] * x + m[4] * y + m[8] * z,
            m[1] * x + m[5] * y + m[9] * z,
            m[2] * x + m[6] * y + m[10] * z)


def translation(t: Vec3) -> Mat4:
    """A translation matrix."""
    return (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, t[0], t[1], t[2], 1)


def rotation_axis(axis: Vec3, angle: float) -> Mat4:
    """Rotation of `angle` radians about a unit `axis` (right-handed)."""
    x, y, z = normalize(axis)
    c, s = math.cos(angle), math.sin(angle)
    t = 1.0 - c
    return (t * x * x + c, t * x * y + s * z, t * x * z - s * y, 0,
            t * x * y - s * z, t * y * y + c, t * y * z + s * x, 0,
            t * x * z + s * y, t * y * z - s * x, t * z * z + c, 0,
            0, 0, 0, 1)


def perspective(fov_y: float, aspect: float, near: float, far: float) -> Mat4:
    """Right-handed, camera looking down -Z, depth mapped to -1..1."""
    f = 1.0 / math.tan(fov_y / 2.0)
    return (f / aspect, 0, 0, 0,
            0, f, 0, 0,
            0, 0, (far + near) / (near - far), -1,
            0, 0, 2 * far * near / (near - far), 0)


def orthographic(left: float, right: float, bottom: float, top: float,
                 near: float, far: float) -> Mat4:
    """An orthographic projection matrix."""
    return (2 / (right - left), 0, 0, 0,
            0, 2 / (top - bottom), 0, 0,
            0, 0, -2 / (far - near), 0,
            -(right + left) / (right - left), -(top + bottom) / (top - bottom),
            -(far + near) / (far - near), 1)


def look_at(eye: Vec3, target: Vec3, up: Vec3) -> Mat4:
    """A view matrix: world to a camera at `eye` looking at `target`.

    Works for any world up axis - the camera's own basis is built from the
    look direction and `up`, which is what lets Y-up and Z-up models share one
    code path.
    """
    f = normalize(sub(target, eye))
    if length(cross(f, up)) < 1e-6:
        # looking straight along the up axis: pick any perpendicular
        up = (1.0, 0.0, 0.0) if abs(f[0]) < 0.9 else (0.0, 1.0, 0.0)
    s = normalize(cross(f, up))
    u = cross(s, f)
    return (s[0], u[0], -f[0], 0,
            s[1], u[1], -f[1], 0,
            s[2], u[2], -f[2], 0,
            -dot(s, eye), -dot(u, eye), dot(f, eye), 1)


def inverse_rigid(m: Mat4) -> Mat4:
    """Inverse of a rotation + translation matrix (no scale)."""
    # the transposed rotation, row-major: row r of R^T is column r of R
    r = (m[0], m[1], m[2],
         m[4], m[5], m[6],
         m[8], m[9], m[10])
    t = (m[12], m[13], m[14])
    tx = -(r[0] * t[0] + r[1] * t[1] + r[2] * t[2])
    ty = -(r[3] * t[0] + r[4] * t[1] + r[5] * t[2])
    tz = -(r[6] * t[0] + r[7] * t[1] + r[8] * t[2])
    return (r[0], r[3], r[6], 0,
            r[1], r[4], r[7], 0,
            r[2], r[5], r[8], 0,
            tx, ty, tz, 1)
