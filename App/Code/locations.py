"""
Where the editor's folders are.

App owns every writable path; Core is handed the ones it needs and never looks
for them itself. Nothing here points outside the application folder, so C2UI
stays portable - copy the folder to another disk and it keeps working.
"""
from __future__ import annotations

import os
import shutil
import uuid
from pathlib import Path
from typing import Iterable

__all__ = [
    "APP_ROOT", "PROJECT_ROOT",
    "DATA", "USER", "CACHE", "TEMPORARY", "LEGAL",
    "SETTINGS", "CONTENT_CACHE", "THUMBNAIL_CACHE", "MATERIAL_CACHE", "SHADER_CACHE",
    "ensure_dirs", "new_session_dir", "clear_temporary", "clear_cache", "is_inside_app",
]

#: .../C2UI_SDK/App
APP_ROOT: Path = Path(__file__).resolve().parents[1]
#: .../C2UI_SDK
PROJECT_ROOT: Path = APP_ROOT.parent

# what ships with the program
DATA: Path = APP_ROOT / "Data"
LEGAL: Path = APP_ROOT / "Legal"

# what belongs to the user - never deleted automatically
USER: Path = APP_ROOT / "User"
SETTINGS: Path = USER / "Settings"
USER_THEMES: Path = USER / "Themes"
USER_WORKSPACES: Path = USER / "Workspaces"
USER_LOCALES: Path = USER / "Locales"
USER_PLUGINS: Path = USER / "Plug-ins"

# regenerable, shared by every session, kept across restarts
CACHE: Path = APP_ROOT / "Cache"
CONTENT_CACHE: Path = CACHE / "content"
THUMBNAIL_CACHE: Path = CACHE / "thumbnails"
MATERIAL_CACHE: Path = CACHE / "materials"
SHADER_CACHE: Path = CACHE / "shaders"

# per-session scratch, cleared on start
TEMPORARY: Path = APP_ROOT / "Temporary"

_WRITABLE = (USER, SETTINGS, USER_THEMES, USER_WORKSPACES, USER_LOCALES, USER_PLUGINS,
             CACHE, CONTENT_CACHE, THUMBNAIL_CACHE, MATERIAL_CACHE, SHADER_CACHE, TEMPORARY)


def ensure_dirs() -> None:
    """Create the writable tree.  Cheap and idempotent; call once at startup."""
    for d in _WRITABLE:
        d.mkdir(parents=True, exist_ok=True)


def new_session_dir() -> Path:
    """A fresh scratch folder for this run of the editor."""
    TEMPORARY.mkdir(parents=True, exist_ok=True)
    folder = TEMPORARY / uuid.uuid4().hex[:12]
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _is_placeholder(entry: Path) -> bool:
    """Dot-files such as .gitkeep keep an empty folder present in the project.

    Cleaning must never remove them: the folders themselves are part of the
    application, only their contents are disposable.
    """
    return entry.name.startswith(".")


def clear_temporary(keep: Iterable[Path] = ()) -> int:
    """Remove session folders left behind, including by a crashed run.

    Returns how many were removed. Never touches `User` or `Cache`.
    """
    if not TEMPORARY.is_dir():
        return 0
    protect = {Path(p).resolve() for p in keep}
    removed = 0
    for entry in TEMPORARY.iterdir():
        try:
            if _is_placeholder(entry) or entry.resolve() in protect:
                continue
            if entry.is_dir():
                shutil.rmtree(entry, ignore_errors=True)
            else:
                entry.unlink()
            removed += 1
        except OSError:
            pass
    return removed


def clear_cache() -> int:
    """Delete every regenerable file.  Returns how many were removed."""
    removed = 0
    for folder in (CONTENT_CACHE, THUMBNAIL_CACHE, MATERIAL_CACHE, SHADER_CACHE):
        if not folder.is_dir():
            continue
        for entry in folder.iterdir():
            try:
                if _is_placeholder(entry):
                    continue
                if entry.is_dir():
                    removed += sum(1 for _ in entry.rglob("*") if _.is_file())
                    shutil.rmtree(entry, ignore_errors=True)
                else:
                    entry.unlink()
                    removed += 1
            except OSError:
                pass
    ensure_dirs()
    return removed


def is_inside_app(path) -> bool:
    """True when `path` lives under the application folder.

    The portability rule is asserted by the tests rather than trusted.
    """
    try:
        Path(path).resolve().relative_to(PROJECT_ROOT)
        return True
    except (ValueError, OSError):
        return False


def describe() -> str:
    """One line: app, cache and user folders."""
    return f"app={APP_ROOT} cache={CACHE} user={USER}"
