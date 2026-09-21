"""Source maps: a BSP built here from its lumps reads back as faces, a displacement,
static props, entities and the embedded pakfile."""
import io
import struct
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Core.Code.formats.bsp import EMIT_POINT, EMIT_SKYLIGHT, EMIT_SPOTLIGHT, FormatError, map_path, parse_bsp

# ------------------------------------------------------------------- a tiny map
def _texinfo(width_dir, height_dir, flags, texdata, lm_s=(0, 0, 0, 0), lm_t=(0, 0, 0, 0)):
    # textureVecs s, t; then the lightmap's two
    return struct.pack("<16fii", *width_dir, *height_dir, *lm_s, *lm_t, flags, texdata)


def _face(first_edge, num_edges, texinfo, dispinfo=-1, planenum=0, side=0, lightofs=-1, lm_size=(0, 0)):
    return struct.pack("<HBBihhhh4BifiiiiiHHI", planenum, side, 0, first_edge, num_edges, texinfo, dispinfo,
                       -1, 0, 0, 0, 0, lightofs, 1.0, 0, 0, lm_size[0], lm_size[1], 0, 0, 0, 0)


def _build(faces, texinfos, texdata_names, vertexes, edges, surfedges, dispinfo=b"", dispverts=b"",
           entities="", props=None, pak=None, version=20, models=None, lighting=b"", extra=None):
    lumps = {}
    lumps[8] = lighting
    if extra:
        lumps.update(extra)
    lumps[1] = struct.pack("<3ffi", 0, 0, 1, 0, 0)                          # one plane, +z
    names = b"".join(n.encode() + b"\0" for n in texdata_names)
    offsets, at = [], 0
    for n in texdata_names:
        offsets.append(at); at += len(n) + 1
    lumps[43] = names
    lumps[44] = struct.pack(f"<{len(offsets)}i", *offsets)
    lumps[2] = b"".join(struct.pack("<3fiiiii", 1, 1, 1, i, 64, 64, 64, 64) for i in range(len(texdata_names)))
    lumps[3] = b"".join(struct.pack("<3f", *v) for v in vertexes)
    lumps[6] = b"".join(texinfos)
    lumps[7] = b"".join(faces)
    lumps[12] = b"".join(struct.pack("<HH", *e) for e in edges)
    lumps[13] = struct.pack(f"<{len(surfedges)}i", *surfedges)
    lumps[14] = models if models is not None else struct.pack("<3f3f3fiii", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, len(faces))
    lumps[26] = dispinfo
    lumps[33] = dispverts
    lumps[0] = entities.encode() + b"\0"
    if pak is not None:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            for name, data in pak.items():
                z.writestr(name, data)
        lumps[40] = buf.getvalue()
    if props is not None:
        lumps[35] = props
    header_size = 8 + 64 * 16 + 4
    body = b""
    table = []
    at = header_size
    for i in range(64):
        raw = lumps.get(i, b"")
        table.append((at if raw else 0, len(raw)))
        body += raw
        at += len(raw)
    header = b"VBSP" + struct.pack("<i", version)
    for offset, length in table:
        header += struct.pack("<iiii", offset, length, 0, 0)
    header += struct.pack("<i", 1)
    return header + body


