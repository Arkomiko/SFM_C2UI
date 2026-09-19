"""
Expressions and rig constraints on a scene graph built in memory.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Core.API.dmx import ARRAY_OFFSET, AttrType, DmxDocument, Element, Time
from Core.API.session import FilmClip
from Core.Code.expression import ExpressionError, evaluate
from Core.Code.operators import OperatorRunner
from Core.Code.transform import apply, apply_direction, translation_of


def _close(a, b, eps=1e-5):
    return len(a) == len(b) and all(abs(x - y) <= eps for x, y in zip(a, b))


# ------------------------------------------------------------------- expressions
def test_arithmetic_and_precedence():
    assert evaluate("1 + 2 * 3", {}) == 7
    assert evaluate("(1 + 2) * 3", {}) == 9
    assert evaluate("2 ^ 3 ^ 2", {}) == 512                 # right associative
    assert evaluate("-3 + 5", {}) == 2
    assert evaluate("7 % 4", {}) == 3
    assert evaluate("1 / 0", {}) == 0                       # never raises


def test_variables_functions_and_conditionals():
    assert evaluate("lerp(value, lo, hi)", {"value": 0.5, "lo": 10, "hi": 120}) == 65
    assert evaluate("max( 0, (footRoll - 0.5) ) * 140", {"footRoll": 0.75}) == 35
    assert evaluate("inrange( footRoll, 0.5001, 1.0 )", {"footRoll": 0.75}) == 1
    assert evaluate("inrange( footRoll, 0.5001, 1.0 )", {"footRoll": 0.25}) == 0
    assert evaluate("x > 1 ? 10 : 20", {"x": 2}) == 10
    assert evaluate("x > 1 && y < 1 || 0", {"x": 2, "y": 0}) == 1
    assert evaluate("missing + 1", {}) == 1                 # unknown names read as 0
    assert evaluate("", {}) == 0


def test_noise_is_smooth_bounded_and_repeatable():
    a = evaluate("7 * noise(4 * time, 0, 0 )", {"time": 1.3})
    b = evaluate("7 * noise(4 * time, 0, 0 )", {"time": 1.3})
    c = evaluate("7 * noise(4 * time, 0, 0 )", {"time": 1.3001})
    assert a == b and abs(a - c) < 0.2 and abs(a) <= 7


def test_bad_expressions_raise():
    for text in ("1 +", "foo(1)", "(1", "1 2"):
        try:
            evaluate(text, {})
        except ExpressionError:
            continue
        raise AssertionError(text)


# ------------------------------------------------------------------- scene helpers
def _transform(doc, pos=(0, 0, 0), rot=(0, 0, 0, 1)):
    t = doc.add(Element("DmeTransform", "unnamed"))
    t.set("position", AttrType.VECTOR3, tuple(float(v) for v in pos))
    t.set("orientation", AttrType.QUATERNION, tuple(float(v) for v in rot))
    return t


def _dag(doc, name, pos=(0, 0, 0), rot=(0, 0, 0, 1), children=(), etype="DmeDag"):
    d = doc.add(Element(etype, name))
    d.set("transform", AttrType.ELEMENT, _transform(doc, pos, rot))
    d.set("shape", AttrType.ELEMENT, None)
    d.set("visible", AttrType.BOOL, True)
    d.set("children", AttrType.ELEMENT + ARRAY_OFFSET, list(children))
    return d


def _target(doc, dag, weight=1.0, offset=(0, 0, 0), rotation=(0, 0, 0, 1)):
    t = doc.add(Element("DmeConstraintTarget", dag.name))
    t.set("target", AttrType.ELEMENT, dag)
    t.set("targetWeight", AttrType.FLOAT, weight)
    t.set("vecOffset", AttrType.VECTOR3, tuple(float(v) for v in offset))
    t.set("oOffset", AttrType.QUATERNION, tuple(float(v) for v in rotation))
    return t


def _slave(doc, dag, pos=(0, 0, 0), rot=(0, 0, 0, 1)):
    s = doc.add(Element("DmeConstraintSlave", "unnamed"))
    s.set("target", AttrType.ELEMENT, dag)
    s.set("position", AttrType.VECTOR3, tuple(float(v) for v in pos))
    s.set("orientation", AttrType.QUATERNION, tuple(float(v) for v in rot))
    return s


def _shot(doc, scene, operators):
    aset = doc.add(Element("DmeAnimationSet", "rig"))
    aset.set("operators", AttrType.ELEMENT + ARRAY_OFFSET, list(operators))
    shot = doc.add(Element("DmeFilmClip", "shot"))
    shot.set("scene", AttrType.ELEMENT, scene)
    shot.set("animationSets", AttrType.ELEMENT + ARRAY_OFFSET, [aset])
    return FilmClip(shot)


def _op(doc, etype, name, **attrs):
    op = doc.add(Element(etype, name))
    for key, value in attrs.items():
        if isinstance(value, list):
            op.set(key, AttrType.ELEMENT + ARRAY_OFFSET, value)
        elif isinstance(value, Element):
            op.set(key, AttrType.ELEMENT, value)
        else:
            op.set(key, AttrType.FLOAT, float(value))
    return op


# ------------------------------------------------------------------- constraints
def test_point_constraint_moves_the_slave_in_its_parents_space():
    doc = DmxDocument()
    handle = _dag(doc, "handle", pos=(10, 20, 30))
    bone = _dag(doc, "bone", pos=(0, 0, 0))
    holder = _dag(doc, "holder", pos=(100, 0, 0), children=[bone])       # the bone's parent
    scene = _dag(doc, "scene", children=[holder, handle])
    op = _op(doc, "DmeRigPointConstraintOperator", "point",
             targets=[_target(doc, handle)], slave=_slave(doc, bone))
    runner = OperatorRunner(_shot(doc, scene, [op]))
    runner.run(Time(0))
    assert runner.operators_run == 1 and runner.errors == []
    assert _close(bone["transform"]["position"], (-90, 20, 30))          # local to the holder
    assert _close(translation_of(runner.world(bone)), (10, 20, 30))      # world: on the handle


def test_point_constraint_blends_with_the_base_below_full_weight():
    doc = DmxDocument()
    handle = _dag(doc, "handle", pos=(10, 0, 0))
    bone = _dag(doc, "bone", pos=(0, 0, 0))
    scene = _dag(doc, "scene", children=[bone, handle])
    op = _op(doc, "DmeRigPointConstraintOperator", "point",
             targets=[_target(doc, handle, weight=0.25)], slave=_slave(doc, bone, pos=(2, 0, 0)))
    OperatorRunner(_shot(doc, scene, [op])).run(Time(0))
    assert _close(bone["transform"]["position"], (4, 0, 0))             # 0.75 * 2 + 0.25 * 10


def test_orient_constraint_copies_the_targets_rotation():
    doc = DmxDocument()
    quarter = (0, 0, math.sin(math.pi / 4), math.cos(math.pi / 4))
    handle = _dag(doc, "handle", rot=quarter)
    bone = _dag(doc, "bone")
    scene = _dag(doc, "scene", children=[bone, handle])
    op = _op(doc, "DmeRigOrientConstraintOperator", "orient",
             targets=[_target(doc, handle)], slave=_slave(doc, bone))
    OperatorRunner(_shot(doc, scene, [op])).run(Time(0))
    q = bone["transform"]["orientation"]
    assert _close(q, quarter) or _close(q, tuple(-v for v in quarter))


def test_aim_constraint_points_the_bone_at_the_target():
    doc = DmxDocument()
    handle = _dag(doc, "handle", pos=(0, 50, 0))
    bone = _dag(doc, "bone", pos=(0, 0, 0))
    scene = _dag(doc, "scene", children=[bone, handle])
    op = _op(doc, "DmeRigAimConstraintOperator", "aim",
             targets=[_target(doc, handle)], slave=_slave(doc, bone))
    runner = OperatorRunner(_shot(doc, scene, [op]))
    runner.run(Time(0))
    forward = apply_direction(runner.world(bone), (1, 0, 0))
    assert _close(forward, (0, 1, 0))


def test_two_bone_ik_reaches_the_goal_and_keeps_lengths():
    doc = DmxDocument()
    # a straight leg along +X: hip at origin, knee 10 out, foot 20 out
    foot = _dag(doc, "foot", pos=(10, 0, 0))
    knee = _dag(doc, "knee", pos=(10, 0, 0), children=[foot])
    hip = _dag(doc, "hip", pos=(0, 0, 0), children=[knee])
    goal = _dag(doc, "goal", pos=(12, 0, 8))
    pole = _dag(doc, "pole", pos=(5, 0, 30))
    scene = _dag(doc, "scene", children=[hip, goal, pole])
    op = _op(doc, "DmeRigIKConstraintOperator", "ik",
             targets=[_target(doc, goal)], startJoint=_slave(doc, hip), midJoint=_slave(doc, knee),
             endJoint=_slave(doc, foot), pvTarget=pole)
    runner = OperatorRunner(_shot(doc, scene, [op]))
    runner.run(Time(0))
    assert runner.errors == []
    h = translation_of(runner.world(hip))
    k = translation_of(runner.world(knee))
    f = translation_of(runner.world(foot))
    assert _close(f, (12, 0, 8), 1e-4)
    assert abs(math.dist(h, k) - 10) < 1e-6 and abs(math.dist(k, f) - 10) < 1e-6
    assert k[2] > 0                                                      # the knee bends towards the pole


def test_ik_out_of_reach_stretches_towards_the_goal():
    doc = DmxDocument()
    foot = _dag(doc, "foot", pos=(10, 0, 0))
    knee = _dag(doc, "knee", pos=(10, 0, 0), children=[foot])
    hip = _dag(doc, "hip", children=[knee])
    goal = _dag(doc, "goal", pos=(0, 0, 100))
    scene = _dag(doc, "scene", children=[hip, goal])
    op = _op(doc, "DmeRigIKConstraintOperator", "ik", targets=[_target(doc, goal)],
             startJoint=_slave(doc, hip), midJoint=_slave(doc, knee), endJoint=_slave(doc, foot))
    runner = OperatorRunner(_shot(doc, scene, [op]))
    runner.run(Time(0))
    f = translation_of(runner.world(foot))
    assert abs(f[2] - 20) < 0.01 and abs(f[0]) < 0.1 and abs(f[1]) < 0.1


def test_expression_operator_writes_result_and_pack_operators_pack():
    doc = DmxDocument()
    scene = _dag(doc, "scene")
    expr = _op(doc, "DmeExpressionOperator", "fov", value=0.5, lo=10, hi=120)
    expr.set("expr", AttrType.STRING, "lerp(value, lo, hi)")
    expr.set("result", AttrType.FLOAT, 0.0)
    color = _op(doc, "DmePackColorOperator", "c", red=1.0, green=0.5, blue=0.0, alpha=1.0)
    color.set("color", AttrType.COLOR, (0, 0, 0, 0))
    vec = _op(doc, "DmePackVector3Operator", "v", x=1, y=2, z=3)
    vec.set("vector", AttrType.VECTOR3, (0.0, 0.0, 0.0))
    runner = OperatorRunner(_shot(doc, scene, [expr, color, vec]))
    runner.run(Time.from_seconds(2.0))
    assert expr["result"] == 65.0
    assert color["color"] == (255, 128, 0, 255)
    assert vec["vector"] == (1.0, 2.0, 3.0)
    assert runner.operators_run == 3


def test_a_broken_operator_is_reported_and_the_rest_still_run():
    doc = DmxDocument()
    scene = _dag(doc, "scene")
    bad = _op(doc, "DmeExpressionOperator", "bad")
    bad.set("expr", AttrType.STRING, "1 +")
    good = _op(doc, "DmePackVector3Operator", "v", x=4, y=5, z=6)
    good.set("vector", AttrType.VECTOR3, (0.0, 0.0, 0.0))
    runner = OperatorRunner(_shot(doc, scene, [bad, good]))
    runner.run(Time(0))
    assert good["vector"] == (4.0, 5.0, 6.0)
    assert len(runner.errors) == 1 and "bad" in runner.errors[0]
