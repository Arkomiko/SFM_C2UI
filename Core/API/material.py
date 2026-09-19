"""
A material, as a renderer wants to see it.

A .vmt names a shader and a bag of parameters. Almost every shipped material
uses one of three shaders and a dozen parameters, so this type reads those out
into plain fields and keeps the rest in `params` for anything that needs more.

    mat = load_material(library, "materials/models/player/scout/scout_red.vmt")
    mat.shader                       # "VertexLitGeneric"
    mat.base_texture                 # "materials/models/player/scout/scout_red.vtf"
    mat.translucent, mat.alpha_test  # blending flags
    mat.param("$phongexponent")      # anything else, as text
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

__all__ = ["Material", "texture_path", "is_dynamic_texture", "as_float", "as_vec", "as_bool"]

_NUMBER = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")


def texture_path(value: str) -> str:
    """Turn a `$basetexture` value into a content-relative .vtf path.

    Values are written relative to `materials/`, usually without the extension,
    with either slash and in any case - the file system is case-blind on the
    platform these were made for, and content is indexed lower-cased.

    Returns "" for a render target or `env_cubemap`: there is no file to load.
    """
    value = value.strip().replace("\\", "/").strip("/").lower()
    if not value or is_dynamic_texture(value):
        return ""
    if value.endswith(".vtf"):
        value = value[:-4]
    return f"materials/{value}.vtf"


def is_dynamic_texture(value: str) -> bool:
    """A texture the engine makes at run time rather than loads: render
    targets (`_rt_camera`, `_rt_fullframefb`) and `env_cubemap`."""
    value = value.strip().replace("\\", "/").strip("/").lower()
    return value.startswith("_rt_") or value == "env_cubemap"


def as_float(value: Optional[str], default: float = 0.0) -> float:
    """`"0.5"`, `"[0.5]"` and `".5f"` all read as 0.5."""
    if value is None:
        return default
    match = _NUMBER.search(str(value))
    return float(match.group()) if match else default


def as_vec(value: Optional[str], default: Tuple[float, ...] = ()) -> Tuple[float, ...]:
    """`"[1 .5 0]"` or `"{255 128 0}"` (which is 0-255) to a tuple of floats."""
    if value is None:
        return default
    text = str(value).strip()
    numbers = [float(n) for n in _NUMBER.findall(text)]
    if not numbers:
        return default
    if text.startswith("{"):
        numbers = [n / 255.0 for n in numbers]
    return tuple(numbers)


def as_bool(value: Optional[str], default: bool = False) -> bool:
    if value is None:
        return default
    return as_float(value, 1.0 if default else 0.0) != 0.0


@dataclass
class Material:
    """One resolved material.  Paths are content-relative and lower-cased."""

    #: the path this was loaded from, e.g. ``materials/models/x/y.vmt``
    path: str = ""
    shader: str = ""
    #: every parameter, lower-cased keys, last value wins; nested blocks are dropped
    params: Dict[str, str] = field(default_factory=dict)
    #: names of the proxies the material declared, in order
    proxies: List[str] = field(default_factory=list)
    #: for a `patch` material, the material it was built on
    includes: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # -- lookups ------------------------------------------------------------------
    def param(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self.params.get(key.lower(), default)

    def has(self, key: str) -> bool:
        return key.lower() in self.params

    def texture(self, key: str) -> str:
        """A texture parameter as a .vtf path, or `""` when unset."""
        return texture_path(self.params.get(key.lower(), ""))

    # -- what a renderer asks first ---------------------------------------------
    @property
    def base_texture(self) -> str:
        """The texture to draw with.  `$basetexture` for nearly everything;
        eye shaders keep theirs in `$iris`, HDR skies in `$hdrbasetexture`."""
        for key in ("$basetexture", "$iris", "$hdrbasetexture", "$hdrcompressedtexture"):
            path = self.texture(key)
            if path:
                return path
        return ""

    @property
    def bump_map(self) -> str:
        return self.texture("$bumpmap")

    @property
    def translucent(self) -> bool:
        return as_bool(self.param("$translucent"))

    @property
    def alpha_test(self) -> bool:
        return as_bool(self.param("$alphatest"))

    @property
    def additive(self) -> bool:
        return as_bool(self.param("$additive"))

    @property
    def two_sided(self) -> bool:
        return as_bool(self.param("$nocull"))

    @property
    def self_illum(self) -> bool:
        return as_bool(self.param("$selfillum"))

    @property
    def color(self) -> Tuple[float, float, float]:
        """`$color` and `$color2` multiplied, as most shaders do; white when unset."""
        r, g, b = 1.0, 1.0, 1.0
        for key in ("$color", "$color2"):
            vec = as_vec(self.param(key))
            if len(vec) >= 3:
                r, g, b = r * vec[0], g * vec[1], b * vec[2]
            elif len(vec) == 1:
                r, g, b = r * vec[0], g * vec[0], b * vec[0]
        return r, g, b

    @property
    def alpha(self) -> float:
        return as_float(self.param("$alpha"), 1.0)

    @property
    def is_model_shader(self) -> bool:
        """Lit like a model (as opposed to a world surface or a sprite)."""
        return self.shader.lower() in _MODEL_SHADERS

    def textures(self) -> Dict[str, str]:
        """Every texture-valued parameter as ``{param: vtf path}``."""
        out = {}
        for key, value in self.params.items():
            if key in _TEXTURE_PARAMS and value:
                out[key] = texture_path(value)
        return out

    def summary(self) -> str:
        return (f"{self.shader or '<no shader>'} {self.path}: {len(self.params)} params, "
                f"base {self.base_texture or '<none>'}")


_MODEL_SHADERS = frozenset({
    "vertexlitgeneric", "eyerefract", "eyes", "eyeball", "teeth", "vertexlitgeneric_dx6",
    "vertexlitgeneric_dx9", "vertexlitgeneric_hdr_dx9",
})

_TEXTURE_PARAMS = frozenset({
    "$basetexture", "$basetexture2", "$bumpmap", "$bumpmap2", "$detail", "$envmapmask",
    "$lightwarptexture", "$phongexponenttexture", "$selfillummask", "$sheenmap",
    "$sheenmapmask", "$blendmodulatetexture", "$normalmap", "$iris", "$corneatexture",
    "$ambientoccltexture", "$hdrbasetexture", "$hdrcompressedtexture", "$texture2",
    "$refracttinttexture", "$flowmap", "$wrinkle", "$stretch", "$emissiveblendtexture",
    "$emissiveblendbasetexture", "$emissiveblendflowtexture", "$texture1", "$fleshinteriortexture",
})
