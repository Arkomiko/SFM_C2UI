"""
Faces: from controller values to moved vertices.

A model's face is driven in three steps, all compiled into the .mdl:

1. **controllers** - the handles an animator moves (`right_Smile`, `blink`),
   each with a range;
2. **rules** - for every flex target, a small stack program computing its
   weight from the controllers (Valve's `RunFlexRules`; the ops are the
   compiler's, reproduced here one for one);
3. **vertex animations** - per mesh, the offset each target adds to each
   vertex, scaled by a ramp over the target's weight and, for paired
   left/right targets, blended across the face by the vertex's `side`.

    values = controller_values(model, {"right_Smile": 0.8, ...})   # by name, 0..1
    weights = run_rules(model, values)                             # per flex desc
    positions, normals = morph(mesh, weights)                       # new arrays

Everything is pure Python and per frame; a face mesh has a few thousand
vertices and a few dozen active targets, which is a few milliseconds.
"""
from __future__ import annotations

import math
from array import array
from typing import List, Mapping, Optional, Sequence, Tuple

from Core.API.model import Mesh, Model

__all__ = ["controller_values", "run_rules", "ramp", "morph", "active_flexes"]

# ops, as studio.h numbers them
_CONST, _FETCH1, _FETCH2, _ADD, _SUB, _MUL, _DIV, _NEG, _EXP, _OPEN, _CLOSE, _COMMA = range(1, 13)
_MAX, _MIN, _2WAY_0, _2WAY_1, _NWAY, _COMBO, _DOMINATE, _LOWER_EYELID, _UPPER_EYELID = range(13, 22)


def _remap_clamped(value: float, a: float, b: float, c: float, d: float) -> float:
    if b == a:
        return c
    t = (value - a) / (b - a)
    t = 0.0 if t < 0.0 else 1.0 if t > 1.0 else t
    return c + (d - c) * t


def controller_values(model: Model, normalised: Mapping[str, float]) -> List[float]:
    """Raw controller values in the model's controller order.

    A session stores every controller normalised to 0..1; the rules expect
    the controller's own range (a `multi_` controller runs -1..1 with rest at
    0). Unnamed controllers rest at the middle of their range for two-sided
    ones and at the bottom otherwise, which is where the model was built.
    """
    out: List[float] = []
    for controller in model.flex_controllers:
        w = normalised.get(controller.name)
        if w is None:
            w = 0.5 if controller.min < 0.0 < controller.max else 0.0
        w = 0.0 if w < 0.0 else 1.0 if w > 1.0 else w
        out.append(controller.min + (controller.max - controller.min) * w)
    return out


