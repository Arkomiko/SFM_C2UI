"""
The .mdl file: skeleton, mesh table and material names.

A Source model is three files. This one is the index: it holds the bones, the
body parts that own the meshes, and the names of the materials - but no geometry
at all. Vertices live in .vvd and triangle indices in .vtx, both keyed by the
offsets recorded here.

Versions 44 to 49 share this layout; SFM ships a mix of 48 and 49.
"""
from __future__ import annotations

import struct
from dataclasses import dataclass, field
from typing import List, Tuple

from Core.API.model import Bone, FlexController, FlexRule, MeshFlex, ModelInfo

from .binary import Cursor, FormatError, Reader

__all__ = ["MdlFile", "parse_mdl", "MDL_MAGIC", "SUPPORTED_VERSIONS"]

MDL_MAGIC = b"IDST"
SUPPORTED_VERSIONS = range(44, 50)

# offsets inside studiohdr_t
_H_VERSION = 4
_H_CHECKSUM = 8
_H_NAME = 12
_H_NAME_LEN = 64
_H_LENGTH = 76
_H_EYE = 80
_H_HULL_MIN = 104
_H_HULL_MAX = 116
_H_FLAGS = 152
_H_NUM_BONES = 156
_H_BONE_INDEX = 160
_H_NUM_TEXTURES = 204
_H_TEXTURE_INDEX = 208
_H_NUM_CDTEXTURES = 212
_H_CDTEXTURE_INDEX = 216
#: the skin table: how many textures a family names, how many families, where they are
_H_NUM_SKINREF = 220
_H_NUM_SKINFAMILIES = 224
_H_SKIN_INDEX = 228
#: the skin table: how many textures a family names, how many families, where they are
_H_NUM_SKINREF = 220
_H_NUM_SKINFAMILIES = 224
_H_SKIN_INDEX = 228
_H_NUM_BODYPARTS = 232
_H_BODYPART_INDEX = 236
_H_NUM_FLEXDESC = 260
_H_FLEXDESC_INDEX = 264
_H_NUM_FLEXCONTROLLERS = 268
_H_FLEXCONTROLLER_INDEX = 272
_H_NUM_FLEXRULES = 276
_H_FLEXRULE_INDEX = 280

_BONE_STRIDE = 216
_BONE_POS = 32
_BONE_QUAT = 44
_BONE_POSE_TO_BONE = 96
_BONE_FLAGS = 160

_TEXTURE_STRIDE = 64

_BODYPART_STRIDE = 16
_BODYPART_NUM_MODELS = 4
_BODYPART_BASE = 8
_BODYPART_MODEL_INDEX = 12

_MODEL_STRIDE = 148
_MODEL_NAME_LEN = 64
_MODEL_NUM_MESHES = 72
_MODEL_MESH_INDEX = 76
_MODEL_NUM_VERTICES = 80
_MODEL_VERTEX_INDEX = 84

_MESH_STRIDE = 116
_MESH_MATERIAL = 0
_MESH_NUM_VERTICES = 8
_MESH_VERTEX_OFFSET = 12
_MESH_NUM_FLEXES = 16
_MESH_FLEX_INDEX = 20

_FLEXDESC_STRIDE = 4
_FLEXCONTROLLER_STRIDE = 20
_FLEXRULE_STRIDE = 12
_FLEXOP_STRIDE = 8
_FLEX_STRIDE = 60
_FLEX_DESC = 0
_FLEX_TARGETS = 4
_FLEX_NUM_VERTS = 20
_FLEX_VERT_INDEX = 24
_FLEX_PAIR = 28
_FLEX_VERTANIM_TYPE = 32
#: mstudiovertanim_t: index u16, speed u8, side u8, delta 3 x float16, ndelta 3 x float16
_VERTANIM = struct.Struct("<HBB3e3e")
_VERTANIM_WRINKLE_STRIDE = 18
_MESH_LOD_VERTICES = 52         # numLODVertexes[8]

_POSE_TO_BONE = struct.Struct("<12f")


