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
from .scene import DrawItem, Scene
from .shaders import MODEL_FRAG, MODEL_VERT, build_program

__all__ = ["Renderer"]


class Renderer:
    def __init__(self) -> None:
        self.program = 0
        self.uniforms: Dict[str, int] = {}
        self.scene: Optional[Scene] = None
        self.meshes: List[Tuple[DrawItem, GLMesh]] = []
        self.textures: Dict[str, GLTexture] = {}
        self.background = (0.16, 0.17, 0.19, 1.0)
        self.model_matrix = IDENTITY
        self.wireframe = False
        #: Source winds triangles clockwise when seen from outside
        self.front_face_ccw = False
        self.errors: List[str] = []

    # -- lifecycle -----------------------------------------------------------------
    def initialize(self) -> None:
        self.program = build_program(MODEL_VERT, MODEL_FRAG)
        for name in ("u_mvp", "u_model", "u_texture", "u_textured", "u_lit", "u_alpha_test",
                     "u_color", "u_alpha", "u_light_dir", "u_eye"):
            self.uniforms[name] = GL.glGetUniformLocation(self.program, name)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthFunc(GL.GL_LEQUAL)

    def set_scene(self, scene: Optional[Scene]) -> None:
        self._release_scene()
        self.scene = scene
        if scene is None:
            return
        for key, vtf in scene.textures.items():
            try:
                self.textures[key] = GLTexture(vtf, key)
            except Exception as exc:                        # noqa: BLE001 - driver errors vary
                self.errors.append(f"texture {key}: {exc}")
        for item in scene.items:
            if item.mesh.indices:
                self.meshes.append((item, GLMesh(item.mesh)))

    def _release_scene(self) -> None:
        for _item, mesh in self.meshes:
            mesh.release()
        for texture in self.textures.values():
            texture.release()
        self.meshes = []
        self.textures = {}
        self.scene = None

    def release(self) -> None:
        self._release_scene()
        if self.program:
            GL.glDeleteProgram(self.program)
            self.program = 0

    # -- drawing -----------------------------------------------------------------
    def draw(self, camera: OrbitCamera, width: int, height: int) -> None:
        GL.glViewport(0, 0, max(1, width), max(1, height))
        GL.glClearColor(*self.background)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        if not self.meshes or not self.program:
            return

        view = camera.view()
        projection = camera.projection(width / max(1, height))
        mvp = multiply(projection, multiply(view, self.model_matrix))
        eye = camera.eye()
        # key light a little above and to the side of the camera
        light = normalize(sub(eye, camera.target))
        light = normalize((light[0] + camera.up[0] * 0.5, light[1] + camera.up[1] * 0.5,
                           light[2] + camera.up[2] * 0.5))

        u = self.uniforms
        GL.glUseProgram(self.program)
        GL.glUniformMatrix4fv(u["u_mvp"], 1, GL.GL_FALSE, mvp)
        GL.glUniformMatrix4fv(u["u_model"], 1, GL.GL_FALSE, self.model_matrix)
        GL.glUniform3f(u["u_light_dir"], *light)
        GL.glUniform3f(u["u_eye"], *eye)
        GL.glUniform1i(u["u_texture"], 0)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE if self.wireframe else GL.GL_FILL)
        GL.glFrontFace(GL.GL_CCW if self.front_face_ccw else GL.GL_CW)

        for item, mesh in self.meshes:
            self._apply_state(item)
            texture = self.textures.get(item.texture_key)
            if texture is not None:
                texture.bind(0)
            GL.glUniform1i(u["u_textured"], 1 if texture is not None else 0)
            mesh.draw()

        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glDisable(GL.GL_BLEND)
        GL.glDepthMask(GL.GL_TRUE)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glUseProgram(0)

    def _apply_state(self, item: DrawItem) -> None:
        u = self.uniforms
        GL.glUniform3f(u["u_color"], *item.color)
        GL.glUniform1f(u["u_alpha"], item.alpha)
        GL.glUniform1i(u["u_lit"], 1 if item.lit else 0)
        GL.glUniform1i(u["u_alpha_test"], 1 if item.alpha_test else 0)
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
