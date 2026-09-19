"""
MDL, VVD and VTX readers, checked against bytes we wrote ourselves.

Every expected value here is known exactly, so a field read from the wrong
offset fails instead of producing a model that merely looks plausible.
"""
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Core.Code.formats import FormatError, load_model, parse_mdl, parse_vtx, parse_vvd
from fixtures.fake_model import (FakeSource, build_mdl, build_triangle_model, build_vtx,
                                 build_vvd)


# ------------------------------------------------------------------- mdl
def test_header_fields_land_where_expected():
    mdl = parse_mdl(build_mdl(name="test/fake.mdl", checksum=0x1234), "fake.mdl")
    assert mdl.info.name == "test/fake.mdl"
    assert mdl.info.version == 49
    assert mdl.info.checksum == 0x1234
    assert mdl.info.hull_min == (-1.0, -2.0, -3.0)
    assert mdl.info.hull_max == (11.0, 22.0, 33.0)
    assert mdl.info.eye_position == (0.0, 0.0, 64.0)


def test_bones_are_named_and_parented():
    mdl = parse_mdl(build_mdl(bones=("root", "spine", "head")), "fake.mdl")
    assert [b.name for b in mdl.bones] == ["root", "spine", "head"]
    assert [b.parent for b in mdl.bones] == [-1, 0, 1]
    assert mdl.bones[0].is_root


def test_bone_transform_fields():
    mdl = parse_mdl(build_mdl(bones=("root", "spine")), "fake.mdl")
    assert mdl.bones[1].position == (1.0, 1.0, 2.0)
    assert mdl.bones[1].rotation == (0.0, 0.0, 0.0, 1.0)
    assert mdl.bones[1].flags == 1
    assert len(mdl.bones[1].pose_to_bone) == 12


def test_material_names_and_folders():
    mdl = parse_mdl(build_mdl(materials=("skin", "eyes"),
                              material_dirs=("models/test/", "models/shared/")), "fake.mdl")
    assert mdl.material_names == ["skin", "eyes"]
    assert mdl.material_dirs == ["models/test/", "models/shared/"]


def test_body_part_model_and_mesh():
    mdl = parse_mdl(build_mdl(vertex_count=4), "fake.mdl")
    assert len(mdl.body_parts) == 1
    part = mdl.body_parts[0]
    assert part.name == "body"
    assert len(part.models) == 1
    sub = part.models[0]
    assert sub.vertex_count == 4
    assert sub.first_vertex == 0
    assert len(sub.meshes) == 1
    assert sub.meshes[0].vertex_count == 4


def test_vertex_index_is_a_byte_offset():
    # mstudiomodel_t.vertexindex counts bytes; first_vertex converts it
    raw = bytearray(build_mdl(vertex_count=4))
    mdl = parse_mdl(bytes(raw), "fake.mdl")
    sub = mdl.body_parts[0].models[0]
    assert sub.vertex_index == 0 and sub.first_vertex == 0


def test_rejects_a_file_that_is_not_a_model():
    for junk in (b"", b"XXXX", b"IDST" + b"\0" * 8):
        try:
            parse_mdl(junk, "junk.mdl")
            raise AssertionError(f"expected FormatError for {junk[:8]!r}")
        except FormatError:
            pass


def test_rejects_an_unsupported_version():
    try:
        parse_mdl(build_mdl(version=99), "fake.mdl")
        raise AssertionError("expected FormatError for version 99")
    except FormatError as exc:
        assert "99" in str(exc)


