"""
Scene assembly: model -> materials -> textures -> draw order, with fake content.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from App.Code.render.scene import build_scene
from Core.Code.formats.vtf import ImageFormat
from fixtures.fake_model import build_triangle_model
from fixtures.fake_texture import build_vtf


class _Content:
    """Just enough of a content library: bytes and text by path."""

    def __init__(self, files):
        self.files = {k.lower(): v for k, v in files.items()}

    def read_bytes(self, rel):
        v = self.files.get(rel.lower())
        return v if isinstance(v, bytes) else None

    def read_text(self, rel):
        v = self.files.get(rel.lower())
        return v if isinstance(v, str) else None


def _content(material_text, with_texture=True, **model_kw):
    mdl, vvd, vtx = build_triangle_model(**model_kw)
    files = {
        "models/test/thing.mdl": mdl,
        "models/test/thing.vvd": vvd,
        "models/test/thing.dx90.vtx": vtx,
        "materials/models/test/fakemat.vmt": material_text,
    }
    if with_texture:
        files["materials/models/test/skin.vtf"] = build_vtf(
            [(255, 0, 0, 255)] * 16, 4, 4, fmt=ImageFormat.DXT1)
    return _Content(files)


def test_scene_resolves_material_and_texture():
    src = _content('"VertexLitGeneric" { "$basetexture" "models/test/skin" }')
    scene = build_scene(src, "models/test/thing.mdl")
    assert len(scene.items) == 1
    item = scene.items[0]
    assert item.material is not None and item.material.shader == "VertexLitGeneric"
    assert item.texture_key == "materials/models/test/skin.vtf"
    assert scene.textures[item.texture_key].width == 4
    assert item.lit and not item.blended
    assert scene.warnings == []


def test_missing_texture_is_a_warning_not_a_failure():
    src = _content('"VertexLitGeneric" { "$basetexture" "models/test/skin" }', with_texture=False)
    scene = build_scene(src, "models/test/thing.mdl")
    assert scene.items[0].texture_key == ""
    assert any("could be read" in w for w in scene.warnings)


def test_a_material_falls_through_to_the_texture_it_can_read():
    # shipped materials name a base texture that was never packed and an HDR twin
    # that was; the engine draws with whichever it finds
    src = _content('"Sky" { "$basetexture" "models/test/missing" "$hdrbasetexture" "models/test/skin" }')
    scene = build_scene(src, "models/test/thing.mdl")
    assert scene.items[0].texture_key == "materials/models/test/skin.vtf"
    assert not scene.warnings


def test_a_self_shadowed_bump_is_not_used_as_a_normal_map():
    from Core.Code.formats.vmt import parse_vmt
    plain = parse_vmt('"LightmappedGeneric" { "$bumpmap" "nature/x_normal" }', "a.vmt")
    assert plain.bump_map == "materials/nature/x_normal.vtf" and not plain.self_shadowed_bump
    ss = parse_vmt('"LightmappedGeneric" { "$bumpmap" "nature/x-ssbump" "$ssbump" 1 }', "b.vmt")
    assert ss.self_shadowed_bump and ss.bump_map == ""


def test_missing_material_is_a_warning_not_a_failure():
    src = _content("")
    src.files.pop("materials/models/test/fakemat.vmt")
    scene = build_scene(src, "models/test/thing.mdl")
    assert scene.items[0].material is None
    assert any("no material" in w for w in scene.warnings)


def test_blend_flags_flow_through():
    src = _content('"UnlitGeneric" { "$basetexture" "models/test/skin" "$translucent" 1 "$nocull" 1 }')
    item = build_scene(src, "models/test/thing.mdl").items[0]
    assert item.translucent and item.two_sided and item.blended and not item.lit


def test_alpha_below_one_counts_as_translucent():
    src = _content('"VertexLitGeneric" { "$basetexture" "models/test/skin" "$alpha" 0.5 }')
    item = build_scene(src, "models/test/thing.mdl").items[0]
    assert item.translucent and item.alpha == 0.5


def test_materials_and_textures_are_shared_not_reloaded():
    src = _content('"VertexLitGeneric" { "$basetexture" "models/test/skin" }')
    scene = build_scene(src, "models/test/thing.mdl")
    assert len(scene.materials) == 1 and len(scene.textures) == 1


def test_summary_mentions_what_was_found():
    src = _content('"VertexLitGeneric" { "$basetexture" "models/test/skin" }')
    text = build_scene(src, "models/test/thing.mdl").summary()
    assert "1 draw items" in text and "1 textured" in text


# -- the sky ------------------------------------------------------------------------
def _sky_content(faces=("rt", "lf", "bk", "ft", "up", "dn"), transform=True):
    files = {}
    pixel = build_vtf([(10, 20, 30, 255)] * 16, 4, 4, fmt=ImageFormat.DXT1)
    for face in faces:
        extra = ' "$basetexturetransform" "center 0 0 scale 1 2 rotate 0 translate 0 0"' \
            if transform and face not in ("up", "dn") else ""
        files[f"materials/skybox/test_sky{face}.vmt"] = \
            f'"sky" {{ "$basetexture" "skybox/test_sky{face}" "$nofog" 1 "$ignorez" 1{extra} }}'
        files[f"materials/skybox/test_sky{face}.vtf"] = pixel
    return _Content(files)


def test_sky_faces_sit_on_the_unit_cube_where_the_engine_puts_them():
    from App.Code.render.scene import SKY_FACES, sky_face_corners
    where = {"rt": (0, 1), "lf": (0, -1), "bk": (1, 1), "ft": (1, -1), "up": (2, 1), "dn": (2, -1)}
    for name, table in SKY_FACES:
        positions, uvs = sky_face_corners(table)
        axis, sign = where[name]
        assert all(p[axis] == sign for p in positions), name
        assert all(abs(p[a]) == 1 for p in positions for a in range(3)), name
        assert uvs == [(0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0)]
    # neighbours share an edge with matching texture sides: rt's left (u=0) is +Y,
    # where bk's right (u=1) is +X - that is what keeps the seams continuous
    rt, _ = sky_face_corners(dict(SKY_FACES)["rt"])
    bk, _ = sky_face_corners(dict(SKY_FACES)["bk"])
    assert rt[0][1] == 1 and rt[3][1] == 1 and bk[1][0] == 1 and bk[2][0] == 1


def test_load_sky_builds_six_unlit_faces_with_the_transform_applied():
    from App.Code.render.scene import Scene, load_sky
    scene = Scene()
    sky = load_sky(_sky_content(), scene, "test_sky")
    assert sky is not None and len(sky.items) == 6
    for item in sky.items:
        assert not item.lit and item.two_sided and not item.blended
        assert item.texture_key == f"materials/skybox/{item.mesh.material.split('/')[-1]}.vtf"
        assert item.mesh.vertex_count == 4 and item.mesh.triangle_count == 2
    by_name = {item.mesh.material[-2:]: item for item in sky.items}
    # a side: the texture is the top half of the face, so v runs 0..2 top to bottom
    assert list(by_name["rt"].mesh.uvs[1::2]) == [2.0, 2.0, 0.0, 0.0]
    # the top has no transform and covers the face
    assert list(by_name["up"].mesh.uvs[1::2]) == [1.0, 1.0, 0.0, 0.0]
    assert len(scene.textures) == 6 and not scene.warnings


def test_sky_is_none_without_a_name_and_a_missing_face_is_a_warning():
    from App.Code.render.scene import Scene, load_sky
    assert load_sky(_sky_content(), Scene(), "") is None
    scene = Scene()
    sky = load_sky(_sky_content(faces=("rt", "lf", "bk", "ft", "up")), scene, "test_sky")
    assert sky is not None and len(sky.items) == 5
    assert any("test_skydn" in w for w in scene.warnings)
    assert load_sky(_Content({}), Scene(), "nothing") is None


def test_texture_transform_scales_rotates_and_translates_about_the_centre():
    from App.Code.render.scene import _texture_transform
    from Core.Code.formats.vmt import parse_vmt
    m = parse_vmt('"sky" { "$basetexturetransform" "center .5 .5 scale 2 2 rotate 90 translate .1 0" }', "t")
    f = _texture_transform(m)
    u, v = f(1.0, 0.5)                  # (0.5, 0) after scaling about the centre, then a quarter turn
    assert abs(u - 0.6) < 1e-9 and abs(v - 1.5) < 1e-9
    assert _texture_transform(parse_vmt('"sky" { }', "t")) is None


def test_look_takes_exposure_from_the_camera_and_the_map():
    from App.Code.render.scene import Look
    from Core.Code.formats.bsp import BspFile
    plain = Look.of(None)
    assert plain.tone_map_scale == 1.0 and not plain.auto_exposure and plain.bloom_scale == 0.0

    class _Camera:
        tone_map_scale, bloom_scale, bloom_width = 1.5, 0.28, 9.0
    look = Look.of(_Camera())
    assert look.tone_map_scale == 1.5 and look.bloom_scale == 0.28 and not look.auto_exposure
    # a map without a tonemap controller is shown as it is lit
    bsp = BspFile(name="m", version=20)
    bsp.entities = [{"classname": "worldspawn"}]
    assert not Look.of(_Camera(), bsp).auto_exposure and bsp.tone_map is None
    # with one, auto exposure is on and its bounds come from the entity
    bsp.entities.append({"classname": "env_tonemap_controller", "mat_autoexposure_min": "0.8",
                         "mat_autoexposure_max": "4", "mat_tonemap_target": "0.22"})
    look = Look.of(_Camera(), bsp)
    assert look.auto_exposure and look.exposure_min == 0.8 and look.exposure_max == 4.0
    assert look.target == 0.22 and look.tone_map_scale == 1.5
    assert bsp.tone_map["classname"] == "env_tonemap_controller"
