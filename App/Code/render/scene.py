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

from array import array
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Protocol, Tuple

from Core.API.material import Material
from Core.API.model import Mesh, Model
from Core.API.material import as_bool, as_float, as_vec
from Core.API.session import FilmClip, GameModel, ProjectedLight
from Core.Code.formats import FormatError, load_material, load_model, parse_vtf
from Core.Code.formats.bsp import (EMIT_POINT, EMIT_SKYLIGHT, EMIT_SPOTLIGHT, BspFile, WorldLight, map_path,
                                   parse_bsp)
from Core.Code.formats.vtf import VtfFile
from Core.Code.flex import controller_values, morph, run_rules
from Core.Code.pose import skin_matrices
from Core.Code.transform import (IDENTITY as IDENTITY34, Mat34, apply, apply_direction, matrix_from,
                                 quaternion_from_angles, to_column_major_4x4)

from .math3d import IDENTITY, Mat4

__all__ = ["DrawItem", "LoadedModel", "SceneInstance", "Scene", "build_scene", "build_shot_scene",
           "refresh_shot_scene", "SceneSource"]


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
    # Source's VertexLitGeneric look, straight from the .vmt
    halflambert: bool = False
    phong: bool = False
    phong_exponent: float = 5.0
    phong_boost: float = 1.0
    #: $phongfresnelranges: specular at normal incidence, grazing and in between
    fresnel: Tuple[float, float, float] = (0.0, 0.5, 1.0)
    rim: bool = False
    rim_exponent: float = 4.0
    rim_boost: float = 1.0
    self_illum: bool = False
    #: key into Scene.textures for $lightwarptexture, or ""
    lightwarp_key: str = ""
    #: a map face: draw with the lightmap atlas
    lightmapped: bool = False

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
    visible: bool = True
    #: the map's light at this instance: its ambient cube (six RGB, +x -x +y -y +z -z) and the
    #: sun and nearest world lights - None on a scene without a map
    ambient_cube: Optional[Tuple[Tuple[float, float, float], ...]] = None
    map_lights: List["LightState"] = field(default_factory=list)
    #: morphed (positions, normals) by item index, for meshes a face moved
    morphs: Dict[int, Tuple[array, array]] = field(default_factory=dict)
    #: bumped whenever `morphs` changes, so the renderer knows to re-upload
    morph_version: int = 0

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
        for index, item in enumerate(self.loaded.items):
            mesh = item.mesh
            positions = mesh.positions
            count = mesh.vertex_count
            step = max(1, count // 400)
            morphed = self.morphs.get(index)
            if morphed is not None:
                positions = morphed[0]
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


# how a LightState lights: the session's projected frustum, or the map's point / spot / sun
LIGHT_PROJECTED, LIGHT_POINT, LIGHT_SPOT, LIGHT_SUN = 0, 1, 2, 3


@dataclass
class LightState:
    """A light, world-placed for the current time: a session light or one of the map's."""
    position: Tuple[float, float, float]
    direction: Tuple[float, float, float]           # the way it shines, unit
    color: Tuple[float, float, float]               # colour x intensity
    attenuation: Tuple[float, float, float]         # constant, linear, quadratic (Source's inverse form)
    near: float
    far: float
    fade_from: float                                # farZAtten: fades to nothing at `far`
    cone_cos: float                                 # cos of the half-angle of the frustum
    ambient: float = 0.0
    source: Optional[ProjectedLight] = None
    kind: int = LIGHT_PROJECTED
    cone_inner_cos: float = 1.0                     # spot: full inside this, off beyond cone_cos


@dataclass
class Scene:
    instances: List[SceneInstance] = field(default_factory=list)
    #: the session's projected lights, updated with the pose
    lights: List[LightState] = field(default_factory=list)
    #: the map's lightmaps packed into one RGB image: (width, height, bytes)
    lightmap_atlas: Optional[Tuple[int, int, bytes]] = None
    #: the map, kept for light lookups as instances move
    bsp: Optional[BspFile] = None
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
        boxes = [i.bounds() for i in self.instances if i.visible]
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


def build_shot_scene(source: SceneSource, shot: FilmClip, map_name: str = "") -> Scene:
    """Every visible game model of a shot, placed and posed as the session says,
    on the map the shot (or, failing that, `map_name` - the sequence's) names.
    A model that cannot be read is a warning; the shot still shows."""
    scene = Scene(title=shot.name, up_axis="z")
    if shot.scene is None:
        scene.warnings.append("the shot has no scene")
        return scene
    map_name = shot.map_name or map_name
    if map_name:
        _load_map(source, scene, map_name)
    for node, world, visible in shot.scene.walk_visibility():
        if isinstance(node, ProjectedLight):
            if visible:
                scene.lights.append(_light_state(node, world))
            continue
        if not isinstance(node, GameModel):
            continue
        rel = node.model_name
        if not rel or rel.startswith("*"):
            continue                              # a map brush, not a file
        try:
            loaded = _load(source, scene, rel, 0, node.body)
        except FormatError as exc:
            scene.warnings.append(f"{node.name}: {exc}")
            continue
        bones = skin_matrices(loaded.model, node.bones) if loaded.model.bones else []
        instance = SceneInstance(
            loaded, name=node.name, world=to_column_major_4x4(world), bones=bones,
            source=node, visible=visible)
        _apply_face(instance)
        _map_light(scene, instance, apply(world, (0.0, 0.0, 0.0)))
        scene.instances.append(instance)
    if not scene.instances and not scene.warnings:
        scene.warnings.append("the shot has no game models")
    return scene


def _load_map(source: SceneSource, scene: Scene, name: str) -> None:
    """The shot's map: the world's faces as one model (a mesh per material) and the
    static props as instances.  A missing map is a warning, as SFM's own message is."""
    rel = map_path(name)
    data = source.read_bytes(rel)
    if data is None:
        scene.warnings.append(f"map {rel} not found")
        return
    try:
        bsp = parse_bsp(data, rel)
    except FormatError as exc:
        scene.warnings.append(str(exc))
        return
    scene.warnings.extend(f"{rel}: {w}" for w in bsp.warnings)
    scene.bsp = bsp
    pak = bsp.pak_files()
    if pak:
        source = _WithPak(source, pak)                # the map's own materials come first
    world = Model()
    world.info.name = rel
    world.material_dirs = [""]
    atlas = _LightmapAtlas()
    by_material: Dict[str, Mesh] = {}
    for face in bsp.faces:
        mesh = by_material.get(face.material)
        if mesh is None:
            mesh = by_material[face.material] = Mesh(material=face.material)
        base = mesh.vertex_count
        n = face.normal
        place = atlas.place(face.lightmap) if face.lightmap is not None else None
        for k, (p, uv) in enumerate(zip(face.positions, face.uvs)):
            mesh.positions.extend(p)
            mesh.normals.extend(n)
            mesh.uvs.extend(uv)
            if place is not None and k < len(face.lightmap_uvs):
                s, t = face.lightmap_uvs[k]
                mesh.lightmap_uvs.extend(place(s, t))
            else:
                mesh.lightmap_uvs.extend((0.0, 0.0))
        mesh.indices.extend(base + i for i in face.indices)
    world.meshes = list(by_material.values())
    scene.lightmap_atlas = atlas.image()
    loaded = LoadedModel(rel=rel, model=world)
    for mesh in world.meshes:
        item = _item_for(source, scene, world, mesh)
        item.lit = True
        item.lightmapped = scene.lightmap_atlas is not None
        item.two_sided = True                         # brush winding is not the model convention
        loaded.items.append(item)
    loaded.items.sort(key=lambda item: item.blended)
    scene.models[rel] = loaded
    scene.instances.append(SceneInstance(loaded, name=rel, world=to_column_major_4x4(IDENTITY34)))
    for prop in bsp.static_props:
        try:
            prop_model = _load(source, scene, prop.model, 0, 0)
        except FormatError as exc:
            scene.warnings.append(f"{prop.model}: {exc}")
            continue
        pitch, yaw, roll = prop.angles
        placement = matrix_from(prop.origin, quaternion_from_angles(pitch, yaw, roll))
        # a static prop stays in its bind pose: no skin to upload, positions are used as stored
        instance = SceneInstance(prop_model, name=f"prop_static {prop.model}", world=to_column_major_4x4(placement))
        _map_light(scene, instance, prop.origin)
        scene.instances.append(instance)


def _map_light(scene: Scene, instance: SceneInstance, point) -> None:
    """The map's light at a point, cached until the instance moves more than a few units."""
    bsp = scene.bsp
    if bsp is None:
        return
    cached = getattr(instance, "_light_point", None)
    if cached is not None and sum((cached[a] - point[a]) ** 2 for a in range(3)) < 16.0:
        return
    instance._light_point = point
    cube = bsp.ambient_at(point)
    if cube is None:
        # inside something solid, or a map without ambient data: use the sky's ambient dimmed
        sky = bsp.sky_ambient
        cube = tuple(tuple(v * 0.5 for v in sky) for _ in range(6)) if sky is not None else None
    instance.ambient_cube = cube
    lights: List[LightState] = []
    sky_ambient = bsp.sky_ambient
    for light in bsp.lights_at(point):
        if light.kind == EMIT_SKYLIGHT:
            # no sky trace yet: the ambient's brightness says how much of the sky the point sees
            weight = 1.0
            if cube is not None and sky_ambient is not None and sum(sky_ambient) > 1e-6:
                # the brightest face of the cube against the sky's own ambient: open sky gives ~1
                brightest = max(sum(f) for f in cube)
                weight = min(1.0, brightest / sum(sky_ambient))
            n = light.normal
            lights.append(LightState(point, n, tuple(v * weight for v in light.intensity), (1.0, 0.0, 0.0),
                                     0.0, 1e9, 1e9, -1.0, kind=LIGHT_SUN))
        elif light.kind == EMIT_SPOTLIGHT:
            lights.append(LightState(light.origin, light.normal, light.intensity, light.attenuation,
                                     0.0, 1e9, 1e9, light.stopdot2, kind=LIGHT_SPOT, cone_inner_cos=light.stopdot))
        else:
            lights.append(LightState(light.origin, (0.0, 0.0, 1.0), light.intensity, light.attenuation,
                                     0.0, 1e9, 1e9, -1.0, kind=LIGHT_POINT))
    instance.map_lights = lights


class _LightmapAtlas:
    """Every face's lightmap side by side in one image, a pixel of padding around
    each so filtering never bleeds a neighbour in.  Rows of the tallest block."""

    WIDTH = 2048

    def __init__(self) -> None:
        self.blocks: List[Tuple[int, int, int, int, bytes]] = []      # x, y, w, h, data
        self.x = 1
        self.y = 1
        self.row_h = 0
        self.height = 0

    def place(self, lightmap: Tuple[int, int, bytes]):
        w, h, data = lightmap
        if self.x + w + 1 > self.WIDTH:
            self.x = 1
            self.y += self.row_h + 1
            self.row_h = 0
        x, y = self.x, self.y
        self.blocks.append((x, y, w, h, data))
        self.x += w + 1
        self.row_h = max(self.row_h, h)
        self.height = max(self.height, y + h + 1)

        def uv(s: float, t: float, x=x, y=y, w=w, h=h):
            # luxel s in [0, w-1] sits at its centre: (x + s + 0.5) / atlas width
            s = min(max(s, 0.0), w - 1)
            t = min(max(t, 0.0), h - 1)
            return (x + s + 0.5) / self.WIDTH, (y + t + 0.5) / max(1, self.final_height)
        return uv

    @property
    def final_height(self) -> int:
        return 1 << max(1, (self.height - 1).bit_length())

    def image(self) -> Optional[Tuple[int, int, bytes]]:
        if not self.blocks:
            return None
        height = self.final_height
        stride = self.WIDTH * 3
        out = bytearray(stride * height)
        for x, y, w, h, data in self.blocks:
            for row in range(h):
                at = (y + row) * stride + x * 3
                out[at:at + w * 3] = data[row * w * 3:(row + 1) * w * 3]
        return self.WIDTH, height, bytes(out)


class _WithPak:
    """A content source with a map's embedded files in front of it."""

    def __init__(self, source: SceneSource, files: Dict[str, bytes]) -> None:
        self._source = source
        self._files = files

    def read_bytes(self, rel: str) -> Optional[bytes]:
        data = self._files.get(rel.replace("\\", "/").lower())
        return data if data is not None else self._source.read_bytes(rel)

    def read_text(self, rel: str) -> Optional[str]:
        data = self._files.get(rel.replace("\\", "/").lower())
        if data is not None:
            return data.decode("utf-8", "replace")
        return self._source.read_text(rel)


def refresh_shot_scene(scene: Scene, shot: FilmClip) -> None:
    """Re-read every instance's transform, pose and visibility from the
    session - what to do after the session was evaluated at a new time."""
    if shot.scene is None:
        return
    state = {}
    lights = []
    for node, world, visible in shot.scene.walk_visibility():
        if isinstance(node, GameModel):
            state[node.element] = (world, visible)
        elif isinstance(node, ProjectedLight) and visible:
            lights.append(_light_state(node, world))
    scene.lights = lights
    for instance in scene.instances:
        if instance.source is None:
            continue
        found = state.get(instance.source.element)
        if found is None:
            instance.visible = False
            continue
        world, visible = found
        instance.world = to_column_major_4x4(world)
        instance.visible = visible
        if instance.model.bones:
            instance.bones = skin_matrices(instance.model, instance.source.bones)
        if visible:
            _apply_face(instance)
            _map_light(scene, instance, apply(world, (0.0, 0.0, 0.0)))


def _apply_face(instance: SceneInstance) -> None:
    """Move the face meshes to the session's control values."""
    model = instance.model
    if not model.has_flexes or instance.source is None:
        return
    weights = run_rules(model, controller_values(model, instance.source.flex_values()))
    morphs: Dict[int, Tuple[array, array]] = {}
    for index, item in enumerate(instance.items):
        if item.mesh.flexes:
            result = morph(item.mesh, weights)
            if result is not None:
                morphs[index] = result
    instance.morphs = morphs
    instance.morph_version += 1


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
    _shading(item, material)
    for warning in material.warnings:
        scene.warnings.append(f"{material.path}: {warning}")

    warp = material.texture("$lightwarptexture")
    if warp and _texture(source, scene, warp):
        item.lightwarp_key = warp
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


def _texture(source: SceneSource, scene: Scene, key: str) -> bool:
    """Parse a texture into the scene once; False when it cannot be read."""
    if key in scene.textures:
        return True
    data = source.read_bytes(key)
    if data is None:
        scene.warnings.append(f"texture {key} not found")
        return False
    try:
        vtf = parse_vtf(data, key)
    except FormatError as exc:
        scene.warnings.append(str(exc))
        return False
    if not vtf.mips:
        return False
    scene.textures[key] = vtf
    return True


def _shading(item: DrawItem, material: Material) -> None:
    """VertexLitGeneric's lighting parameters, with the engine's defaults."""
    item.halflambert = as_bool(material.param("$halflambert"))
    item.phong = as_bool(material.param("$phong"))
    item.phong_exponent = as_float(material.param("$phongexponent"), 5.0)
    item.phong_boost = as_float(material.param("$phongboost"), 1.0)
    ranges = as_vec(material.param("$phongfresnelranges"))
    if len(ranges) >= 3:
        item.fresnel = (ranges[0], ranges[1], ranges[2])
    item.rim = as_bool(material.param("$rimlight"))
    item.rim_exponent = as_float(material.param("$rimlightexponent"), 4.0)
    item.rim_boost = as_float(material.param("$rimlightboost"), 1.0)
    item.self_illum = material.self_illum


def _light_state(light: ProjectedLight, world: Mat34) -> LightState:
    import math
    position = apply(world, (0.0, 0.0, 0.0))
    forward = apply_direction(world, (1.0, 0.0, 0.0))     # Source lights shine along their +X
    n = math.sqrt(sum(v * v for v in forward)) or 1.0
    forward = (forward[0] / n, forward[1] / n, forward[2] / n)
    r, g, b = light.color
    k = light.intensity
    half = math.radians(max(light.horizontal_fov, light.vertical_fov) / 2.0)
    return LightState(position, forward, (r * k, g * k, b * k), light.attenuation,
                      light.min_distance, light.max_distance, min(light.far_z_atten, light.max_distance),
                      math.cos(half), light.ambient_intensity, light)


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
