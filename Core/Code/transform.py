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
from typing import Tuple

__all__ = ["Mat34", "IDENTITY", "matrix_from", "multiply", "apply", "apply_direction",
           "invert", "quaternion_to_matrix", "quaternion_multiply", "quaternion_normalize",
           "quaternion_from_angles", "quaternion_slerp", "to_column_major_4x4", "translation_of",
           "matrix_to_quaternion", "quaternion_inverse", "rotation_between", "rotate_vector",
           "quaternion_from_axis_angle", "angles_from_quaternion"]

Mat34 = Tuple[float, ...]            # 12 values: r0c0 r0c1 r0c2 r0c3  r1c0 ...  r2c3
Quat = Tuple[float, float, float, float]
Vec3 = Tuple[float, float, float]

IDENTITY: Mat34 = (1.0, 0.0, 0.0, 0.0,
                   0.0, 1.0, 0.0, 0.0,
                   0.0, 0.0, 1.0, 0.0)


def quaternion_normalize(q: Quat) -> Quat:
    """Unit quaternion; identity for a zero input."""
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


def angles_from_quaternion(q: Quat) -> Tuple[float, float, float]:
    """The QAngle (pitch, yaw, roll in degrees) a rotation came from; Source's MatrixAngles."""
    m = quaternion_to_matrix(q)
    forward = (m[0], m[3], m[6])                         # first column
    left = (m[1], m[4], m[7])
    up_z = m[8]
    xy = math.sqrt(forward[0] * forward[0] + forward[1] * forward[1])
    if xy > 0.001:
        yaw = math.atan2(forward[1], forward[0])
        pitch = math.atan2(-forward[2], xy)
        roll = math.atan2(left[2], up_z)
    else:                                                # looking straight up or down: roll is folded into yaw
        yaw = math.atan2(-left[0], left[1])
        pitch = math.atan2(-forward[2], xy)
        roll = 0.0
    return (math.degrees(pitch), math.degrees(yaw), math.degrees(roll))


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


def matrix_to_quaternion(m: Mat34) -> Quat:
    """The rotation of a rigid matrix as x, y, z, w (Shepperd's method)."""
    r00, r01, r02 = m[0], m[1], m[2]
    r10, r11, r12 = m[4], m[5], m[6]
    r20, r21, r22 = m[8], m[9], m[10]
    trace = r00 + r11 + r22
    if trace > 0.0:
        s = math.sqrt(trace + 1.0) * 2.0
        return quaternion_normalize(((r21 - r12) / s, (r02 - r20) / s, (r10 - r01) / s, 0.25 * s))
    if r00 > r11 and r00 > r22:
        s = math.sqrt(1.0 + r00 - r11 - r22) * 2.0
        return quaternion_normalize((0.25 * s, (r01 + r10) / s, (r02 + r20) / s, (r21 - r12) / s))
    if r11 > r22:
        s = math.sqrt(1.0 + r11 - r00 - r22) * 2.0
        return quaternion_normalize(((r01 + r10) / s, 0.25 * s, (r12 + r21) / s, (r02 - r20) / s))
    s = math.sqrt(1.0 + r22 - r00 - r11) * 2.0
    return quaternion_normalize(((r02 + r20) / s, (r12 + r21) / s, 0.25 * s, (r10 - r01) / s))


def quaternion_inverse(q: Quat) -> Quat:
    """The rotation that undoes `q`."""
    x, y, z, w = quaternion_normalize(q)
    return (-x, -y, -z, w)


def rotation_between(a: Vec3, b: Vec3) -> Quat:
    """The shortest rotation taking direction `a` onto direction `b`."""
    ax, ay, az = a
    bx, by, bz = b
    la = math.sqrt(ax * ax + ay * ay + az * az)
    lb = math.sqrt(bx * bx + by * by + bz * bz)
    if la < 1e-9 or lb < 1e-9:
        return (0.0, 0.0, 0.0, 1.0)
    ax, ay, az = ax / la, ay / la, az / la
    bx, by, bz = bx / lb, by / lb, bz / lb
    d = ax * bx + ay * by + az * bz
    if d < -0.999999:
        # opposite: turn half a circle about any perpendicular axis
        px, py, pz = (0.0, -az, ay) if abs(ax) < 0.9 else (-az, 0.0, ax)
        n = math.sqrt(px * px + py * py + pz * pz) or 1.0
        return (px / n, py / n, pz / n, 0.0)
    cx = ay * bz - az * by
    cy = az * bx - ax * bz
    cz = ax * by - ay * bx
    return quaternion_normalize((cx, cy, cz, 1.0 + d))


def quaternion_from_axis_angle(axis: Vec3, angle: float) -> Quat:
    """Rotation of `angle` radians about `axis`."""
    x, y, z = axis
    n = math.sqrt(x * x + y * y + z * z)
    if n < 1e-12:
        return (0.0, 0.0, 0.0, 1.0)
    s = math.sin(angle / 2.0) / n
    return (x * s, y * s, z * s, math.cos(angle / 2.0))


def rotate_vector(q: Quat, v: Vec3) -> Vec3:
    """Rotate a vector by a quaternion."""
    m = quaternion_to_matrix(q)
    return (m[0] * v[0] + m[1] * v[1] + m[2] * v[2],
            m[3] * v[0] + m[4] * v[1] + m[5] * v[2],
            m[6] * v[0] + m[7] * v[1] + m[8] * v[2])


def matrix_from(position: Vec3, rotation: Quat) -> Mat34:
    """A 3x4 matrix from a position and a rotation."""
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
    """Transform a point."""
    x, y, z = p
    return (m[0] * x + m[1] * y + m[2] * z + m[3],
            m[4] * x + m[5] * y + m[6] * z + m[7],
            m[8] * x + m[9] * y + m[10] * z + m[11])


def apply_direction(m: Mat34, d: Vec3) -> Vec3:
    """Transform a direction (no translation)."""
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
    """The translation column."""
    return (m[3], m[7], m[11])


def to_column_major_4x4(m: Mat34) -> Tuple[float, ...]:
    """The 16-value column-major form OpenGL takes."""
    return (m[0], m[4], m[8], 0.0,
            m[1], m[5], m[9], 0.0,
            m[2], m[6], m[10], 0.0,
            m[3], m[7], m[11], 1.0)
