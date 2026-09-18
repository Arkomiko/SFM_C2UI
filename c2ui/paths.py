"""
Where C2UI keeps its files.

C2UI is **portable**: it never writes outside its own folder.  Settings, layouts,
logs, thumbnails and every cache live under ``<app root>/User Data``, so the whole
editor can be copied to another disk or machine and keep working.

    User Data/
        settings.json          application settings
        layouts/               saved window layouts
        logs/                  rotating log files
        sessions/              recovery / autosave data
        Cache/                 everything regenerable - safe to delete
            content/           content index of the mounted SFM install
            thumbnails/        model and material previews
            materials/         decoded textures
            shaders/           compiled shader cache

Nothing here touches %APPDATA% or the SFM installation.  The only exception a user
can request is ``C2UI_USER_DATA``, an environment variable used by the test suite
to redirect the whole tree somewhere disposable.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

__all__ = [
    "APP_ROOT", "PACKAGE_DIR", "RESOURCES_DIR",
    "USER_DATA", "SETTINGS_FILE", "LAYOUTS_DIR", "LOGS_DIR", "SESSIONS_DIR",
    "CACHE_DIR", "CONTENT_CACHE_DIR", "THUMBNAIL_CACHE_DIR", "MATERIAL_CACHE_DIR", "SHADER_CACHE_DIR",
    "ensure_dirs", "cache_dirs", "clear_cache", "describe",
]

# --- application tree (read-only at runtime) ---------------------------------
PACKAGE_DIR: Path = Path(__file__).resolve().parent          # .../c2ui
APP_ROOT: Path = PACKAGE_DIR.parent                          # the folder to ship
RESOURCES_DIR: Path = APP_ROOT / "resources"


def _user_data_root() -> Path:
    """``<app root>/User Data`` unless a test redirects it."""
    override = os.environ.get("C2UI_USER_DATA")
    return Path(override).expanduser() if override else APP_ROOT / "User Data"


# --- writable tree (everything the app produces) ------------------------------
USER_DATA: Path = _user_data_root()
SETTINGS_FILE: Path = USER_DATA / "settings.json"
LAYOUTS_DIR: Path = USER_DATA / "layouts"
LOGS_DIR: Path = USER_DATA / "logs"
SESSIONS_DIR: Path = USER_DATA / "sessions"

CACHE_DIR: Path = USER_DATA / "Cache"
CONTENT_CACHE_DIR: Path = CACHE_DIR / "content"
THUMBNAIL_CACHE_DIR: Path = CACHE_DIR / "thumbnails"
MATERIAL_CACHE_DIR: Path = CACHE_DIR / "materials"
SHADER_CACHE_DIR: Path = CACHE_DIR / "shaders"

_ALL_DIRS = (USER_DATA, LAYOUTS_DIR, LOGS_DIR, SESSIONS_DIR,
             CACHE_DIR, CONTENT_CACHE_DIR, THUMBNAIL_CACHE_DIR, MATERIAL_CACHE_DIR, SHADER_CACHE_DIR)


def ensure_dirs() -> None:
    """Create the writable tree.  Cheap and idempotent; call once at startup."""
    for d in _ALL_DIRS:
        d.mkdir(parents=True, exist_ok=True)


def cache_dirs() -> Iterable[Path]:
    return (CONTENT_CACHE_DIR, THUMBNAIL_CACHE_DIR, MATERIAL_CACHE_DIR, SHADER_CACHE_DIR)


def clear_cache() -> int:
    """Delete every regenerable file.  Returns how many files were removed."""
    import shutil

    removed = 0
    for d in cache_dirs():
        if not d.is_dir():
            continue
        for entry in d.iterdir():
            try:
                if entry.is_dir():
                    removed += sum(1 for _ in entry.rglob("*") if _.is_file())
                    shutil.rmtree(entry)
                else:
                    entry.unlink()
                    removed += 1
            except OSError:
                pass
    ensure_dirs()
    return removed


def is_inside_app(path) -> bool:
    """True when ``path`` lives under the application folder.

    Used by the tests that guard the portability rule: C2UI must not write
    anywhere else.
    """
    try:
        Path(path).resolve().relative_to(APP_ROOT)
        return True
    except (ValueError, OSError):
        return False


def describe() -> str:
    return f"app={APP_ROOT}  user data={USER_DATA}"
