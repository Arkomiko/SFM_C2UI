"""
C2UI public API.

The contract between Core and everything built on it: the editor in `App/`, the
utilities in `Tools/` and third-party plugins. Import from here, never from
`Core.Code` directly - that is what lets the engine change underneath without
breaking anything.

    from Core.API import SourceBridge, MountSet, Availability
"""
from .bridge import BridgeInfo, SourceBridge
from .material import Material, as_bool, as_float, as_vec, texture_path
from .model import Bone, Mesh, Model, ModelInfo
from .types import CONTENT_DIRS, Availability, Mount, MountSet, ProbeResult, order_mounts

#: Bumped when anything in this package changes shape. Plugins check it.
API_VERSION = "1.0"

__all__ = [
    "API_VERSION",
    "SourceBridge", "BridgeInfo",
    "Availability", "Mount", "MountSet", "ProbeResult",
    "CONTENT_DIRS", "order_mounts",
    "Model", "ModelInfo", "Mesh", "Bone",
    "Material", "texture_path", "as_float", "as_vec", "as_bool",
]
