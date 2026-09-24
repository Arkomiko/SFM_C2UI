"""
GLSL sources and the small amount of code needed to build them.

One program draws everything.  Without lights a surface gets a directional
key light from the camera and a floor of ambient - enough to read a model's
shape in the browser.  With lights it is lit the way Source lights a model:
the session's projected lights are frustums with the flashlight attenuation
(constant + linear / d + quadratic / d^2) and a fade to nothing between
farZAtten and maxDistance; the map's point, spot and sun lights use vrad's
attenuation and the spot's inner / outer cone; the ambient is the map's
ambient cube sampled by the normal.  Diffuse has optional half-lambert and
a $lightwarptexture ramp, specular is Blinn phong with $phongexponent,
$phongboost and $phongfresnelranges, $rimlight is fed by the ambient and
$selfillum glows through the base alpha.  World faces skip all of that and
multiply the base texture by their lightmap.  Light is summed in linear
space and written out in gamma, as the engine does.
The vertex stage skins with up to three bones per vertex when the instance
has a pose; otherwise the bind pose goes through untouched.
"""
from __future__ import annotations

from OpenGL import GL

__all__ = ["MODEL_VERT", "MODEL_FRAG", "LINE_VERT", "LINE_FRAG", "ID_FRAG", "DEPTH_FRAG", "MAX_BONES", "MAX_LIGHTS",
           "MAX_SHADOWS", "SHADOW_SIZE", "POST_VERT", "ADD_FRAG", "BRIGHT_FRAG", "BLUR_FRAG", "RESOLVE_FRAG",
           "build_program", "ShaderError"]


class ShaderError(RuntimeError):
    """A shader failed to compile or link."""
    pass


#: bones a single draw can address; Source itself allows 128 per model
MAX_BONES = 128
#: lights a surface takes at once: the session's and the map's nearest
MAX_LIGHTS = 12
#: projected lights that get a cookie and a shadow map each frame (the rest keep the plain cone)
MAX_SHADOWS = 4
#: shadow map side in texels
SHADOW_SIZE = 2048

MODEL_VERT = """
#version 330 core
layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;
layout(location = 2) in vec2 in_uv;
layout(location = 3) in ivec3 in_bones;
layout(location = 4) in vec3 in_weights;
layout(location = 6) in vec2 in_lightmap_uv;
layout(location = 7) in vec4 in_tangent;     // xyz and the bitangent's sign

uniform mat4 u_view_proj;
uniform mat4 u_model;
uniform bool u_skinned;
// three rows of a 3x4 matrix per bone: bind-pose model space to posed model space
uniform vec4 u_bones[3 * MAX_BONES];

out vec3 v_normal;
out vec4 v_tangent;
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
    vec3 tangent = in_tangent.xyz;
    if (u_skinned) {
        vec4 p = vec4(in_position, 1.0);
        vec4 n = vec4(in_normal, 0.0);
        vec4 t = vec4(in_tangent.xyz, 0.0);
        vec3 sp = vec3(0.0);
        vec3 sn = vec3(0.0);
        vec3 st = vec3(0.0);
        float total = 0.0;
        for (int k = 0; k < 3; ++k) {
            float w = in_weights[k];
            if (w <= 0.0) continue;
            int bone = clamp(in_bones[k], 0, MAX_BONES - 1);
            sp += w * bone_point(bone, p);
            sn += w * bone_point(bone, n);
            st += w * bone_point(bone, t);
            total += w;
        }
        if (total > 0.0) {
            position = sp / total;
            normal = sn / total;
            tangent = st / total;
        }
    }
    vec4 world = u_model * vec4(position, 1.0);
    v_world = world.xyz;
    v_normal = mat3(u_model) * normal;
    v_tangent = vec4(mat3(u_model) * tangent, in_tangent.w);
    v_uv = in_uv;
    v_lightmap_uv = in_lightmap_uv;
    gl_Position = u_view_proj * world;
}
""".replace("MAX_BONES", str(MAX_BONES))

