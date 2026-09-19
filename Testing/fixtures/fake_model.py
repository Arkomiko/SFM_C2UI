"""
Build a Source model in memory, byte for byte.

Testing a binary reader against files we cannot edit proves only that it agrees
with itself. Writing the bytes here means the expected values are known exactly,
so a wrong field offset fails a test instead of producing a model that merely
looks plausible.

    mdl, vvd, vtx = build_triangle_model()

The result is a two-bone model with one body part holding one mesh of four
vertices and two triangles.
"""
from __future__ import annotations

import struct
from typing import Dict, List, Sequence, Tuple

__all__ = ["build_triangle_model", "build_mdl", "build_vvd", "build_vtx", "FakeVertex"]

MDL_VERSION = 49
VERTEX_SIZE = 48

#: (position, normal, uv, bone, weight)
FakeVertex = Tuple[Tuple[float, float, float], Tuple[float, float, float],
                   Tuple[float, float], int, float]

DEFAULT_VERTICES: List[FakeVertex] = [
    ((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 0.0), 0, 1.0),
    ((10.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0), 0, 1.0),
    ((10.0, 20.0, 0.0), (0.0, 0.0, 1.0), (1.0, 1.0), 1, 1.0),
    ((0.0, 20.0, 5.0), (0.0, 0.0, 1.0), (0.0, 1.0), 1, 1.0),
]
DEFAULT_TRIANGLES = [(0, 1, 2), (0, 2, 3)]


class _Blob:
    """A growing buffer that can patch an int once its target is known."""

    def __init__(self) -> None:
        self.data = bytearray()

    def __len__(self) -> int:
        return len(self.data)

    def write(self, raw: bytes) -> int:
        at = len(self.data)
        self.data.extend(raw)
        return at

    def i32(self, value: int = 0) -> int:
        return self.write(struct.pack("<i", value))

    def pad(self, count: int) -> int:
        return self.write(b"\0" * count)

    def string(self, text: str, length: int) -> int:
        raw = text.encode("utf-8")[:length - 1]
        return self.write(raw + b"\0" * (length - len(raw)))

    def cstring(self, text: str) -> int:
        return self.write(text.encode("utf-8") + b"\0")

    def patch(self, at: int, value: int) -> None:
        struct.pack_into("<i", self.data, at, value)

    def align(self, size: int = 4) -> None:
        while len(self.data) % size:
            self.data.append(0)


