"""
The .vtx file: which vertices form which triangles.

Geometry lives in .vvd, but the order the hardware draws it in lives here, split
by level of detail and grouped into strips. Its nesting mirrors the .mdl exactly
- body part, model, mesh - which is what lets the two be zipped together.

Two details make this file awkward, and both are handled below:

* every offset is relative to the struct that holds it, not to the file;
* its vertices are indirections - each names a vertex of the *mesh*, which the
  caller turns into an index into the model's vertex array.

The usual name is `<model>.dx90.vtx`; `.dx80.vtx` and `.sw.vtx` hold the same
layout for older hardware.
"""
from __future__ import annotations

import struct
from array import array
from dataclasses import dataclass, field
from typing import List

from .binary import Cursor, FormatError, Reader

__all__ = ["VtxFile", "VtxMesh", "parse_vtx", "VTX_VERSION", "VTX_SUFFIXES"]

VTX_VERSION = 7
#: tried in this order when looking for a model's index data
VTX_SUFFIXES = (".dx90.vtx", ".dx80.vtx", ".vtx", ".sw.vtx")

_H_VERSION = 0
_H_NUM_LODS = 20
_H_NUM_BODY_PARTS = 28
_H_BODY_PART_OFFSET = 32
_HEADER_SIZE = 36

_BODY_PART_STRIDE = 8
_MODEL_STRIDE = 8
_LOD_STRIDE = 12
_MESH_STRIDE = 9
_STRIP_GROUP_STRIDE = 25
_STRIP_STRIDE = 27
_VTX_VERTEX_STRIDE = 9
_VTX_VERTEX_ORIG_ID = 4        # offset of origMeshVertID inside Vertex_t

_STRIP_GROUP_IS_FLEXED = 0x01
_STRIP_GROUP_IS_HWSKINNED = 0x02


@dataclass
class VtxMesh:
    """Indices for one mesh, already expanded to a plain triangle list.

    Indices are relative to the mesh's own vertices; the caller adds the mesh's
    position inside the model.
    """

    indices: array = field(default_factory=lambda: array("I"))

    @property
    def triangle_count(self) -> int:
        return len(self.indices) // 3


