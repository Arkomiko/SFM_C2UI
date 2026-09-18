"""
Central path registry for C2UI.

Two different kinds of paths live here:

* **SDK paths** (Core/, Themes/, Workspaces/, ...) are fixed relative to this file.
* **SFM paths** are *runtime configurable*: C2UI ships as a standalone shell and must
  start even when Source Filmmaker is missing.  Use the accessor functions
  (:func:`sfm_root`, :func:`sfm_exe`, ...) - they re-evaluate the currently configured
  root and return ``None`` when SFM is not available.

Resolution order for the SFM root (the folder that contains ``game/sfm.exe``):

1. ``set_sfm_root()`` - what the user picked in Preferences (persisted in settings)
2. ``C2UI_SFM_ROOT`` environment variable
3. auto-detection: the SDK's parent folder, then every Steam library on the machine

Legacy module constants (``paths.SFM_GAME_DIR`` etc.) still work through PEP 562
``__getattr__`` and always reflect the *current* root, but new code should call the
functions so the "not configured" case stays explicit.
"""
from __future__ import annotations

import logging
import os
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

log = logging.getLogger("c2ui.paths")

# --- SDK tree (always available) ----------------------------------------------
SDK_ROOT: Path = Path(__file__).resolve().parents[2]          # .../C2UI_SDK
CORE_DIR: Path = SDK_ROOT / "Core"
API_DIR: Path = CORE_DIR / "API"
LIBRARY_DIR: Path = CORE_DIR / "Library"
SCRIPTS_DIR: Path = CORE_DIR / "Scripts"
AGENT_DIR: Path = API_DIR / "agent"
WORKSPACES_DIR: Path = SDK_ROOT / "Workspaces"
THEMES_DIR: Path = SDK_ROOT / "Themes"
LOCALES_DIR: Path = SDK_ROOT / "Locales"
ASSETS_DIR: Path = SDK_ROOT / "Assets"
ICONS_DIR: Path = ASSETS_DIR / "icons"
FONTS_DIR: Path = ASSETS_DIR / "fonts"


# --- Per-user data (kept *outside* the SDK tree) -------------------------------
def _default_user_dir() -> Path:
    override = os.environ.get("C2UI_USER_DIR")
    if override:
        return Path(override)
    base = os.environ.get("LOCALAPPDATA") or os.environ.get("XDG_CONFIG_HOME") or str(Path.home())
    return Path(base) / "C2UI"


USER_DIR: Path = _default_user_dir()
USER_SETTINGS_FILE: Path = USER_DIR / "settings.json"
USER_LAYOUTS_DIR: Path = USER_DIR / "layouts"
USER_THEMES_DIR: Path = USER_DIR / "themes"
USER_LOGS_DIR: Path = USER_DIR / "logs"
USER_CACHE_DIR: Path = USER_DIR / "cache"


def ensure_user_dirs() -> None:
    for d in (USER_DIR, USER_LAYOUTS_DIR, USER_THEMES_DIR, USER_LOGS_DIR, USER_CACHE_DIR):
        d.mkdir(parents=True, exist_ok=True)


# =============================================================================
#  SFM installation (runtime configurable, may be absent)
# =============================================================================
_sfm_root: Optional[Path] = None          # None = not configured / not found yet
_detect_cache: Optional[Path] = None
_detect_done = False


def validate_sfm_root(candidate) -> Tuple[bool, str]:
    """Check whether ``candidate`` is a usable SFM installation.

    Accepts the install folder, its ``game`` sub-folder or ``sfm.exe`` itself and
    returns ``(ok, normalised_root_or_reason)``.
    """
    if not candidate:
        return False, "empty path"
    p = Path(candidate).expanduser()
    try:
        p = p.resolve()
    except OSError:
        return False, "invalid path"
    # Accept sfm.exe directly, or a "game" folder, or the install root.
    if p.is_file() and p.name.lower() == "sfm.exe":
        p = p.parent.parent
    elif p.name.lower() == "game" and (p / "sfm.exe").is_file():
        p = p.parent
    if not p.is_dir():
        return False, "folder does not exist"
    if not (p / "game" / "sfm.exe").is_file():
        return False, "game/sfm.exe not found in this folder"
    return True, str(p)


def set_sfm_root(candidate, validate: bool = True) -> Tuple[bool, str]:
    """Point C2UI at an SFM installation.  Returns ``(ok, normalised_root_or_reason)``."""
    global _sfm_root
    if not candidate:
        _sfm_root = None
        return True, ""
    if validate:
        ok, result = validate_sfm_root(candidate)
        if not ok:
            return False, result
        _sfm_root = Path(result)
    else:
        _sfm_root = Path(candidate).expanduser()
    log.info("SFM root set to %s", _sfm_root)
    return True, str(_sfm_root)


