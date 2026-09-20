"""
GLSL sources and the small amount of code needed to build them.

One program draws everything.  Without session lights a surface gets a
directional key light from the camera and a floor of ambient - enough to
read a model's shape in the browser.  With lights it is lit the way Source
lights a model under SFM's projected lights: each light is a frustum with
the flashlight attenuation (constant + linear / d + quadratic / d^2), a
fade to nothing between farZAtten and maxDistance, diffuse with optional
half-lambert and a $lightwarptexture ramp, Blinn phong with $phongexponent,
$phongboost and $phongfresnelranges, and $rimlight fed by the ambient.
The vertex stage skins with up to three bones per vertex when the instance
has a pose; otherwise the bind pose goes through untouched.
"""
from __future__ import annotations

from OpenGL import GL

__all__ = ["MODEL_VERT", "MODEL_FRAG", "LINE_VERT", "LINE_FRAG", "ID_FRAG", "MAX_BONES", "MAX_LIGHTS",
           "build_program", "ShaderError"]


class ShaderError(RuntimeError):
    pass


#: bones a single draw can address; Source itself allows 128 per model
MAX_BONES = 128
#: session lights a surface takes at once
MAX_LIGHTS = 8

MODEL_VERT = """
#version 330 core
layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;
layout(location = 2) in vec2 in_uv;
layout(location = 3) in ivec3 in_bones;
layout(location = 4) in vec3 in_weights;
layout(location = 6) in vec2 in_lightmap_uv;

uniform mat4 u_view_proj;
uniform mat4 u_model;
uniform bool u_skinned;
// three rows of a 3x4 matrix per bone: bind-pose model space to posed model space
uniform vec4 u_bones[3 * MAX_BONES];

out vec3 v_normal;
out vec2 v_uv;
out vec2 v_lightmap_uv;
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
    v_lightmap_uv = in_lightmap_uv;
    gl_Position = u_view_proj * world;
}
""".replace("MAX_BONES", str(MAX_BONES))

