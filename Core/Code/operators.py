"""
Operators: the part of a session that computes rather than plays back.

After the channels have written the moment's values, each animation set's
operators run in order:

* **DmeExpressionOperator** - `result = expr(attributes, time)`;
* **DmePackColorOperator**, **DmePackVector3Operator** - floats into a
  colour or a vector;
* **rig constraints** - point, orient, parent, aim and the two-bone IK. A
  constraint has targets (dags with weights and offsets) and a slave: the
  dag it drives, plus the unconstrained position and orientation the
  animation wrote, which the result blends with when the weights sum below
  one. The result is written into the slave dag's transform, in its
  parent's space, so the scene graph stays consistent.

Then the channels that merely pass a value along run again, so an
expression's result reaches the camera it drives.

    run_operators(shot, shot_time)
"""
from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple

from Core.API.dmx import AttrType, Element, Time
from Core.API.session import FilmClip

from .expression import ExpressionError, evaluate
from .transform import (IDENTITY, Mat34, apply, apply_direction, invert, matrix_from,
                        matrix_to_quaternion, multiply, quaternion_multiply, quaternion_normalize,
                        quaternion_slerp, rotation_between, translation_of)

__all__ = ["run_operators", "OperatorRunner"]

Vec3 = Tuple[float, float, float]
Quat = Tuple[float, float, float, float]


