"""
The viewport camera: orbits a target, or looks and flies like SFM's.

The state is a target point, a distance and yaw / pitch about a chosen up
axis; the eye follows from those.  `orbit`, `dolly` and `pan` move about the
target; `look` turns about the eye instead (the target swings with it) and
`fly` moves the whole camera along its own axes - SFM's right-drag and WASD.
Source content does not agree on which axis is up (Y in most re-exported
models, Z in the rest), so the up axis is a property and `frame()` can guess
it from the model's shape.

    cam = OrbitCamera()
    cam.frame(model.bounds())          # fit the model, guess its up axis
    cam.orbit(dx, dy); cam.dolly(steps); cam.pan(dx, dy, height)
    cam.look(dx, dy); cam.fly(forward, right, up); cam.tilt(dx)
    cam.view(), cam.projection(aspect)
"""
from __future__ import annotations

import math
from typing import Optional, Tuple

from .math3d import (Mat4, Vec3, add, cross, dot, length, look_at, normalize, perspective,
                     scale, sub)

__all__ = ["OrbitCamera", "UP_AXES"]

UP_AXES = {
    "x": (1.0, 0.0, 0.0),
    "y": (0.0, 1.0, 0.0),
    "z": (0.0, 0.0, 1.0),
}

Bounds = Tuple[Vec3, Vec3]


class OrbitCamera:
    """The viewport camera: orbit about a target or fly freely."""
    def __init__(self) -> None:
        self.target: Vec3 = (0.0, 0.0, 0.0)
        #: tilt about the view direction, radians (SFM's R + mouse)
        self.roll = 0.0
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

    def look_from(self, eye: Vec3, target: Vec3, fov_y: Optional[float] = None) -> None:
        """Place the orbit so the view matches a camera at `eye` looking at `target`."""
        self.target = tuple(target)
        offset = sub(eye, target)
        self.distance = min(max(length(offset), self.min_distance), self.max_distance)
        if self.distance <= 0.0:
            return
        d = scale(offset, 1.0 / length(offset))
        forward, right = self._basis()
        self.pitch = math.asin(max(-1.0, min(1.0, dot(d, self.up))))
        self.yaw = math.atan2(dot(d, right), dot(d, forward))
        if fov_y is not None:
            self.fov_y = fov_y

    # -- basis -------------------------------------------------------------------
    @property
    def up(self) -> Vec3:
        """World up for the current up axis."""
        return UP_AXES[self.up_axis]

    def _basis(self) -> Tuple[Vec3, Vec3]:
        """Two horizontal unit vectors perpendicular to the up axis."""
        up = self.up
        forward = (1.0, 0.0, 0.0) if self.up_axis != "x" else (0.0, 0.0, 1.0)
        right = normalize(cross(forward, up))
        forward = normalize(cross(up, right))
        return forward, right

    def eye(self) -> Vec3:
        """Where the camera is."""
        forward, right = self._basis()
        cp = math.cos(self.pitch)
        offset = add(add(scale(forward, cp * math.cos(self.yaw)),
                         scale(right, cp * math.sin(self.yaw))),
                     scale(self.up, math.sin(self.pitch)))
        return add(self.target, scale(offset, self.distance))

    def view(self) -> Mat4:
        """The view matrix."""
        return look_at(self.eye(), self.target, self.rolled_up())

    def rolled_up(self) -> Vec3:
        """The up vector with `roll` applied: turned about the view direction."""
        up = self.up
        if abs(self.roll) < 1e-9:
            return up
        forward = normalize(sub(self.target, self.eye()))
        cos_a, sin_a = math.cos(self.roll), math.sin(self.roll)
        # Rodrigues about the view direction
        return normalize(add(add(scale(up, cos_a), scale(cross(forward, up), sin_a)),
                             scale(forward, dot(forward, up) * (1.0 - cos_a))))

    def tilt(self, dx: float, speed: float = 0.004) -> None:
        """Roll the camera, as holding R and moving the mouse sideways does in SFM."""
        self.roll += dx * speed

    def depth_range(self) -> Tuple[float, float]:
        """Near and far clip distances.  Both scale with the distance to the target,
        so a model an inch across and a map a mile across each get the precision."""
        return max(self.distance * 0.01, 0.05), self.distance * 50.0 + 1000.0

    def projection(self, aspect: float) -> Mat4:
        """A perspective matrix for this aspect ratio."""
        aspect = aspect if aspect > 1e-6 else 1.0
        near, far = self.depth_range()
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

    # -- SFM's camera: look from where the eye is, fly through the scene --------------
    def look(self, dx: float, dy: float, speed: float = 0.004) -> None:
        """Turn the camera about its own eye (right-drag in SFM); the target follows."""
        eye = self.eye()
        self.yaw -= dx * speed
        self.pitch -= dy * speed
        self.pitch = max(-self._pitch_limit, min(self._pitch_limit, self.pitch))
        offset = sub(self.eye(), self.target)             # the new eye-from-target offset
        self.target = sub(eye, offset)                    # keep the eye where it was

    def screen_axes(self) -> Tuple[Vec3, Vec3, Vec3]:
        """Forward, right and up as the viewer sees them, roll included."""
        forward = normalize(sub(self.target, self.eye()))
        up = self.rolled_up()
        right = normalize(cross(forward, up))
        return forward, right, cross(right, forward)

    def fly(self, forward: float, right: float, up: float) -> None:
        """Move eye and target together by world units along the view axes (WASD in SFM)."""
        f, r, u = self.screen_axes()
        step = add(add(scale(f, forward), scale(r, right)), scale(u, up))
        self.target = add(self.target, step)

    def describe(self) -> str:
        """One line for the status bar."""
        return (f"target {tuple(round(v, 1) for v in self.target)} dist {self.distance:.1f} "
                f"yaw {math.degrees(self.yaw):.0f} pitch {math.degrees(self.pitch):.0f} up {self.up_axis}")
