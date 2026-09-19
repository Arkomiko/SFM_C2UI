"""
Readers for Valve's binary formats.

These understand the files, not the game that shipped them, so every bridge -
Source Filmmaker, Garry's Mod, anything else on the engine - shares them.

    from Core.Code.formats import load_model, load_material, parse_vtf
    model = load_model(library, "models/player/scout.mdl")
    material = load_material(library, model.material_candidates(model.meshes[0].material)[0])
    texture = parse_vtf(library.read_bytes(material.base_texture))
"""
from .binary import FormatError, Reader
from .mdl import MdlFile, parse_mdl
from .studio import build_model, find_model_files, load_model
from .vmt import load_material, parse_vmt
from .vtf import VtfFile, parse_vtf
from .vtx import VtxFile, parse_vtx
from .vvd import VvdFile, parse_vvd

__all__ = [
    "FormatError", "Reader",
    "MdlFile", "parse_mdl",
    "VvdFile", "parse_vvd",
    "VtxFile", "parse_vtx",
    "load_model", "build_model", "find_model_files",
    "parse_vmt", "load_material",
    "VtfFile", "parse_vtf",
]
