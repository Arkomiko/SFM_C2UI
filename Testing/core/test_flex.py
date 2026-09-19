"""
Faces: controller ranges, the rule stack machine, ramps and vertex morphs.
"""
import sys
from array import array
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Core.API.dmx import ARRAY_OFFSET, AttrType, DmxDocument, Element
from Core.API.model import FlexController, FlexRule, Mesh, MeshFlex, Model
from Core.Code.flex import active_flexes, controller_values, morph, ramp, run_rules

CONST, FETCH1, FETCH2, ADD, SUB, MUL, DIV, NEG, EXP = range(1, 10)
MAX, MIN, TWOWAY_0, TWOWAY_1, NWAY, COMBO, DOMINATE, LOWER_EYELID, UPPER_EYELID = range(13, 22)


def _close(a, b, eps=1e-6):
    return abs(a - b) <= eps


def _model(controllers, descs, rules):
    return Model(flex_controllers=[FlexController(n, lo, hi) for n, lo, hi in controllers],
                 flex_descs=list(descs), flex_rules=[FlexRule(d, tuple(ops)) for d, ops in rules])


def op(code, index=0, value=0.0):
    return (code, index, value)


# ------------------------------------------------------------------- controllers
def test_controller_values_map_the_session_range_onto_the_models():
    model = _model([("smile", 0.0, 1.0), ("multi_lid", -1.0, 1.0), ("wide", 0.0, 2.0)], [], [])
    values = controller_values(model, {"smile": 0.25, "multi_lid": 0.5, "wide": 1.0})
    assert values == [0.25, 0.0, 2.0]
    # unnamed: rest at the bottom, or the middle of a two-sided range
    assert controller_values(model, {}) == [0.0, 0.0, 0.0]
    assert controller_values(model, {"smile": 7.0})[0] == 1.0           # clamped


# ------------------------------------------------------------------- rules
def test_arithmetic_ops():
    model = _model([("a", 0, 1), ("b", 0, 1)], ["sum", "product", "diff", "quot", "neg", "pow", "hi", "lo"], [
        (0, [op(FETCH1, 0), op(FETCH1, 1), op(ADD)]),
        (1, [op(FETCH1, 0), op(FETCH1, 1), op(MUL)]),
        (2, [op(FETCH1, 0), op(FETCH1, 1), op(SUB)]),
        (3, [op(FETCH1, 0), op(FETCH1, 1), op(DIV)]),
        (4, [op(FETCH1, 0), op(NEG)]),
        (5, [op(FETCH1, 0), op(CONST, value=2.0), op(EXP)]),
        (6, [op(FETCH1, 0), op(FETCH1, 1), op(MAX)]),
        (7, [op(FETCH1, 0), op(FETCH1, 1), op(MIN)]),
    ])
    out = run_rules(model, [0.6, 0.3])
    assert [round(v, 6) for v in out] == [0.9, 0.18, 0.3, 2.0, -0.6, 0.36, 0.6, 0.3]


def test_fetch2_reads_an_earlier_target():
    model = _model([("a", 0, 1)], ["base", "half"], [
        (0, [op(FETCH1, 0)]),
        (1, [op(FETCH2, 0), op(CONST, value=0.5), op(MUL)]),
    ])
    assert run_rules(model, [0.8]) == [0.8, 0.4]


def test_two_way_splits_a_signed_controller():
    model = _model([("lid", -1, 1)], ["down", "up"], [
        (0, [op(TWOWAY_0, 0)]), (1, [op(TWOWAY_1, 0)])])
    assert run_rules(model, [-0.5]) == [0.5, 0.0]
    assert run_rules(model, [0.25]) == [0.0, 0.25]
    assert run_rules(model, [0.0]) == [0.0, 0.0]


def test_nway_ramps_a_value_controller_and_scales_by_the_amount():
    # stack: ramp 0 1 2 3, value controller 1; op index 0 is the amount
    model = _model([("amount", 0, 1), ("value", -1, 1)], ["x"], [
        (0, [op(CONST, value=0.0), op(CONST, value=1.0), op(CONST, value=2.0), op(CONST, value=3.0),
             op(CONST, value=1.0), op(NWAY, 0)])])
    assert _close(run_rules(model, [0.8, 0.5])[0], 0.4)          # rising edge: 0.5 * 0.8
    assert _close(run_rules(model, [0.8, 1.5])[0], 0.8)          # plateau
    assert run_rules(model, [0.8, 3.5])[0] == 0.0                 # outside


def test_combo_multiplies_and_dominate_suppresses():
    model = _model([("a", 0, 1), ("b", 0, 1), ("c", 0, 1)], ["combo", "dom"], [
        (0, [op(FETCH1, 0), op(FETCH1, 1), op(FETCH1, 2), op(COMBO, 3)]),
        (1, [op(FETCH1, 0), op(FETCH1, 1), op(FETCH1, 2), op(DOMINATE, 2)]),
    ])
    out = run_rules(model, [0.5, 0.5, 0.5])
    assert _close(out[0], 0.125)
    assert _close(out[1], 0.5 * (1 - 0.25))


