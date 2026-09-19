"""
What a loaded model looks like.

Geometry is kept in flat `array` buffers rather than lists of tuples: that is
how a GPU wants it, so the renderer can hand these straight to a vertex buffer
without converting anything, and a 30 000-vertex model costs megabytes rather
than tens of them.

    model = load_model(...)
    for mesh in model.meshes:
        mesh.positions     # array('f') [x,y,z, x,y,z, ...]
        mesh.indices       # array('I') triangle list
        mesh.material      # "models/player/scout"

Coordinates are Source's: X forward, Y left, Z up, units of one inch. Nothing
converts them here - a renderer decides its own convention once, in one place.
"""
from __future__ import annotations

from array import array
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

__all__ = ["Bone", "Mesh", "Model", "ModelInfo"]


@dataclass
class Bone:
    """One joint of the skeleton, in its parent's space."""

    name: str
    parent: int                                   # -1 for a root
    position: Tuple[float, float, float]
    rotation: Tuple[float, float, float, float]   # quaternion x, y, z, w
    pose_to_bone: Tuple[float, ...] = ()          # 3x4 row-major, model -> bone
    flags: int = 0

    @property
    def is_root(self) -> bool:
        return self.parent < 0


@dataclass
class Mesh:
    """One drawable chunk: a triangle list sharing a single material."""

    material: str = ""
    material_index: int = -1
    body_part: str = ""
    positions: array = field(default_factory=lambda: array("f"))
    normals: array = field(default_factory=lambda: array("f"))
    uvs: array = field(default_factory=lambda: array("f"))
    bone_indices: array = field(default_factory=lambda: array("B"))
    bone_weights: array = field(default_factory=lambda: array("f"))
    indices: array = field(default_factory=lambda: array("I"))

    @property
    def vertex_count(self) -> int:
        return len(self.positions) // 3

    @property
    def triangle_count(self) -> int:
        return len(self.indices) // 3

    def bounds(self) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        """Axis-aligned bounds of this mesh, or zeros when it is empty."""
        if not self.positions:
            return (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)
        xs = self.positions[0::3]
        ys = self.positions[1::3]
        zs = self.positions[2::3]
        return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))

    def __repr__(self) -> str:
        return f"<Mesh {self.material!r} {self.vertex_count} verts, {self.triangle_count} tris>"


@dataclass
class ModelInfo:
    """Header facts worth showing before anything is drawn."""

    name: str = ""
    version: int = 0
    checksum: int = 0
    flags: int = 0
    bone_count: int = 0
    mesh_count: int = 0
    lod_count: int = 1
    #: the body group selection this model was built with
    body: int = 0
    #: The *movement* hull the engine collides with, in game space. It is not
    #: the size of the geometry and routinely disagrees with it - measured over
    #: 271 shipped models, the mesh fits inside this box in 5% of cases. Use
    #: Model.bounds() to frame or scale anything.
    hull_min: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    hull_max: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    eye_position: Tuple[float, float, float] = (0.0, 0.0, 0.0)


@dataclass
class Model:
    """A Source model: skeleton, geometry and the materials it asks for."""

    info: ModelInfo = field(default_factory=ModelInfo)
    bones: List[Bone] = field(default_factory=list)
    meshes: List[Mesh] = field(default_factory=list)
    #: material names as written in the model, without a path
    material_names: List[str] = field(default_factory=list)
    #: folders to search for those materials, from the model's cdtextures
    material_dirs: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.info.name

    @property
    def vertex_count(self) -> int:
        return sum(m.vertex_count for m in self.meshes)

    @property
    def triangle_count(self) -> int:
        return sum(m.triangle_count for m in self.meshes)

    def __bool__(self) -> bool:
        return bool(self.meshes)

    def bounds(self) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        """Bounds of the actual geometry, or zeros when there is none.

        Deliberately does not fall back to the header hull: that is a collision
        box in game space and usually a different shape entirely, so returning
        it here would quietly mis-frame every model that has no mesh.
        """
        boxes = [m.bounds() for m in self.meshes if m.positions]
        if not boxes:
            return (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)
        lows = [b[0] for b in boxes]
        highs = [b[1] for b in boxes]
        return (
            (min(p[0] for p in lows), min(p[1] for p in lows), min(p[2] for p in lows)),
            (max(p[0] for p in highs), max(p[1] for p in highs), max(p[2] for p in highs)),
        )

    def bone_map(self) -> Dict[str, int]:
        return {bone.name: i for i, bone in enumerate(self.bones)}

    def material_candidates(self, material: str) -> List[str]:
        """Content-relative paths to try for a material, best first.

        A model names a material and separately lists the folders it may live in,
        so resolving one means trying each folder in order.
        """
        material = material.replace("\\", "/").strip("/")
        if not material:
            return []
        out: List[str] = []
        for folder in self.material_dirs:
            folder = folder.replace("\\", "/").strip("/")
            candidate = f"materials/{folder}/{material}.vmt" if folder else f"materials/{material}.vmt"
            if candidate not in out:
                out.append(candidate)
        fallback = f"materials/{material}.vmt"
        if fallback not in out:
            out.append(fallback)
        return out

    def summary(self) -> str:
        return (f"{self.info.name or '<unnamed>'} v{self.info.version}: "
                f"{len(self.bones)} bones, {len(self.meshes)} meshes, "
                f"{self.vertex_count} verts, {self.triangle_count} tris")

    def __repr__(self) -> str:
        return f"<Model {self.summary()}>"
