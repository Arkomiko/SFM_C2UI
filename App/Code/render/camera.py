"""
An orbit camera: the viewport's default way of looking at a model.

It circles a target point at a distance, with yaw and pitch about a chosen up
axis. Source content does not agree on which axis is up (see the model notes:
Y in most re-exported models, Z in the rest), so the up axis is a property,
and `frame()` can guess it from the model's shape.

    cam = OrbitCamera()
    cam.frame(model.bounds())          # fit the model, guess its up axis
    cam.orbit(dx, dy); cam.dolly(steps); cam.pan(dx, dy)
    cam.view(), cam.projection(aspect)
"""
from __future__ import annotations

import math
from typing import Tuple

from .math3d import (Mat4, Vec3, add, cross, length, look_at, normalize, perspective, scale,
                     sub)

__all__ = ["OrbitCamera", "UP_AXES"]

UP_AXES = {
    "x": (1.0, 0.0, 0.0),
    "y": (0.0, 1.0, 0.0),
    "z": (0.0, 0.0, 1.0),
}

Bounds = Tuple[Vec3, Vec3]


class OrbitCamera:
    def __init__(self) -> None:
        self.target: Vec3 = (0.0, 0.0, 0.0)
        self.distance = 100.0
        self.yaw = math.radians(35.0)
        self.pitch = math.radians(20.0)
        self.fov_y = math.radians(45.0)
        self.up_axis = "z"
        self.min_distance = 0.5
        self.max_distance = 100000.0
        self._pitch_limit = math.radians(89.0)

    # -- framing -----------------------------------------------------------------
    @staticmethod
    def guess_up_axis(bounds: Bounds) -> str:
        """Which axis a model is standing on.

        Source models put their origin at the feet, so along the up axis the
        geometry starts at about zero and goes up; along the other axes it is
        spread to both sides. Of the axes that look like that, the tallest
        wins. Models centred on their origin (many props) give no such hint,
        and then the tallest axis is taken. Over 693 installed models the
        ground test answers for 425 and agrees with the eye position wherever
        one is stored. A heuristic all the same: the user can override it.
        """
        lo, hi = bounds
        extents = [hi[i] - lo[i] for i in range(3)]
        if max(extents) <= 0.0:
            return "z"
        grounded = [i for i in range(3)
                    if extents[i] > 0.0 and hi[i] > 0.0 and lo[i] >= -0.15 * extents[i]]
        if grounded:
            return "xyz"[max(grounded, key=lambda i: extents[i])]
        return "xyz"[extents.index(max(extents))]

    def frame(self, bounds: Bounds, guess_up: bool = True) -> None:
        """Move so the whole box is in view."""
        lo, hi = bounds
        if guess_up:
            self.up_axis = self.guess_up_axis(bounds)
        self.target = tuple((lo[i] + hi[i]) / 2.0 for i in range(3))
        radius = length(sub(hi, lo)) / 2.0
        if radius <= 0.0:
            radius = 10.0
        # the sphere must fit the narrower field of view; add a little air
        self.distance = radius / math.sin(self.fov_y / 2.0) * 1.1
        self.distance = min(max(self.distance, self.min_distance), self.max_distance)

    # -- basis -------------------------------------------------------------------
    @property
    def up(self) -> Vec3:
        return UP_AXES[self.up_axis]

    def _basis(self) -> Tuple[Vec3, Vec3]:
        """Two horizontal unit vectors perpendicular to the up axis."""
        up = self.up
        forward = (1.0, 0.0, 0.0) if self.up_axis != "x" else (0.0, 0.0, 1.0)
        right = normalize(cross(forward, up))
        forward = normalize(cross(up, right))
        return forward, right

    def eye(self) -> Vec3:
        forward, right = self._basis()
        cp = math.cos(self.pitch)
        offset = add(add(scale(forward, cp * math.cos(self.yaw)),
                         scale(right, cp * math.sin(self.yaw))),
                     scale(self.up, math.sin(self.pitch)))
        return add(self.target, scale(offset, self.distance))

    def view(self) -> Mat4:
        return look_at(self.eye(), self.target, self.up)

    def projection(self, aspect: float) -> Mat4:
        aspect = aspect if aspect > 1e-6 else 1.0
        near = max(self.distance * 0.01, 0.05)
        far = self.distance * 50.0 + 1000.0
        return perspective(self.fov_y, aspect, near, far)

    # -- interaction -------------------------------------------------------------
    def orbit(self, dx: float, dy: float, speed: float = 0.008) -> None:
        """`dx`/`dy` in pixels; dragging right turns the model to the right."""
        self.yaw -= dx * speed
        self.pitch += dy * speed
        self.pitch = max(-self._pitch_limit, min(self._pitch_limit, self.pitch))

    def dolly(self, steps: float) -> None:
        """Wheel steps: positive brings the camera closer."""
        factor = 0.85 ** steps
        self.distance = min(max(self.distance * factor, self.min_distance), self.max_distance)

    def pan(self, dx: float, dy: float, viewport_height: int) -> None:
        """Slide the target across the view plane by a pixel delta."""
        if viewport_height <= 0:
            return
        forward, right = self._basis()
        # world units per pixel at the target's depth
        per_pixel = 2.0 * self.distance * math.tan(self.fov_y / 2.0) / viewport_height
        eye_dir = normalize(sub(self.target, self.eye()))
        screen_right = normalize(cross(eye_dir, self.up))
        screen_up = cross(screen_right, eye_dir)
        self.target = add(self.target, scale(screen_right, -dx * per_pixel))
        self.target = add(self.target, scale(screen_up, dy * per_pixel))

    def describe(self) -> str:
        return (f"target {tuple(round(v, 1) for v in self.target)} dist {self.distance:.1f} "
                f"yaw {math.degrees(self.yaw):.0f} pitch {math.degrees(self.pitch):.0f} up {self.up_axis}")
