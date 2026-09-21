"""
Source engine maps: `.bsp` versions 19 to 21 (Team Fortress 2 and SFM's own).

What the editor needs from a map is what SFM shows of it: the world's
drawable faces with their materials and lightmaps, the displacement terrain
built on top of some of those faces, the brush entities, the static props,
and the light vrad baked in - so that models placed on the map are lit the
way the map is.  This reader gives exactly that:

    bsp = parse_bsp(data, "maps/cp_badlands.bsp")
    bsp.faces          # WorldFace: material, polygon in world units, uvs, normal, lightmap
    bsp.static_props   # StaticProp: model path, origin, QAngle, skin
    bsp.entities       # the entity lump as a list of key/value dicts
    bsp.world_lights   # WorldLight: sun, point and spot lights as vrad saw them
    bsp.ambient_at(p)  # the ambient cube around a point, from the leaf it is in
    bsp.lights_at(p)   # the strongest world lights at a point

Lumps read: entities 0, planes 1, texdata 2, vertexes 3, nodes 5, texinfo 6,
faces 7, lighting 8, leafs 10, edges 12, surfedges 13, models 14, worldlights
15, dispinfo 26, disp verts 33, game lump 35 (static props), pakfile 40 (the
zip of the map's own materials), texdata string data/table 43/44, leaf ambient
index/lighting 52/56 - and the HDR twins 53, 54 and 51/55 of the lighting
lumps when a map was compiled for HDR only, as SFM's own sets are.  Each
face's luxels are decoded from RGBExp32 to gamma-space bytes, with per-vertex
luxel coordinates from the texinfo's lightmap vectors (a displacement's cover
its grid).  Brush entities (model "*N") are placed at their entity's origin.

Faces that are never drawn (sky, nodraw, hint, skip, trigger, the tool
textures) are dropped.  A face with a displacement is replaced by the
displacement's grid, built the way the engine does: the four face corners,
the start corner the dispinfo names, then each vertex moved along its
recorded vector by its recorded distance.
"""
from __future__ import annotations

import math
import struct
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

__all__ = ["BspFile", "WorldFace", "StaticProp", "WorldLight", "parse_bsp", "map_path",
           "EMIT_POINT", "EMIT_SPOTLIGHT", "EMIT_SKYLIGHT", "EMIT_SKYAMBIENT"]

Vec3 = Tuple[float, float, float]

IDENT = b"VBSP"
LUMP_ENTITIES, LUMP_PLANES, LUMP_TEXDATA, LUMP_VERTEXES = 0, 1, 2, 3
LUMP_TEXINFO, LUMP_FACES, LUMP_LIGHTING = 6, 7, 8
LUMP_LIGHTING_HDR = 53
LUMP_EDGES, LUMP_SURFEDGES, LUMP_MODELS = 12, 13, 14
LUMP_DISPINFO, LUMP_DISP_VERTS, LUMP_GAME_LUMP = 26, 33, 35
LUMP_NODES, LUMP_LEAFS, LUMP_WORLDLIGHTS = 5, 10, 15
LUMP_PAKFILE = 40
LUMP_LEAF_AMBIENT_INDEX, LUMP_LEAF_AMBIENT_LIGHTING = 52, 56
# a map compiled for HDR only (SFM's own sets) fills these twins and leaves the LDR lumps empty
LUMP_WORLDLIGHTS_HDR, LUMP_LEAF_AMBIENT_INDEX_HDR, LUMP_LEAF_AMBIENT_LIGHTING_HDR = 54, 51, 55
LUMP_TEXDATA_STRING_DATA, LUMP_TEXDATA_STRING_TABLE = 43, 44

# texinfo flags that mean "not a drawn surface"
SURF_SKY2D, SURF_SKY, SURF_NODRAW, SURF_HINT, SURF_SKIP, SURF_TRIGGER = 0x2, 0x4, 0x80, 0x100, 0x200, 0x40
SURF_NOT_DRAWN = SURF_SKY2D | SURF_SKY | SURF_NODRAW | SURF_HINT | SURF_SKIP | SURF_TRIGGER
TOOL_MATERIALS = ("tools/", "dev/dev_blendmeasure")

