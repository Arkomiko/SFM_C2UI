"""
Readers for Valve's binary formats.

These understand the files, not the game that shipped them, so every bridge -
Source Filmmaker, Garry's Mod, anything else on the engine - shares them.

    from Core.Code.formats import load_model
    model = load_model(library, "models/player/scout.mdl")
"""
from .binary import FormatError, Reader
from .mdl import MdlFile, parse_mdl
from .studio import build_model, find_model_files, load_model
from .vtx import VtxFile, parse_vtx
from .vvd import VvdFile, parse_vvd

__all__ = [
    "FormatError", "Reader",
    "MdlFile", "parse_mdl",
    "VvdFile", "parse_vvd",
    "VtxFile", "parse_vtx",
    "load_model", "build_model", "find_model_files",
]