MODEL_FRAG = """
#version 330 core
in vec3 v_normal;
in vec4 v_tangent;
in vec2 v_uv;
in vec2 v_lightmap_uv;
in vec3 v_world;

uniform sampler2D u_texture;
uniform sampler2D u_lightwarp;
uniform sampler2D u_lightmap;
uniform sampler2D u_bumpmap;
uniform sampler2D u_exponent;     // $phongexponenttexture: r exponent, g albedo tint, a rim mask
uniform sampler2D u_selfillum_mask;
uniform bool u_has_bumpmap;
uniform bool u_has_exponent;
uniform bool u_has_selfillum_mask;
uniform int u_phong_mask;         // 0 none, 1 base alpha, 2 normal map alpha
uniform bool u_invert_phong_mask;
uniform bool u_albedo_tint;
uniform bool u_rim_mask;
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
uniform bool u_gamma_out;     // write gamma (drawing straight to the screen) instead of linear

// session lights
uniform int u_light_count;
uniform vec3 u_light_pos[MAX_LIGHTS];
uniform vec3 u_light_dirs[MAX_LIGHTS];    // the way each shines, unit
uniform vec3 u_light_color[MAX_LIGHTS];   // colour x intensity
uniform vec4 u_light_atten[MAX_LIGHTS];   // constant, linear, quadratic, cos of the cone edge
uniform vec3 u_light_range[MAX_LIGHTS];   // near, fade-from, far
uniform vec4 u_light_kind[MAX_LIGHTS];    // kind (0 projected, 1 point, 2 spot, 3 sun), inner cone cos
uniform vec3 u_ambient;
uniform vec3 u_ambient_cube[6];           // +x -x +y -y +z -z, the map's ambient at the model
uniform bool u_has_cube;

// projected lights with a frustum of their own: the cookie they throw and their shadow map
uniform mat4 u_shadow_matrix[MAX_SHADOWS];
uniform sampler2DShadow u_shadow_map[MAX_SHADOWS];
uniform sampler2D u_cookie[MAX_SHADOWS];
uniform bool u_has_shadow[MAX_SHADOWS];
uniform bool u_has_cookie[MAX_SHADOWS];
uniform float u_shadow_texel;             // 1 / shadow map side
uniform int u_light_slot[MAX_LIGHTS];     // a light's slot above, or -1

// GLSL 330 indexes sampler arrays with constants only
float shadow_sample(int slot, vec3 c) {
    if (slot == 0) return texture(u_shadow_map[0], c);
    if (slot == 1) return texture(u_shadow_map[1], c);
    if (slot == 2) return texture(u_shadow_map[2], c);
    return texture(u_shadow_map[3], c);
}

float cookie_sample(int slot, vec2 uv) {
    if (slot == 0) return texture(u_cookie[0], uv).r;
    if (slot == 1) return texture(u_cookie[1], uv).r;
    if (slot == 2) return texture(u_cookie[2], uv).r;
    return texture(u_cookie[3], uv).r;
}

// how much of a slotted light reaches `world`: its cookie through its frustum, times
// the shadow map with a 3x3 filter, as SFM's shadowFilterSize 3 does
float projected_factor(int slot, vec3 world) {
    vec4 p = u_shadow_matrix[slot] * vec4(world, 1.0);
    if (p.w <= 0.0) return 0.0;
    vec3 c = p.xyz / p.w * 0.5 + 0.5;
    if (c.x < 0.0 || c.x > 1.0 || c.y < 0.0 || c.y > 1.0 || c.z > 1.0) return 0.0;
    float factor = u_has_cookie[slot] ? cookie_sample(slot, c.xy) : 1.0;
    if (u_has_shadow[slot] && factor > 0.0) {
        float lit = 0.0;
        for (int y = -1; y <= 1; ++y)
            for (int x = -1; x <= 1; ++x)
                lit += shadow_sample(slot, vec3(c.xy + vec2(x, y) * u_shadow_texel, c.z - 0.0008));
        factor *= lit / 9.0;
    }
    return factor;
}

vec3 ambient_light(vec3 n) {
    if (!u_has_cube) return u_ambient;
    vec3 sq = n * n;
    return sq.x * (n.x >= 0.0 ? u_ambient_cube[0] : u_ambient_cube[1])
         + sq.y * (n.y >= 0.0 ? u_ambient_cube[2] : u_ambient_cube[3])
         + sq.z * (n.z >= 0.0 ? u_ambient_cube[4] : u_ambient_cube[5]);
}

out vec4 out_color;

// light i as seen from `world`: the direction towards it and its radiance there;
// false when the point is outside the light's reach
bool light_at(int i, vec3 world, out vec3 l, out vec3 radiance) {
    int kind = int(u_light_kind[i].x + 0.5);
    if (kind == 3) {
        // the sun: parallel, no falloff
        l = -u_light_dirs[i];
        radiance = u_light_color[i];
        return true;
    }
    vec3 to_light = u_light_pos[i] - world;
    float d = length(to_light);
    l = to_light / max(d, 1e-4);
    if (kind == 0) {
        vec3 range = u_light_range[i];
        if (d < range.x || d > range.z) return false;
        // the projected frustum: the light's cookie and shadow when it has a slot, else a
        // cone with a soft edge; fade to nothing towards maxDistance
        int slot = u_light_slot[i];
        float cone = slot >= 0 ? projected_factor(slot, world)
                               : smoothstep(u_light_atten[i].w, u_light_atten[i].w + 0.03, dot(-l, u_light_dirs[i]));
        if (cone <= 0.0) return false;
        float fade = range.z > range.y ? 1.0 - clamp((d - range.y) / (range.z - range.y), 0.0, 1.0) : 1.0;
        float atten = u_light_atten[i].x + u_light_atten[i].y / d + u_light_atten[i].z / (d * d);
        radiance = u_light_color[i] * min(atten, 8.0) * cone * fade;     // the near field is bright, not clipped
        return true;
    }
    // the map's point and spot lights: intensity over (c + l d + q d^2), as vrad's
    float denominator = max(u_light_atten[i].x + u_light_atten[i].y * d + u_light_atten[i].z * d * d, 1e-3);
    radiance = u_light_color[i] / denominator;
    if (kind == 2) {
        float cos_angle = dot(-l, u_light_dirs[i]);
        radiance *= smoothstep(u_light_atten[i].w, max(u_light_kind[i].y, u_light_atten[i].w + 1e-3), cos_angle);
    }
    return true;
}

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
    vec4 bump = vec4(0.5, 0.5, 1.0, 1.0);
    if (u_has_bumpmap) {
        bump = texture(u_bumpmap, v_uv);
        vec3 t = v_tangent.xyz - n * dot(n, v_tangent.xyz);
        if (dot(t, t) > 1e-8) {
            t = normalize(t);
            vec3 b = cross(n, t) * (v_tangent.w < 0.0 ? -1.0 : 1.0);
            vec3 tn = bump.xyz * 2.0 - 1.0;
            n = normalize(t * tn.x + b * tn.y + n * tn.z);
        }
    }
    vec3 v = normalize(u_eye - v_world);

    // everything below is linear light; the frame is developed to gamma afterwards
    vec3 albedo = pow(base.rgb, vec3(2.2));
    vec3 color = albedo;
    if (u_lightmapped) {
        // Source's lightmaps carry twice the range: the overbright factor
        color = pow(base.rgb * texture(u_lightmap, v_lightmap_uv).rgb * 2.0, vec3(2.2));
        // the session's projected lights fall on the world as well, on top of what
        // vrad baked (a set lit only by them has a black lightmap)
        for (int i = 0; i < u_light_count; ++i) {
            if (int(u_light_kind[i].x + 0.5) != 0) continue;
            vec3 l;
            vec3 radiance;
            if (light_at(i, v_world, l, radiance)) color += albedo * radiance * max(dot(n, l), 0.0);
        }
    } else if (u_lit && u_light_count == 0) {
        // the browser: half-lambert keeps the dark side readable, as Source does
        float l = dot(n, u_light_dir) * 0.5 + 0.5;
        color *= 0.25 + 0.75 * l * l;
    } else if (u_lit) {
        vec3 lit = ambient_light(n);
        vec3 spec = vec3(0.0);
        float ndotv = max(dot(n, v), 0.0);
        // Source's fresnel: three ranges over the view angle
        float f = 1.0 - ndotv;
        float fresnel = f < 0.5 ? mix(u_fresnel.x, u_fresnel.y, f * 2.0) : mix(u_fresnel.y, u_fresnel.z, (f - 0.5) * 2.0);
        // the specular mask and exponent, as the material says
        float mask = 1.0;
        if (u_phong_mask == 1) mask = base.a;
        else if (u_phong_mask == 2) mask = bump.a;
        if (u_invert_phong_mask) mask = 1.0 - mask;
        float exponent = u_phong_exponent;
        vec3 spec_tint = vec3(1.0);
        float rim_mask = 1.0;
        if (u_has_exponent) {
            vec4 e = texture(u_exponent, v_uv);
            if (exponent <= 0.0) exponent = 1.0 + 149.0 * e.r;
            if (u_albedo_tint) spec_tint = mix(vec3(1.0), pow(base.rgb, vec3(2.2)), e.g);
            if (u_rim_mask) rim_mask = e.a;
        }
        if (exponent <= 0.0) exponent = 5.0;
        for (int i = 0; i < u_light_count; ++i) {
            vec3 l;
            vec3 radiance;
            if (!light_at(i, v_world, l, radiance)) continue;
            float ndotl = dot(n, l);
            lit += radiance * diffuse_term(ndotl);
            if (u_phong && ndotl > 0.0) {
                vec3 h = normalize(l + v);
                spec += radiance * spec_tint * pow(max(dot(n, h), 0.0), exponent) * fresnel * u_phong_boost * mask * ndotl;
            }
        }
        if (u_rim) {
            // rim light: the ambient wrapping the silhouette, through the phong mask as Source does
            spec += ambient_light(v) * pow(1.0 - ndotv, u_rim_exponent) * u_rim_boost * mask * rim_mask;
        }
        color = max(albedo * lit + spec, vec3(0.0));
        if (u_self_illum) {
            float glow = u_has_selfillum_mask ? texture(u_selfillum_mask, v_uv).r : base.a;
            color = max(color, albedo * glow);
        }
    }
    if (u_gamma_out) color = pow(min(color, vec3(1.0)), vec3(1.0 / 2.2));
    // an opaque surface's alpha is a mask for other shaders (phong, cloak),
    // not coverage; writing it to the frame would punch holes in a capture
    out_color = vec4(color, u_blended ? base.a : 1.0);
}
""".replace("MAX_LIGHTS", str(MAX_LIGHTS)).replace("MAX_SHADOWS", str(MAX_SHADOWS))