def build_mdl(name: str = "test/fake.mdl",
              bones: Sequence[str] = ("root", "child"),
              materials: Sequence[str] = ("fakemat",),
              material_dirs: Sequence[str] = ("models/test/",),
              vertex_count: int = 4,
              checksum: int = 0x1234,
              version: int = MDL_VERSION) -> bytes:
    """A .mdl with one body part, one model and one mesh."""
    b = _Blob()
    b.write(b"IDST")                                      # 0   id
    b.i32(version)                                        # 4   version
    b.i32(checksum)                                       # 8   checksum
    b.string(name, 64)                                    # 12  name
    length_at = b.i32(0)                                  # 76  length
    b.write(struct.pack("<3f", 0.0, 0.0, 64.0))           # 80  eyeposition
    b.write(struct.pack("<3f", 0.0, 0.0, 0.0))            # 92  illumposition
    b.write(struct.pack("<3f", -1.0, -2.0, -3.0))         # 104 hull_min
    b.write(struct.pack("<3f", 11.0, 22.0, 33.0))         # 116 hull_max
    b.write(struct.pack("<3f", 0.0, 0.0, 0.0))            # 128 view_bbmin
    b.write(struct.pack("<3f", 0.0, 0.0, 0.0))            # 140 view_bbmax
    b.i32(0)                                              # 152 flags
    num_bones_at = b.i32(len(bones))                      # 156
    bone_index_at = b.i32(0)                              # 160
    b.pad(40)                                             # 164..203 controllers/hitboxes/anims/seqs
    b.i32(len(materials))                                 # 204 numtextures
    texture_index_at = b.i32(0)                           # 208
    b.i32(len(material_dirs))                             # 212 numcdtextures
    cd_index_at = b.i32(0)                                # 216
    b.pad(12)                                             # 220 skin table
    b.i32(1)                                              # 232 numbodyparts
    bodypart_index_at = b.i32(0)                          # 236
    b.pad(120)                                            # remainder of the header

    # ---- bones -----------------------------------------------------------
    b.align()
    b.patch(bone_index_at, len(b))
    bone_start = len(b)
    name_slots: List[Tuple[int, int, str]] = []
    for index, bone_name in enumerate(bones):
        here = len(b)
        slot = b.i32(0)                                   # 0   sznameindex
        b.i32(-1 if index == 0 else index - 1)            # 4   parent
        b.pad(24)                                         # 8   bonecontroller[6]
        b.write(struct.pack("<3f", float(index), 1.0, 2.0))       # 32  pos
        b.write(struct.pack("<4f", 0.0, 0.0, 0.0, 1.0))           # 44  quat
        b.pad(12)                                         # 60  rot
        b.pad(12)                                         # 72  posscale
        b.pad(12)                                         # 84  rotscale
        b.write(struct.pack("<12f", *([1.0, 0.0, 0.0, 0.0,
                                       0.0, 1.0, 0.0, 0.0,
                                       0.0, 0.0, 1.0, 0.0])))     # 96  poseToBone
        b.pad(16)                                         # 144 qAlignment
        b.i32(index)                                      # 160 flags
        b.pad(216 - (len(b) - here))                      # to the full 216 bytes
        name_slots.append((here, slot, bone_name))

    for here, slot, bone_name in name_slots:
        b.patch(slot, len(b) - here)                      # relative to the bone
        b.cstring(bone_name)

    # ---- material names --------------------------------------------------
    b.align()
    b.patch(texture_index_at, len(b))
    texture_slots = []
    for material in materials:
        here = len(b)
        slot = b.i32(0)
        b.pad(60)                                         # 64 bytes total
        texture_slots.append((here, slot, material))
    for here, slot, material in texture_slots:
        b.patch(slot, len(b) - here)
        b.cstring(material)

    # ---- material folders: absolute offsets, not relative ----------------
    b.align()
    b.patch(cd_index_at, len(b))
    cd_slots = [b.i32(0) for _ in material_dirs]
    for slot, folder in zip(cd_slots, material_dirs):
        b.patch(slot, len(b))
        b.cstring(folder)

    # ---- body part -> model -> mesh --------------------------------------
    b.align()
    b.patch(bodypart_index_at, len(b))
    part_start = len(b)
    part_name_slot = b.i32(0)                             # 0  sznameindex
    b.i32(1)                                              # 4  nummodels
    b.i32(0)                                              # 8  base
    part_model_slot = b.i32(0)                            # 12 modelindex

    b.align()
    b.patch(part_model_slot, len(b) - part_start)
    model_start = len(b)
    b.string("fake_reference.smd", 64)                    # 0   name
    b.i32(0)                                              # 64  type
    b.write(struct.pack("<f", 1.0))                       # 68  boundingradius
    b.i32(1)                                              # 72  nummeshes
    model_mesh_slot = b.i32(0)                            # 76  meshindex
    b.i32(vertex_count)                                   # 80  numvertices
    b.i32(0)                                              # 84  vertexindex
    b.pad(148 - (len(b) - model_start))

    b.align()
    b.patch(model_mesh_slot, len(b) - model_start)
    mesh_start = len(b)
    b.i32(0)                                              # 0  material
    b.i32(model_start - len(b) + 4)                       # 4  modelindex (unused here)
    b.i32(vertex_count)                                   # 8  numvertices
    b.i32(0)                                              # 12 vertexoffset
    b.pad(52 - (len(b) - mesh_start))
    for level in range(8):                                # 52 numLODVertexes[8]
        b.i32(vertex_count)
    b.pad(116 - (len(b) - mesh_start))

    b.patch(part_name_slot, len(b) - part_start)
    b.cstring("body")

    b.patch(length_at, len(b))
    return bytes(b.data)


def build_vvd(vertices: Sequence[FakeVertex] = tuple(DEFAULT_VERTICES),
              checksum: int = 0x1234,
              fixups: Sequence[Tuple[int, int, int]] = (),
              lod_counts: Sequence[int] = ()) -> bytes:
    """A .vvd holding `vertices`, optionally with a fixup table."""
    counts = list(lod_counts) or [len(vertices)]
    counts = (counts + [0] * 8)[:8]
    num_lods = max(1, len([c for c in counts if c]))

    header = bytearray()
    header += b"IDSV"
    header += struct.pack("<i", 4)                       # version
    header += struct.pack("<i", checksum)
    header += struct.pack("<i", num_lods)
    header += struct.pack("<8i", *counts)
    header += struct.pack("<i", len(fixups))
    fixup_at = len(header); header += struct.pack("<i", 0)
    vertex_at = len(header); header += struct.pack("<i", 0)
    tangent_at = len(header); header += struct.pack("<i", 0)

    body = bytearray()
    fixup_start = len(header) + len(body)
    for lod, source, count in fixups:
        body += struct.pack("<3i", lod, source, count)

    vertex_start = len(header) + len(body)
    for position, normal, uv, bone, weight in vertices:
        body += struct.pack("<3f", weight, 0.0, 0.0)
        body += bytes((bone, 0, 0, 1))
        body += struct.pack("<3f", *position)
        body += struct.pack("<3f", *normal)
        body += struct.pack("<2f", *uv)

    tangent_start = len(header) + len(body)
    struct.pack_into("<i", header, fixup_at, fixup_start if fixups else 0)
    struct.pack_into("<i", header, vertex_at, vertex_start)
    struct.pack_into("<i", header, tangent_at, tangent_start)
    return bytes(header + body)


