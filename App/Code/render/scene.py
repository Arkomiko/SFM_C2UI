"""
From loaded content to a list of things to draw.

A scene is a set of *instances*: a model placed somewhere, in some pose. The
model browser shows one instance at the origin in its bind pose; a shot of a
session shows every game model in its scene DAG, each with its world matrix
and the bone transforms the session stored for it.

Models and textures are loaded once per scene however many instances share
them. Nothing here touches OpenGL, which keeps it testable with fake content.

    scene = build_scene(library, "models/player/scout.mdl")
    scene = build_shot_scene(library, shot)          # a FilmClip from a session
    for instance in scene.instances:
        instance.items, instance.world, instance.bones
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Protocol, Tuple

from Core.API.material import Material
from Core.API.model import Mesh, Model
from Core.API.session import FilmClip, GameModel
from Core.Code.formats import FormatError, load_material, load_model, parse_vtf
from Core.Code.formats.vtf import VtfFile
from Core.Code.pose import skin_matrices
from Core.Code.transform import IDENTITY as IDENTITY34, Mat34, apply, to_column_major_4x4

from .math3d import IDENTITY, Mat4

__all__ = ["DrawItem", "LoadedModel", "SceneInstance", "Scene", "build_scene", "build_shot_scene",
           "SceneSource"]


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
class LoadedModel:
    """A model and its draw items, shared by every instance of it."""
    rel: str
    model: Model
    items: List[DrawItem] = field(default_factory=list)


@dataclass
class SceneInstance:
    loaded: LoadedModel
    #: a label for the UI - the game model's name in a session
    name: str = ""
    #: model space to world, column-major 4x4
    world: Mat4 = IDENTITY
    #: one 3x4 skinning matrix per bone, or empty for the bind pose
    bones: List[Mat34] = field(default_factory=list)
    #: the session element this came from, when any
    source: Optional[GameModel] = None

    @property
    def model(self) -> Model:
        return self.loaded.model

    @property
    def items(self) -> List[DrawItem]:
        return self.loaded.items

    def bounds(self):
        """World-space bounds of the posed geometry, sampled from the vertices."""
        lo = [float("inf")] * 3
        hi = [float("-inf")] * 3
        m = self.loaded.model
        world34 = _to_34(self.world)
        for mesh in m.meshes:
            positions = mesh.positions
            count = mesh.vertex_count
            step = max(1, count // 400)
            for v in range(0, count, step):
                p = (positions[v * 3], positions[v * 3 + 1], positions[v * 3 + 2])
                if self.bones:
                    p = _skin_point(mesh, v, p, self.bones)
                p = apply(world34, p)
                for a in range(3):
                    if p[a] < lo[a]:
                        lo[a] = p[a]
                    if p[a] > hi[a]:
                        hi[a] = p[a]
        if lo[0] == float("inf"):
            return (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)
        return tuple(lo), tuple(hi)


@dataclass
class Scene:
    instances: List[SceneInstance] = field(default_factory=list)
    #: models by content path, each loaded once
    models: Dict[str, LoadedModel] = field(default_factory=dict)
    #: textures by content path, each parsed once however many meshes use it
    textures: Dict[str, VtfFile] = field(default_factory=dict)
    #: materials by content path
    materials: Dict[str, Material] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    #: what the scene is: a model path or a shot name
    title: str = ""
    #: world up axis when known ("z" for a session), else "" to guess
    up_axis: str = ""

    @property
    def model(self) -> Optional[Model]:
        """The single model of a one-model scene, for the model browser."""
        return self.instances[0].model if len(self.instances) == 1 else None

    @property
    def items(self) -> List[DrawItem]:
        return [item for instance in self.instances for item in instance.items]

    @property
    def bounds(self):
        boxes = [i.bounds() for i in self.instances]
        boxes = [b for b in boxes if b[0] != b[1]]
        if not boxes:
            return (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)
        return (tuple(min(b[0][a] for b in boxes) for a in range(3)),
                tuple(max(b[1][a] for b in boxes) for a in range(3)))

    def summary(self) -> str:
        textured = sum(1 for i in self.items if i.texture_key)
        verts = sum(i.model.vertex_count for i in self.instances)
        tris = sum(i.model.triangle_count for i in self.instances)
        return (f"{self.title}: {len(self.instances)} instances of {len(self.models)} models, "
                f"{verts} verts, {tris} tris; {len(self.items)} draw items, {textured} textured, "
                f"{len(self.textures)} textures, {len(self.warnings)} warnings")


# ---------------------------------------------------------------------------
#  Builders
# ---------------------------------------------------------------------------
def build_scene(source: SceneSource, rel: str, lod: int = 0) -> Scene:
    """One model at the origin in its bind pose.  Raises FormatError only when
    the model itself cannot be read; a missing material or texture becomes a
    warning and an untextured item."""
    scene = Scene(title=rel)
    loaded = _load(source, scene, rel, lod, 0)
    scene.instances.append(SceneInstance(loaded, name=rel))
    return scene


def build_shot_scene(source: SceneSource, shot: FilmClip) -> Scene:
    """Every visible game model of a shot, placed and posed as the session says.
    A model that cannot be read is a warning; the shot still shows."""
    scene = Scene(title=shot.name, up_axis="z")
    for game_model, world in shot.game_models():
        rel = game_model.model_name
        if not rel:
            continue
        try:
            loaded = _load(source, scene, rel, 0, game_model.body)
        except FormatError as exc:
            scene.warnings.append(f"{game_model.name}: {exc}")
            continue
        bones = skin_matrices(loaded.model, game_model.bones) if loaded.model.bones else []
        scene.instances.append(SceneInstance(
            loaded, name=game_model.name, world=to_column_major_4x4(world), bones=bones,
            source=game_model))
    if not scene.instances and not scene.warnings:
        scene.warnings.append("the shot has no visible game models")
    return scene


def _load(source: SceneSource, scene: Scene, rel: str, lod: int, body: int) -> LoadedModel:
    key = rel.replace("\\", "/").lower()
    if body:
        key = f"{key}#{body}"                     # a different body group choice is a different mesh set
    loaded = scene.models.get(key)
    if loaded is not None:
        return loaded
    model = load_model(source, rel, lod, body)
    loaded = LoadedModel(rel=key, model=model)
    scene.warnings.extend(f"{key}: {w}" for w in model.warnings)
    for mesh in model.meshes:
        loaded.items.append(_item_for(source, scene, model, mesh))
    # opaque first, then blended surfaces (which rely on what is already drawn)
    loaded.items.sort(key=lambda item: item.blended)
    scene.models[key] = loaded
    return loaded


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


# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------
def _to_34(m: Mat4) -> Mat34:
    return (m[0], m[4], m[8], m[12],
            m[1], m[5], m[9], m[13],
            m[2], m[6], m[10], m[14])


def _skin_point(mesh: Mesh, v: int, p, bones: List[Mat34]):
    indices = mesh.bone_indices
    weights = mesh.bone_weights
    out = [0.0, 0.0, 0.0]
    total = 0.0
    for k in range(3):
        w = weights[v * 3 + k] if v * 3 + k < len(weights) else 0.0
        if w <= 0.0:
            continue
        index = indices[v * 3 + k] if v * 3 + k < len(indices) else 0
        if index >= len(bones):
            continue
        q = apply(bones[index], p)
        out[0] += w * q[0]
        out[1] += w * q[1]
        out[2] += w * q[2]
        total += w
    if total <= 0.0:
        return p
    return (out[0] / total, out[1] / total, out[2] / total)