#: a full-screen triangle from the vertex id alone: the post passes need no buffers
POST_VERT = """
#version 330 core
out vec2 v_uv;
void main() {
    vec2 p = vec2((gl_VertexID == 1) ? 3.0 : -1.0, (gl_VertexID == 2) ? 3.0 : -1.0);
    v_uv = p * 0.5 + 0.5;
    gl_Position = vec4(p, 0.0, 1.0);
}
"""

#: adds one sample of the frame into the accumulation, weighted
ADD_FRAG = """
#version 330 core
uniform sampler2D u_source;
uniform float u_weight;
in vec2 v_uv;
out vec4 out_color;
void main() { out_color = vec4(texture(u_source, v_uv).rgb * u_weight, 1.0); }
"""

#: keeps what is brighter than the threshold: the bloom's seed, at quarter size
BRIGHT_FRAG = """
#version 330 core
uniform sampler2D u_source;
uniform float u_scale;        // 1 / accumulated weight
uniform float u_threshold;
in vec2 v_uv;
out vec4 out_color;
void main() {
    vec3 c = texture(u_source, v_uv).rgb * u_scale;
    float l = dot(c, vec3(0.299, 0.587, 0.114));
    out_color = vec4(c * smoothstep(u_threshold, u_threshold + 0.5, l), 1.0);
}
"""