def test_eyelid_ops_follow_valves_formula():
    ctrls = [("closeLidV", 0, 1), ("closeLid", 0, 1), ("blink", 0, 1), ("eyeUpDown", -1, 1)]
    # stack: eyeUpDown index, blink index, closeLid index; op index = closeLidV
    program = [op(CONST, value=3.0), op(CONST, value=2.0), op(CONST, value=1.0)]
    model = _model(ctrls, ["lower", "upper"], [
        (0, program + [op(LOWER_EYELID, 0)]), (1, program + [op(UPPER_EYELID, 0)])])
    lower, upper = run_rules(model, [0.25, 0.8, 0.0, 0.0])
    assert _close(lower, 0.75 * 0.8) and _close(upper, 0.25 * 0.8)
    lower, upper = run_rules(model, [0.25, 0.8, 0.0, 0.5])      # eyes up: the lower lid gives way
    assert _close(lower, 0.5 * 0.75 * 0.8) and _close(upper, 0.25 * 0.8)


def test_a_rule_out_of_range_is_harmless():
    model = _model([("a", 0, 1)], ["x"], [(5, [op(FETCH1, 9)]), (0, [op(FETCH1, 0)])])
    assert run_rules(model, [0.3]) == [0.3]


# ------------------------------------------------------------------- ramps and morphs
def test_ramp_shape():
    t = (0.0, 1.0, 10.0, 11.0)
    assert ramp(-1.0, t) == 0.0 and ramp(0.0, t) == 0.0
    assert ramp(0.5, t) == 0.5 and ramp(1.0, t) == 1.0 and ramp(5.0, t) == 1.0
    assert _close(ramp(10.5, t), 0.5) and ramp(11.0, t) == 0.0


def _mesh():
    mesh = Mesh()
    mesh.positions = array("f", [0, 0, 0, 1, 0, 0, 2, 0, 0])
    mesh.normals = array("f", [0, 0, 1] * 3)
    smile = MeshFlex(desc=0, pair=1,
                     indices=array("H", [0, 2]), sides=array("B", [0, 255]),
                     deltas=array("f", [0, 1, 0, 0, 1, 0]),
                     normal_deltas=array("f", [0.1, 0, 0, 0.1, 0, 0]))
    frown = MeshFlex(desc=2, indices=array("H", [1]), sides=array("B", [0]),
                     deltas=array("f", [0, -1, 0]), normal_deltas=array("f", [0, 0, 0]))
    mesh.flexes = [smile, frown]
    return mesh


def test_morph_applies_weighted_deltas_and_leaves_the_mesh_alone():
    mesh = _mesh()
    assert morph(mesh, [0.0, 0.0, 0.0]) is None
    positions, normals = morph(mesh, [0.5, 0.5, 1.0])
    assert list(positions) == [0, 0.5, 0, 1, -1, 0, 2, 0.5, 0]
    assert _close(normals[0], 0.05) and normals[2] == 1.0
    assert list(mesh.positions) == [0, 0, 0, 1, 0, 0, 2, 0, 0]          # untouched


def test_paired_targets_blend_across_the_face_by_side():
    mesh = _mesh()
    # left target full, right target off: vertex 0 (side 0) moves, vertex 2 (side 255) does not
    positions, _n = morph(mesh, [1.0, 0.0, 0.0])
    assert positions[1] == 1.0 and positions[7] == 0.0
    positions, _n = morph(mesh, [0.0, 1.0, 0.0])
    assert positions[1] == 0.0 and positions[7] == 1.0


def test_active_flexes_lists_only_what_moves():
    mesh = _mesh()
    assert [f.desc for f, _a, _b in active_flexes(mesh, [0.0, 0.0, 0.3])] == [2]
    assert len(active_flexes(mesh, [0.2, 0.0, 0.0])) == 1


# ------------------------------------------------------------------- session operators
def test_flex_operators_write_the_game_model_by_name():
    from Core.API.session import FilmClip
    from Core.Code.animation import Evaluator
    doc = DmxDocument()
    gm = doc.add(Element("DmeGameModel", "gm"))
    gm.set("transform", AttrType.ELEMENT, None)
    gm.set("visible", AttrType.BOOL, True)
    gm.set("children", AttrType.ELEMENT + ARRAY_OFFSET, [])
    gm.set("flexnames", AttrType.STRING + ARRAY_OFFSET, ["smile", "blink"])
    gm.set("flexWeights", AttrType.FLOAT + ARRAY_OFFSET, [0.0, 0.0])
    ops = []
    for name, value in (("blink", 0.7), ("smile", 0.2), ("gone", 0.9)):
        o = doc.add(Element("DmeGlobalFlexControllerOperator", name))
        o.set("flexWeight", AttrType.FLOAT, value)
        ops.append(o)
    gm.set("globalFlexControllers", AttrType.ELEMENT + ARRAY_OFFSET, ops)
    scene = doc.add(Element("DmeDag", "scene"))
    scene.set("transform", AttrType.ELEMENT, None)
    scene.set("visible", AttrType.BOOL, True)
    scene.set("children", AttrType.ELEMENT + ARRAY_OFFSET, [gm])
    shot = doc.add(Element("DmeFilmClip", "shot"))
    shot.set("scene", AttrType.ELEMENT, scene)
    Evaluator()._run_flex_operators(FilmClip(shot))
    assert gm["flexWeights"] == [0.2, 0.7]
    from Core.API.session import GameModel
    assert GameModel(gm).flex_values() == {"blink": 0.7, "smile": 0.2, "gone": 0.9}
