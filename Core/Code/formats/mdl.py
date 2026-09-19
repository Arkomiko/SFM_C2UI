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

from Core.API.model import Bone, ModelInfo

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
_H_NUM_BODYPARTS = 232
_H_BODYPART_INDEX = 236

_BONE_STRIDE = 216
_BONE_POS = 32
_BONE_QUAT = 44
_BONE_POSE_TO_BONE = 96
_BONE_FLAGS = 160

_TEXTURE_STRIDE = 64

_BODYPART_STRIDE = 16
_BODYPART_NUM_MODELS = 4
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

_POSE_TO_BONE = struct.Struct("<12f")


@dataclass
class MdlMesh:
    """One mesh inside a model: a slice of that model's vertices."""

    material_index: int
    vertex_count: int
    vertex_offset: int          # relative to the owning model's vertices


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
    name: str
    models: List[MdlModel] = field(default_factory=list)


@dataclass
class MdlFile:
    """Everything the .mdl itself knows."""

    info: ModelInfo
    bones: List[Bone] = field(default_factory=list)
    body_parts: List[MdlBodyPart] = field(default_factory=list)
    material_names: List[str] = field(default_factory=list)
    material_dirs: List[str] = field(default_factory=list)
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
    parts = _parse_body_parts(reader, warnings)
    info.mesh_count = sum(len(m.meshes) for p in parts for m in p.models)

    return MdlFile(info=info, bones=bones, body_parts=parts,
                   material_names=materials, material_dirs=dirs, warnings=warnings)


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
        part = MdlBodyPart(name=part_cur.string(0))
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
            model.meshes.append(MdlMesh(
                material_index=mesh_cur.i32(_MESH_MATERIAL),
                vertex_count=mesh_cur.i32(_MESH_NUM_VERTICES),
                vertex_offset=mesh_cur.i32(_MESH_VERTEX_OFFSET),
            ))
    return model