#: one direction of a gaussian blur
BLUR_FRAG = """
#version 330 core
uniform sampler2D u_source;
uniform vec2 u_step;          // one texel along the blur direction
uniform float u_sigma;        // in texels
in vec2 v_uv;
out vec4 out_color;
void main() {
    int radius = int(ceil(u_sigma * 2.5));
    vec3 sum = vec3(0.0);
    float total = 0.0;
    for (int i = -radius; i <= radius; ++i) {
        float w = exp(-0.5 * float(i * i) / (u_sigma * u_sigma));
        sum += texture(u_source, v_uv + u_step * float(i)).rgb * w;
        total += w;
    }
    out_color = vec4(sum / total, 1.0);
}
"""

#: the developed frame: accumulated linear light, bloom, exposure, gamma
RESOLVE_FRAG = """
#version 330 core
uniform sampler2D u_source;
uniform sampler2D u_bloom;
uniform float u_scale;        // 1 / accumulated weight
uniform float u_tonemap;
uniform float u_bloom_scale;
in vec2 v_uv;
out vec4 out_color;
void main() {
    vec3 c = texture(u_source, v_uv).rgb * u_scale;
    c += texture(u_bloom, v_uv).rgb * u_bloom_scale;
    c = min(c * u_tonemap, vec3(1.0));
    out_color = vec4(pow(c, vec3(1.0 / 2.2)), 1.0);
}
"""

#: writes depth only: the shadow map pass (alpha-tested surfaces still cut holes)
DEPTH_FRAG = """
#version 330 core
uniform sampler2D u_texture;
uniform bool u_textured;
uniform bool u_alpha_test;
in vec2 v_uv;
in vec3 v_normal;
in vec3 v_world;
void main() {
    if (u_alpha_test && u_textured && texture(u_texture, v_uv).a < 0.5) discard;
}
"""


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