def sfm_root() -> Optional[Path]:
    """Currently configured SFM install folder, or ``None`` when unavailable."""
    if _sfm_root is not None:
        return _sfm_root
    env = os.environ.get("C2UI_SFM_ROOT")
    if env:
        ok, result = validate_sfm_root(env)
        if ok:
            return Path(result)
    return detect_sfm_root()


def sfm_is_configured() -> bool:
    """True when a root is set or detectable (does not re-validate the exe)."""
    return sfm_root() is not None


def sfm_is_installed() -> bool:
    """True when sfm.exe is actually present at the configured root."""
    exe = sfm_exe()
    return bool(exe and exe.is_file())


def _sub(*parts: str) -> Optional[Path]:
    root = sfm_root()
    return root.joinpath(*parts) if root else None


def sfm_game_dir() -> Optional[Path]:
    return _sub("game")


def sfm_exe() -> Optional[Path]:
    return _sub("game", "sfm.exe")


def sfm_bin_dir() -> Optional[Path]:
    return _sub("game", "bin")


def sfm_usermod_dir() -> Optional[Path]:
    return _sub("game", "usermod")


def sfm_usermod_scripts_dir() -> Optional[Path]:
    return _sub("game", "usermod", "scripts", "sfm")


def sfm_py27_dir() -> Optional[Path]:
    return _sub("game", "sdktools", "python", "2.7", "win32")


def sfm_py27_exe() -> Optional[Path]:
    return _sub("game", "sdktools", "python", "2.7", "win32", "python.exe")


def sfm_layouts_dir() -> Optional[Path]:
    return _sub("game", "platform", "tools", "layouts", "sfm")


# --- auto detection ------------------------------------------------------------
def detect_sfm_root(force: bool = False) -> Optional[Path]:
    """Best-effort search for an SFM installation.  Cached after the first run."""
    global _detect_cache, _detect_done
    if _detect_done and not force:
        return _detect_cache
    _detect_done = True
    _detect_cache = None
    for candidate in _detection_candidates():
        ok, result = validate_sfm_root(candidate)
        if ok:
            _detect_cache = Path(result)
            log.info("Auto-detected SFM installation: %s", _detect_cache)
            break
    else:
        log.info("No SFM installation auto-detected")
    return _detect_cache


def _detection_candidates() -> List[Path]:
    out: List[Path] = []

    def add(p) -> None:
        if p:
            p = Path(p)
            if p not in out:
                out.append(p)

    # C2UI unpacked inside the SFM folder (the classic layout)
    add(SDK_ROOT.parent)
    add(SDK_ROOT.parent.parent)
    # Steam libraries
    for lib in _steam_libraries():
        add(lib / "steamapps" / "common" / "SourceFilmmaker")
    # Last-resort well-known locations
    if sys.platform == "win32":
        for drive in ("C:", "D:", "E:"):
            add(Path(f"{drive}/Program Files (x86)/Steam/steamapps/common/SourceFilmmaker"))
            add(Path(f"{drive}/SteamLibrary/steamapps/common/SourceFilmmaker"))
    return out


def _steam_libraries() -> List[Path]:
    """Every Steam library folder known to the local Steam client."""
    libs: List[Path] = []
    steam = _steam_path()
    if steam is None:
        return libs
    libs.append(steam)
    vdf = steam / "steamapps" / "libraryfolders.vdf"
    if vdf.is_file():
        try:
            text = vdf.read_text(encoding="utf-8", errors="replace")
            # matches both the old ("1" "D:\\Games") and new ("path" "D:\\Games") formats
            for match in re.finditer(r'"(?:\d+|path)"\s*"([^"]+)"', text):
                p = Path(match.group(1).replace("\\\\", "\\"))
                if p.is_dir() and p not in libs:
                    libs.append(p)
        except OSError:
            log.debug("Could not read %s", vdf)
    return libs


def _steam_path() -> Optional[Path]:
    if sys.platform != "win32":
        return None
    try:
        import winreg
    except ImportError:
        return None
    for hive, key in ((winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam"),
                      (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")):
        for value in ("SteamPath", "InstallPath"):
            try:
                with winreg.OpenKey(hive, key) as k:
                    raw, _ = winreg.QueryValueEx(k, value)
                p = Path(str(raw))
                if p.is_dir():
                    return p
            except OSError:
                continue
    return None


# --- legacy constant access (always reflects the current root) ------------------
_LEGACY = {
    "SFM_ROOT": sfm_root,
    "SFM_GAME_DIR": sfm_game_dir,
    "SFM_EXE": sfm_exe,
    "SFM_BIN_DIR": sfm_bin_dir,
    "SFM_USERMOD_DIR": sfm_usermod_dir,
    "SFM_USERMOD_SCRIPTS_DIR": sfm_usermod_scripts_dir,
    "SFM_PY27_DIR": sfm_py27_dir,
    "SFM_PY27_EXE": sfm_py27_exe,
    "SFM_LAYOUTS_DIR": sfm_layouts_dir,
}


def __getattr__(name: str):          # PEP 562
    fn = _LEGACY.get(name)
    if fn is not None:
        return fn()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