MODEL_FRAG = """
#version 330 core
in vec3 v_normal;
in vec2 v_uv;
in vec2 v_lightmap_uv;
in vec3 v_world;

uniform sampler2D u_texture;
uniform sampler2D u_lightwarp;
uniform sampler2D u_lightmap;
uniform bool u_lightmapped;   // a map face: its compiled light instead of the model lighting
uniform bool u_textured;
uniform bool u_lit;
uniform bool u_alpha_test;
uniform bool u_blended;       // a translucent or additive surface keeps its alpha
uniform vec3 u_color;
uniform float u_alpha;
uniform vec3 u_light_dir;     // the browser's key light: towards it, world space, unit
uniform vec3 u_eye;

// Source shading
uniform bool u_halflambert;
uniform bool u_has_lightwarp;
uniform bool u_phong;
uniform float u_phong_exponent;
uniform float u_phong_boost;
uniform vec3 u_fresnel;       // $phongfresnelranges
uniform bool u_rim;
uniform float u_rim_exponent;
uniform float u_rim_boost;
uniform bool u_self_illum;

// session lights
uniform int u_light_count;
uniform vec3 u_light_pos[MAX_LIGHTS];
uniform vec3 u_light_dirs[MAX_LIGHTS];    // the way each shines, unit
uniform vec3 u_light_color[MAX_LIGHTS];   // colour x intensity
uniform vec4 u_light_atten[MAX_LIGHTS];   // constant, linear, quadratic, cos of the cone half-angle
uniform vec3 u_light_range[MAX_LIGHTS];   // near, fade-from, far
uniform vec3 u_ambient;

out vec4 out_color;

float diffuse_term(float ndotl) {
    if (u_has_lightwarp) {
        // the ramp is indexed by the half-lambert value, as Source does
        return texture(u_lightwarp, vec2(ndotl * 0.5 + 0.5, 0.5)).r;
    }
    if (u_halflambert) {
        float h = ndotl * 0.5 + 0.5;
        return h * h;
    }
    return max(ndotl, 0.0);
}

void main() {
    vec4 base = u_textured ? texture(u_texture, v_uv) : vec4(0.8, 0.8, 0.8, 1.0);
    base.rgb *= u_color;
    base.a *= u_alpha;
    if (u_alpha_test && base.a < 0.5) discard;

    vec3 n = normalize(v_normal);
    // a near-zero normal is real in shipped art; treat it as facing the viewer
    if (dot(n, n) < 0.25) n = normalize(u_eye - v_world);
    if (!gl_FrontFacing) n = -n;
    vec3 v = normalize(u_eye - v_world);

    vec3 color = base.rgb;
    if (u_lightmapped) {
        // Source's lightmaps carry twice the range: the overbright factor
        color = base.rgb * texture(u_lightmap, v_lightmap_uv).rgb * 2.0;
    } else if (u_lit && u_light_count == 0) {
        // the browser: half-lambert keeps the dark side readable, as Source does
        float l = dot(n, u_light_dir) * 0.5 + 0.5;
        color *= 0.25 + 0.75 * l * l;
    } else if (u_lit) {
        vec3 lit = u_ambient;
        vec3 spec = vec3(0.0);
        float ndotv = max(dot(n, v), 0.0);
        // Source's fresnel: three ranges over the view angle
        float f = 1.0 - ndotv;
        float fresnel = f < 0.5 ? mix(u_fresnel.x, u_fresnel.y, f * 2.0) : mix(u_fresnel.y, u_fresnel.z, (f - 0.5) * 2.0);
        for (int i = 0; i < u_light_count; ++i) {
            vec3 to_light = u_light_pos[i] - v_world;
            float d = length(to_light);
            vec3 l = to_light / max(d, 1e-4);
            vec3 range = u_light_range[i];
            if (d < range.x || d > range.z) continue;
            // the frustum: a cone with a soft edge; fade to nothing towards maxDistance
            float cone = smoothstep(u_light_atten[i].w, u_light_atten[i].w + 0.03, dot(-l, u_light_dirs[i]));
            float fade = range.z > range.y ? 1.0 - clamp((d - range.y) / (range.z - range.y), 0.0, 1.0) : 1.0;
            float atten = u_light_atten[i].x + u_light_atten[i].y / d + u_light_atten[i].z / (d * d);
            vec3 radiance = u_light_color[i] * min(atten, 4.0) * cone * fade;
            float ndotl = dot(n, l);
            lit += radiance * diffuse_term(ndotl);
            if (u_phong && ndotl > 0.0) {
                vec3 h = normalize(l + v);
                spec += radiance * pow(max(dot(n, h), 0.0), u_phong_exponent) * fresnel * u_phong_boost * ndotl;
            }
        }
        if (u_rim) {
            // rim light: the ambient wrapping the silhouette
            spec += u_ambient * pow(1.0 - ndotv, u_rim_exponent) * u_rim_boost;
        }
        color = base.rgb * lit + spec;
        if (u_self_illum) color = max(color, base.rgb * base.a);
    }
    // an opaque surface's alpha is a mask for other shaders (phong, cloak),
    // not coverage; writing it to the frame would punch holes in a capture
    out_color = vec4(min(color, vec3(1.0)), u_blended ? base.a : 1.0);
}
""".replace("MAX_LIGHTS", str(MAX_LIGHTS))


LINE_VERT = """
#version 330 core
layout(location = 0) in vec3 in_position;
uniform mat4 u_view_proj;
void main() { gl_Position = u_view_proj * vec4(in_position, 1.0); }
"""

LINE_FRAG = """
#version 330 core
uniform vec4 u_color;
out vec4 out_color;
void main() { out_color = u_color; }
"""

#: draws every surface in one flat colour: the picking pass
ID_FRAG = """
#version 330 core
uniform vec4 u_color;
uniform sampler2D u_texture;
uniform bool u_textured;
uniform bool u_alpha_test;
in vec2 v_uv;
in vec3 v_normal;
in vec3 v_world;
out vec4 out_color;
void main() {
    if (u_alpha_test && u_textured && texture(u_texture, v_uv).a < 0.5) discard;
    out_color = u_color;
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
