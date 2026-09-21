"""
The .vvd file: vertex positions, normals, texture coordinates and skin weights.

Vertices are stored once for the highest detail level. Lower levels do not get
their own copy - instead a fixup table says which runs of vertices each level
keeps, and in what order. Reading a level means walking that table and
concatenating the runs; ignoring it silently gives a model whose triangles point
at the wrong vertices, which looks like an exploded mesh rather than an error.
"""
from __future__ import annotations

import struct
from array import array
from dataclasses import dataclass, field
from typing import List, Tuple

from .binary import FormatError, Reader

__all__ = ["VvdFile", "parse_vvd", "VVD_MAGIC", "VERTEX_SIZE"]

VVD_MAGIC = b"IDSV"
VERTEX_SIZE = 48

_H_VERSION = 4
_H_CHECKSUM = 8
_H_NUM_LODS = 12
_H_LOD_COUNTS = 16          # int[8]
_H_NUM_FIXUPS = 48
_H_FIXUP_INDEX = 52
_H_VERTEX_INDEX = 56
_H_TANGENT_INDEX = 60
_HEADER_SIZE = 64

#: weight[3], bone[3], numbones, position, normal, uv
_VERTEX = struct.Struct("<3f4B3f3f2f")
_FIXUP = struct.Struct("<3i")
#: the tangent block that follows the vertices: xyz and the bitangent's sign, per vertex
_TANGENT = struct.Struct("<4f")
TANGENT_SIZE = 16


@dataclass
class VvdFile:
    """Vertices for one level of detail, already fixed up."""

    version: int = 0
    checksum: int = 0
    lod_count: int = 1
    lod: int = 0
    #: whether the file carries a fixup table; without one every level shares
    #: the stored array and the vertex offsets of level 0 stay valid
    has_fixups: bool = False
    positions: array = field(default_factory=lambda: array("f"))
    normals: array = field(default_factory=lambda: array("f"))
    uvs: array = field(default_factory=lambda: array("f"))
    bone_indices: array = field(default_factory=lambda: array("B"))
    bone_weights: array = field(default_factory=lambda: array("f"))
    #: four floats per vertex - the tangent and the sign of the bitangent - or empty
    #: when the file carries none; normal maps need them
    tangents: array = field(default_factory=lambda: array("f"))
    warnings: List[str] = field(default_factory=list)

    @property
    def vertex_count(self) -> int:
        """Number of vertices."""
        return len(self.positions) // 3


def parse_vvd(data: bytes, name: str = "model.vvd", lod: int = 0) -> VvdFile:
    """Read a .vvd and return the vertices of `lod`, in that level's order."""
    reader = Reader(data, name)
    if reader.size < _HEADER_SIZE:
        raise FormatError(f"{name}: too small to be vertex data ({reader.size} bytes)")
    if data[:4] != VVD_MAGIC:
        raise FormatError(f"{name}: not Source vertex data (magic {data[:4]!r})")

    warnings: List[str] = []
    version = reader.i32_at(_H_VERSION)
    lod_count = max(1, reader.i32_at(_H_NUM_LODS))
    if lod >= lod_count:
        warnings.append(f"level {lod} does not exist ({lod_count} present), using 0")
        lod = 0

    lod_counts = [reader.i32_at(_H_LOD_COUNTS + i * 4) for i in range(8)]
    fixup_count = reader.i32_at(_H_NUM_FIXUPS)
    fixup_offset = reader.i32_at(_H_FIXUP_INDEX)
    vertex_offset = reader.i32_at(_H_VERTEX_INDEX)
    tangent_offset = reader.i32_at(_H_TANGENT_INDEX)

    # the vertices run up to the tangent block (which studiomdl always writes after them)
    vertices_end = tangent_offset if vertex_offset < tangent_offset <= reader.size else reader.size
    stored = (vertices_end - vertex_offset) // VERTEX_SIZE
    wanted = lod_counts[0] if lod_counts[0] > 0 else stored
    if wanted > stored:
        warnings.append(f"header promises {wanted} vertices, only {stored} are present")
        wanted = stored

    runs = _runs_for_lod(reader, fixup_count, fixup_offset, lod, wanted, warnings)

    out = VvdFile(version=version, checksum=reader.i32_at(_H_CHECKSUM),
                  lod_count=lod_count, lod=lod, has_fixups=fixup_count > 0, warnings=warnings)
    _read_runs(reader, vertex_offset, runs, out)
    if tangent_offset > 0 and tangent_offset + stored * TANGENT_SIZE <= reader.size:
        _read_tangents(reader, tangent_offset, runs, out)
    return out


def _runs_for_lod(reader: Reader, count: int, offset: int, lod: int,
                  total: int, warnings: List[str]) -> List[Tuple[int, int]]:
    """Which (start, length) runs of stored vertices this level uses."""
    if count <= 0 or offset <= 0:
        return [(0, total)]                      # no fixups: every level is the same
    runs: List[Tuple[int, int]] = []
    try:
        entries = list(reader.iter_structs(_FIXUP, offset, count, 0, "fixups"))
    except FormatError as exc:
        warnings.append(f"fixup table unreadable ({exc}); using vertices unchanged")
        return [(0, total)]
    for fixup_lod, source, length in entries:
        # a fixup belongs to every level at least as detailed as its own
        if fixup_lod < lod or length <= 0:
            continue
        if source < 0 or source + length > total:
            warnings.append(f"fixup {source}+{length} lies outside {total} vertices; skipped")
            continue
        if runs and runs[-1][0] + runs[-1][1] == source:
            runs[-1] = (runs[-1][0], runs[-1][1] + length)      # merge touching runs
        else:
            runs.append((source, length))
    if not runs:
        warnings.append(f"no fixups apply to level {lod}; using vertices unchanged")
        return [(0, total)]
    return runs


def _read_tangents(reader: Reader, base: int, runs: List[Tuple[int, int]], out: VvdFile) -> None:
    """The tangent of every vertex the runs cover, in the same order as the vertices."""
    tangents = out.tangents
    unpack = _TANGENT.unpack_from
    data = reader.data
    for start, length in runs:
        cursor = base + start * TANGENT_SIZE
        for _ in range(length):
            tangents.extend(unpack(data, cursor))
            cursor += TANGENT_SIZE


def _read_runs(reader: Reader, base: int, runs: List[Tuple[int, int]], out: VvdFile) -> None:
    positions, normals, uvs = out.positions, out.normals, out.uvs
    bones, weights = out.bone_indices, out.bone_weights
    unpack = _VERTEX.unpack_from
    data = reader.data
    for start, length in runs:
        reader.check(base + start * VERTEX_SIZE, length * VERTEX_SIZE, "vertices")
        cursor = base + start * VERTEX_SIZE
        for _ in range(length):
            (w0, w1, w2, b0, b1, b2, nbones,
             px, py, pz, nx, ny, nz, u, v) = unpack(data, cursor)
            cursor += VERTEX_SIZE
            positions.append(px); positions.append(py); positions.append(pz)
            normals.append(nx); normals.append(ny); normals.append(nz)
            uvs.append(u); uvs.append(v)
            bones.append(b0); bones.append(b1); bones.append(b2)
            weights.append(w0); weights.append(w1); weights.append(w2)
