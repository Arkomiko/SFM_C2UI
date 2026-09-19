"""
The .vmt file: a material description in KeyValues.

    VertexLitGeneric
    {
        $basetexture "models/player/scout/scout_red"
        $phong 1
        >=DX90 { $bumpmap "..." }        // only on this hardware level
        Proxies { Sine { ... } }         // animated parameters
    }

Three things need resolving before the parameters mean anything:

* **conditional blocks** - `>=DX90`, `<DX90`, `LightmappedGeneric_DX9` and
  the like hold parameters that apply only at a hardware level. Everything is
  evaluated as DirectX 9, which is what Source Filmmaker itself runs;
* **patch materials** - a shader called `patch` names another file in
  `include` and layers `insert`/`replace` over it;
* **fallback shaders** - a name such as `LightmappedGeneric_DX8` at the top
  level is the material for old hardware, and is ignored.

    material = load_material(library, "materials/models/props/crate.vmt")
"""
from __future__ import annotations

import re
from typing import Optional, Protocol, Set

from Core.API.material import Material
from Core.Code.keyvalues import KeyValues, KeyValuesError, loads

__all__ = ["parse_vmt", "load_material", "MaterialSource", "DX_LEVEL"]

#: the hardware level conditional blocks are judged against
DX_LEVEL = 90

_CONDITION = re.compile(r"^\s*([<>]=?|==|!=)\s*dx(\d+)\s*$", re.IGNORECASE)
#: `LightmappedGeneric_DX8`, `Water_DX60`, `VertexLitGeneric_HDR_DX9`...
_FALLBACK = re.compile(r"_(?:hdr_)?dx(\d+)$", re.IGNORECASE)
_MAX_INCLUDE_DEPTH = 8
#: the name given to a file's root block, so an unwrapped shader block is told apart
_FILE = "<file>"


class MaterialSource(Protocol):
    def read_text(self, rel: str) -> Optional[str]: ...


# ---------------------------------------------------------------------------
#  Text -> Material
# ---------------------------------------------------------------------------
def parse_vmt(text: str, path: str = "") -> Material:
    """Read one .vmt.  Does not follow `include`; :func:`load_material` does."""
    try:
        root = loads(text, _FILE)
    except KeyValuesError as exc:
        raise ValueError(f"{path or 'material'}: {exc}") from exc

    material = Material(path=path.replace("\\", "/").lower())
    shader_block = _pick_shader(root, material)
    if shader_block is None:
        material.warnings.append("no shader block")
        return material
    material.shader = shader_block.name
    _apply_block(shader_block, material)
    return material


def _pick_shader(root: KeyValues, material: Material) -> Optional[KeyValues]:
    """The block whose name is the shader.

    `loads` unwraps a lone outer block and names it after its key, so normally
    `root` *is* the shader. When a file carries several top-level blocks (a
    shader plus fallbacks for older hardware) `root` keeps the file name and
    the first block that is not a fallback wins.
    """
    if root.name != _FILE:
        return root
    fallbacks = []
    for key, value in root.items():
        if not isinstance(value, KeyValues):
            continue
        match = _FALLBACK.search(key)
        if match is None:
            value.name = key
            return value
        fallbacks.append((_dx_level(match), key, value))
    if fallbacks:
        # only fallbacks - take the highest hardware level
        _level, key, value = max(fallbacks)
        value.name = key
        material.warnings.append(f"only fallback shaders present; using {key}")
        return value
    return None


def _dx_level(match: "re.Match[str]") -> int:
    """`_dx9` and `_dx90` mean the same level; `_dx60` is 60."""
    level = int(match.group(1))
    return level * 10 if level < 10 else level


def _is_conditional(key: str) -> bool:
    return bool(_CONDITION.match(key))


def _condition_holds(key: str) -> bool:
    match = _CONDITION.match(key)
    if not match:
        return False
    op, level = match.group(1), int(match.group(2))
    return {
        "<": DX_LEVEL < level, "<=": DX_LEVEL <= level,
        ">": DX_LEVEL > level, ">=": DX_LEVEL >= level,
        "==": DX_LEVEL == level, "!=": DX_LEVEL != level,
    }[op]


def _apply_block(block: KeyValues, material: Material) -> None:
    for key, value in block.items():
        lowered = key.lower()
        if isinstance(value, KeyValues):
            if lowered == "proxies":
                material.proxies.extend(k for k, _v in value.items())
            elif _is_conditional(key):
                if _condition_holds(key):
                    _apply_block(value, material)
            elif (match := _FALLBACK.search(key)):
                # a nested fallback shader; the DX9 ones carry real parameters
                if _dx_level(match) >= DX_LEVEL:
                    _apply_block(value, material)
            # other nested blocks (insert/replace/templates) are the caller's business
            continue
        material.params[lowered] = str(value)


# ---------------------------------------------------------------------------
#  Loading with patch resolution
# ---------------------------------------------------------------------------
def load_material(source: MaterialSource, rel: str) -> Optional[Material]:
    """Read a material from content, resolving `patch` includes.

    Returns None when the file does not exist. Raises ValueError when it
    exists but is not KeyValues.
    """
    return _load(source, _normalise(rel), set(), 0)


def _normalise(rel: str) -> str:
    rel = rel.replace("\\", "/").strip("/").lower()
    if not rel.endswith(".vmt"):
        rel += ".vmt"
    if not rel.startswith("materials/"):
        rel = "materials/" + rel
    return rel


def _load(source: MaterialSource, rel: str, seen: Set[str], depth: int) -> Optional[Material]:
    text = source.read_text(rel)
    if text is None:
        return None
    material = parse_vmt(text, rel)
    if material.shader.lower() != "patch":
        return material

    root = loads(text, rel)
    include = root.get_str("include").strip()
    if not include:
        material.warnings.append("patch without an include")
        return material
    include_rel = _normalise(include)
    material.includes.append(include_rel)
    if include_rel in seen or depth >= _MAX_INCLUDE_DEPTH:
        material.warnings.append(f"include loop through {include_rel}")
        return material

    seen.add(rel)
    base = _load(source, include_rel, seen, depth + 1)
    if base is None:
        # the base is missing (shipped content has a few of these); keep what
        # the patch itself says so at least its textures resolve
        material.warnings.append(f"included material {include_rel} not found")
        for block_name in ("insert", "replace"):
            block = root.block(block_name)
            if block is not None:
                _apply_block(block, material)
        return material

    # the patch keeps its own identity but the base's shader and parameters
    merged = Material(path=material.path, shader=base.shader,
                      params=dict(base.params), proxies=list(base.proxies),
                      includes=[include_rel] + base.includes,
                      warnings=base.warnings + material.warnings)
    for block_name in ("insert", "replace"):
        block = root.block(block_name)
        if block is not None:
            _apply_block(block, merged)
    return merged