GAME_LUMP_STATIC_PROPS = 0x73707270            # 'sprp' as the engine packs it


class FormatError(ValueError):
    """The data is not a BSP this reader understands."""
    pass


@dataclass
class WorldFace:
    """One drawable polygon of the world, already in world units."""
    material: str                              # content path without "materials/" and ".vmt", lower case
    positions: List[Vec3]
    uvs: List[Tuple[float, float]]
    normal: Vec3
    #: triangle indices into `positions`; a plain polygon is a fan, a displacement a grid
    indices: List[int]
    lightmap_offset: int = -1
    displacement: bool = False
    #: the face's compiled light: width, height in luxels and RGB bytes (gamma space),
    #: with `lightmap_uvs` in luxels for every position; None when the map has no light
    lightmap: Optional[Tuple[int, int, bytes]] = None
    lightmap_uvs: List[Tuple[float, float]] = field(default_factory=list)


@dataclass
class StaticProp:
    """One prop_static: model, placement, skin."""
    model: str                                 # "models/props_xxx/yyy.mdl"
    origin: Vec3
    angles: Vec3                               # QAngle: pitch, yaw, roll in degrees
    skin: int = 0


EMIT_SURFACE, EMIT_POINT, EMIT_SPOTLIGHT, EMIT_SKYLIGHT, EMIT_QUAKELIGHT, EMIT_SKYAMBIENT = range(6)


@dataclass
class WorldLight:
    """A light the map was compiled with (lump 15): what lights a model in the game."""
    kind: int                                  # EMIT_*
    origin: Vec3
    intensity: Vec3                            # linear colour x brightness
    normal: Vec3                               # the way a spot or the sun shines
    stopdot: float = 0.0                       # spot: cos of the inner and outer cone
    stopdot2: float = 0.0
    exponent: float = 0.0
    attenuation: Tuple[float, float, float] = (1.0, 0.0, 0.0)   # constant, linear, quadratic over distance

    def strength_at(self, point: Vec3) -> float:
        """How much this light matters at a point, for choosing the nearest few."""
        if self.kind == EMIT_SKYLIGHT:
            return sum(self.intensity)
        if self.kind not in (EMIT_POINT, EMIT_SPOTLIGHT):
            return 0.0
        d2 = sum((self.origin[a] - point[a]) ** 2 for a in range(3))
        d = math.sqrt(d2)
        c, l, q = self.attenuation
        denominator = c + l * d + q * d2
        if denominator <= 1e-6:
            return sum(self.intensity)
        if self.kind == EMIT_SPOTLIGHT and d > 1e-3:
            to_point = tuple((point[a] - self.origin[a]) / d for a in range(3))
            cos = sum(to_point[a] * self.normal[a] for a in range(3))
            if cos < self.stopdot2:
                return 0.0
        return sum(self.intensity) / denominator


