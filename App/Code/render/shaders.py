"""
GLSL sources and the small amount of code needed to build them.

One program draws everything for now: a textured surface with a directional
light from the camera and a floor of ambient, which is enough to read a model's
shape. The vertex stage skins with up to three bones per vertex when the
instance has a pose; otherwise the bind pose goes through untouched.
Source's own shading (phong, rim, lightwarp) comes later and will be more
programs, not more branches in this one.
"""
from __future__ import annotations

from OpenGL import GL

__all__ = ["MODEL_VERT", "MODEL_FRAG", "MAX_BONES", "build_program", "ShaderError"]


class ShaderError(RuntimeError):
    pass


#: bones a single draw can address; Source itself allows 128 per model
MAX_BONES = 128

MODEL_VERT = """
#version 330 core
layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;
layout(location = 2) in vec2 in_uv;
layout(location = 3) in ivec3 in_bones;
layout(location = 4) in vec3 in_weights;

uniform mat4 u_view_proj;
uniform mat4 u_model;
uniform bool u_skinned;
// three rows of a 3x4 matrix per bone: bind-pose model space to posed model space
uniform vec4 u_bones[3 * MAX_BONES];

out vec3 v_normal;
out vec2 v_uv;
out vec3 v_world;

vec3 bone_point(int bone, vec4 p) {
    return vec3(dot(u_bones[bone * 3 + 0], p),
                dot(u_bones[bone * 3 + 1], p),
                dot(u_bones[bone * 3 + 2], p));
}

void main() {
    vec3 position = in_position;
    vec3 normal = in_normal;
    if (u_skinned) {
        vec4 p = vec4(in_position, 1.0);
        vec4 n = vec4(in_normal, 0.0);
        vec3 sp = vec3(0.0);
        vec3 sn = vec3(0.0);
        float total = 0.0;
        for (int k = 0; k < 3; ++k) {
            float w = in_weights[k];
            if (w <= 0.0) continue;
            int bone = clamp(in_bones[k], 0, MAX_BONES - 1);
            sp += w * bone_point(bone, p);
            sn += w * bone_point(bone, n);
            total += w;
        }
        if (total > 0.0) {
            position = sp / total;
            normal = sn / total;
        }
    }
    vec4 world = u_model * vec4(position, 1.0);
    v_world = world.xyz;
    v_normal = mat3(u_model) * normal;
    v_uv = in_uv;
    gl_Position = u_view_proj * world;
}
""".replace("MAX_BONES", str(MAX_BONES))

MODEL_FRAG = """
#version 330 core
in vec3 v_normal;
in vec2 v_uv;
in vec3 v_world;

uniform sampler2D u_texture;
uniform bool u_textured;
uniform bool u_lit;
uniform bool u_alpha_test;
uniform bool u_blended;       // a translucent or additive surface keeps its alpha
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
    // an opaque surface's alpha is a mask for other shaders (phong, cloak),
    // not coverage; writing it to the frame would punch holes in a capture
    out_color = vec4(base.rgb * shade, u_blended ? base.a : 1.0);
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
