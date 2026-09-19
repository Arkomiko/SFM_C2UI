"""
VTF and VMT readers, checked against bytes and text we wrote ourselves.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Core.API.material import Material, as_bool, as_float, as_vec, texture_path
from Core.Code.formats import FormatError, load_material, parse_vmt, parse_vtf
from Core.Code.formats.vtf import ImageFormat, image_size
from fixtures.fake_texture import FLAG_ENVMAP, build_vtf

RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
CLEAR = (0, 0, 0, 0)


def _checker(width, height, a=RED, b=BLUE):
    return [a if (x + y) % 2 == 0 else b for y in range(height) for x in range(width)]


def _pixel(rgba, width, x, y):
    i = (y * width + x) * 4
    return tuple(rgba[i:i + 4])


# ------------------------------------------------------------------- vtf header
def test_header_fields_land_where_expected():
    data = build_vtf(_checker(8, 4), 8, 4, fmt=ImageFormat.BGRA8888, version=(7, 2), mips=3)
    tex = parse_vtf(data, "t.vtf")
    assert (tex.width, tex.height) == (8, 4)
    assert tex.version == (7, 2)
    assert tex.image_format == ImageFormat.BGRA8888
    assert tex.format_name == "BGRA8888"
    assert tex.mip_count == 3
    assert tex.reflectivity == (0.5, 0.5, 0.5)
    assert tex.depth == 1
    assert not tex.is_cubemap
    assert tex.warnings == []


def test_rejects_things_that_are_not_textures():
    for bad in (b"", b"VTF\0" + bytes(10), b"IDST" + bytes(100)):
        try:
            parse_vtf(bad, "bad.vtf")
        except FormatError:
            continue
        raise AssertionError(f"accepted {bad[:4]!r}")


def test_unknown_version_is_refused():
    data = bytearray(build_vtf(_checker(4, 4), 4, 4))
    data[4:8] = (8).to_bytes(4, "little")
    try:
        parse_vtf(bytes(data), "v8.vtf")
    except FormatError as exc:
        assert "8.2" in str(exc)
    else:
        raise AssertionError("version 8 accepted")


# ------------------------------------------------------------------- locating the image
def test_thumbnail_is_skipped_in_pre_73_files():
    """A 7.2 file has a low-res image between header and data. Reading from
    the header size would decode the thumbnail as the image."""
    px = _checker(4, 4, GREEN, GREEN)
    data = build_vtf(px, 4, 4, fmt=ImageFormat.RGBA8888, version=(7, 2), thumbnail=True)
    tex = parse_vtf(data, "t.vtf")
    rgba, w, h = tex.to_rgba()
    assert (w, h) == (4, 4)
    assert _pixel(rgba, 4, 0, 0) == GREEN


def test_resource_table_locates_the_image_in_73_and_later():
    px = _checker(4, 4, BLUE, BLUE)
    data = build_vtf(px, 4, 4, fmt=ImageFormat.RGBA8888, version=(7, 4))
    tex = parse_vtf(data, "t.vtf")
    rgba, _w, _h = tex.to_rgba()
    assert _pixel(rgba, 4, 3, 3) == BLUE
    assert tex.warnings == []


def test_mips_are_stored_smallest_first_and_returned_largest_first():
    px = _checker(8, 8, RED, RED)
    data = build_vtf(px, 8, 8, fmt=ImageFormat.RGBA8888, mips=4)
    tex = parse_vtf(data, "t.vtf")
    assert [len(m) for m in tex.mips] == [8 * 8 * 4, 4 * 4 * 4, 2 * 2 * 4, 1 * 1 * 4]
    assert tex.mip_size(3) == (1, 1)
    rgba, w, h = tex.to_rgba(level=2)
    assert (w, h) == (2, 2) and _pixel(rgba, 2, 1, 1) == RED


def test_max_size_picks_the_smallest_mip_that_is_big_enough():
    data = build_vtf(_checker(64, 32), 64, 32, fmt=ImageFormat.RGBA8888, mips=7)
    tex = parse_vtf(data, "t.vtf")
    _rgba, w, h = tex.to_rgba(max_size=16)
    assert (w, h) == (16, 8)
    _rgba, w, h = tex.to_rgba(max_size=1000)
    assert (w, h) == (64, 32)


def test_cubemap_faces_do_not_shift_later_mips():
    """Each mip holds one copy per face; forgetting that reads the wrong bytes
    for every mip after the first."""
    px = _checker(8, 8, GREEN, GREEN)
    data = build_vtf(px, 8, 8, fmt=ImageFormat.RGBA8888, version=(7, 5), mips=2,
                     flags=FLAG_ENVMAP, faces=6)
    tex = parse_vtf(data, "cube.vtf")
    assert tex.is_cubemap
    rgba, w, _h = tex.to_rgba(level=0)
    assert w == 8 and _pixel(rgba, 8, 7, 7) == GREEN
    assert tex.warnings == []


def test_frames_do_not_shift_later_mips():
    px = _checker(8, 8, BLUE, BLUE)
    data = build_vtf(px, 8, 8, fmt=ImageFormat.RGBA8888, mips=3, frames=3)
    tex = parse_vtf(data, "anim.vtf")
    assert tex.frames == 3
    rgba, _w, _h = tex.to_rgba()
    assert _pixel(rgba, 8, 0, 7) == BLUE


def test_truncated_file_keeps_what_it_has_and_warns():
    px = _checker(8, 8, RED, RED)
    full = build_vtf(px, 8, 8, fmt=ImageFormat.RGBA8888, mips=4)
    tex = parse_vtf(full[:-100], "short.vtf")
    assert tex.mips                                   # the small mips were intact
    assert (tex.width, tex.height) == (4, 4)          # largest present became the image
    assert any("ends early" in w for w in tex.warnings)
    assert any("full-size image is missing" in w for w in tex.warnings)


# ------------------------------------------------------------------- decoding
def test_uncompressed_channel_orders():
    px = [(10, 20, 30, 40)]
    for fmt in (ImageFormat.RGBA8888, ImageFormat.BGRA8888, ImageFormat.ABGR8888,
                ImageFormat.ARGB8888):
        tex = parse_vtf(build_vtf(px, 1, 1, fmt=fmt, thumbnail=False), "t.vtf")
        rgba, _w, _h = tex.to_rgba()
        assert tuple(rgba) == (10, 20, 30, 40), fmt
    for fmt in (ImageFormat.RGB888, ImageFormat.BGR888):
        tex = parse_vtf(build_vtf(px, 1, 1, fmt=fmt, thumbnail=False), "t.vtf")
        rgba, _w, _h = tex.to_rgba()
        assert tuple(rgba) == (10, 20, 30, 255), fmt


def test_single_channel_formats():
    px = [(77, 0, 0, 200)]
    rgba, _, _ = parse_vtf(build_vtf(px, 1, 1, fmt=ImageFormat.I8), "t").to_rgba()
    assert tuple(rgba) == (77, 77, 77, 255)
    rgba, _, _ = parse_vtf(build_vtf(px, 1, 1, fmt=ImageFormat.A8), "t").to_rgba()
    assert tuple(rgba) == (255, 255, 255, 200)
    rgba, _, _ = parse_vtf(build_vtf(px, 1, 1, fmt=ImageFormat.IA88), "t").to_rgba()
    assert tuple(rgba) == (77, 77, 77, 200)


def test_half_float_hdr_is_clamped_to_byte_range():
    px = [(255, 128, 0, 255)]
    tex = parse_vtf(build_vtf(px, 1, 1, fmt=ImageFormat.RGBA16161616F), "hdr")
    rgba, _, _ = tex.to_rgba()
    r, g, b, a = rgba
    assert r == 255 and b == 0 and a == 255
    assert abs(g - 128) <= 1                          # half precision rounding


def test_dxt1_blocks_decode_to_their_two_colours():
    px = _checker(4, 4, RED, BLUE)
    tex = parse_vtf(build_vtf(px, 4, 4, fmt=ImageFormat.DXT1), "t.vtf")
    assert len(tex.mips[0]) == 8
    rgba, _w, _h = tex.to_rgba()
    for y in range(4):
        for x in range(4):
            assert _pixel(rgba, 4, x, y) == (RED if (x + y) % 2 == 0 else BLUE), (x, y)


def test_dxt5_carries_alpha_per_pixel():
    px = [RED if x < 2 else (255, 0, 0, 0) for y in range(4) for x in range(4)]
    tex = parse_vtf(build_vtf(px, 4, 4, fmt=ImageFormat.DXT5), "t.vtf")
    assert len(tex.mips[0]) == 16
    rgba, _w, _h = tex.to_rgba()
    assert _pixel(rgba, 4, 0, 0) == RED
    assert _pixel(rgba, 4, 3, 0) == (255, 0, 0, 0)


def test_dxt_handles_sizes_that_are_not_multiples_of_four():
    px = _checker(6, 2, GREEN, GREEN)
    tex = parse_vtf(build_vtf(px, 6, 2, fmt=ImageFormat.DXT1), "t.vtf")
    assert len(tex.mips[0]) == image_size(ImageFormat.DXT1, 6, 2) == 2 * 8
    rgba, w, h = tex.to_rgba()
    assert (w, h) == (6, 2) and len(rgba) == 6 * 2 * 4
    assert _pixel(rgba, 6, 5, 1) == GREEN


def test_block_sizes_never_drop_below_one_block():
    assert image_size(ImageFormat.DXT1, 1, 1) == 8
    assert image_size(ImageFormat.DXT5, 2, 2) == 16
    assert image_size(ImageFormat.BGR888, 3, 3) == 27


# ------------------------------------------------------------------- vmt values
def test_value_helpers():
    assert as_float("0.5") == 0.5
    assert as_float("[0.25]") == 0.25
    assert as_float(None, 7.0) == 7.0
    assert as_vec("[1 .5 0]") == (1.0, 0.5, 0.0)
    assert as_vec("{255 0 51}") == (1.0, 0.0, 0.2)
    assert as_vec("junk") == ()
    assert as_bool("1") and not as_bool("0") and not as_bool(None)


def test_texture_paths_are_normalised():
    assert texture_path("models\\Player\\Scout\\scout_red") == "materials/models/player/scout/scout_red.vtf"
    assert texture_path("brick/wall01.vtf") == "materials/brick/wall01.vtf"
    assert texture_path("  ") == ""
    assert texture_path("_rt_Camera") == ""
    assert texture_path("env_cubemap") == ""


# ------------------------------------------------------------------- vmt parsing
SCOUT = '''
"VertexLitGeneric"
{
    "$baseTexture" "models/player/scout/scout_red"
    "$bumpmap" "models/player/scout/scout_normal"
    "$phong" 1
    "$color2" "[1 0.5 1]"
    ">=DX90"
    {
        "$phongexponent" 25
    }
    "<DX90"
    {
        "$phong" 0
    }
    "Proxies"
    {
        "Sine" { "resultVar" "$color" }
        "Clamp" { }
    }
}
'''


def test_shader_parameters_and_conditionals():
    mat = parse_vmt(SCOUT, "materials/models/player/scout/scout_red.vmt")
    assert mat.shader == "VertexLitGeneric"
    assert mat.base_texture == "materials/models/player/scout/scout_red.vtf"
    assert mat.bump_map == "materials/models/player/scout/scout_normal.vtf"
    assert mat.param("$phong") == "1"                 # <DX90 did not apply
    assert mat.param("$phongexponent") == "25"        # >=DX90 did
    assert mat.proxies == ["Sine", "Clamp"]
    assert mat.color == (1.0, 0.5, 1.0)
    assert mat.is_model_shader
    assert not mat.translucent
    assert mat.warnings == []


def test_parameter_keys_are_case_blind_and_last_wins():
    mat = parse_vmt('LightmappedGeneric { $BaseTexture "a" $basetexture "b" }', "x.vmt")
    assert mat.param("$BASETEXTURE") == "b"
    assert mat.textures() == {"$basetexture": "materials/b.vtf"}


def test_fallback_shaders_at_top_level_are_ignored():
    text = '''
    "LightmappedGeneric_DX8" { "$basetexture" "old" }
    "LightmappedGeneric" { "$basetexture" "new" }
    "Water_DX60" { "$basetexture" "older" }
    '''
    mat = parse_vmt(text, "x.vmt")
    assert mat.shader == "LightmappedGeneric"
    assert mat.base_texture == "materials/new.vtf"


def test_only_fallbacks_takes_the_highest_level_and_warns():
    text = '"Water_DX60" { "$basetexture" "a" } "Water_DX80" { "$basetexture" "b" }'
    mat = parse_vmt(text, "x.vmt")
    assert mat.shader == "Water_DX80" and mat.base_texture == "materials/b.vtf"
    assert any("fallback" in w for w in mat.warnings)


def test_nested_dx9_fallback_blocks_apply():
    text = '"VertexLitGeneric" { "$basetexture" "a" "VertexLitGeneric_DX9" { "$bumpmap" "n" } "VertexLitGeneric_DX8" { "$bumpmap" "old" } }'
    mat = parse_vmt(text, "x.vmt")
    assert mat.bump_map == "materials/n.vtf"


def test_eye_shaders_draw_with_the_iris():
    mat = parse_vmt('"EyeRefract" { "$iris" "models/x/eye" "$corneatexture" "models/x/cornea" }', "e.vmt")
    assert mat.base_texture == "materials/models/x/eye.vtf"


def test_blend_flags():
    mat = parse_vmt('"UnlitGeneric" { "$translucent" 1 "$nocull" "1" "$additive" 0 "$alpha" ".5" }', "x.vmt")
    assert mat.translucent and mat.two_sided and not mat.additive
    assert mat.alpha == 0.5


def test_garbage_is_reported_not_swallowed():
    mat = parse_vmt("", "empty.vmt")
    assert mat.shader == "" and "no shader block" in mat.warnings


# ------------------------------------------------------------------- patch materials
class _Source:
    def __init__(self, files):
        self.files = {k.lower(): v for k, v in files.items()}
        self.reads = []

    def read_text(self, rel):
        self.reads.append(rel)
        return self.files.get(rel.lower())


BASE = '"VertexLitGeneric" { "$basetexture" "models/base" "$phong" 1 "$phongexponent" 10 }'


def test_patch_layers_insert_and_replace_over_the_included_material():
    src = _Source({
        "materials/models/base.vmt": BASE,
        "materials/models/blue.vmt": '''
            "Patch" {
                include "materials/models/base.vmt"
                insert { "$color2" "[0 0 1]" }
                replace { "$phongexponent" 40 }
            }''',
    })
    mat = load_material(src, "materials/models/blue.vmt")
    assert mat.shader == "VertexLitGeneric"
    assert mat.path == "materials/models/blue.vmt"
    assert mat.base_texture == "materials/models/base.vtf"
    assert mat.param("$phongexponent") == "40"
    assert mat.color == (0.0, 0.0, 1.0)
    assert mat.includes == ["materials/models/base.vmt"]
    assert mat.warnings == []


def test_patch_chains_and_loops_are_bounded():
    src = _Source({
        "materials/a.vmt": '"Patch" { include "materials/b.vmt" insert { "$x" 1 } }',
        "materials/b.vmt": '"Patch" { include "materials/a.vmt" insert { "$y" 2 } }',
    })
    mat = load_material(src, "a")
    assert any("loop" in w for w in mat.warnings)
    assert len(src.reads) < 10


def test_patch_with_missing_base_keeps_its_own_parameters():
    src = _Source({"materials/p.vmt": '"Patch" { include "materials/gone.vmt" insert { "$basetexture" "models/mine" } }'})
    mat = load_material(src, "materials/p.vmt")
    assert mat.shader == "Patch"
    assert mat.base_texture == "materials/models/mine.vtf"
    assert any("not found" in w for w in mat.warnings)


def test_load_material_normalises_the_request():
    src = _Source({"materials/models/base.vmt": BASE})
    assert load_material(src, "Models\\Base").path == "materials/models/base.vmt"
    assert load_material(src, "materials/models/base.vmt") is not None
    assert load_material(src, "materials/nothing.vmt") is None


def test_material_is_a_plain_value():
    mat = Material(shader="UnlitGeneric", params={"$basetexture": "x"})
    assert mat.summary().startswith("UnlitGeneric")
    assert mat.has("$BaseTexture") and not mat.has("$bumpmap")