@dataclass
class MdlMesh:
    """One mesh inside a model: a slice of that model's vertices."""

    material_index: int
    vertex_count: int
    vertex_offset: int          # relative to the owning model's vertices, at level 0
    #: how many of this mesh's vertices each level of detail keeps
    lod_vertex_counts: Tuple[int, ...] = ()
    flexes: List[MeshFlex] = field(default_factory=list)

    def vertices_at(self, lod: int) -> int:
        """Vertices this mesh has at a level.

        A mesh with no vertices at level 0 has none at any level - the
        compiler leaves a copy of a neighbour's table in such meshes, and
        trusting it would shift every mesh after them. The level-0 count is
        used when the table is absent or empty.
        """
        if self.vertex_count <= 0:
            return 0
        if 0 <= lod < len(self.lod_vertex_counts) and any(self.lod_vertex_counts):
            return max(0, self.lod_vertex_counts[lod])
        return self.vertex_count


@dataclass
class MdlModel:
    """One model inside a body part - the level .vtx also splits on."""

    name: str
    vertex_count: int
    vertex_index: int           # byte offset into the .vvd vertex array
    meshes: List[MdlMesh] = field(default_factory=list)

    @property
    def first_vertex(self) -> int:
        """Where this model's vertices start, counted in vertices not bytes."""
        return self.vertex_index // 48        # sizeof(mstudiovertex_t)