def run_rules(model: Model, src: Sequence[float]) -> List[float]:
    """Weights for every flex desc, from raw controller values."""
    controllers = model.flex_controllers
    dest = [0.0] * len(model.flex_descs)
    stack: List[float] = [0.0] * 64
    count = len(src)
    for rule in model.flex_rules:
        k = 0
        for op, index, value in rule.ops:
            if op == _CONST:
                stack[k] = value; k += 1
            elif op == _FETCH1:
                stack[k] = src[index] if 0 <= index < count else 0.0; k += 1
            elif op == _FETCH2:
                stack[k] = dest[index] if 0 <= index < len(dest) else 0.0; k += 1
            elif op == _ADD:
                stack[k - 2] += stack[k - 1]; k -= 1
            elif op == _SUB:
                stack[k - 2] -= stack[k - 1]; k -= 1
            elif op == _MUL:
                stack[k - 2] *= stack[k - 1]; k -= 1
            elif op == _DIV:
                stack[k - 2] = stack[k - 2] / stack[k - 1] if stack[k - 1] > 0.0001 else 0.0; k -= 1
            elif op == _NEG:
                stack[k - 1] = -stack[k - 1]
            elif op == _EXP:
                try:
                    stack[k - 2] = math.pow(stack[k - 2], stack[k - 1])
                except (ValueError, OverflowError):
                    stack[k - 2] = 0.0
                k -= 1
            elif op == _MAX:
                stack[k - 2] = max(stack[k - 2], stack[k - 1]); k -= 1
            elif op == _MIN:
                stack[k - 2] = min(stack[k - 2], stack[k - 1]); k -= 1
            elif op == _2WAY_0:
                stack[k] = _remap_clamped(src[index] if 0 <= index < count else 0.0, -1.0, 0.0, 1.0, 0.0); k += 1
            elif op == _2WAY_1:
                stack[k] = _remap_clamped(src[index] if 0 <= index < count else 0.0, 0.0, 1.0, 0.0, 1.0); k += 1
            elif op == _NWAY:
                # stack: ramp0 ramp1 ramp2 ramp3 valueController; the op's own
                # index is the amount controller
                value_index = int(stack[k - 1])
                v = src[value_index] if 0 <= value_index < count else 0.0
                r0, r1, r2, r3 = stack[k - 5], stack[k - 4], stack[k - 3], stack[k - 2]
                if v <= r0 or v >= r3:
                    f = 0.0
                elif v < r1:
                    f = (v - r0) / (r1 - r0) if r1 > r0 else 1.0
                elif v > r2:
                    f = (r3 - v) / (r3 - r2) if r3 > r2 else 1.0
                else:
                    f = 1.0
                stack[k - 5] = f * (src[index] if 0 <= index < count else 0.0)
                k -= 4
            elif op == _COMBO:
                m = index
                v = stack[k - m]
                for i in range(1, m):
                    v *= stack[k - m + i]
                stack[k - m] = v
                k -= m - 1
            elif op == _DOMINATE:
                m = index
                dv = stack[k - m]
                for i in range(1, m):
                    dv *= stack[k - m + i]
                stack[k - m - 1] *= 1.0 - dv
                k -= m
            elif op in (_LOWER_EYELID, _UPPER_EYELID):
                close_v = controllers[index] if 0 <= index < len(controllers) else None
                fl_close_v = _remap_clamped(src[index], close_v.min, close_v.max, 0.0, 1.0) if close_v else 0.0
                close_index = int(stack[k - 1])
                close = controllers[close_index] if 0 <= close_index < len(controllers) else None
                fl_close = _remap_clamped(src[close_index], close.min, close.max, 0.0, 1.0) if close else 0.0
                eye_index = int(stack[k - 3])
                fl_eye = 0.0
                if 0 <= eye_index < len(controllers):
                    eye = controllers[eye_index]
                    fl_eye = _remap_clamped(src[eye_index], eye.min, eye.max, -1.0, 1.0)
                if op == _LOWER_EYELID:
                    stack[k - 3] = ((1.0 - fl_eye) if fl_eye > 0.0 else 1.0) * (1.0 - fl_close_v) * fl_close
                else:
                    stack[k - 3] = (1.0 if fl_eye > 0.0 else (1.0 + fl_eye)) * fl_close_v * fl_close
                k -= 2
            # OPEN, CLOSE, COMMA never reach a compiled rule
            if k < 0 or k >= len(stack) - 1:
                break
        if k > 0 and 0 <= rule.desc < len(dest):
            dest[rule.desc] = stack[0]
    return dest


def ramp(weight: float, targets: Tuple[float, float, float, float]) -> float:
    """How much of a target applies at a weight: 0 outside t0..t3, full
    between t1 and t2, rising and falling in between."""
    t0, t1, t2, t3 = targets
    if weight <= t0 or weight >= t3:
        return 0.0
    if weight < t1:
        return (weight - t0) / (t1 - t0) if t1 > t0 else 1.0
    if weight > t2:
        return (t3 - weight) / (t3 - t2) if t3 > t2 else 1.0
    return 1.0


def active_flexes(mesh: Mesh, weights: Sequence[float], threshold: float = 1e-4):
    """(flex, amount for side 0, amount for side 1) for every target that moves."""
    out = []
    for flex in mesh.flexes:
        w0 = ramp(weights[flex.desc], flex.targets) if 0 <= flex.desc < len(weights) else 0.0
        w1 = ramp(weights[flex.pair], flex.targets) if 0 <= flex.pair < len(weights) else w0
        if abs(w0) > threshold or abs(w1) > threshold:
            out.append((flex, w0, w1))
    return out


def morph(mesh: Mesh, weights: Sequence[float]) -> Optional[Tuple[array, array]]:
    """The mesh's positions and normals with every active target applied, or
    None when nothing moves."""
    active = active_flexes(mesh, weights)
    if not active:
        return None
    positions = array("f", mesh.positions)
    normals = array("f", mesh.normals)
    limit = len(positions) // 3
    for flex, w0, w1 in active:
        indices = flex.indices
        sides = flex.sides
        deltas = flex.deltas
        ndeltas = flex.normal_deltas
        same = abs(w0 - w1) < 1e-6
        for i in range(len(indices)):
            v = indices[i]
            if v >= limit:
                continue
            if same:
                w = w0
            else:
                s = sides[i] / 255.0
                w = w0 * (1.0 - s) + w1 * s
            if w == 0.0:
                continue
            j = v * 3
            d = i * 3
            positions[j] += deltas[d] * w
            positions[j + 1] += deltas[d + 1] * w
            positions[j + 2] += deltas[d + 2] * w
            normals[j] += ndeltas[d] * w
            normals[j + 1] += ndeltas[d + 1] * w
            normals[j + 2] += ndeltas[d + 2] * w
    return positions, normals