def build_vtx(triangles: Sequence[Tuple[int, int, int]] = tuple(DEFAULT_TRIANGLES),
              vertex_count: int = 4, strip_flags: int = 0x01,
              indices: Sequence[int] = (), extended: bool = MDL_VERSION >= 49,
              groups: int = 1) -> bytes:
    """A .vtx with one body part, model, level and mesh.

    `groups` strip groups are written, each holding the same triangles, so a
    reader that steps through groups with the wrong stride reads garbage from
    the second one. `extended` writes the model-49 layout with the two extra
    topology fields in every group and strip header.
    """
    flat: List[int] = list(indices) if indices else [i for tri in triangles for i in tri]
    group_size = 33 if extended else 25
    strip_size = 35 if extended else 27

    b = _Blob()
    b.i32(7)                                              # 0  version
    b.i32(0)                                              # 4  vertCacheSize
    b.write(struct.pack("<2H", 0, 0))                     # 8  maxBonesPerStrip/Tri
    b.i32(3)                                              # 12 maxBonesPerVert
    b.i32(0)                                              # 16 checkSum
    b.i32(1)                                              # 20 numLODs
    b.i32(0)                                              # 24 materialReplacementListOffset
    b.i32(1)                                              # 28 numBodyParts
    part_slot = b.i32(0)                                  # 32 bodyPartOffset

    b.patch(part_slot, len(b))
    part_start = len(b)
    b.i32(1)                                              # numModels
    model_slot = b.i32(0)

    b.patch(model_slot, len(b) - part_start)
    model_start = len(b)
    b.i32(1)                                              # numLODs
    lod_slot = b.i32(0)

    b.patch(lod_slot, len(b) - model_start)
    lod_start = len(b)
    b.i32(1)                                              # numMeshes
    mesh_slot = b.i32(0)
    b.write(struct.pack("<f", 0.0))                       # switchPoint

    b.patch(mesh_slot, len(b) - lod_start)
    mesh_start = len(b)
    b.i32(groups)                                         # numStripGroups
    group_slot = b.i32(0)
    b.write(b"\0")                                        # flags

    b.patch(group_slot, len(b) - mesh_start)
    # the group headers sit together; each one's data follows all of them
    group_starts = []
    slots = []
    for _g in range(groups):
        group_start = len(b)
        group_starts.append(group_start)
        b.i32(vertex_count)                               # 0  numVerts
        vert_slot = b.i32(0)                              # 4  vertOffset
        b.i32(len(flat))                                  # 8  numIndices
        index_slot = b.i32(0)                             # 12 indexOffset
        b.i32(1)                                          # 16 numStrips
        strip_slot = b.i32(0)                             # 20 stripOffset
        b.write(b"\0")                                    # 24 flags
        if extended:
            b.i32(0)                                      # 25 numTopologyIndices
            b.i32(0)                                      # 29 topologyOffset
        assert len(b) - group_start == group_size
        slots.append((vert_slot, index_slot, strip_slot))

    for group_start, (vert_slot, index_slot, strip_slot) in zip(group_starts, slots):
        b.patch(vert_slot, len(b) - group_start)
        for i in range(vertex_count):
            b.write(bytes((0, 0, 0, 1)))                  # boneWeightIndex[3], numBones
            b.write(struct.pack("<H", i))                 # origMeshVertID
            b.write(bytes((0, 0, 0)))                     # boneID[3]

        b.patch(index_slot, len(b) - group_start)
        for index in flat:
            b.write(struct.pack("<H", index))

        b.patch(strip_slot, len(b) - group_start)
        strip_start = len(b)
        b.i32(len(flat))                                  # 0  numIndices
        b.i32(0)                                          # 4  indexOffset
        b.i32(vertex_count)                               # 8  numVerts
        b.i32(0)                                          # 12 vertOffset
        b.write(struct.pack("<h", 0))                     # 16 numBones
        b.write(bytes((strip_flags,)))                    # 18 flags
        b.i32(0)                                          # 19 numBoneStateChanges
        b.i32(0)                                          # 23 boneStateChangeOffset
        if extended:
            b.i32(0)                                      # 27 numTopologyIndices
            b.i32(0)                                      # 31 topologyOffset
        b.pad(strip_size - (len(b) - strip_start))
    return bytes(b.data)


def build_triangle_model(**kwargs) -> Tuple[bytes, bytes, bytes]:
    """The default two-triangle model as (mdl, vvd, vtx)."""
    return (build_mdl(**kwargs.get("mdl", {})),
            build_vvd(**kwargs.get("vvd", {})),
            build_vtx(**kwargs.get("vtx", {})))


class FakeSource:
    """A ModelSource backed by a dict - what load_model() reads from in tests."""

    def __init__(self, files: Dict[str, bytes]) -> None:
        self.files = files

    def read_bytes(self, rel: str):
        return self.files.get(rel.replace("\\", "/"))