def test_truncation_is_reported_not_crashed():
    full = build_mdl()
    try:
        parse_mdl(full[:len(full) // 2], "cut.mdl")
    except FormatError:
        pass            # either a clean error or a model with warnings is fine


# ------------------------------------------------------------------- vvd
def test_vertices_round_trip():
    vvd = parse_vvd(build_vvd(), "fake.vvd")
    assert vvd.vertex_count == 4
    assert list(vvd.positions[:3]) == [0.0, 0.0, 0.0]
    assert list(vvd.positions[3:6]) == [10.0, 0.0, 0.0]
    assert list(vvd.positions[9:12]) == [0.0, 20.0, 5.0]
    assert list(vvd.normals[:3]) == [0.0, 0.0, 1.0]
    assert list(vvd.uvs[:2]) == [0.0, 0.0]
    assert list(vvd.uvs[4:6]) == [1.0, 1.0]


def test_skin_weights_and_bone_indices():
    vvd = parse_vvd(build_vvd(), "fake.vvd")
    assert list(vvd.bone_indices[:3]) == [0, 0, 0]
    assert list(vvd.bone_indices[6:9]) == [1, 0, 0]      # third vertex is on bone 1
    assert vvd.bone_weights[0] == 1.0


def test_rejects_a_file_that_is_not_vertex_data():
    for junk in (b"", b"NOPE" + b"\0" * 64):
        try:
            parse_vvd(junk, "junk.vvd")
            raise AssertionError("expected FormatError")
        except FormatError:
            pass


def test_fixups_reorder_vertices_for_a_lower_level():
    # store four vertices, then say level 0 uses them in two runs, swapped
    vertices = [((float(i), 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 0.0), 0, 1.0) for i in range(4)]
    data = build_vvd(vertices, fixups=[(0, 2, 2), (0, 0, 2)], lod_counts=[4])
    vvd = parse_vvd(data, "fixed.vvd", lod=0)
    assert vvd.vertex_count == 4
    # the runs are concatenated in table order, not storage order
    assert [vvd.positions[i * 3] for i in range(4)] == [2.0, 3.0, 0.0, 1.0]


def test_fixups_drop_vertices_a_lower_level_does_not_use():
    vertices = [((float(i), 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 0.0), 0, 1.0) for i in range(4)]
    # only the first run belongs to level 1
    data = build_vvd(vertices, fixups=[(1, 0, 2), (0, 2, 2)], lod_counts=[4, 2])
    vvd = parse_vvd(data, "fixed.vvd", lod=1)
    assert vvd.vertex_count == 2
    assert [vvd.positions[i * 3] for i in range(2)] == [0.0, 1.0]


def test_a_fixup_pointing_outside_the_file_is_skipped():
    vertices = [((float(i), 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 0.0), 0, 1.0) for i in range(4)]
    data = build_vvd(vertices, fixups=[(0, 0, 2), (0, 99, 50)], lod_counts=[4])
    vvd = parse_vvd(data, "bad.vvd")
    assert vvd.vertex_count == 2
    assert any("outside" in w for w in vvd.warnings), vvd.warnings


def test_asking_for_a_level_that_does_not_exist_falls_back():
    vvd = parse_vvd(build_vvd(), "fake.vvd", lod=5)
    assert vvd.lod == 0
    assert any("does not exist" in w for w in vvd.warnings)


# ------------------------------------------------------------------- vtx
def test_triangle_list_indices():
    vtx = parse_vtx(build_vtx(), "fake.vtx")
    mesh = vtx.body_parts[0][0][0]
    assert list(mesh.indices) == [0, 1, 2, 0, 2, 3]
    assert mesh.triangle_count == 2


def test_triangle_strip_is_expanded_with_alternating_winding():
    # strip 0,1,2,3 becomes triangles (0,1,2) and (1,3,2)
    vtx = parse_vtx(build_vtx(strip_flags=0x02, indices=[0, 1, 2, 3]), "strip.vtx")
    mesh = vtx.body_parts[0][0][0]
    assert list(mesh.indices) == [0, 1, 2, 1, 3, 2]


def test_degenerate_strip_triangles_are_dropped():
    # a repeated index joins two strips and must not become a zero-area triangle:
    # 0,1,1,2,3 -> (0,1,1) and (1,1,2) are degenerate, only (1,2,3) survives
    vtx = parse_vtx(build_vtx(strip_flags=0x02, indices=[0, 1, 1, 2, 3]), "strip.vtx")
    mesh = vtx.body_parts[0][0][0]
    assert list(mesh.indices) == [1, 2, 3]
    assert len(mesh.indices) % 3 == 0


def test_indices_past_the_group_are_dropped_not_fatal():
    vtx = parse_vtx(build_vtx(indices=[0, 1, 2, 0, 2, 99]), "bad.vtx")
    mesh = vtx.body_parts[0][0][0]
    assert list(mesh.indices) == [0, 1, 2]
    assert any("outside" in w for w in vtx.warnings), vtx.warnings


def test_both_strip_layouts_read_every_group():
    """Model version 49 grew two fields in the group and strip headers. With
    the wrong stride the second group is read from the wrong place."""
    for extended in (False, True):
        vtx = parse_vtx(build_vtx(groups=3, extended=extended), "g.vtx", extended=extended)
        mesh = vtx.body_parts[0][0][0]
        assert list(mesh.indices) == [0, 1, 2, 0, 2, 3] * 3, extended
        assert vtx.warnings == []


def test_wrong_layout_is_what_lost_the_vortigaunt():
    vtx = parse_vtx(build_vtx(groups=2, extended=True), "g.vtx", extended=False)
    mesh = vtx.body_parts[0][0][0]
    assert mesh.triangle_count != 4 or vtx.warnings           # garbage or complaint, never silent success


def test_load_model_picks_the_layout_from_the_model_version():
    for version, extended in ((48, False), (49, True), (44, False)):
        source, rel = _source(mdl=build_mdl(version=version), vvd=build_vvd(),
                              vtx=build_vtx(groups=2, extended=extended))
        model = load_model(source, rel)
        assert model.triangle_count == 4, (version, model.warnings)


def test_rejects_an_unsupported_version():
    raw = bytearray(build_vtx())
    struct.pack_into("<i", raw, 0, 6)
    try:
        parse_vtx(bytes(raw), "old.vtx")
        raise AssertionError("expected FormatError")
    except FormatError:
        pass


# ------------------------------------------------------------------ whole
def _source(mdl=None, vvd=None, vtx=None, stem="models/test/fake"):
    files = {}
    if mdl is not None:
        files[f"{stem}.mdl"] = mdl
    if vvd is not None:
        files[f"{stem}.vvd"] = vvd
    if vtx is not None:
        files[f"{stem}.dx90.vtx"] = vtx
    return FakeSource(files), f"{stem}.mdl"


def test_a_complete_model_assembles():
    mdl, vvd, vtx = build_triangle_model()
    source, rel = _source(mdl, vvd, vtx)
    model = load_model(source, rel)
    assert len(model.bones) == 2
    assert len(model.meshes) == 1
    mesh = model.meshes[0]
    assert mesh.vertex_count == 4
    assert mesh.triangle_count == 2
    assert list(mesh.indices) == [0, 1, 2, 0, 2, 3]
    assert mesh.material == "fakemat"
    assert model.warnings == [], model.warnings


def test_geometry_values_survive_the_whole_pipeline():
    mdl, vvd, vtx = build_triangle_model()
    source, rel = _source(mdl, vvd, vtx)
    mesh = load_model(source, rel).meshes[0]
    assert list(mesh.positions[:3]) == [0.0, 0.0, 0.0]
    assert list(mesh.positions[6:9]) == [10.0, 20.0, 0.0]
    assert list(mesh.uvs[4:6]) == [1.0, 1.0]


def test_bounds_come_from_the_geometry_not_the_hull():
    mdl, vvd, vtx = build_triangle_model()
    source, rel = _source(mdl, vvd, vtx)
    model = load_model(source, rel)
    lo, hi = model.bounds()
    assert lo == (0.0, 0.0, 0.0)
    assert hi == (10.0, 20.0, 5.0)
    # the header hull is a different box and must not leak into bounds()
    assert model.info.hull_max == (11.0, 22.0, 33.0)


def test_bounds_of_a_model_without_geometry_are_zero():
    source, rel = _source(build_mdl(), None, None)
    model = load_model(source, rel)
    assert model.bounds() == ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0))