@dataclass
class BspFile:
    """A parsed map: geometry, props, entities, lighting."""
    name: str
    version: int
    faces: List[WorldFace] = field(default_factory=list)
    static_props: List[StaticProp] = field(default_factory=list)
    entities: List[Dict[str, str]] = field(default_factory=list)
    materials: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    #: the map's own zip of files (cubemap-patched materials, embedded textures), raw
    pakfile: bytes = b""
    #: the BSP tree for point lookups: (plane normal, dist, child front, child back); a child
    #: below zero is -(leaf + 1)
    nodes: List[Tuple[Vec3, float, int, int]] = field(default_factory=list)
    #: per leaf, its ambient samples: [(x, y, z, cube)] with cube = six RGB floats (linear), +x -x +y -y +z -z
    leaf_ambient: List[List[Tuple[Vec3, Tuple[Vec3, ...]]]] = field(default_factory=list)
    sky_name: str = ""
    world_lights: List[WorldLight] = field(default_factory=list)

    @property
    def sky_light(self) -> Optional[WorldLight]:
        """The sun (light_environment), or None."""
        return next((l for l in self.world_lights if l.kind == EMIT_SKYLIGHT), None)

    @property
    def sky_ambient(self) -> Optional[Vec3]:
        """The sky's ambient colour, or None."""
        light = next((l for l in self.world_lights if l.kind == EMIT_SKYAMBIENT), None)
        return light.intensity if light is not None else None

    def lights_at(self, point: Vec3, count: int = 4) -> List[WorldLight]:
        """The sun plus the strongest few point and spot lights at a point.  Answered per
        64-unit cell and remembered: a scene asks for every model every frame."""
        cell = (int(point[0] // 64), int(point[1] // 64), int(point[2] // 64), count)
        cache = self.__dict__.setdefault("_lights_cache", {})
        found = cache.get(cell)
        if found is not None:
            return found
        if len(cache) > 20000:
            cache.clear()
        found = self._lights_at(point, count)
        cache[cell] = found
        return found

    def _lights_at(self, point: Vec3, count: int) -> List[WorldLight]:
        out = [l for l in self.world_lights if l.kind == EMIT_SKYLIGHT][:1]
        local = [l for l in self.world_lights if l.kind in (EMIT_POINT, EMIT_SPOTLIGHT)]
        local.sort(key=lambda l: -l.strength_at(point))
        out.extend(l for l in local[:count] if l.strength_at(point) > 0.002)
        return out

    def ambient_at(self, point: Vec3) -> Optional[Tuple[Vec3, ...]]:
        """The ambient cube nearest a point: what the engine lights a model with from the map."""
        if not self.nodes or not self.leaf_ambient:
            return None
        i = 0
        depth = 0
        while i >= 0 and depth < 512:
            normal, dist, front, back = self.nodes[i]
            i = front if normal[0] * point[0] + normal[1] * point[1] + normal[2] * point[2] - dist >= 0 else back
            depth += 1
        leaf = -(i + 1)
        if not 0 <= leaf < len(self.leaf_ambient):
            return None
        samples = self.leaf_ambient[leaf]
        if not samples:
            # an empty leaf (solid or unlit): take the nearest lit sample anywhere near
            return None
        best = min(samples, key=lambda s: sum((s[0][a] - point[a]) ** 2 for a in range(3)))
        return best[1]

    def pak_files(self) -> Dict[str, bytes]:
        """Every file the map carries inside itself, by lower-case content path."""
        if not self.pakfile:
            return {}
        import io
        import zipfile
        try:
            with zipfile.ZipFile(io.BytesIO(self.pakfile)) as z:
                return {i.filename.replace("\\", "/").lower(): z.read(i) for i in z.infolist() if not i.is_dir()}
        except (zipfile.BadZipFile, OSError):
            self.warnings.append("pakfile: not a zip")
            return {}

    @property
    def bounds(self) -> Tuple[Vec3, Vec3]:
        """Axis-aligned box around every drawn face."""
        lo = [math.inf] * 3
        hi = [-math.inf] * 3
        for face in self.faces:
            for p in face.positions:
                for a in range(3):
                    lo[a] = min(lo[a], p[a])
                    hi[a] = max(hi[a], p[a])
        if lo[0] is math.inf:
            return (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)
        return tuple(lo), tuple(hi)


def map_path(name: str) -> str:
    """The content path of a map a session names: `cp_badlands` or `cp_badlands.bsp`."""
    name = name.replace("\\", "/").strip()
    if not name:
        return ""
    if not name.lower().endswith(".bsp"):
        name += ".bsp"
    if not name.lower().startswith("maps/"):
        name = "maps/" + name
    return name


# ---------------------------------------------------------------------------
#  Reading
# ---------------------------------------------------------------------------
_HEADER = struct.Struct("<4si")
_LUMP = struct.Struct("<iiii")
_PLANE = struct.Struct("<3ffi")
_TEXDATA = struct.Struct("<3fiiiii")
_TEXINFO = struct.Struct("<16fii")
_FACE = struct.Struct("<HBBihhhh4BifiiiiiHHI")
_EDGE = struct.Struct("<HH")
_MODEL = struct.Struct("<3f3f3fiii")
_DISPVERT = struct.Struct("<3fff")
_DISP_STRIDE = 176


def parse_bsp(data: bytes, name: str = "") -> BspFile:
    """Parse a .bsp; `name` labels errors and warnings."""
    if len(data) < 8 + 64 * 16 or data[:4] != IDENT:
        raise FormatError(f"{name}: not a Source BSP")
    _ident, version = _HEADER.unpack_from(data, 0)
    if not 17 <= version <= 21:
        raise FormatError(f"{name}: BSP version {version} is not supported")
    bsp = BspFile(name=name, version=version)
    lumps = [_LUMP.unpack_from(data, 8 + i * 16) for i in range(64)]

    def lump(index: int) -> bytes:
        """Raw bytes of a lump, empty when absent or malformed."""
        offset, length, _version, _fourcc = lumps[index]
        if length <= 0 or offset < 0 or offset + length > len(data):
            return b""
        return data[offset:offset + length]

    planes = [_PLANE.unpack_from(raw, 0) for raw in _chunks(lump(LUMP_PLANES), _PLANE.size)]
    vertexes = [struct.unpack_from("<3f", raw, 0) for raw in _chunks(lump(LUMP_VERTEXES), 12)]
    edges = [_EDGE.unpack_from(raw, 0) for raw in _chunks(lump(LUMP_EDGES), 4)]
    surfedges_raw = lump(LUMP_SURFEDGES)
    surfedges = list(struct.unpack_from(f"<{len(surfedges_raw) // 4}i", surfedges_raw, 0)) if surfedges_raw else []
    texinfo = [_TEXINFO.unpack_from(raw, 0) for raw in _chunks(lump(LUMP_TEXINFO), _TEXINFO.size)]
    texdata = [_TEXDATA.unpack_from(raw, 0) for raw in _chunks(lump(LUMP_TEXDATA), _TEXDATA.size)]
    names = _texdata_names(lump(LUMP_TEXDATA_STRING_DATA), lump(LUMP_TEXDATA_STRING_TABLE))
    bsp.materials = [names[t[3]] if 0 <= t[3] < len(names) else "" for t in texdata]
    faces = [_FACE.unpack_from(raw, 0) for raw in _chunks(lump(LUMP_FACES), _FACE.size)]
    models = [_MODEL.unpack_from(raw, 0) for raw in _chunks(lump(LUMP_MODELS), _MODEL.size)]
    disp_verts = [_DISPVERT.unpack_from(raw, 0) for raw in _chunks(lump(LUMP_DISP_VERTS), _DISPVERT.size)]
    disp_raw = lump(LUMP_DISPINFO)
    dispinfo = [_disp(disp_raw, i * _DISP_STRIDE) for i in range(len(disp_raw) // _DISP_STRIDE)]
    lighting = lump(LUMP_LIGHTING) or lump(LUMP_LIGHTING_HDR)

    bsp.entities = _entities(lump(LUMP_ENTITIES))
    # the world is model 0; the others are brush entities ("*1" - doors, func_brush), whose
    # geometry is stored about their own origin, so each is drawn shifted to where its entity sits
    origins: Dict[int, Vec3] = {}
    for entity in bsp.entities:
        model = entity.get("model", "")
        if model.startswith("*"):
            try:
                parts = entity.get("origin", "0 0 0").split()
                origins[int(model[1:])] = (float(parts[0]), float(parts[1]), float(parts[2]))
            except (ValueError, IndexError):
                continue
    plan: List[Tuple[int, Vec3]] = []
    if models:
        for m, model in enumerate(models):
            first, count = model[10], model[11]
            shift = origins.get(m, (0.0, 0.0, 0.0)) if m else (0.0, 0.0, 0.0)
            plan.extend((f, shift) for f in range(first, min(first + count, len(faces))))
    else:
        plan = [(f, (0.0, 0.0, 0.0)) for f in range(len(faces))]
    for f, shift in plan:
        face = faces[f]
        planenum, side, _on_node, first_edge, num_edges, ti, di = face[0], face[1], face[2], face[3], face[4], face[5], face[6]
        light_offset = face[12]
        lm_mins, lm_size = (face[14], face[15]), (face[16], face[17])
        if not 0 <= ti < len(texinfo) or num_edges < 3:
            continue
        info = texinfo[ti]
        flags, td = info[16], info[17]
        if flags & SURF_NOT_DRAWN:
            continue
        material = bsp.materials[td].lower() if 0 <= td < len(bsp.materials) else ""
        if not material or material.startswith(TOOL_MATERIALS):
            continue
        width = texdata[td][4] if 0 <= td < len(texdata) else 0
        height = texdata[td][5] if 0 <= td < len(texdata) else 0
        polygon: List[Vec3] = []
        for e in range(first_edge, first_edge + num_edges):
            if not 0 <= e < len(surfedges):
                break
            se = surfedges[e]
            edge = edges[abs(se)] if abs(se) < len(edges) else None
            if edge is None:
                break
            v = edge[0] if se >= 0 else edge[1]
            if v < len(vertexes):
                p = vertexes[v]
                polygon.append((p[0] + shift[0], p[1] + shift[1], p[2] + shift[2]) if shift != (0.0, 0.0, 0.0) else p)
        if len(polygon) < 3:
            continue
        normal = planes[planenum][:3] if 0 <= planenum < len(planes) else (0.0, 0.0, 1.0)
        if side:
            normal = (-normal[0], -normal[1], -normal[2])
        if 0 <= di < len(dispinfo):
            world = _displacement(dispinfo[di], polygon, disp_verts, info, width, height)
            if world is not None:
                world.material = material
                world.normal = normal
                world.lightmap_offset = light_offset
                world.lightmap = _lightmap(lighting, light_offset, lm_size)
                if world.lightmap is not None:
                    side = int(round(math.sqrt(len(world.positions))))
                    world.lightmap_uvs = [((c / (side - 1)) * lm_size[0], (r / (side - 1)) * lm_size[1])
                                          for r in range(side) for c in range(side)]
                bsp.faces.append(world)
            continue
        uvs = [_uv(info, p, width, height) for p in polygon]
        indices = [i for k in range(1, len(polygon) - 1) for i in (0, k, k + 1)]
        world = WorldFace(material, polygon, uvs, normal, indices, light_offset)
        world.lightmap = _lightmap(lighting, light_offset, lm_size)
        if world.lightmap is not None:
            world.lightmap_uvs = [(info[8] * p[0] + info[9] * p[1] + info[10] * p[2] + info[11] - lm_mins[0],
                                   info[12] * p[0] + info[13] * p[1] + info[14] * p[2] + info[15] - lm_mins[1])
                                  for p in polygon]
        bsp.faces.append(world)

    bsp.static_props = _static_props(lump(LUMP_GAME_LUMP), data, bsp.warnings)
    bsp.pakfile = lump(LUMP_PAKFILE)
    for entity in bsp.entities:
        if entity.get("classname") == "worldspawn":
            bsp.sky_name = entity.get("skyname", "")
            break
    ambient_index = lump(LUMP_LEAF_AMBIENT_INDEX)
    ambient_lighting = lump(LUMP_LEAF_AMBIENT_LIGHTING)
    if not ambient_lighting or not _any_colour(ambient_lighting):
        # compiled for HDR only: the LDR lumps are missing or there but black
        ambient_index = lump(LUMP_LEAF_AMBIENT_INDEX_HDR)
        ambient_lighting = lump(LUMP_LEAF_AMBIENT_LIGHTING_HDR)
    _ambient(bsp, lump(LUMP_NODES), lump(LUMP_LEAFS), lumps[LUMP_LEAFS][2], ambient_index, ambient_lighting, planes)
    lights_lump = LUMP_WORLDLIGHTS if lump(LUMP_WORLDLIGHTS) else LUMP_WORLDLIGHTS_HDR
    bsp.world_lights = _world_lights(lump(lights_lump), lumps[lights_lump][2])
    return bsp


def _world_lights(raw: bytes, version: int) -> List[WorldLight]:
    """dworldlight_t: 88 bytes, or 100 with the shadow cast offset of version 1."""
    if not raw:
        return []
    stride = 100 if version >= 1 and len(raw) % 100 == 0 else 88
    out = []
    for i in range(len(raw) // stride):
        at = i * stride
        origin = struct.unpack_from("<3f", raw, at)
        intensity = struct.unpack_from("<3f", raw, at + 12)
        normal = struct.unpack_from("<3f", raw, at + 24)
        base = at + (48 if stride == 100 else 36)
        _cluster, kind, _style = struct.unpack_from("<iii", raw, base)
        stopdot, stopdot2, exponent, _radius, c, l, q = struct.unpack_from("<7f", raw, base + 12)
        out.append(WorldLight(kind, origin, intensity, normal, stopdot, stopdot2, exponent, (c, l, q)))
    return out


_NODE = struct.Struct("<iii6h HHh2x")            # planenum, children[2], mins[3], maxs[3], firstface, numfaces, area, pad
_AMBIENT_INDEX = struct.Struct("<HH")           # sample count, first sample
_AMBIENT_SAMPLE = 28                            # six ColorRGBExp32 + x y z (bytes of the leaf's box) + pad


def _ambient(bsp: "BspFile", nodes_raw: bytes, leafs_raw: bytes, leaf_version: int, index_raw: bytes,
             samples_raw: bytes, planes) -> None:
    """The BSP tree and each leaf's ambient light samples (maps of version 20 and up)."""
    if not nodes_raw or not leafs_raw:
        return
    for raw in _chunks(nodes_raw, _NODE.size):
        planenum, c0, c1 = struct.unpack_from("<iii", raw, 0)
        if 0 <= planenum < len(planes):
            n = planes[planenum]
            bsp.nodes.append(((n[0], n[1], n[2]), n[3], c0, c1))
        else:
            bsp.nodes.append(((0.0, 0.0, 1.0), 0.0, c0, c1))
    leaf_size = 32 if leaf_version >= 1 else 56
    leaf_count = len(leafs_raw) // leaf_size
    boxes = []
    for i in range(leaf_count):
        mins = struct.unpack_from("<3h", leafs_raw, i * leaf_size + 8)
        maxs = struct.unpack_from("<3h", leafs_raw, i * leaf_size + 14)
        boxes.append((mins, maxs))
    bsp.leaf_ambient = [[] for _ in range(leaf_count)]
    if not index_raw or not samples_raw:
        return
    for leaf, raw in enumerate(_chunks(index_raw, _AMBIENT_INDEX.size)):
        if leaf >= leaf_count:
            break
        count, first = _AMBIENT_INDEX.unpack_from(raw, 0)
        mins, maxs = boxes[leaf]
        for s in range(first, first + count):
            at = s * _AMBIENT_SAMPLE
            if at + _AMBIENT_SAMPLE > len(samples_raw):
                break
            cube = tuple(_rgbexp(samples_raw, at + k * 4) for k in range(6))
            x, y, z = samples_raw[at + 24], samples_raw[at + 25], samples_raw[at + 26]
            pos = tuple(mins[a] + (maxs[a] - mins[a]) * (v / 255.0) for a, v in enumerate((x, y, z)))
            bsp.leaf_ambient[leaf].append((pos, cube))


def _any_colour(samples_raw: bytes) -> bool:
    """True when any ambient sample carries light (the first 24 bytes of each are its
    six colours; the last four its position, which is never all zero)."""
    for at in range(0, len(samples_raw) - _AMBIENT_SAMPLE + 1, _AMBIENT_SAMPLE):
        if any(samples_raw[at:at + 24]):
            return True
    return False


def _rgbexp(raw: bytes, at: int) -> Vec3:
    """An ambient sample's ColorRGBExp32: linear light where 1.0 is full (unlike the
    lightmaps, whose r * 2^e sits on a 0..255 scale)."""
    r, g, b, e = raw[at], raw[at + 1], raw[at + 2], raw[at + 3]
    scale = 2.0 ** (e - 256 if e > 127 else e)
    return (r * scale, g * scale, b * scale)


_GAMMA = bytes(int(round(255.0 * (i / 255.0) ** (1.0 / 2.2))) for i in range(256))


def _lightmap(lighting: bytes, offset: int, size: Tuple[int, int]) -> Optional[Tuple[int, int, bytes]]:
    """A face's first lightstyle as gamma-space RGB bytes, (width, height, data)."""
    if offset < 0 or not lighting:
        return None
    w, h = size[0] + 1, size[1] + 1
    count = w * h
    if count <= 0 or count > 1 << 20 or offset + count * 4 > len(lighting):
        return None
    out = bytearray(count * 3)
    for i in range(count):
        r, g, b, e = lighting[offset + i * 4:offset + i * 4 + 4]
        scale = 2.0 ** (e - 256 if e > 127 else e)
        # RGBExp32 is linear light; the engine writes it to its lightmap in gamma space
        out[i * 3] = _GAMMA[min(255, int(r * scale))]
        out[i * 3 + 1] = _GAMMA[min(255, int(g * scale))]
        out[i * 3 + 2] = _GAMMA[min(255, int(b * scale))]
    return w, h, bytes(out)


def _chunks(raw: bytes, size: int):
    for i in range(0, len(raw) - size + 1, size):
        yield raw[i:i + size]


def _texdata_names(chars: bytes, table: bytes) -> List[str]:
    if not table:
        return []
    offsets = struct.unpack_from(f"<{len(table) // 4}i", table, 0)
    out = []
    for offset in offsets:
        if 0 <= offset < len(chars):
            end = chars.find(b"\0", offset)
            out.append(chars[offset:end if end >= 0 else len(chars)].decode("latin-1"))
        else:
            out.append("")
    return out


def _uv(info, p: Vec3, width: int, height: int) -> Tuple[float, float]:
    s = info[0] * p[0] + info[1] * p[1] + info[2] * p[2] + info[3]
    t = info[4] * p[0] + info[5] * p[1] + info[6] * p[2] + info[7]
    return (s / width if width else s, t / height if height else t)


def _disp(raw: bytes, at: int) -> Tuple[Vec3, int, int, int]:
    start = struct.unpack_from("<3f", raw, at)
    vert_start, _tri_start, power = struct.unpack_from("<iii", raw, at + 12)
    (map_face,) = struct.unpack_from("<H", raw, at + 36)
    return start, vert_start, power, map_face


def _displacement(disp, polygon: List[Vec3], verts, info, width: int, height: int) -> Optional[WorldFace]:
    """The grid a displacement makes of its (four-cornered) face."""
    start, vert_start, power, _map_face = disp
    if len(polygon) != 4 or power < 1 or power > 4:
        return None
    side = (1 << power) + 1
    count = side * side
    if vert_start < 0 or vert_start + count > len(verts):
        return None
    # rotate the corners so the start position is the first
    best = min(range(4), key=lambda i: sum((polygon[i][a] - start[a]) ** 2 for a in range(3)))
    corners = polygon[best:] + polygon[:best]
    c0, c1, c2, c3 = corners
    positions: List[Vec3] = []
    uvs = []
    for row in range(side):
        v = row / (side - 1)
        left = tuple(c0[a] + (c1[a] - c0[a]) * v for a in range(3))
        right = tuple(c3[a] + (c2[a] - c3[a]) * v for a in range(3))
        for col in range(side):
            u = col / (side - 1)
            base = tuple(left[a] + (right[a] - left[a]) * u for a in range(3))
            dv = verts[vert_start + row * side + col]
            p = (base[0] + dv[0] * dv[3], base[1] + dv[1] * dv[3], base[2] + dv[2] * dv[3])
            positions.append(p)
            uvs.append(_uv(info, base, width, height))
    indices: List[int] = []
    for row in range(side - 1):
        for col in range(side - 1):
            i = row * side + col
            # alternate the diagonal as the engine does, so the terrain does not ridge
            if (row + col) & 1:
                indices += [i, i + 1, i + side, i + 1, i + side + 1, i + side]
            else:
                indices += [i, i + side + 1, i + side, i, i + 1, i + side + 1]
    return WorldFace("", positions, uvs, (0.0, 0.0, 1.0), indices, displacement=True)


def _static_props(raw: bytes, whole: bytes, warnings: List[str]) -> List[StaticProp]:
    """The 'sprp' game lump: a model dictionary, a leaf list, then the props."""
    if len(raw) < 4:
        return []
    (count,) = struct.unpack_from("<i", raw, 0)
    props: List[StaticProp] = []
    for i in range(count):
        at = 4 + i * 16
        if at + 16 > len(raw):
            break
        ident, _flags, version, offset, length = struct.unpack_from("<iHHii", raw, at)
        if ident != GAME_LUMP_STATIC_PROPS or length <= 0 or offset < 0 or offset + length > len(whole):
            continue
        chunk = whole[offset:offset + length]
        try:
            props.extend(_read_props(chunk, version))
        except struct.error:
            warnings.append("static props: lump truncated")
    return props


def _read_props(chunk: bytes, version: int) -> List[StaticProp]:
    (n_names,) = struct.unpack_from("<i", chunk, 0)
    at = 4
    names = []
    for _ in range(n_names):
        raw = chunk[at:at + 128]
        names.append(raw.split(b"\0", 1)[0].decode("latin-1").replace("\\", "/"))
        at += 128
    (n_leaves,) = struct.unpack_from("<i", chunk, at)
    at += 4 + n_leaves * 2
    (n_props,) = struct.unpack_from("<i", chunk, at)
    at += 4
    if n_props <= 0:
        return []
    stride = (len(chunk) - at) // n_props          # the record grew with every version; the fields
    out = []                                         # used here sit at the front of every one
    for i in range(n_props):
        base = at + i * stride
        if base + 36 > len(chunk):
            break
        ox, oy, oz, ax, ay, az = struct.unpack_from("<6f", chunk, base)
        prop_type, _first_leaf, _leaf_count, _solid, _flags = struct.unpack_from("<HHHBB", chunk, base + 24)
        (skin,) = struct.unpack_from("<i", chunk, base + 32)
        if 0 <= prop_type < len(names):
            out.append(StaticProp(names[prop_type], (ox, oy, oz), (ax, ay, az), skin))
    return out


def _entities(raw: bytes) -> List[Dict[str, str]]:
    text = raw.split(b"\0", 1)[0].decode("latin-1")
    out: List[Dict[str, str]] = []
    current: Optional[Dict[str, str]] = None
    for line in text.splitlines():
        line = line.strip()
        if line == "{":
            current = {}
        elif line == "}":
            if current is not None:
                out.append(current)
            current = None
        elif current is not None and line.startswith('"'):
            parts = line.split('"')
            if len(parts) >= 5:
                current[parts[1]] = parts[3]
    return out
