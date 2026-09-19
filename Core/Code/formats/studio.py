"""
Assembling a Source model from its three files.

The .mdl describes the skeleton and which meshes exist, the .vvd holds the
vertices and the .vtx says which of them form triangles. None of the three is
usable alone, and they agree only if they were compiled together - so this is
also where a mismatched set is caught and reported rather than drawn as noise.

    model = load_model(library, "models/player/scout.mdl")
    model.meshes[0].positions      # ready for a vertex buffer

Only one level of detail is built at a time; level 0 is the one the editor
shows.
"""
from __future__ import annotations

import logging
from array import array
from pathlib import Path
from typing import Callable, List, Optional, Protocol

from Core.API.model import Mesh, Model

from .binary import FormatError
from .mdl import MdlFile, parse_mdl
from .vtx import VTX_SUFFIXES, VtxFile, parse_vtx

#: model version from which the .vtx strip headers carry the topology fields
EXTENDED_VTX_FROM_VERSION = 49
from .vvd import VvdFile, parse_vvd

log = logging.getLogger("c2ui.studio")

__all__ = ["load_model", "build_model", "ModelSource", "find_model_files"]


class ModelSource(Protocol):
    """Anything that can hand back content by relative path.

    Both `VirtualFileSystem` and `ContentLibrary` satisfy this, so a model can be
    loaded straight from mounted content or from a folder in a test.
    """

    def read_bytes(self, rel: str) -> Optional[bytes]: ...


def find_model_files(source: ModelSource, rel: str) -> tuple[str, Optional[str], Optional[str]]:
    """Work out the .vvd and .vtx names that go with a .mdl.

    Index data comes in several flavours for different hardware; any of them
    carries the same triangles, so the first one present is used.
    """
    rel = rel.replace("\\", "/")
    stem = rel[:-4] if rel.lower().endswith(".mdl") else rel
    vvd = f"{stem}.vvd"
    if source.read_bytes(vvd) is None:
        vvd = None                                    # type: ignore[assignment]
    vtx = None
    for suffix in VTX_SUFFIXES:
        candidate = f"{stem}{suffix}"
        if source.read_bytes(candidate) is not None:
            vtx = candidate
            break
    return rel, vvd, vtx


def load_model(source: ModelSource, rel: str, lod: int = 0) -> Model:
    """Load a model out of mounted content.

    Raises :class:`FormatError` only when the .mdl itself cannot be read; a
    missing or broken .vvd/.vtx yields a model with bones and a warning, because
    a skeleton with no geometry is still worth showing.
    """
    mdl_bytes = source.read_bytes(rel)
    if mdl_bytes is None:
        raise FormatError(f"{rel}: not found in the mounted content")

    name = rel.rsplit("/", 1)[-1]
    mdl = parse_mdl(mdl_bytes, name)

    _, vvd_rel, vtx_rel = find_model_files(source, rel)
    vvd = vtx = None
    warnings: List[str] = []

    if vvd_rel is None:
        warnings.append("no .vvd beside this model: it has no vertices")
    else:
        try:
            vvd = parse_vvd(source.read_bytes(vvd_rel) or b"", vvd_rel.rsplit("/", 1)[-1], lod)
        except FormatError as exc:
            warnings.append(f"vertex data unusable ({exc})")

    if vtx_rel is None:
        warnings.append("no .vtx beside this model: it has no triangles")
    else:
        try:
            vtx = parse_vtx(source.read_bytes(vtx_rel) or b"", vtx_rel.rsplit("/", 1)[-1], lod,
                            extended=mdl.info.version >= EXTENDED_VTX_FROM_VERSION)
        except FormatError as exc:
            warnings.append(f"index data unusable ({exc})")

    return build_model(mdl, vvd, vtx, extra_warnings=warnings)


