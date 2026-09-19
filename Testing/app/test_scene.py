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
    assert any("not found" in w for w in scene.warnings)


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
