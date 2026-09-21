"""
Bridge to a Source Filmmaker installation.

Mounts SFM the way the engine itself does: read `usermod/gameinfo.txt`, expand
its `FileSystem/SearchPaths` block and hand back the content roots in priority
order. C2UI then reads models, materials, sounds and sessions straight off disk.

sfm.exe is never launched and never touched.
"""
from __future__ import annotations

import logging
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from Core.API import Availability, Mount, MountSet, ProbeResult, SourceBridge
from Core.Code.keyvalues import KeyValues
from Core.Code.keyvalues import load as load_kv

log = logging.getLogger("c2ui.bridge.sfm")

#: Search-path roles that carry content. Others (bin paths, cache write paths)
#: are listed in gameinfo.txt too and must be skipped.
CONTENT_ROLES = frozenset({"game", "mod", "default_write_path"})

#: The tool mod whose gameinfo.txt describes SFM's own mounts.
MOD_FOLDER = "usermod"


class SFMBridge(SourceBridge):
    """Reads an installed Source Filmmaker."""

    ID = "sfm"
    NAME = "Source Filmmaker"
    REQUIRES_SDK = None            # mounting needs no SDK, only the installation

    APP_ID = 1840

    # ------------------------------------------------------------------ discover
    def discover(self) -> List[Path]:
        """Every place an installation might be, best guess first."""
        found: List[Path] = []

        def add(candidate) -> None:
            """Record a candidate once."""
            if not candidate:
                return
            p = Path(candidate)
            if p not in found:
                found.append(p)

        add(os.environ.get("C2UI_SFM_ROOT"))
        for library in _steam_libraries():
            add(library / "steamapps" / "common" / "SourceFilmmaker")
        if sys.platform == "win32":
            for drive in ("C:", "D:", "E:", "F:"):
                add(Path(f"{drive}/Program Files (x86)/Steam/steamapps/common/SourceFilmmaker"))
                add(Path(f"{drive}/SteamLibrary/steamapps/common/SourceFilmmaker"))
        return [p for p in found if self.probe(p).ok]

    # --------------------------------------------------------------------- probe
    def probe(self, path) -> ProbeResult:
        """Is there a usable Source Filmmaker at `path`?

        Accepts the install folder, its `game` folder or `sfm.exe` itself, so a
        user can paste whichever path they happen to have.
        """
        if not path:
            return ProbeResult.failed(Availability.NOT_CONFIGURED, "no path given")
        try:
            p = Path(path).expanduser().resolve()
        except OSError as exc:
            return ProbeResult.failed(Availability.INVALID, f"unusable path ({exc})")

        root = _normalise_root(p)
        if root is None:
            return ProbeResult.failed(Availability.NOT_FOUND, "folder does not exist", p)

        game = root / "game"
        if not game.is_dir():
            return ProbeResult.failed(
                Availability.INVALID, "no 'game' folder here - is this the Source Filmmaker folder?", root)
        gameinfo = game / MOD_FOLDER / "gameinfo.txt"
        if not gameinfo.is_file():
            return ProbeResult.failed(
                Availability.INVALID, f"game/{MOD_FOLDER}/gameinfo.txt is missing", root)

        title = self.NAME
        try:
            title = load_kv(gameinfo).get_str("game") or title
        except (OSError, ValueError):
            pass                      # a readable folder with an odd gameinfo is still usable
        return ProbeResult.available(root, title)

    # --------------------------------------------------------------------- mount
    def mount(self, path) -> MountSet:
        """Expand gameinfo.txt into ordered content roots."""
        result = self.probe(path)
        if not result.ok or result.root is None:
            return MountSet(self.ID, self.NAME, warnings=[result.detail])

        root = result.root
        game = root / "game"
        mod_dir = game / MOD_FOLDER
        warnings: List[str] = []

        try:
            gameinfo = load_kv(mod_dir / "gameinfo.txt")
        except (OSError, ValueError) as exc:
            return MountSet(self.ID, result.title, root,
                            warnings=[f"gameinfo.txt could not be read ({exc})"])

        entries = _search_path_entries(gameinfo, warnings)
        mounts = _build_mounts(entries, game, mod_dir, self.ID, warnings)
        if not mounts:
            warnings.append("gameinfo.txt lists no usable content paths")

        log.info("Mounted %d content paths from %s", len(mounts), game)
        return MountSet(self.ID, result.title, root, mounts, warnings)