class OperatorRunner:
    """Runs a shot's operators against its scene graph."""

    def __init__(self, shot: FilmClip) -> None:
        self.shot = shot
        self.parent: Dict[int, Optional[Element]] = {}
        self.operators_run = 0
        self.errors: List[str] = []
        scene = shot.scene
        if scene is not None:
            self._index(scene.element, None)

    def _index(self, element: Element, parent: Optional[Element], depth: int = 0) -> None:
        if depth > 64 or id(element) in self.parent:
            return
        self.parent[id(element)] = parent
        children = element.get("children")
        if isinstance(children, list):
            for child in children:
                if isinstance(child, Element):
                    self._index(child, element, depth + 1)

    # -- transforms ------------------------------------------------------------------
    @staticmethod
    def local(element: Element) -> Mat34:
        """A dag element's local matrix."""
        t = element.get("transform")
        if not isinstance(t, Element):
            return IDENTITY
        return matrix_from(tuple(t.get("position", (0.0, 0.0, 0.0))),
                           tuple(t.get("orientation", (0.0, 0.0, 0.0, 1.0))))

    def world(self, element: Optional[Element]) -> Mat34:
        """A dag element's world matrix from the recorded parents."""
        if element is None:
            return IDENTITY
        parent = self.parent.get(id(element))
        return multiply(self.world(parent), self.local(element))

    def parent_world(self, element: Element) -> Mat34:
        """World matrix of the element's parent."""
        return self.world(self.parent.get(id(element)))

    def write_world(self, element: Element, position: Optional[Vec3], orientation: Optional[Quat]) -> None:
        """Set a dag's transform so that its world placement is the given one."""
        t = element.get("transform")
        if not isinstance(t, Element):
            return
        inverse_parent = invert(self.parent_world(element))
        if position is not None:
            t.set("position", AttrType.VECTOR3, apply(inverse_parent, position))
        if orientation is not None:
            parent_rot = matrix_to_quaternion(inverse_parent)
            t.set("orientation", AttrType.QUATERNION,
                  quaternion_normalize(quaternion_multiply(parent_rot, orientation)))

    # -- running ---------------------------------------------------------------------
    def run(self, time: Time) -> None:
        """Evaluate every operator of every animation set."""
        self.operators_run = 0
        for aset in self.shot.animation_sets:
            for op in aset.element.get("operators") or []:
                if not isinstance(op, Element):
                    continue
                try:
                    self.run_one(op, time)
                except Exception as exc:                  # noqa: BLE001 - one bad operator must not stop the rest
                    self.errors.append(f"{op.type} {op.name!r}: {type(exc).__name__}: {exc}")

    def run_one(self, op: Element, time: Time) -> bool:
        """Evaluate one operator; True when its type is handled."""
        kind = op.type
        if kind == "DmeExpressionOperator":
            return self._expression(op, time)
        if kind == "DmePackColorOperator":
            color = tuple(int(round(max(0.0, min(1.0, float(op.get(k, 1.0)))) * 255))
                          for k in ("red", "green", "blue", "alpha"))
            op.set("color", AttrType.COLOR, color)
        elif kind == "DmePackVector3Operator":
            op.set("vector", AttrType.VECTOR3, tuple(float(op.get(k, 0.0)) for k in ("x", "y", "z")))
        elif kind == "DmeRigPointConstraintOperator":
            self._point(op)
        elif kind == "DmeRigOrientConstraintOperator":
            self._orient(op)
        elif kind == "DmeRigParentConstraintOperator":
            self._point(op)
            self._orient(op)
        elif kind == "DmeRigAimConstraintOperator":
            self._aim(op)
        elif kind == "DmeRigIKConstraintOperator":
            self._ik(op)
        else:
            return False
        self.operators_run += 1
        return True

    # -- expressions -----------------------------------------------------------------
    def _expression(self, op: Element, time: Time) -> bool:
        text = op.get("expr", "")
        if not text:
            return False
        variables = {"time": time.seconds}
        for attr in op:
            if isinstance(attr.value, (int, float)) and not isinstance(attr.value, bool):
                variables[attr.name] = float(attr.value)
        try:
            result = evaluate(text, variables)
        except ExpressionError as exc:
            self.errors.append(f"{op.name!r}: {exc}")
            return False
        if math.isnan(result) or math.isinf(result):
            result = 0.0
        op.set("result", AttrType.FLOAT, result)
        self.operators_run += 1
        return True

    # -- constraints -----------------------------------------------------------------
    def _targets(self, op: Element) -> List[Tuple[Element, float, Vec3, Quat]]:
        out = []
        for target in op.get("targets") or []:
            if not isinstance(target, Element):
                continue
            dag = target.get("target")
            weight = float(target.get("targetWeight", 1.0))
            if not isinstance(dag, Element) or weight <= 0.0:
                continue
            out.append((dag, weight,
                        tuple(target.get("vecOffset", (0.0, 0.0, 0.0))),
                        tuple(target.get("oOffset", (0.0, 0.0, 0.0, 1.0)))))
        return out

    @staticmethod
    def _slave(op: Element, key: str = "slave"):
        slave = op.get(key)
        if not isinstance(slave, Element):
            return None, None
        dag = slave.get("target")
        return slave, (dag if isinstance(dag, Element) else None)

    def _point(self, op: Element) -> None:
        slave, dag = self._slave(op)
        targets = self._targets(op)
        if slave is None or dag is None or not targets:
            return
        total = sum(w for _d, w, _v, _q in targets)
        acc = [0.0, 0.0, 0.0]
        for target, weight, offset, _q in targets:
            world = self.world(target)
            p = apply(world, offset)
            for i in range(3):
                acc[i] += p[i] * weight
        position = tuple(v / total for v in acc)
        if total < 1.0:
            base = apply(self.parent_world(dag), tuple(slave.get("position", (0.0, 0.0, 0.0))))
            position = tuple(base[i] * (1.0 - total) + position[i] * total for i in range(3))
        self.write_world(dag, position, None)

    def _orient(self, op: Element) -> None:
        slave, dag = self._slave(op)
        targets = self._targets(op)
        if slave is None or dag is None or not targets:
            return
        total = sum(w for _d, w, _v, _q in targets)
        blended: Optional[Quat] = None
        accumulated = 0.0
        for target, weight, _offset, rotation_offset in targets:
            q = quaternion_multiply(matrix_to_quaternion(self.world(target)), rotation_offset)
            if blended is None:
                blended = q
            else:
                blended = quaternion_slerp(blended, q, weight / (accumulated + weight))
            accumulated += weight
        if total < 1.0 and blended is not None:
            parent_rot = matrix_to_quaternion(self.parent_world(dag))
            base = quaternion_multiply(parent_rot, tuple(slave.get("orientation", (0.0, 0.0, 0.0, 1.0))))
            blended = quaternion_slerp(base, blended, total)
        self.write_world(dag, None, blended)

    def _aim(self, op: Element) -> None:
        slave, dag = self._slave(op)
        targets = self._targets(op)
        if slave is None or dag is None or not targets:
            return
        total = sum(w for _d, w, _v, _q in targets)
        acc = [0.0, 0.0, 0.0]
        for target, weight, offset, _q in targets:
            p = apply(self.world(target), offset)
            for i in range(3):
                acc[i] += p[i] * weight / total
        world = self.world(dag)
        origin = translation_of(world)
        to_target = tuple(acc[i] - origin[i] for i in range(3))
        aim = tuple(op.get("aimVector", (1.0, 0.0, 0.0)))
        current = apply_direction(world, aim)
        turn = rotation_between(current, to_target)
        orientation = quaternion_multiply(turn, matrix_to_quaternion(world))
        self.write_world(dag, None, orientation)

    def _ik(self, op: Element) -> None:
        """Two-bone IK: turn the start bone so the chain plane holds the
        pole, then the middle bone so the end reaches the target."""
        _s, start = self._slave(op, "startJoint")
        _m, mid = self._slave(op, "midJoint")
        _e, end = self._slave(op, "endJoint")
        targets = self._targets(op)
        if start is None or mid is None or end is None or not targets:
            return
        target_dag, _w, offset, _q = targets[0]
        goal = apply(self.world(target_dag), offset)

        s = translation_of(self.world(start))
        m = translation_of(self.world(mid))
        e = translation_of(self.world(end))
        a = _length(_sub(m, s))
        b = _length(_sub(e, m))
        if a < 1e-6 or b < 1e-6:
            return
        pole_dag = op.get("pvTarget")
        if isinstance(pole_dag, Element):
            pole = translation_of(self.world(pole_dag))
        else:
            pole = apply(self.parent_world(start), tuple(op.get("poleVector", (0.0, 1.0, 0.0))))

        to_goal = _sub(goal, s)
        d = _length(to_goal)
        d = max(abs(a - b) + 1e-4, min(a + b - 1e-4, d))
        direction = _scale(to_goal, 1.0 / _length(to_goal)) if _length(to_goal) > 1e-9 else _normalize(_sub(m, s))
        # the bend plane: through start, along the goal, towards the pole
        side = _sub(pole, s)
        side = _sub(side, _scale(direction, _dot(side, direction)))
        if _length(side) < 1e-6:
            side = _sub(m, s)
            side = _sub(side, _scale(direction, _dot(side, direction)))
        if _length(side) < 1e-6:
            return
        side = _normalize(side)
        cos_start = (a * a + d * d - b * b) / (2.0 * a * d)
        cos_start = max(-1.0, min(1.0, cos_start))
        sin_start = math.sqrt(max(0.0, 1.0 - cos_start * cos_start))
        new_mid = _add(s, _add(_scale(direction, a * cos_start), _scale(side, a * sin_start)))

        # start bone: rotate so its child lands on new_mid
        start_rot = matrix_to_quaternion(self.world(start))
        turn = rotation_between(_sub(m, s), _sub(new_mid, s))
        self.write_world(start, None, quaternion_multiply(turn, start_rot))
        # middle bone: with the start moved, rotate so the end lands on the goal
        m2 = translation_of(self.world(mid))
        e2 = translation_of(self.world(end))
        mid_rot = matrix_to_quaternion(self.world(mid))
        turn = rotation_between(_sub(e2, m2), _sub(goal, m2))
        self.write_world(mid, None, quaternion_multiply(turn, mid_rot))


