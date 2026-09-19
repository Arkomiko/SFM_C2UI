"""
From a loaded model to a list of things to draw.

This is the step between the format readers and the GPU: every mesh gets its
material resolved through the model's own search folders, every material its
texture, and the result is a flat list of draw items sorted so that opaque
surfaces come first and translucent ones after. Nothing here touches OpenGL,
which keeps it testable with fake content.

    scene = build_scene(library, "models/player/scout.mdl")
    for item in scene.items:
        item.mesh, item.material, item.texture_key
    scene.textures[key]                 # VtfFile, shared between items
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Protocol, Tuple

from Core.API.material import Material
from Core.API.model import Mesh, Model
from Core.Code.formats import FormatError, load_material, load_model, parse_vtf
from Core.Code.formats.vtf import VtfFile

__all__ = ["DrawItem", "Scene", "build_scene", "SceneSource"]


class SceneSource(Protocol):
    def read_bytes(self, rel: str) -> Optional[bytes]: ...
    def read_text(self, rel: str) -> Optional[str]: ...


@dataclass
class DrawItem:
    mesh: Mesh
    material: Optional[Material] = None
    #: key into Scene.textures, or "" when the surface has no texture
    texture_key: str = ""
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    alpha: float = 1.0
    translucent: bool = False
    alpha_test: bool = False
    additive: bool = False
    two_sided: bool = False
    #: lit as a model; unlit surfaces are drawn flat
    lit: bool = True

    @property
    def blended(self) -> bool:
        return self.translucent or self.additive


@dataclass
class Scene:
    model: Model
    items: List[DrawItem] = field(default_factory=list)
    #: textures by content path, each parsed once however many meshes use it
    textures: Dict[str, VtfFile] = field(default_factory=dict)
    #: materials by content path
    materials: Dict[str, Material] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)

    @property
    def bounds(self):
        return self.model.bounds()

    def summary(self) -> str:
        textured = sum(1 for i in self.items if i.texture_key)
        return (f"{self.model.summary()}; {len(self.items)} draw items, {textured} textured, "
                f"{len(self.textures)} textures, {len(self.warnings)} warnings")


def build_scene(source: SceneSource, rel: str, lod: int = 0) -> Scene:
    """Load a model and everything needed to draw it.  Raises FormatError
    only when the model itself cannot be read; a missing material or texture
    becomes a warning and an untextured item."""
    model = load_model(source, rel, lod)
    scene = Scene(model=model)
    scene.warnings.extend(model.warnings)
    for mesh in model.meshes:
        scene.items.append(_item_for(source, scene, model, mesh))
    # opaque first, then blended surfaces (which rely on what is already drawn)
    scene.items.sort(key=lambda item: item.blended)
    return scene


def _item_for(source: SceneSource, scene: Scene, model: Model, mesh: Mesh) -> DrawItem:
    item = DrawItem(mesh=mesh)
    material = _resolve_material(source, scene, model, mesh.material)
    if material is None:
        scene.warnings.append(f"no material for {mesh.material!r}")
        return item

    item.material = material
    item.color = material.color
    item.alpha = material.alpha
    item.translucent = material.translucent or material.alpha < 1.0
    item.alpha_test = material.alpha_test
    item.additive = material.additive
    item.two_sided = material.two_sided
    item.lit = material.is_model_shader
    for warning in material.warnings:
        scene.warnings.append(f"{material.path}: {warning}")

    texture = material.base_texture
    if not texture:
        return item
    if texture not in scene.textures:
        data = source.read_bytes(texture)
        if data is None:
            scene.warnings.append(f"{material.path}: texture {texture} not found")
            return item
        try:
            vtf = parse_vtf(data, texture)
        except FormatError as exc:
            scene.warnings.append(str(exc))
            return item
        for warning in vtf.warnings:
            scene.warnings.append(f"{texture}: {warning}")
        if not vtf.mips:
            return item
        scene.textures[texture] = vtf
    item.texture_key = texture
    return item


def _resolve_material(source: SceneSource, scene: Scene, model: Model, name: str) -> Optional[Material]:
    for candidate in model.material_candidates(name):
        if candidate in scene.materials:
            return scene.materials[candidate]
        try:
            material = load_material(source, candidate)
        except ValueError as exc:
            scene.warnings.append(str(exc))
            continue
        if material is not None:
            scene.materials[candidate] = material
            return material
    return None
