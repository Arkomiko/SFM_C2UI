"""
Rigid transforms the way Source stores them: a position and a quaternion, or
a 3x4 matrix (three rows of four, row-major, the last column the translation).

Pure Python, no dependencies, exact enough for bones. The renderer turns the
result into whatever its API wants; nothing here knows about OpenGL.

    m = matrix_from(position, quaternion)
    world = multiply(parent_world, m)
    p = apply(world, point)
"""
from __future__ import annotations

import math
from typing import List, Sequence, Tuple

__all__ = ["Mat34", "IDENTITY", "matrix_from", "multiply", "apply", "apply_direction",
           "invert", "quaternion_to_matrix", "quaternion_multiply", "quaternion_normalize",
           "quaternion_from_angles", "quaternion_slerp", "to_column_major_4x4", "translation_of"]

Mat34 = Tuple[float, ...]            # 12 values: r0c0 r0c1 r0c2 r0c3  r1c0 ...  r2c3
Quat = Tuple[float, float, float, float]
Vec3 = Tuple[float, float, float]

IDENTITY: Mat34 = (1.0, 0.0, 0.0, 0.0,
                   0.0, 1.0, 0.0, 0.0,
                   0.0, 0.0, 1.0, 0.0)


def quaternion_normalize(q: Quat) -> Quat:
    x, y, z, w = q
    n = math.sqrt(x * x + y * y + z * z + w * w)
    if n < 1e-12:
        return (0.0, 0.0, 0.0, 1.0)
    return (x / n, y / n, z / n, w / n)


def quaternion_to_matrix(q: Quat) -> Tuple[float, ...]:
    """3x3 rotation, row-major, nine values.  `q` is x, y, z, w as stored."""
    x, y, z, w = quaternion_normalize(q)
    xx, yy, zz = x * x, y * y, z * z
    xy, xz, yz = x * y, x * z, y * z
    wx, wy, wz = w * x, w * y, w * z
    return (1 - 2 * (yy + zz), 2 * (xy - wz), 2 * (xz + wy),
            2 * (xy + wz), 1 - 2 * (xx + zz), 2 * (yz - wx),
            2 * (xz - wy), 2 * (yz + wx), 1 - 2 * (xx + yy))


def quaternion_multiply(a: Quat, b: Quat) -> Quat:
    """The Hamilton product a * b: the rotation `b` followed by `a`, like matrices."""
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
            aw * bw - ax * bx - ay * by - az * bz)


def quaternion_from_angles(pitch: float, yaw: float, roll: float) -> Quat:
    """Source's QAngle (degrees: pitch about Y, yaw about Z, roll about X)."""
    sy, cy = math.sin(math.radians(yaw) / 2), math.cos(math.radians(yaw) / 2)
    sp, cp = math.sin(math.radians(pitch) / 2), math.cos(math.radians(pitch) / 2)
    sr, cr = math.sin(math.radians(roll) / 2), math.cos(math.radians(roll) / 2)
    return (sr * cp * cy - cr * sp * sy,
            cr * sp * cy + sr * cp * sy,
            cr * cp * sy - sr * sp * cy,
            cr * cp * cy + sr * sp * sy)


def quaternion_slerp(a: Quat, b: Quat, t: float) -> Quat:
    """Shortest-arc interpolation, `t` from 0 (a) to 1 (b)."""
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    cos = ax * bx + ay * by + az * bz + aw * bw
    if cos < 0.0:
        bx, by, bz, bw, cos = -bx, -by, -bz, -bw, -cos
    if cos > 0.9995:
        return quaternion_normalize((ax + (bx - ax) * t, ay + (by - ay) * t,
                                     az + (bz - az) * t, aw + (bw - aw) * t))
    theta = math.acos(cos)
    s = math.sin(theta)
    wa = math.sin((1 - t) * theta) / s
    wb = math.sin(t * theta) / s
    return (ax * wa + bx * wb, ay * wa + by * wb, az * wa + bz * wb, aw * wa + bw * wb)


def matrix_from(position: Vec3, rotation: Quat) -> Mat34:
    r = quaternion_to_matrix(rotation)
    return (r[0], r[1], r[2], position[0],
            r[3], r[4], r[5], position[1],
            r[6], r[7], r[8], position[2])


def multiply(a: Mat34, b: Mat34) -> Mat34:
    """`a` applied after `b`: the result maps a point through `b` then `a`."""
    return (
        a[0] * b[0] + a[1] * b[4] + a[2] * b[8],
        a[0] * b[1] + a[1] * b[5] + a[2] * b[9],
        a[0] * b[2] + a[1] * b[6] + a[2] * b[10],
        a[0] * b[3] + a[1] * b[7] + a[2] * b[11] + a[3],
        a[4] * b[0] + a[5] * b[4] + a[6] * b[8],
        a[4] * b[1] + a[5] * b[5] + a[6] * b[9],
        a[4] * b[2] + a[5] * b[6] + a[6] * b[10],
        a[4] * b[3] + a[5] * b[7] + a[6] * b[11] + a[7],
        a[8] * b[0] + a[9] * b[4] + a[10] * b[8],
        a[8] * b[1] + a[9] * b[5] + a[10] * b[9],
        a[8] * b[2] + a[9] * b[6] + a[10] * b[10],
        a[8] * b[3] + a[9] * b[7] + a[10] * b[11] + a[11],
    )


def apply(m: Mat34, p: Vec3) -> Vec3:
    x, y, z = p
    return (m[0] * x + m[1] * y + m[2] * z + m[3],
            m[4] * x + m[5] * y + m[6] * z + m[7],
            m[8] * x + m[9] * y + m[10] * z + m[11])


def apply_direction(m: Mat34, d: Vec3) -> Vec3:
    x, y, z = d
    return (m[0] * x + m[1] * y + m[2] * z,
            m[4] * x + m[5] * y + m[6] * z,
            m[8] * x + m[9] * y + m[10] * z)


def invert(m: Mat34) -> Mat34:
    """Inverse of a rotation + translation (no scale): transpose and re-translate."""
    r = (m[0], m[4], m[8],
         m[1], m[5], m[9],
         m[2], m[6], m[10])
    t = (m[3], m[7], m[11])
    return (r[0], r[1], r[2], -(r[0] * t[0] + r[1] * t[1] + r[2] * t[2]),
            r[3], r[4], r[5], -(r[3] * t[0] + r[4] * t[1] + r[5] * t[2]),
            r[6], r[7], r[8], -(r[6] * t[0] + r[7] * t[1] + r[8] * t[2]))


def translation_of(m: Mat34) -> Vec3:
    return (m[3], m[7], m[11])


def to_column_major_4x4(m: Mat34) -> Tuple[float, ...]:
    """The 16-value column-major form OpenGL takes."""
    return (m[0], m[4], m[8], 0.0,
            m[1], m[5], m[9], 0.0,
            m[2], m[6], m[10], 0.0,
            m[3], m[7], m[11], 1.0)