def build_model(mdl: MdlFile, vvd: Optional[VvdFile], vtx: Optional[VtxFile],
                extra_warnings: Optional[List[str]] = None) -> Model:
    """Zip the three files together into one model."""
    model = Model(
        info=mdl.info,
        bones=list(mdl.bones),
        material_names=list(mdl.material_names),
        material_dirs=list(mdl.material_dirs),
        warnings=list(mdl.warnings),
    )
    if extra_warnings:
        model.warnings.extend(extra_warnings)
    if vvd is not None:
        model.warnings.extend(vvd.warnings)
        model.info.lod_count = vvd.lod_count
    if vtx is not None:
        model.warnings.extend(vtx.warnings)

    if vvd is None or vtx is None or vvd.vertex_count == 0:
        return model

    if mdl.info.checksum and vvd.checksum and mdl.info.checksum != vvd.checksum:
        # compiled at different times: offsets will not line up
        model.warnings.append("vertex data was compiled from a different model; geometry may be wrong")

    total_vertices = vvd.vertex_count
    lod = vvd.lod
    # At level 0 every mesh sits where the .mdl says. At lower levels the
    # fixup table has compacted the array, and the engine (Studio_SetRootLOD)
    # re-derives every offset as a running total of numLODVertexes[lod] over
    # all meshes of all models. A file with no fixups is never compacted, so
    # there the level-0 offsets stay and only the counts shrink.
    compacted = lod > 0 and vvd.has_fixups
    cursor = 0
    for part_index, part in enumerate(mdl.body_parts):
        vtx_part = vtx.body_parts[part_index] if part_index < len(vtx.body_parts) else []
        for model_index, sub in enumerate(part.models):
            vtx_model = vtx_part[model_index] if model_index < len(vtx_part) else []
            model_base = cursor if compacted else sub.first_vertex
            mesh_cursor = 0
            for mesh_index, mdl_mesh in enumerate(sub.meshes):
                count = mdl_mesh.vertices_at(lod)
                base = model_base + (mesh_cursor if compacted else mdl_mesh.vertex_offset)
                mesh_cursor += count
                if mesh_index >= len(vtx_model):
                    continue                      # no index data for this mesh
                vtx_mesh = vtx_model[mesh_index]
                if not vtx_mesh.indices:
                    continue
                mesh = _build_mesh(model, part, sub, mdl_mesh, vtx_mesh, vvd, total_vertices,
                                   base, count)
                if mesh is not None:
                    model.meshes.append(mesh)
            cursor += mesh_cursor

    model.info.mesh_count = len(model.meshes)
    return model


def _build_mesh(model: Model, part, sub, mdl_mesh, vtx_mesh, vvd: VvdFile,
                total_vertices: int, base: int, count: int) -> Optional[Mesh]:
    """Copy one mesh's slice of the vertex array and rebase its indices."""
    if count <= 0:
        return None
    if base < 0 or base + count > total_vertices:
        model.warnings.append(
            f"mesh in '{sub.name or part.name}' claims vertices {base}..{base + count} "
            f"of {total_vertices}; skipped")
        return None

    material_index = mdl_mesh.material_index
    material = ""
    if 0 <= material_index < len(model.material_names):
        material = model.material_names[material_index]

    mesh = Mesh(material=material, material_index=material_index, body_part=part.name)
    mesh.positions = vvd.positions[base * 3:(base + count) * 3]
    mesh.normals = vvd.normals[base * 3:(base + count) * 3]
    mesh.uvs = vvd.uvs[base * 2:(base + count) * 2]
    mesh.bone_indices = vvd.bone_indices[base * 3:(base + count) * 3]
    mesh.bone_weights = vvd.bone_weights[base * 3:(base + count) * 3]

    out = array("I")
    dropped = 0
    for index in vtx_mesh.indices:
        if index >= count:
            dropped += 1
            continue
        out.append(index)
    if dropped:
        model.warnings.append(f"{dropped} indices pointed outside mesh '{material}'; dropped")
    # a triangle list must stay a multiple of three
    if len(out) % 3:
        del out[len(out) - (len(out) % 3):]
    mesh.indices = out
    return mesh if mesh.indices else None