def run_operators(shot: FilmClip, time: Time) -> OperatorRunner:
    """Run every operator of the shot at `time`; returns the runner."""
    runner = OperatorRunner(shot)
    runner.run(time)
    return runner


# what each constraint writes: (slave key, transform attribute)
_WRITES = {
    "DmeRigPointConstraintOperator": (("slave", "position"),),
    "DmeRigOrientConstraintOperator": (("slave", "orientation"),),
    "DmeRigParentConstraintOperator": (("slave", "position"), ("slave", "orientation")),
    "DmeRigAimConstraintOperator": (("slave", "orientation"),),
    "DmeRigIKConstraintOperator": (("startJoint", "orientation"), ("midJoint", "orientation")),
}


def constrained_attributes(shot: FilmClip) -> Dict[Tuple[int, str], Element]:
    """(id(transform), attribute) -> the constraint that writes it.

    Setting such an attribute by hand has no lasting effect: the operator
    puts its own value back on the next evaluation. SFM behaves the same
    way - a rigged bone is moved through its rig handle, not directly.
    """
    out: Dict[Tuple[int, str], Element] = {}
    for aset in shot.animation_sets:
        for op in aset.element.get("operators") or []:
            if not isinstance(op, Element):
                continue
            for key, attribute in _WRITES.get(op.type, ()):
                _slave, dag = OperatorRunner._slave(op, key)
                transform = dag.get("transform") if dag is not None else None
                if isinstance(transform, Element):
                    out[(id(transform), attribute)] = op
    return out


# -- small vector helpers -----------------------------------------------------------
def _sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _scale(a: Vec3, s: float) -> Vec3:
    return (a[0] * s, a[1] * s, a[2] * s)


def _dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _length(a: Vec3) -> float:
    return math.sqrt(_dot(a, a))


def _normalize(a: Vec3) -> Vec3:
    n = _length(a)
    return _scale(a, 1.0 / n) if n > 1e-12 else (0.0, 0.0, 0.0)


def constraint_handle(op: Element) -> Optional[Element]:
    """The dag a constraint follows - the rig handle to move instead of the bone it owns."""
    for target in op.get("targets") or []:
        if isinstance(target, Element):
            dag = target.get("target")
            if isinstance(dag, Element):
                return dag
    return None