# ---------------------------------------------------------------------------
#  gameinfo.txt
# ---------------------------------------------------------------------------
def _search_path_entries(gameinfo: KeyValues, warnings: List[str]) -> List[Tuple[str, str]]:
    search = gameinfo.path("FileSystem", "SearchPaths")
    if search is None:
        warnings.append("gameinfo.txt has no FileSystem/SearchPaths block; mounting the mod folder only")
        return [("Game", "|gameinfo_path|.")]
    return search.pairs()


def _build_mounts(entries, game: Path, mod_dir: Path, source_id: str,
                  warnings: List[str]) -> List[Mount]:
    mounts: List[Mount] = []
    index: Dict[Path, int] = {}
    for roles_raw, raw_path in entries:
        roles = tuple(r.strip().lower() for r in roles_raw.split("+") if r.strip())
        if not roles or not (set(roles) & CONTENT_ROLES):
            continue                      # bin paths and cache write paths
        resolved = _resolve(raw_path, game, mod_dir)
        if resolved is None:
            continue                      # .vpk entries and malformed values
        if not resolved.is_dir():
            warnings.append(f"search path does not exist: {raw_path}")
            continue
        if resolved in index:
            # the same folder listed twice keeps its first, higher priority
            position = index[resolved]
            existing = mounts[position]
            merged = tuple(dict.fromkeys(existing.roles + _public_roles(roles)))
            mounts[position] = Mount(existing.name, existing.path, position, merged, source_id)
            continue
        index[resolved] = len(mounts)
        mounts.append(Mount(
            name=resolved.name or str(resolved),
            path=resolved,
            priority=len(mounts),
            roles=_public_roles(roles),
            source_id=source_id,
        ))
    return mounts


def _public_roles(roles: Tuple[str, ...]) -> Tuple[str, ...]:
    """Translate engine role names into the ones the API exposes."""
    out = []
    for role in roles:
        out.append("write" if role == "default_write_path" else role)
    return tuple(dict.fromkeys(out))


def _resolve(raw: str, game: Path, mod_dir: Path) -> Optional[Path]:
    """Expand the engine's path tokens and make the result absolute."""
    value = raw.strip().strip('"')
    if not value:
        return None
    value = value.replace("|gameinfo_path|", str(mod_dir) + os.sep)
    value = value.replace("|all_source_engine_paths|", str(game) + os.sep)
    if value.lower().endswith(".vpk"):
        return None                       # loose-file installations only, for now
    p = Path(value)
    if not p.is_absolute():
        p = game / p
    try:
        return Path(os.path.normpath(str(p)))
    except (OSError, ValueError):
        return None


def _normalise_root(p: Path) -> Optional[Path]:
    """Turn any of install / install/game / install/game/sfm.exe into install."""
    if p.is_file():
        return p.parent.parent if p.name.lower() == "sfm.exe" else None
    if p.name.lower() == "game" and p.is_dir():
        return p.parent
    return p if p.is_dir() else None


# ---------------------------------------------------------------------------
#  Steam
# ---------------------------------------------------------------------------
def _steam_path() -> Optional[Path]:
    if sys.platform != "win32":
        return None
    try:
        import winreg
    except ImportError:
        return None
    for hive, key in ((getattr(winreg, "HKEY_CURRENT_USER"), r"Software\Valve\Steam"),
                      (getattr(winreg, "HKEY_LOCAL_MACHINE"), r"SOFTWARE\WOW6432Node\Valve\Steam")):
        for value in ("SteamPath", "InstallPath"):
            try:
                with winreg.OpenKey(hive, key) as handle:
                    raw, _ = winreg.QueryValueEx(handle, value)
                candidate = Path(str(raw))
                if candidate.is_dir():
                    return candidate
            except OSError:
                continue
    return None


def _steam_libraries() -> List[Path]:
    """Every Steam library folder the local client knows about."""
    libraries: List[Path] = []
    steam = _steam_path()
    if steam is None:
        return libraries
    libraries.append(steam)
    vdf = steam / "steamapps" / "libraryfolders.vdf"
    if not vdf.is_file():
        return libraries
    try:
        text = vdf.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return libraries
    # both the old ("1" "D:\\Games") and new ("path" "D:\\Games") layouts
    for match in re.finditer(r'"(?:\d+|path)"\s*"([^"]+)"', text):
        candidate = Path(match.group(1).replace("\\\\", "\\"))
        if candidate.is_dir() and candidate not in libraries:
            libraries.append(candidate)
    return libraries