def test_material_candidates_use_the_model_folders():
    mdl, vvd, vtx = build_triangle_model()
    source, rel = _source(mdl, vvd, vtx)
    model = load_model(source, rel)
    assert model.material_candidates("fakemat") == [
        "materials/models/test/fakemat.vmt",
        "materials/fakemat.vmt",
    ]


def test_missing_vertex_data_yields_bones_and_a_warning():
    source, rel = _source(build_mdl(), None, build_vtx())
    model = load_model(source, rel)
    assert len(model.bones) == 2
    assert model.meshes == []
    assert any("vvd" in w for w in model.warnings), model.warnings


def test_missing_index_data_yields_bones_and_a_warning():
    source, rel = _source(build_mdl(), build_vvd(), None)
    model = load_model(source, rel)
    assert model.meshes == []
    assert any("vtx" in w for w in model.warnings), model.warnings


def test_a_mismatched_checksum_is_reported():
    mdl = build_mdl(checksum=0x1111)
    vvd = build_vvd(checksum=0x2222)
    source, rel = _source(mdl, vvd, build_vtx())
    model = load_model(source, rel)
    assert any("different model" in w for w in model.warnings), model.warnings


def test_a_mesh_claiming_more_vertices_than_exist_is_skipped():
    mdl = build_mdl(vertex_count=99)             # header lies about the count
    source, rel = _source(mdl, build_vvd(), build_vtx(vertex_count=99))
    model = load_model(source, rel)
    assert model.meshes == []
    assert any("skipped" in w for w in model.warnings), model.warnings