@dataclass
class VtxFile:
    """Index data for one level of detail, shaped like the .mdl."""

    version: int = 0
    lod_count: int = 1
    lod: int = 0
    #: body_parts[part][model][mesh]
    body_parts: List[List[List[VtxMesh]]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def triangle_count(self) -> int:
        return sum(mesh.triangle_count
                   for part in self.body_parts for model in part for mesh in model)


def parse_vtx(data: bytes, name: str = "model.vtx", lod: int = 0) -> VtxFile:
    """Read a .vtx and return the triangle lists for `lod`."""
    reader = Reader(data, name)
    if reader.size < _HEADER_SIZE:
        raise FormatError(f"{name}: too small to be index data ({reader.size} bytes)")

    version = reader.i32_at(_H_VERSION)
    if version != VTX_VERSION:
        raise FormatError(f"{name}: index data version {version} is not supported")

    warnings: List[str] = []
    lod_count = max(1, reader.i32_at(_H_NUM_LODS))
    if lod >= lod_count:
        warnings.append(f"level {lod} does not exist ({lod_count} present), using 0")
        lod = 0

    out = VtxFile(version=version, lod_count=lod_count, lod=lod, warnings=warnings)
    part_count = reader.i32_at(_H_NUM_BODY_PARTS)
    part_offset = reader.i32_at(_H_BODY_PART_OFFSET)
    if part_count <= 0 or part_offset <= 0:
        return out

    for part_cur in reader.array(part_offset, part_count, _BODY_PART_STRIDE, "body parts"):
        out.body_parts.append(_parse_body_part(reader, part_cur, lod, warnings))
    return out


def _parse_body_part(reader: Reader, cur: Cursor, lod: int, warnings: List[str]):
    models = []
    count = cur.i32(0)
    offset = cur.i32(4)
    if count <= 0 or offset <= 0:
        return models
    for model_cur in reader.array(cur.start + offset, count, _MODEL_STRIDE, "models"):
        models.append(_parse_model(reader, model_cur, lod, warnings))
    return models


def _parse_model(reader: Reader, cur: Cursor, lod: int, warnings: List[str]) -> List[VtxMesh]:
    lod_count = cur.i32(0)
    lod_offset = cur.i32(4)
    if lod_count <= 0 or lod_offset <= 0:
        return []
    wanted = min(lod, lod_count - 1)
    lod_cur = reader.cursor(cur.start + lod_offset + wanted * _LOD_STRIDE)

    meshes: List[VtxMesh] = []
    mesh_count = lod_cur.i32(0)
    mesh_offset = lod_cur.i32(4)
    if mesh_count <= 0 or mesh_offset <= 0:
        return meshes
    for mesh_cur in reader.array(lod_cur.start + mesh_offset, mesh_count, _MESH_STRIDE, "meshes"):
        meshes.append(_parse_mesh(reader, mesh_cur, warnings))
    return meshes


def _parse_mesh(reader: Reader, cur: Cursor, warnings: List[str]) -> VtxMesh:
    mesh = VtxMesh()
    group_count = cur.i32(0)
    group_offset = cur.i32(4)
    if group_count <= 0 or group_offset <= 0:
        return mesh
    for group_cur in reader.array(cur.start + group_offset, group_count,
                                  _STRIP_GROUP_STRIDE, "strip groups"):
        _parse_strip_group(reader, group_cur, mesh, warnings)
    return mesh


def _parse_strip_group(reader: Reader, cur: Cursor, mesh: VtxMesh, warnings: List[str]) -> None:
    vertex_count = cur.i32(0)
    vertex_offset = cur.i32(4)
    index_count = cur.i32(8)
    index_offset = cur.i32(12)
    strip_count = cur.i32(16)
    strip_offset = cur.i32(20)
    if vertex_count <= 0 or index_count <= 0:
        return

    # each Vertex_t names a vertex of the mesh; collect that mapping once
    try:
        base = cur.start + vertex_offset
        reader.check(base, vertex_count * _VTX_VERTEX_STRIDE, "strip vertices")
        mapping = [reader.u16_at(base + i * _VTX_VERTEX_STRIDE + _VTX_VERTEX_ORIG_ID)
                   for i in range(vertex_count)]
    except FormatError as exc:
        warnings.append(f"strip group vertices unreadable ({exc})")
        return

    try:
        index_base = cur.start + index_offset
        reader.check(index_base, index_count * 2, "strip indices")
    except FormatError as exc:
        warnings.append(f"strip group indices unreadable ({exc})")
        return

    if strip_count <= 0 or strip_offset <= 0:
        # no strip table: the whole group is one triangle list
        _emit_list(reader, index_base, 0, index_count, mapping, mesh, warnings)
        return

    for strip_cur in reader.array(cur.start + strip_offset, strip_count, _STRIP_STRIDE, "strips"):
        strip_indices = strip_cur.i32(0)
        strip_start = strip_cur.i32(4)
        flags = strip_cur.u8(18)
        if strip_indices <= 0:
            continue
        if strip_start + strip_indices > index_count:
            warnings.append("strip runs past the end of its group; skipped")
            continue
        if flags & 0x02:                       # STRIP_TRILIST is 0x01, TRISTRIP is 0x02
            _emit_strip(reader, index_base, strip_start, strip_indices, mapping, mesh, warnings)
        else:
            _emit_list(reader, index_base, strip_start, strip_indices, mapping, mesh, warnings)


def _emit_list(reader: Reader, base: int, start: int, count: int,
               mapping: List[int], mesh: VtxMesh, warnings: List[str]) -> None:
    out = mesh.indices
    limit = len(mapping)
    dropped = 0
    for i in range(start, start + count - 2, 3):
        a = reader.u16_at(base + i * 2)
        b = reader.u16_at(base + (i + 1) * 2)
        c = reader.u16_at(base + (i + 2) * 2)
        if a >= limit or b >= limit or c >= limit:
            dropped += 1
            continue
        out.append(mapping[a]); out.append(mapping[b]); out.append(mapping[c])
    if dropped:
        warnings.append(f"{dropped} triangles referenced vertices outside their group")


def _emit_strip(reader: Reader, base: int, start: int, count: int,
                mapping: List[int], mesh: VtxMesh, warnings: List[str]) -> None:
    """Expand a triangle strip, flipping winding on every other triangle."""
    out = mesh.indices
    limit = len(mapping)
    dropped = 0
    for i in range(count - 2):
        a = reader.u16_at(base + (start + i) * 2)
        b = reader.u16_at(base + (start + i + 1) * 2)
        c = reader.u16_at(base + (start + i + 2) * 2)
        if a == b or b == c or a == c:
            continue                            # degenerate: joins two strips
        if a >= limit or b >= limit or c >= limit:
            dropped += 1
            continue
        if i % 2:
            out.append(mapping[a]); out.append(mapping[c]); out.append(mapping[b])
        else:
            out.append(mapping[a]); out.append(mapping[b]); out.append(mapping[c])
    if dropped:
        warnings.append(f"{dropped} strip triangles referenced vertices outside their group")
