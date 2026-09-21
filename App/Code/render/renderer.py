"""
Draws a Scene with a camera into whatever context is current.

The renderer owns the GPU copies of the scene and nothing else: no window, no
events. The viewport widget drives it on screen and the offscreen probe drives
it into an image, which is how the output gets checked without a person
looking at a window.

    renderer = Renderer()
    renderer.initialize()              # once, with a context current
    renderer.set_scene(scene)
    renderer.draw(camera, width, height)
    renderer.release()
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from OpenGL import GL

from .camera import OrbitCamera
from .gl_resources import GLMesh, GLTexture
from .math3d import IDENTITY, multiply, normalize, sub
from .scene import DrawItem, Scene, SceneInstance
from .shaders import (ID_FRAG, LINE_FRAG, LINE_VERT, MAX_BONES, MAX_LIGHTS, MODEL_FRAG, MODEL_VERT,
                      build_program)

__all__ = ["Renderer"]


class Renderer:
    """Draws a Scene with the model, line and id shaders."""
    def __init__(self) -> None:
        self.program = 0
        self.uniforms: Dict[str, int] = {}
        self.scene: Optional[Scene] = None
        #: GPU meshes by model path, in the model's item order
        self.meshes: Dict[str, List[Tuple[DrawItem, GLMesh]]] = {}
        #: per-instance copies of meshes a face moves: (instance id, item index) -> mesh
        self.morphed: Dict[Tuple[int, int], Tuple[GLMesh, int]] = {}
        self.lightmap: Optional[GLTexture] = None
        #: the sky's six faces on the GPU, drawn first around the eye
        self.sky: List[Tuple[DrawItem, GLMesh]] = []
        #: per-instance uniform arrays, rebuilt when the placement or skin objects change
        self._instance_cache: Dict[int, tuple] = {}
        self._light_cache: Dict[tuple, tuple] = {}
        self._lights_key = None
        self._bounds_cache: Dict[int, tuple] = {}
        self.drawn_instances = 0
        self._item_state = None
        self._int_state: Dict[str, int] = {}
        self.textures: Dict[str, GLTexture] = {}
        self.background = (0.16, 0.17, 0.19, 1.0)
        self.line_program = 0
        self.id_program = 0
        self._line_vao = 0
        self._line_vbo = 0
        #: line segments to draw over the scene: [(a, b, (r, g, b, a)), ...]
        self.overlay_lines: List[Tuple[Tuple[float, float, float], Tuple[float, float, float],
                                       Tuple[float, float, float, float]]] = []
        self.model_matrix = IDENTITY
        self.wireframe = False
        #: Source winds triangles clockwise when seen from outside
        self.front_face_ccw = False
        self.errors: List[str] = []

    # -- lifecycle -----------------------------------------------------------------
    def initialize(self) -> None:
        """Compile the shaders and look up their uniforms; needs a current context."""
        self.program = build_program(MODEL_VERT, MODEL_FRAG)
        for name in ("u_view_proj", "u_model", "u_skinned", "u_bones", "u_texture", "u_textured",
                     "u_lit", "u_alpha_test", "u_blended", "u_color", "u_alpha", "u_light_dir", "u_eye",
                     "u_lightwarp", "u_halflambert", "u_has_lightwarp", "u_phong", "u_phong_exponent",
                     "u_phong_boost", "u_fresnel", "u_rim", "u_rim_exponent", "u_rim_boost", "u_self_illum",
                     "u_light_count", "u_light_pos", "u_light_dirs", "u_light_color", "u_light_atten",
                     "u_light_range", "u_ambient", "u_lightmap", "u_lightmapped", "u_light_kind",
                     "u_ambient_cube", "u_has_cube"):
            self.uniforms[name] = GL.glGetUniformLocation(self.program, name)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthFunc(GL.GL_LEQUAL)
        self.line_program = build_program(LINE_VERT, LINE_FRAG)
        self.id_program = build_program(MODEL_VERT, ID_FRAG)
        self._line_vao = int(GL.glGenVertexArrays(1))
        self._line_vbo = int(GL.glGenBuffers(1))
        GL.glBindVertexArray(self._line_vao)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._line_vbo)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
        GL.glBindVertexArray(0)

    def set_scene(self, scene: Optional[Scene]) -> None:
        """Upload a scene's meshes and textures, releasing the previous one."""
        self._release_scene()
        self.scene = scene
        if scene is None:
            return
        for key, vtf in scene.textures.items():
            try:
                self.textures[key] = GLTexture(vtf, key)
            except Exception as exc:                        # noqa: BLE001 - driver errors vary
                self.errors.append(f"texture {key}: {exc}")
        if scene.lightmap_atlas is not None:
            try:
                self.lightmap = GLTexture(None, "lightmap", rgb=scene.lightmap_atlas)
                self.lightmap.set_clamp()
            except Exception as exc:                        # noqa: BLE001
                self.errors.append(f"lightmap atlas: {exc}")
        for key, loaded in scene.models.items():
            self.meshes[key] = [(item, GLMesh(item.mesh)) for item in loaded.items
                                if item.mesh.indices]
        if scene.sky is not None:
            self.sky = [(item, GLMesh(item.mesh)) for item in scene.sky.items if item.mesh.indices]
            for item, _mesh in self.sky:
                texture = self.textures.get(item.texture_key)
                if texture is not None:
                    texture.set_clamp()               # the sides' lower half repeats the horizon row
        for instance in scene.instances:
            if len(instance.bones) > MAX_BONES:
                self.errors.append(f"{instance.name}: {len(instance.bones)} bones, only "
                                   f"{MAX_BONES} can be posed; the rest stay in bind pose")

    def _release_scene(self) -> None:
        for meshes in self.meshes.values():
            for _item, mesh in meshes:
                mesh.release()
        for mesh, _version in self.morphed.values():
            mesh.release()
        self.morphed = {}
        for texture in self.textures.values():
            texture.release()
        if self.lightmap is not None:
            self.lightmap.release()
            self.lightmap = None
        for _item, mesh in self.sky:
            mesh.release()
        self.sky = []
        self.meshes = {}
        self.textures = {}
        self.scene = None

    def release(self) -> None:
        """Free every GPU object."""
        self._release_scene()
        for name in ("program", "line_program", "id_program"):
            if getattr(self, name):
                GL.glDeleteProgram(getattr(self, name))
                setattr(self, name, 0)
        if self._line_vao:
            GL.glDeleteVertexArrays(1, [self._line_vao])
            GL.glDeleteBuffers(1, [self._line_vbo])
            self._line_vao = self._line_vbo = 0

    # -- drawing -----------------------------------------------------------------
    def draw(self, camera: OrbitCamera, width: int, height: int) -> None:
        """Draw the scene from `camera` into a width x height viewport."""
        GL.glViewport(0, 0, max(1, width), max(1, height))
        GL.glClearColor(*self.background)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        if self.scene is None or not self.meshes or not self.program:
            return

        view = camera.view()
        projection = camera.projection(width / max(1, height))
        view_proj = multiply(projection, view)
        eye = camera.eye()
        # key light a little above and to the side of the camera
        light = normalize(sub(eye, camera.target))
        light = normalize((light[0] + camera.up[0] * 0.5, light[1] + camera.up[1] * 0.5,
                           light[2] + camera.up[2] * 0.5))

        u = self.uniforms
        GL.glUseProgram(self.program)
        GL.glUniformMatrix4fv(u["u_view_proj"], 1, GL.GL_FALSE, view_proj)
        GL.glUniform3f(u["u_light_dir"], *light)
        GL.glUniform3f(u["u_eye"], *eye)
        GL.glUniform1i(u["u_texture"], 0)
        GL.glUniform1i(u["u_lightwarp"], 1)
        GL.glUniform1i(u["u_lightmap"], 2)
        self._lights_key = None
        if self.lightmap is not None:
            self.lightmap.bind(2)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE if self.wireframe else GL.GL_FILL)
        GL.glFrontFace(GL.GL_CCW if self.front_face_ccw else GL.GL_CW)
        self._item_state = None
        self._int_state = {}
        if self.sky and not self.wireframe:
            self._draw_sky(camera, eye)
        if len(self._instance_cache) > 4 * max(1, len(self.scene.instances)):
            self._instance_cache = {}             # instances came and went: start over
            self._bounds_cache = {}

        # what the camera cannot see is not drawn: a map is mostly out of view at any moment
        planes = frustum_planes(view_proj)
        shown = []
        for instance in self.scene.instances:
            if not instance.visible:
                continue
            if instance.source is None and not instance.bones:
                box = self._static_bounds(instance)
                if box is not None and not box_in_frustum(box, planes):
                    continue
            shown.append(instance)
        self.drawn_instances = len(shown)

        # opaque surfaces of every instance first, then the blended ones over them
        for blended in (False, True):
            for instance in shown:
                meshes = self.meshes.get(instance.loaded.rel, [])
                if not any(item.blended == blended for item, _m in meshes):
                    continue
                self._apply_instance(instance)
                self._apply_lights(instance)
                for index, (item, mesh) in enumerate(meshes):
                    if item.blended != blended:
                        continue
                    if index in instance.morphs:
                        mesh = self._morphed_mesh(instance, index, item)
                    self._apply_state(item)
                    texture = self.textures.get(item.texture_key)
                    if texture is not None:
                        texture.bind(0)
                    self._set_int("u_textured", 1 if texture is not None else 0)
                    mesh.draw()

        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glDisable(GL.GL_BLEND)
        GL.glDepthMask(GL.GL_TRUE)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glUseProgram(0)
        if self.overlay_lines:
            self._draw_lines(view_proj)

    def _draw_sky(self, camera: OrbitCamera, eye) -> None:
        """The sky: the unit cube's six faces scaled to sit inside the far plane and
        centred on the eye, drawn unlit with depth off so everything else paints
        over them - the map's own sky brushes were dropped by the reader."""
        u = self.uniforms
        _near, far = camera.depth_range()
        h = far * 0.5                                # the far corner is at h * sqrt(3) < far
        model = (GL.GLfloat * 16)(h, 0.0, 0.0, 0.0, 0.0, h, 0.0, 0.0, 0.0, 0.0, h, 0.0,
                                  eye[0], eye[1], eye[2], 1.0)
        GL.glUniformMatrix4fv(u["u_model"], 1, GL.GL_FALSE, model)
        self._set_int("u_skinned", 0)
        GL.glDisable(GL.GL_DEPTH_TEST)
        for item, mesh in self.sky:
            self._apply_state(item)
            GL.glDepthMask(GL.GL_FALSE)
            texture = self.textures.get(item.texture_key)
            if texture is not None:
                texture.bind(0)
            self._set_int("u_textured", 1 if texture is not None else 0)
            mesh.draw()
        GL.glDepthMask(GL.GL_TRUE)
        GL.glEnable(GL.GL_DEPTH_TEST)

    def _draw_lines(self, view_proj) -> None:
        """Overlay lines (manipulators), on top of everything."""
        import struct
        GL.glUseProgram(self.line_program)
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.line_program, "u_view_proj"), 1, GL.GL_FALSE, view_proj)
        colour_location = GL.glGetUniformLocation(self.line_program, "u_color")
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glLineWidth(1.0)                      # core profiles allow nothing wider
        GL.glBindVertexArray(self._line_vao)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._line_vbo)
        # group by colour to keep the draw count small
        groups: Dict[Tuple[float, float, float, float], List[float]] = {}
        for a, b, colour in self.overlay_lines:
            groups.setdefault(colour, []).extend((*a, *b))
        for colour, floats in groups.items():
            raw = struct.pack(f"<{len(floats)}f", *floats)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(raw), raw, GL.GL_STREAM_DRAW)
            GL.glUniform4f(colour_location, *colour)
            GL.glDrawArrays(GL.GL_LINES, 0, len(floats) // 3)
        GL.glBindVertexArray(0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(0)

    def draw_ids(self, camera: OrbitCamera, width: int, height: int) -> None:
        """Draw every visible instance in a colour that encodes its index, for
        picking; the caller reads the pixel back with `instance_at`."""
        GL.glViewport(0, 0, max(1, width), max(1, height))
        GL.glClearColor(0.0, 0.0, 0.0, 0.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        if self.scene is None or not self.meshes or not self.id_program:
            return
        view_proj = multiply(camera.projection(width / max(1, height)), camera.view())
        program = self.id_program
        GL.glUseProgram(program)
        loc = lambda name: GL.glGetUniformLocation(program, name)
        GL.glUniformMatrix4fv(loc("u_view_proj"), 1, GL.GL_FALSE, view_proj)
        GL.glUniform1i(loc("u_texture"), 0)
        GL.glFrontFace(GL.GL_CCW if self.front_face_ccw else GL.GL_CW)
        GL.glDisable(GL.GL_BLEND)
        GL.glDepthMask(GL.GL_TRUE)
        for index, instance in enumerate(self.scene.instances):
            if not instance.visible:
                continue
            meshes = self.meshes.get(instance.loaded.rel, [])
            if not meshes:
                continue
            code = index + 1
            GL.glUniform4f(loc("u_color"), (code & 0xFF) / 255.0, ((code >> 8) & 0xFF) / 255.0,
                           ((code >> 16) & 0xFF) / 255.0, 1.0)
            GL.glUniformMatrix4fv(loc("u_model"), 1, GL.GL_FALSE, multiply(self.model_matrix, instance.world))
            if instance.bones:
                rows = []
                for m in instance.bones[:MAX_BONES]:
                    rows.extend(m)
                GL.glUniform4fv(loc("u_bones"), len(rows) // 4, rows)
                GL.glUniform1i(loc("u_skinned"), 1)
            else:
                GL.glUniform1i(loc("u_skinned"), 0)
            for item_index, (item, mesh) in enumerate(meshes):
                if item.two_sided:
                    GL.glDisable(GL.GL_CULL_FACE)
                else:
                    GL.glEnable(GL.GL_CULL_FACE)
                    GL.glCullFace(GL.GL_BACK)
                texture = self.textures.get(item.texture_key)
                if texture is not None:
                    texture.bind(0)
                GL.glUniform1i(loc("u_textured"), 1 if texture is not None else 0)
                GL.glUniform1i(loc("u_alpha_test"), 1 if item.alpha_test else 0)
                if item_index in instance.morphs:
                    mesh = self._morphed_mesh(instance, item_index, item)
                mesh.draw()
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glUseProgram(0)

    def instance_at(self, x: int, y: int, width: int, height: int) -> Optional[SceneInstance]:
        """The instance under a pixel of the id pass just drawn (y from the top)."""
        if self.scene is None:
            return None
        if not (0 <= x < width and 0 <= y < height):
            return None
        GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)
        raw = bytes(GL.glReadPixels(x, height - 1 - y, 1, 1, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE))
        code = raw[0] | (raw[1] << 8) | (raw[2] << 16)
        if code == 0 or code > len(self.scene.instances):
            return None
        return self.scene.instances[code - 1]

    def _morphed_mesh(self, instance: SceneInstance, index: int, item: DrawItem) -> GLMesh:
        key = (id(instance), index)
        entry = self.morphed.get(key)
        if entry is None:
            entry = (GLMesh(item.mesh), -1)
        mesh, version = entry
        if version != instance.morph_version:
            positions, normals = instance.morphs[index]
            mesh.update(positions, normals)
            self.morphed[key] = (mesh, instance.morph_version)
        return mesh

    def _apply_instance(self, instance: SceneInstance) -> None:
        """Upload the instance's placement and skin.  The arrays are built once per
        placement (a static prop keeps its own for the scene's whole life) and handed
        to GL as ctypes, which skips PyOpenGL's per-call conversion - that conversion was
        most of a frame on a map with two thousand props."""
        u = self.uniforms
        cached = self._instance_cache.get(id(instance))
        if cached is None or cached[0] is not instance.world or cached[1] is not instance.bones or cached[2] is not self.model_matrix:
            model = (GL.GLfloat * 16)(*multiply(self.model_matrix, instance.world))
            bones = None
            if instance.bones:
                rows: List[float] = []
                for m in instance.bones[:MAX_BONES]:
                    rows.extend(m)                # three rows of four, as stored
                bones = (GL.GLfloat * len(rows))(*rows)
            cached = (instance.world, instance.bones, self.model_matrix, model, bones)
            self._instance_cache[id(instance)] = cached
        GL.glUniformMatrix4fv(u["u_model"], 1, GL.GL_FALSE, cached[3])
        if cached[4] is not None:
            GL.glUniform4fv(u["u_bones"], len(cached[4]) // 4, cached[4])
            self._set_int("u_skinned", 1)
        else:
            self._set_int("u_skinned", 0)

    def _apply_lights(self, instance: SceneInstance) -> None:
        """The lights on an instance: the session's, then the map's at its place; and the
        map's ambient cube.  Arrays are built once per (lights, cube) pair and reused."""
        u = self.uniforms
        session = self.scene.lights if self.scene is not None else []
        key = (id(session), len(session), id(instance.map_lights), id(instance.ambient_cube))
        if key == self._lights_key:
            return
        self._lights_key = key
        cached = self._light_cache.get(key)
        if cached is None:
            lights = (list(session) + list(instance.map_lights))[:MAX_LIGHTS]
            n = len(lights)
            arrays = None
            if n:
                arrays = ((GL.GLfloat * (3 * n))(*[c for l in lights for c in l.position]),
                          (GL.GLfloat * (3 * n))(*[c for l in lights for c in l.direction]),
                          (GL.GLfloat * (3 * n))(*[c for l in lights for c in l.color]),
                          (GL.GLfloat * (4 * n))(*[c for l in lights for c in (*l.attenuation, l.cone_cos)]),
                          (GL.GLfloat * (3 * n))(*[c for l in lights for c in (l.near, l.fade_from, l.far)]),
                          (GL.GLfloat * (4 * n))(*[c for l in lights for c in (float(l.kind), l.cone_inner_cos, 0.0, 0.0)]))
            ambient = [0.0, 0.0, 0.0]
            if session:
                for l in session:
                    for a in range(3):
                        ambient[a] += l.color[a] * l.ambient
            if instance.ambient_cube is None:
                # no map: a floor so nothing is pitch black
                ambient = [min(0.12 + a, 1.0) for a in ambient]
            cube = None
            if instance.ambient_cube is not None:
                cube = (GL.GLfloat * 18)(*[min(v + a, 1.0) for face in instance.ambient_cube for v, a in zip(face, ambient)])
            cached = (n, arrays, (GL.GLfloat * 3)(*ambient), cube)
            if len(self._light_cache) > 4096:
                self._light_cache = {}
            self._light_cache[key] = cached
        n, arrays, ambient, cube = cached
        GL.glUniform1i(u["u_light_count"], n)
        if arrays is not None:
            GL.glUniform3fv(u["u_light_pos"], n, arrays[0])
            GL.glUniform3fv(u["u_light_dirs"], n, arrays[1])
            GL.glUniform3fv(u["u_light_color"], n, arrays[2])
            GL.glUniform4fv(u["u_light_atten"], n, arrays[3])
            GL.glUniform3fv(u["u_light_range"], n, arrays[4])
            GL.glUniform4fv(u["u_light_kind"], n, arrays[5])
        GL.glUniform3fv(u["u_ambient"], 1, ambient)
        if cube is not None:
            GL.glUniform3fv(u["u_ambient_cube"], 6, cube)
        self._set_int("u_has_cube", 1 if cube is not None else 0)

    def _static_bounds(self, instance: SceneInstance):
        """World bounds of an unskinned instance from its model's box, kept per placement."""
        cached = self._bounds_cache.get(id(instance))
        if cached is not None and cached[0] is instance.world:
            return cached[1]
        lo, hi = instance.loaded.model.bounds()
        if lo == hi:
            box = None
        else:
            w = instance.world
            corners = [(x, y, z) for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]
            pts = [(w[0] * x + w[4] * y + w[8] * z + w[12], w[1] * x + w[5] * y + w[9] * z + w[13],
                    w[2] * x + w[6] * y + w[10] * z + w[14]) for x, y, z in corners]
            box = (tuple(min(p[a] for p in pts) for a in range(3)), tuple(max(p[a] for p in pts) for a in range(3)))
        self._bounds_cache[id(instance)] = (instance.world, box)
        return box

    def _set_int(self, name: str, value: int) -> None:
        if self._int_state.get(name) != value:
            GL.glUniform1i(self.uniforms[name], value)
            self._int_state[name] = value

    def _apply_state(self, item: DrawItem) -> None:
        """Per-surface state, set only when it differs from the last surface drawn."""
        u = self.uniforms
        key = (item.color, item.alpha, item.lit, item.alpha_test, item.blended, item.two_sided, item.additive,
               item.lightmapped, item.halflambert, item.phong, item.phong_exponent, item.phong_boost, item.fresnel, item.rim,
               item.rim_exponent, item.rim_boost, item.self_illum, item.lightwarp_key)
        if key == self._item_state:
            return
        self._item_state = key
        GL.glUniform3f(u["u_color"], *item.color)
        GL.glUniform1f(u["u_alpha"], item.alpha)
        self._set_int("u_lit", 1 if item.lit else 0)
        self._set_int("u_halflambert", 1 if item.halflambert else 0)
        self._set_int("u_phong", 1 if item.phong else 0)
        self._set_int("u_rim", 1 if item.rim else 0)
        self._set_int("u_self_illum", 1 if item.self_illum else 0)
        GL.glUniform1f(u["u_phong_exponent"], item.phong_exponent)
        GL.glUniform1f(u["u_phong_boost"], item.phong_boost)
        GL.glUniform3f(u["u_fresnel"], *item.fresnel)
        GL.glUniform1f(u["u_rim_exponent"], item.rim_exponent)
        GL.glUniform1f(u["u_rim_boost"], item.rim_boost)
        warp = self.textures.get(item.lightwarp_key) if item.lightwarp_key else None
        if warp is not None:
            warp.bind(1)
        self._set_int("u_has_lightwarp", 1 if warp is not None else 0)
        self._set_int("u_lightmapped", 1 if item.lightmapped and self.lightmap is not None else 0)
        self._set_int("u_alpha_test", 1 if item.alpha_test else 0)
        self._set_int("u_blended", 1 if item.blended else 0)
        if item.two_sided:
            GL.glDisable(GL.GL_CULL_FACE)
        else:
            GL.glEnable(GL.GL_CULL_FACE)
            GL.glCullFace(GL.GL_BACK)
        if item.blended:
            GL.glEnable(GL.GL_BLEND)
            if item.additive:
                GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE)
            else:
                GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
            GL.glDepthMask(GL.GL_FALSE)
        else:
            GL.glDisable(GL.GL_BLEND)
            GL.glDepthMask(GL.GL_TRUE)

    def read_pixels(self, width: int, height: int) -> bytes:
        """The framebuffer as RGBA, top row first."""
        GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)
        raw = GL.glReadPixels(0, 0, width, height, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE)
        raw = bytes(raw)
        stride = width * 4
        return b"".join(raw[y * stride:(y + 1) * stride] for y in reversed(range(height)))


def frustum_planes(m):
    """The six planes (a, b, c, d) of a column-major clip matrix; inside is ax+by+cz+d >= 0."""
    r = lambda i: (m[i], m[4 + i], m[8 + i], m[12 + i])      # row i of the matrix
    r0, r1, r2, r3 = r(0), r(1), r(2), r(3)
    return [tuple(r3[k] + r0[k] for k in range(4)), tuple(r3[k] - r0[k] for k in range(4)),
            tuple(r3[k] + r1[k] for k in range(4)), tuple(r3[k] - r1[k] for k in range(4)),
            tuple(r3[k] + r2[k] for k in range(4)), tuple(r3[k] - r2[k] for k in range(4))]


def box_in_frustum(box, planes) -> bool:
    """False only when the whole box is beyond one plane."""
    lo, hi = box
    for a, b, c, d in planes:
        x = hi[0] if a >= 0 else lo[0]
        y = hi[1] if b >= 0 else lo[1]
        z = hi[2] if c >= 0 else lo[2]
        if a * x + b * y + c * z + d < 0:
            return False
    return True