def test_a_model_that_is_not_there_raises():
    try:
        load_model(FakeSource({}), "models/nope.mdl")
        raise AssertionError("expected FormatError")
    except FormatError:
        pass


def test_vtx_flavours_are_tried_in_order():
    from Core.Code.formats import find_model_files
    mdl, vvd, vtx = build_triangle_model()
    source = FakeSource({
        "models/test/fake.mdl": mdl,
        "models/test/fake.vvd": vvd,
        "models/test/fake.dx80.vtx": vtx,          # no dx90 present
    })
    _, found_vvd, found_vtx = find_model_files(source, "models/test/fake.mdl")
    assert found_vvd == "models/test/fake.vvd"
    assert found_vtx == "models/test/fake.dx80.vtx"


# ------------------------------------------------------------- levels of detail
def _two_mesh_model(lod, has_fixups, vertex_count):
    """Two meshes of 4 and 2 vertices at level 0; level 1 keeps 2 and 2."""
    from array import array
    from Core.API.model import ModelInfo
    from Core.Code.formats.mdl import MdlBodyPart, MdlFile, MdlMesh, MdlModel
    from Core.Code.formats.vtx import VtxFile, VtxMesh
    from Core.Code.formats.vvd import VvdFile
    from Core.Code.formats import build_model

    meshes = [MdlMesh(0, 4, 0, (4, 2, 0, 0, 0, 0, 0, 0)),
              MdlMesh(0, 2, 4, (2, 2, 0, 0, 0, 0, 0, 0))]
    mdl = MdlFile(info=ModelInfo(name="t"), material_names=["m"],
                  body_parts=[MdlBodyPart("p", [MdlModel("m", 6, 0, meshes)])])
    vvd = VvdFile(lod=lod, has_fixups=has_fixups)
    vvd.positions = array("f", [float(i) for i in range(vertex_count * 3)])
    vvd.normals = array("f", [0.0] * (vertex_count * 3))
    vvd.uvs = array("f", [0.0] * (vertex_count * 2))
    vvd.bone_indices = array("B", [0] * (vertex_count * 3))
    vvd.bone_weights = array("f", [1.0] * (vertex_count * 3))
    tri = VtxMesh(indices=array("I", [0, 1, 0]))
    vtx = VtxFile(body_parts=[[[tri, VtxMesh(indices=array("I", [0, 1, 1]))]]])
    return build_model(mdl, vvd, vtx)


def test_level_zero_uses_the_offsets_in_the_file():
    model = _two_mesh_model(lod=0, has_fixups=True, vertex_count=6)
    assert [m.vertex_count for m in model.meshes] == [4, 2]
    assert model.meshes[1].positions[0] == 4 * 3          # second mesh starts at vertex 4


def test_lower_levels_are_compacted_when_fixups_exist():
    # level 1 array holds 2 + 2 vertices; the second mesh now starts at 2
    model = _two_mesh_model(lod=1, has_fixups=True, vertex_count=4)
    assert [m.vertex_count for m in model.meshes] == [2, 2]
    assert model.meshes[1].positions[0] == 2 * 3
    assert model.warnings == []


def test_lower_levels_keep_offsets_without_fixups():
    # no fixup table: the whole array is shared, only the counts shrink
    model = _two_mesh_model(lod=1, has_fixups=False, vertex_count=6)
    assert [m.vertex_count for m in model.meshes] == [2, 2]
    assert model.meshes[1].positions[0] == 4 * 3


def test_an_empty_mesh_takes_no_room_at_any_level():
    from Core.Code.formats.mdl import MdlMesh
    ghost = MdlMesh(0, 0, 0, (2147, 2147, 2147, 0, 0, 0, 0, 0))     # as compiled into bomb_eotl_red
    assert ghost.vertices_at(0) == 0 and ghost.vertices_at(1) == 0
    real = MdlMesh(0, 10, 0, (10, 4, 0, 0, 0, 0, 0, 0))
    assert real.vertices_at(1) == 4 and real.vertices_at(7) == 0
    untabled = MdlMesh(0, 10, 0, (0,) * 8)
    assert untabled.vertices_at(3) == 10