def _quad_map(**kw):
    verts = [(0, 0, 0), (64, 0, 0), (64, 64, 0), (0, 64, 0)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    surfedges = [0, 1, 2, 3]
    texinfos = [_texinfo((1, 0, 0, 0), (0, 1, 0, 0), 0, 0),
                _texinfo((1, 0, 0, 0), (0, 1, 0, 0), 0x80, 0),        # nodraw
                _texinfo((1, 0, 0, 0), (0, 1, 0, 0), 0, 1)]           # a tool texture
    faces = kw.pop("faces", [_face(0, 4, 0)])
    return _build(faces, texinfos, ["CONCRETE/Floor01", "tools/toolsnodraw"], verts, edges, surfedges, **kw)


# ------------------------------------------------------------------- tests
def test_map_path_forms():
    assert map_path("cp_badlands") == "maps/cp_badlands.bsp"
    assert map_path("cp_badlands.bsp") == "maps/cp_badlands.bsp"
    assert map_path("maps\\stage.bsp") == "maps/stage.bsp"
    assert map_path("") == ""


def test_rejects_other_files():
    try:
        parse_bsp(b"IBSP" + b"\0" * 2000, "x")
    except FormatError:
        return
    raise AssertionError


def test_quad_face_reads_with_uvs_and_normal():
    bsp = parse_bsp(_quad_map(), "quad")
    assert bsp.version == 20 and len(bsp.faces) == 1
    face = bsp.faces[0]
    assert face.material == "concrete/floor01"
    assert face.positions == [(0, 0, 0), (64, 0, 0), (64, 64, 0), (0, 64, 0)]
    assert face.uvs == [(0, 0), (1, 0), (1, 1), (0, 1)]                # texture vectors over the 64px texture
    assert face.normal == (0, 0, 1)
    assert face.indices == [0, 1, 2, 0, 2, 3]                             # a fan
    assert bsp.bounds == ((0, 0, 0), (64, 64, 0))


def test_nodraw_and_tool_faces_are_dropped():
    bsp = parse_bsp(_quad_map(faces=[_face(0, 4, 0), _face(0, 4, 1), _face(0, 4, 2)]), "quad")
    assert len(bsp.faces) == 1


def test_negative_surfedges_walk_the_edge_backwards():
    verts = [(0, 0, 0), (64, 0, 0), (64, 64, 0)]
    edges = [(0, 1), (2, 1), (2, 0)]
    data = _build([_face(0, 3, 0)], [_texinfo((1, 0, 0, 0), (0, 1, 0, 0), 0, 0)], ["a"], verts, edges, [0, -1, 2])
    face = parse_bsp(data, "tri").faces[0]
    assert face.positions == [(0, 0, 0), (64, 0, 0), (64, 64, 0)]


def test_displacement_becomes_a_grid_moved_by_its_verts():
    power = 2
    side = (1 << power) + 1
    disp = struct.pack("<3f", 0, 0, 0) + struct.pack("<iii", 0, 0, power) + b"\0" * 12 + struct.pack("<H", 0)
    disp += b"\0" * (176 - len(disp))
    verts = b"".join(struct.pack("<3fff", 0, 0, 1, float(i), 1.0) for i in range(side * side))   # rise i units
    bsp = parse_bsp(_quad_map(faces=[_face(0, 4, 0, dispinfo=0)], dispinfo=disp, dispverts=verts), "disp")
    face = bsp.faces[0]
    assert face.displacement and len(face.positions) == side * side
    assert len(face.indices) == (side - 1) * (side - 1) * 6
    assert face.positions[0] == (0, 0, 0)
    assert face.positions[-1][2] == side * side - 1                    # the last vertex rose the most
    assert face.positions[side - 1][:2] == (0, 64)                       # a row runs from the start corner's edge to the far edge


def test_static_props_and_entities_and_pak():
    names = struct.pack("<i", 2) + b"models/props/a.mdl".ljust(128, b"\0") + b"models/props/b.mdl".ljust(128, b"\0")
    leaves = struct.pack("<i", 0)
    record = struct.pack("<6f", 10, 20, 30, 0, 90, 0) + struct.pack("<HHHBB", 1, 0, 0, 6, 0) + struct.pack("<i", 2) + b"\0" * 24   # a v5-sized record
    props_chunk = names + leaves + struct.pack("<i", 1) + record
    game = struct.pack("<i", 1) + struct.pack("<iHHii", 0x73707270, 0, 5, 0, len(props_chunk))
    data = _quad_map(props=game + props_chunk,
                     entities='{\n"classname" "worldspawn"\n"skyname" "sky_day01"\n}\n{\n"classname" "info_player"\n"origin" "1 2 3"\n}\n',
                     pak={"materials/maps/quad/metal/x.vmt": b'"VertexLitGeneric" {}'})
    # the game lump's file offsets are absolute: patch the one we wrote
    lumps_at = 8 + 35 * 16
    offset, length, _v, _f = struct.unpack_from("<iiii", data, lumps_at)
    data = bytearray(data)
    struct.pack_into("<iHHii", data, offset + 4, 0x73707270, 0, 5, offset + 4 + 16, len(props_chunk))
    bsp = parse_bsp(bytes(data), "quad")
    assert len(bsp.static_props) == 1
    prop = bsp.static_props[0]
    assert prop.model == "models/props/b.mdl" and prop.origin == (10, 20, 30) and prop.angles == (0, 90, 0) and prop.skin == 2
    assert bsp.entities[0]["classname"] == "worldspawn" and bsp.entities[1]["origin"] == "1 2 3"
    assert bsp.sky_name == "sky_day01"
    assert bsp.pak_files() == {"materials/maps/quad/metal/x.vmt": b'"VertexLitGeneric" {}'}


def test_brush_entities_are_shifted_to_their_origin():
    verts = [(0, 0, 0), (64, 0, 0), (64, 64, 0), (0, 64, 0)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    models = struct.pack("<3f3f3fiii", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1) + struct.pack("<3f3f3fiii", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1)
    data = _build([_face(0, 4, 0), _face(0, 4, 0)], [_texinfo((1, 0, 0, 0), (0, 1, 0, 0), 0, 0)], ["a"], verts, edges, [0, 1, 2, 3],
                  models=models, entities='{\n"classname" "func_door"\n"model" "*1"\n"origin" "100 0 50"\n}\n')
    bsp = parse_bsp(data, "door")
    assert len(bsp.faces) == 2
    assert bsp.faces[0].positions[0] == (0, 0, 0)
    assert bsp.faces[1].positions[0] == (100, 0, 50)


def test_lightmap_decodes_to_gamma_bytes_with_luxel_coordinates():
    verts = [(0, 0, 0), (64, 0, 0), (64, 64, 0), (0, 64, 0)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    # a 2x2 lightmap (size 1x1 luxels): red at full, half green, an exponent of +1 on blue, black
    lighting = bytes([255, 0, 0, 0, 0, 128, 0, 0, 0, 0, 64, 1, 0, 0, 0, 0])
    info = _texinfo((1, 0, 0, 0), (0, 1, 0, 0), 0, 0, lm_s=(1 / 64, 0, 0, 0), lm_t=(0, 1 / 64, 0, 0))
    data = _build([_face(0, 4, 0, lightofs=0, lm_size=(1, 1))], [info], ["a"], verts, edges, [0, 1, 2, 3], lighting=lighting)
    face = parse_bsp(data, "lit").faces[0]
    w, h, rgb = face.lightmap
    assert (w, h) == (2, 2)
    assert rgb[0:3] == bytes([255, 0, 0])
    assert rgb[3:6] == bytes([0, 186, 0])                    # 128/255 in gamma 2.2 is 186
    assert rgb[6:9] == bytes([0, 0, 186])                    # 64 * 2^1 = 128
    assert rgb[9:12] == bytes([0, 0, 0])
    assert face.lightmap_uvs == [(0, 0), (1, 0), (1, 1), (0, 1)]


def test_no_lighting_lump_means_no_lightmap():
    face = parse_bsp(_quad_map(), "quad").faces[0]
    assert face.lightmap is None and face.lightmap_uvs == []


def _worldlight(kind, origin, intensity, normal=(0, 0, -1), atten=(1, 0, 0), stopdot=0.0, stopdot2=0.0):
    return (struct.pack("<3f3f3f", *origin, *intensity, *normal) + struct.pack("<iii", 0, kind, 0)
            + struct.pack("<7f", stopdot, stopdot2, 0.0, 0.0, *atten) + struct.pack("<iii", 0, 0, 0))


def test_world_lights_sun_and_nearest_point_lights():
    lights = (_worldlight(EMIT_SKYLIGHT, (0, 0, 0), (1.0, 0.8, 0.6), normal=(-0.6, 0, -0.8))
              + _worldlight(5, (0, 0, 0), (0.2, 0.3, 0.4))                             # sky ambient
              + _worldlight(EMIT_POINT, (10, 0, 0), (500, 500, 500), atten=(200, 0, 1))
              + _worldlight(EMIT_POINT, (1000, 0, 0), (500, 500, 500), atten=(200, 0, 1))
              + _worldlight(EMIT_SPOTLIGHT, (0, 50, 0), (500, 500, 500), normal=(0, -1, 0), atten=(1, 0, 0), stopdot=0.9, stopdot2=0.8))
    bsp = parse_bsp(_quad_map(extra={15: lights}), "lit")
    assert len(bsp.world_lights) == 5
    assert bsp.sky_light is not None and all(abs(a - b) < 1e-6 for a, b in zip(bsp.sky_light.intensity, (1.0, 0.8, 0.6)))
    assert all(abs(a - b) < 1e-6 for a, b in zip(bsp.sky_ambient, (0.2, 0.3, 0.4)))
    near = bsp.lights_at((0, 0, 0))
    assert near[0].kind == EMIT_SKYLIGHT
    kinds = [(l.kind, l.origin) for l in near[1:]]
    assert (EMIT_POINT, (10, 0, 0)) in kinds                            # the near one is there
    assert all(o != (1000, 0, 0) for _k, o in kinds)                   # the far one is too weak
    assert (EMIT_SPOTLIGHT, (0, 50, 0)) in kinds                       # in its cone (it points at the origin)
    assert not [l for l in bsp.lights_at((0, 100, 0)) if l.kind == EMIT_SPOTLIGHT]   # behind the spot


def test_ambient_cube_by_leaf():
    # a tree of one node splitting on x = 32: front (x >= 32) leaf 0, back leaf 1
    plane_split = struct.pack("<3ffi", 1, 0, 0, 32, 0)
    nodes = struct.pack("<iii6hHHh2x", 1, -1, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    leaf = lambda: struct.pack("<ihh3h3hHHHHh2x", 0, 0, 0, 0, 0, 0, 64, 64, 64, 0, 0, 0, 0, 0)
    leaves = leaf() + leaf()
    index = struct.pack("<HH", 1, 0) + struct.pack("<HH", 1, 1)
    def sample(r):
        return bytes([r, 0, 0, 0] * 6) + bytes([128, 128, 128, 0])   # six faces the same, at the box centre
    samples = sample(128) + sample(64)                                  # leaf 0 bright, leaf 1 dim
    data = _quad_map(extra={5: nodes, 10: leaves, 52: index, 56: samples})
    data = bytearray(data)
    struct.pack_into("<iiii", data, 8 + 10 * 16, *struct.unpack_from("<iiii", data, 8 + 10 * 16)[:2], 1, 0)   # leaf lump v1
    # the plane lump of _quad_map holds one plane (+z); add ours as plane 1
    bsp = parse_bsp(bytes(data), "amb")
    assert bsp.nodes and len(bsp.leaf_ambient) == 2
    assert bsp.ambient_at((100, 0, 0)) is not None
    cube_hi = bsp.ambient_at((100, 0, 0))
    cube_lo = bsp.ambient_at((-100, 0, 0))
    assert cube_hi is not None and cube_lo is not None


def test_hdr_only_maps_fall_back_to_the_hdr_lighting_lumps():
    # SFM's own sets: LDR worldlights empty, LDR ambient present but black, the HDR twins filled
    lights = _worldlight(EMIT_SKYLIGHT, (0, 0, 0), (1.0, 0.8, 0.6), normal=(-0.6, 0, -0.8))
    plane_split = struct.pack("<3ffi", 1, 0, 0, 32, 0)
    nodes = struct.pack("<iii6hHHh2x", 1, -1, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    leaf = lambda: struct.pack("<ihh3h3hHHHHh2x", 0, 0, 0, 0, 0, 0, 64, 64, 64, 0, 0, 0, 0, 0)
    leaves = leaf() + leaf()
    index = struct.pack("<HH", 1, 0) + struct.pack("<HH", 1, 1)
    def sample(r):
        return bytes([r, 0, 0, 0] * 6) + bytes([128, 128, 128, 0])
    black = sample(0) + sample(0)
    lit = sample(128) + sample(64)
    data = bytearray(_quad_map(extra={5: nodes, 10: leaves, 52: index, 56: black, 51: index, 55: lit, 54: lights}))
    struct.pack_into("<iiii", data, 8 + 10 * 16, *struct.unpack_from("<iiii", data, 8 + 10 * 16)[:2], 1, 0)
    bsp = parse_bsp(bytes(data), "hdr")
    assert len(bsp.world_lights) == 1 and bsp.sky_light is not None
    cube = bsp.ambient_at((100, 0, 0))
    assert cube is not None and cube[0][0] > 0.0                       # the HDR samples, not the black LDR ones
    # with real LDR samples those win, as before
    data = bytearray(_quad_map(extra={5: nodes, 10: leaves, 52: index, 56: lit, 51: index, 55: black}))
    struct.pack_into("<iiii", data, 8 + 10 * 16, *struct.unpack_from("<iiii", data, 8 + 10 * 16)[:2], 1, 0)
    assert parse_bsp(bytes(data), "ldr").ambient_at((100, 0, 0))[0][0] > 0.0
