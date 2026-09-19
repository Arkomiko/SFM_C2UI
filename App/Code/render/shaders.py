"""
GLSL sources and the small amount of code needed to build them.

One program draws everything for now: a textured surface with a directional
light from the camera and a floor of ambient, which is enough to read a model's
shape. Source's own shading (phong, rim, lightwarp) comes later and will be
more programs, not more branches in this one.
"""
from __future__ import annotations

from OpenGL import GL

__all__ = ["MODEL_VERT", "MODEL_FRAG", "build_program", "ShaderError"]


class ShaderError(RuntimeError):
    pass


MODEL_VERT = """
#version 330 core
layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;
layout(location = 2) in vec2 in_uv;

uniform mat4 u_mvp;
uniform mat4 u_model;

out vec3 v_normal;
out vec2 v_uv;
out vec3 v_world;

void main() {
    vec4 world = u_model * vec4(in_position, 1.0);
    v_world = world.xyz;
    v_normal = mat3(u_model) * in_normal;
    v_uv = in_uv;
    gl_Position = u_mvp * vec4(in_position, 1.0);
}
"""

MODEL_FRAG = """
#version 330 core
in vec3 v_normal;
in vec2 v_uv;
in vec3 v_world;

uniform sampler2D u_texture;
uniform bool u_textured;
uniform bool u_lit;
uniform bool u_alpha_test;
uniform vec3 u_color;
uniform float u_alpha;
uniform vec3 u_light_dir;     // towards the light, world space, unit
uniform vec3 u_eye;

out vec4 out_color;

void main() {
    vec4 base = u_textured ? texture(u_texture, v_uv) : vec4(0.8, 0.8, 0.8, 1.0);
    base.rgb *= u_color;
    base.a *= u_alpha;
    if (u_alpha_test && base.a < 0.5) discard;

    vec3 n = normalize(v_normal);
    // a near-zero normal is real in shipped art; treat it as facing the viewer
    if (dot(n, n) < 0.25) n = normalize(u_eye - v_world);
    if (!gl_FrontFacing) n = -n;

    float shade = 1.0;
    if (u_lit) {
        // half-lambert keeps the dark side readable, as Source does
        float l = dot(n, u_light_dir) * 0.5 + 0.5;
        shade = 0.25 + 0.75 * l * l;
    }
    out_color = vec4(base.rgb * shade, base.a);
}
"""


def _compile(kind: int, source: str) -> int:
    shader = GL.glCreateShader(kind)
    GL.glShaderSource(shader, source)
    GL.glCompileShader(shader)
    if not GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS):
        log = GL.glGetShaderInfoLog(shader)
        GL.glDeleteShader(shader)
        raise ShaderError(log.decode("utf-8", "replace") if isinstance(log, bytes) else str(log))
    return shader


def build_program(vertex: str, fragment: str) -> int:
    """Compile and link; raises ShaderError with the driver's message."""
    vs = _compile(GL.GL_VERTEX_SHADER, vertex)
    fs = _compile(GL.GL_FRAGMENT_SHADER, fragment)
    program = GL.glCreateProgram()
    GL.glAttachShader(program, vs)
    GL.glAttachShader(program, fs)
    GL.glLinkProgram(program)
    GL.glDeleteShader(vs)
    GL.glDeleteShader(fs)
    if not GL.glGetProgramiv(program, GL.GL_LINK_STATUS):
        log = GL.glGetProgramInfoLog(program)
        GL.glDeleteProgram(program)
        raise ShaderError(log.decode("utf-8", "replace") if isinstance(log, bytes) else str(log))
    return program
