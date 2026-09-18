"""
Where Core's own folders are.

Core knows about *itself* only. It never looks for the user's settings, cache or
installed games - those paths arrive from `App` through `Core.API`, which is
what keeps the engine read-only and usable from `Program Files`.
"""
from __future__ import annotations

from pathlib import Path

__all__ = ["CORE_ROOT", "PROJECT_ROOT", "DEV_KIT", "RESOURCES", "sdk_slot", "sdk_is_filled"]

#: .../C2UI_SDK/Core
CORE_ROOT: Path = Path(__file__).resolve().parents[1]
#: .../C2UI_SDK
PROJECT_ROOT: Path = CORE_ROOT.parent

DEV_KIT: Path = CORE_ROOT / "dev-kit"
RESOURCES: Path = CORE_ROOT / "Resources"

#: A slot holding only this file counts as empty.
SDK_PLACEHOLDER = "PLACE_SDK_HERE.md"


def sdk_slot(name: str) -> Path:
    """Folder for an SDK, e.g. ``sdk_slot("sfm_sdk")``."""
    return DEV_KIT / name


def sdk_is_filled(name: str) -> bool:
    """True when someone has actually placed the SDK in its slot."""
    folder = sdk_slot(name)
    if not folder.is_dir():
        return False
    return any(p.name != SDK_PLACEHOLDER for p in folder.iterdir())