@dataclass
class MdlBodyPart:
    """A body group: alternatives of which exactly one is shown.

    A model's `body` value picks one alternative per group: this group's
    choice is ``(body // base) % len(models)``, with `base` the product of
    the group counts before it, as the compiler wrote it.
    """
    name: str
    models: List[MdlModel] = field(default_factory=list)
    base: int = 1

    def chosen(self, body: int) -> int:
        """Index of the sub-model this body group value selects."""
        if not self.models:
            return -1
        return (body // max(1, self.base)) % len(self.models)


@dataclass
class MdlFile:
    """Everything the .mdl itself knows."""

    info: ModelInfo
    bones: List[Bone] = field(default_factory=list)
    body_parts: List[MdlBodyPart] = field(default_factory=list)
    material_names: List[str] = field(default_factory=list)
    material_dirs: List[str] = field(default_factory=list)
    #: one row per skin: which texture each material slot takes when that skin is chosen
    skin_families: List[List[int]] = field(default_factory=list)
    flex_descs: List[str] = field(default_factory=list)
    flex_controllers: List[FlexController] = field(default_factory=list)
    flex_rules: List[FlexRule] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


def parse_mdl(data: bytes, name: str = "model.mdl") -> MdlFile:
    """Read a .mdl.  Raises :class:`FormatError` when it is not one."""
    reader = Reader(data, name)
    if reader.size < 240:
        raise FormatError(f"{name}: too small to be a model ({reader.size} bytes)")
    if data[:4] != MDL_MAGIC:
        raise FormatError(f"{name}: not a Source model (magic {data[:4]!r})")

    version = reader.i32_at(_H_VERSION)
    if version not in SUPPORTED_VERSIONS:
        raise FormatError(f"{name}: model version {version} is not supported")

    warnings: List[str] = []
    info = ModelInfo(
        name=reader.fixed_string_at(_H_NAME, _H_NAME_LEN),
        version=version,
        checksum=reader.i32_at(_H_CHECKSUM),
        flags=reader.i32_at(_H_FLAGS),
        hull_min=reader.vec3_at(_H_HULL_MIN),
        hull_max=reader.vec3_at(_H_HULL_MAX),
        eye_position=reader.vec3_at(_H_EYE),
    )

    declared = reader.i32_at(_H_LENGTH)
    if declared and declared != reader.size:
        warnings.append(f"header says {declared} bytes, file is {reader.size}")

    bones = _parse_bones(reader, warnings)
    info.bone_count = len(bones)
    materials = _parse_materials(reader, warnings)
    dirs = _parse_material_dirs(reader, warnings)
    skins = _parse_skins(reader, len(materials))
    parts = _parse_body_parts(reader, warnings)
    info.mesh_count = sum(len(m.meshes) for p in parts for m in p.models)
    descs, controllers, rules = _parse_flex_tables(reader, warnings)

    return MdlFile(info=info, bones=bones, body_parts=parts,
                   material_names=materials, material_dirs=dirs, skin_families=skins, warnings=warnings,
                   flex_descs=descs, flex_controllers=controllers, flex_rules=rules)


def _parse_flex_tables(reader: Reader, warnings: List[str]):
    """Flex descs (target names), controllers (face controls) and rules."""
    descs: List[str] = []
    controllers: List[FlexController] = []
    rules: List[FlexRule] = []
    try:
        count = reader.i32_at(_H_NUM_FLEXDESC)
        offset = reader.i32_at(_H_FLEXDESC_INDEX)
        if count > 0 and offset > 0:
            for cur in reader.array(offset, count, _FLEXDESC_STRIDE, "flex descs"):
                descs.append(cur.string(0))
        count = reader.i32_at(_H_NUM_FLEXCONTROLLERS)
        offset = reader.i32_at(_H_FLEXCONTROLLER_INDEX)
        if count > 0 and offset > 0:
            for cur in reader.array(offset, count, _FLEXCONTROLLER_STRIDE, "flex controllers"):
                controllers.append(FlexController(name=cur.string(4), type=cur.string(0),
                                                  min=cur.f32(12), max=cur.f32(16)))
        count = reader.i32_at(_H_NUM_FLEXRULES)
        offset = reader.i32_at(_H_FLEXRULE_INDEX)
        if count > 0 and offset > 0:
            for cur in reader.array(offset, count, _FLEXRULE_STRIDE, "flex rules"):
                op_count = cur.i32(4)
                op_offset = cur.i32(8)
                ops = []
                for op_cur in reader.array(cur.start + op_offset, op_count, _FLEXOP_STRIDE, "flex ops"):
                    ops.append((op_cur.i32(0), op_cur.i32(4), op_cur.f32(4)))
                rules.append(FlexRule(desc=cur.i32(0), ops=tuple(ops)))
    except FormatError as exc:
        warnings.append(f"flex tables unreadable ({exc}); the face will not move")
        return [], [], []
    return descs, controllers, rules


# ---------------------------------------------------------------------------
def _parse_bones(reader: Reader, warnings: List[str]) -> List[Bone]:
    count = reader.i32_at(_H_NUM_BONES)
    offset = reader.i32_at(_H_BONE_INDEX)
    if count <= 0 or offset <= 0:
        return []
    bones: List[Bone] = []
    for index, cur in enumerate(reader.array(offset, count, _BONE_STRIDE, "bones")):
        parent = cur.i32(4)
        if parent >= index:
            # a parent must already exist, or a transform pass would loop
            warnings.append(f"bone {index} points at parent {parent}; treating it as a root")
            parent = -1
        bones.append(Bone(
            name=cur.string(0) or f"bone{index}",
            parent=parent,
            position=cur.vec3(_BONE_POS),
            rotation=cur.vec4(_BONE_QUAT),
            pose_to_bone=reader.unpack_at(_POSE_TO_BONE, cur.start + _BONE_POSE_TO_BONE, "poseToBone"),
            flags=cur.i32(_BONE_FLAGS),
        ))
    return bones


def _parse_materials(reader: Reader, warnings: List[str]) -> List[str]:
    count = reader.i32_at(_H_NUM_TEXTURES)
    offset = reader.i32_at(_H_TEXTURE_INDEX)
    if count <= 0 or offset <= 0:
        return []
    out: List[str] = []
    for cur in reader.array(offset, count, _TEXTURE_STRIDE, "textures"):
        out.append(cur.string(0).replace("\\", "/").strip())
    return out


def _parse_skins(reader: Reader, textures: int) -> List[List[int]]:
    """The skin table: `families` rows of `refs` texture indices.

    A mesh names a material slot; the row of the chosen skin says which texture that
    slot actually uses.  A model without the table gets the identity row, so asking
    for skin 0 always works.
    """
    refs = reader.i32_at(_H_NUM_SKINREF)
    families = reader.i32_at(_H_NUM_SKINFAMILIES)
    offset = reader.i32_at(_H_SKIN_INDEX)
    if refs <= 0 or families <= 0 or offset <= 0:
        return [list(range(textures))] if textures else []
    out: List[List[int]] = []
    try:
        reader.check(offset, refs * families * 2, "skin table")
    except FormatError:
        return [list(range(textures))] if textures else []
    for family in range(families):
        row = [reader.i16_at(offset + (family * refs + ref) * 2) for ref in range(refs)]
        out.append([index if 0 <= index < max(textures, 1) else 0 for index in row])
    return out


def _parse_material_dirs(reader: Reader, warnings: List[str]) -> List[str]:
    count = reader.i32_at(_H_NUM_CDTEXTURES)
    offset = reader.i32_at(_H_CDTEXTURE_INDEX)
    if count <= 0 or offset <= 0:
        return []
    dirs: List[str] = []
    # this table holds absolute offsets, not offsets relative to the entry
    for (pointer,) in reader.iter_structs(struct.Struct("<i"), offset, count, 4, "cdtextures"):
        text = reader.string_at(pointer).replace("\\", "/").strip()
        if text and text not in dirs:
            dirs.append(text)
    return dirs


def _parse_body_parts(reader: Reader, warnings: List[str]) -> List[MdlBodyPart]:
    count = reader.i32_at(_H_NUM_BODYPARTS)
    offset = reader.i32_at(_H_BODYPART_INDEX)
    if count <= 0 or offset <= 0:
        return []
    parts: List[MdlBodyPart] = []
    for part_cur in reader.array(offset, count, _BODYPART_STRIDE, "body parts"):
        part = MdlBodyPart(name=part_cur.string(0), base=max(1, part_cur.i32(_BODYPART_BASE)))
        model_count = part_cur.i32(_BODYPART_NUM_MODELS)
        model_offset = part_cur.i32(_BODYPART_MODEL_INDEX)
        if model_count > 0 and model_offset:
            for model_cur in reader.array(part_cur.start + model_offset, model_count,
                                          _MODEL_STRIDE, "models"):
                part.models.append(_parse_model(reader, model_cur, warnings))
        parts.append(part)
    return parts


def _parse_model(reader: Reader, cur: Cursor, warnings: List[str]) -> MdlModel:
    model = MdlModel(
        name=cur.fixed_string(0, _MODEL_NAME_LEN),
        vertex_count=cur.i32(_MODEL_NUM_VERTICES),
        vertex_index=cur.i32(_MODEL_VERTEX_INDEX),
    )
    mesh_count = cur.i32(_MODEL_NUM_MESHES)
    mesh_offset = cur.i32(_MODEL_MESH_INDEX)
    if mesh_count > 0 and mesh_offset:
        for mesh_cur in reader.array(cur.start + mesh_offset, mesh_count, _MESH_STRIDE, "meshes"):
            mesh = MdlMesh(
                material_index=mesh_cur.i32(_MESH_MATERIAL),
                vertex_count=mesh_cur.i32(_MESH_NUM_VERTICES),
                vertex_offset=mesh_cur.i32(_MESH_VERTEX_OFFSET),
                lod_vertex_counts=tuple(mesh_cur.i32(_MESH_LOD_VERTICES + 4 * i) for i in range(8)),
            )
            mesh.flexes = _parse_mesh_flexes(reader, mesh_cur, warnings)
            model.meshes.append(mesh)
    return model


def _parse_mesh_flexes(reader: Reader, mesh_cur: Cursor, warnings: List[str]) -> List[MeshFlex]:
    count = mesh_cur.i32(_MESH_NUM_FLEXES)
    offset = mesh_cur.i32(_MESH_FLEX_INDEX)
    if count <= 0 or offset <= 0:
        return []
    out: List[MeshFlex] = []
    try:
        for cur in reader.array(mesh_cur.start + offset, count, _FLEX_STRIDE, "flexes"):
            flex = MeshFlex(desc=cur.i32(_FLEX_DESC),
                            targets=tuple(cur.f32(_FLEX_TARGETS + 4 * i) for i in range(4)),
                            pair=cur.i32(_FLEX_PAIR))
            vert_count = cur.i32(_FLEX_NUM_VERTS)
            vert_offset = cur.i32(_FLEX_VERT_INDEX)
            wrinkle = cur.u8(_FLEX_VERTANIM_TYPE) == 1
            stride = _VERTANIM_WRINKLE_STRIDE if wrinkle else _VERTANIM.size
            base = cur.start + vert_offset
            reader.check(base, vert_count * stride, "vertex animations")
            data = reader.data
            for i in range(vert_count):
                index, _speed, side, dx, dy, dz, nx, ny, nz = _VERTANIM.unpack_from(data, base + i * stride)
                flex.indices.append(index)
                flex.sides.append(side)
                flex.deltas.extend((dx, dy, dz))
                flex.normal_deltas.extend((nx, ny, nz))
            out.append(flex)
    except FormatError as exc:
        warnings.append(f"flex vertex data unreadable ({exc}); the face will not move")
        return []
    return out
