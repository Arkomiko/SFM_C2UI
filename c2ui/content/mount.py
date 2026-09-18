"""
Mounting a Source Filmmaker installation.

C2UI is a standalone editor: it never launches sfm.exe and never drives its
windows.  Instead it *mounts* an SFM installation the way the engine itself does
- by reading ``usermod/gameinfo.txt`` and turning its ``SearchPaths`` block into
an ordered list of content roots - and then reads models, materials, sounds and
sessions straight off disk.

    install = SFMInstall.discover()          # or SFMInstall(path)
    install.validate()                       # -> MountReport
    for m in install.mounts: print(m.name, m.path)

Search-path rules implemented here (engine behaviour):

* ``|gameinfo_path|`` expands to the folder holding gameinfo.txt
* ``|all_source_engine_paths|`` expands to the base directory (``game/``)
* a path may carry several roles (``Game+Mod``); only content roles are mounted
* the first ``Game`` path is the mod root and the default write target
* duplicates keep their first (highest priority) position
"""
from __future__ import annotations

import logging
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from .keyvalues import KeyValues, load as load_kv

log = logging.getLogger("c2ui.mount")

__all__ = ["Mount", "MountReport", "SFMInstall", "discover_sfm", "validate_sfm_path"]

#: Search-path roles that carry content we care about.
CONTENT_ROLES = {"game", "mod", "default_write_path"}

#: Sub-folders that make a mount interesting, in the order we report them.
CONTENT_DIRS = ("models", "materials", "sound", "maps", "particles", "scripts", "elements")


@dataclass(frozen=True)
class Mount:
    """One content root, in engine search order (index 0 wins)."""

    name: str                 # folder name, e.g. "usermod", "tf"
    path: Path
    roles: Tuple[str, ...]    # game / mod / default_write_path / ...
    index: int

    @property
    def is_writable(self) -> bool:
        return "default_write_path" in self.roles or "mod" in self.roles

    def has(self, sub: str) -> bool:
        return (self.path / sub).is_dir()

    def content_dirs(self) -> List[str]:
        return [d for d in CONTENT_DIRS if self.has(d)]


@dataclass
class MountReport:
    """Result of validating an installation - drives the UI's setup screen."""

    ok: bool
    root: Optional[Path] = None
    game_dir: Optional[Path] = None
    reason: str = ""
    mounts: List[Mount] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def summary(self) -> str:
        if not self.ok:
            return self.reason
        return f"{len(self.mounts)} content paths mounted from {self.game_dir}"


# ---------------------------------------------------------------------------
#  Validation & discovery
# ---------------------------------------------------------------------------
def validate_sfm_path(candidate) -> Tuple[bool, str]:
    """Accept the install folder, its ``game`` folder or ``sfm.exe`` itself.

    Returns ``(ok, normalised_root)`` or ``(False, reason)``.
    """
    if not candidate:
        return False, "empty path"
    p = Path(str(candidate)).expanduser()
    try:
        p = p.resolve()
    except OSError:
        return False, "invalid path"
    if p.is_file():
        if p.name.lower() != "sfm.exe":
            return False, "not sfm.exe"
        p = p.parent.parent
    elif p.name.lower() == "game" and (p / "gameinfo.txt").is_file():
        p = p.parent
    elif p.name.lower() == "game":
        p = p.parent
    if not p.is_dir():
        return False, "folder does not exist"
    game = p / "game"
    if not game.is_dir():
        return False, "no 'game' folder here"
    if not (game / "usermod" / "gameinfo.txt").is_file():
        return False, "game/usermod/gameinfo.txt is missing"
    return True, str(p)


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


def _steam_libraries() -> List[Path]:
    libs: List[Path] = []
    steam = _steam_path()
    if steam is None:
        return libs
    libs.append(steam)
    vdf = steam / "steamapps" / "libraryfolders.vdf"
    if vdf.is_file():
        try:
            text = vdf.read_text(encoding="utf-8", errors="replace")
            for match in re.finditer(r'"(?:\d+|path)"\s*"([^"]+)"', text):
                p = Path(match.group(1).replace("\\\\", "\\"))
                if p.is_dir() and p not in libs:
                    libs.append(p)
        except OSError:
            pass
    return libs


def discover_sfm(extra: Sequence[Path] = ()) -> Optional[Path]:
    """Best-effort search for an SFM installation (Steam libraries first)."""
    candidates: List[Path] = [Path(p) for p in extra]
    env = os.environ.get("C2UI_SFM_ROOT")
    if env:
        candidates.append(Path(env))
    for lib in _steam_libraries():
        candidates.append(lib / "steamapps" / "common" / "SourceFilmmaker")
    if sys.platform == "win32":
        for drive in ("C:", "D:", "E:", "F:"):
            candidates.append(Path(f"{drive}/Program Files (x86)/Steam/steamapps/common/SourceFilmmaker"))
            candidates.append(Path(f"{drive}/SteamLibrary/steamapps/common/SourceFilmmaker"))
    seen = set()
    for c in candidates:
        if c in seen:
            continue
        seen.add(c)
        ok, result = validate_sfm_path(c)
        if ok:
            log.info("Found Source Filmmaker at %s", result)
            return Path(result)
    return None


# ---------------------------------------------------------------------------
#  The installation
# ---------------------------------------------------------------------------
class SFMInstall:
    """A mounted Source Filmmaker installation."""

    #: gameinfo.txt of the mod we mount (SFM's own tool mod).
    MOD = "usermod"

    def __init__(self, root) -> None:
        self.root = Path(root)
        self.mounts: List[Mount] = []
        self.gameinfo: Optional[KeyValues] = None
        self._report: Optional[MountReport] = None

    # -- factory ---------------------------------------------------------------
    @classmethod
    def discover(cls) -> Optional["SFMInstall"]:
        found = discover_sfm()
        return cls(found) if found else None

    # -- paths -----------------------------------------------------------------
    @property
    def game_dir(self) -> Path:
        return self.root / "game"

    @property
    def mod_dir(self) -> Path:
        return self.game_dir / self.MOD

    @property
    def exe(self) -> Path:
        """Only used to show the user what was found - C2UI never runs it."""
        return self.game_dir / "sfm.exe"

    @property
    def write_dir(self) -> Path:
        """Where new user content belongs (the mod root, like the engine)."""
        for m in self.mounts:
            if m.is_writable:
                return m.path
        return self.mod_dir

    # -- mounting --------------------------------------------------------------
    def validate(self) -> MountReport:
        """Check the installation and build the mount list.  Never raises."""
        ok, result = validate_sfm_path(self.root)
        if not ok:
            self._report = MountReport(ok=False, reason=result)
            return self._report
        self.root = Path(result)
        warnings: List[str] = []
        try:
            self.gameinfo = load_kv(self.mod_dir / "gameinfo.txt")
        except (OSError, ValueError) as exc:
            self._report = MountReport(ok=False, reason=f"gameinfo.txt could not be read ({exc})")
            return self._report

        self.mounts = self._build_mounts(warnings)
        if not self.mounts:
            self._report = MountReport(ok=False, root=self.root, game_dir=self.game_dir,
                                       reason="gameinfo.txt lists no usable content paths")
            return self._report
        self._report = MountReport(ok=True, root=self.root, game_dir=self.game_dir,
                                   mounts=self.mounts, warnings=warnings)
        log.info("Mounted %d content paths from %s", len(self.mounts), self.game_dir)
        return self._report

    def _build_mounts(self, warnings: List[str]) -> List[Mount]:
        search = None
        fs = self.gameinfo.block("FileSystem") if self.gameinfo else None
        if fs is not None:
            search = fs.block("SearchPaths")
        if search is None:
            warnings.append("gameinfo.txt has no FileSystem/SearchPaths block; mounting the mod folder only")
            entries: List[Tuple[str, str]] = [("Game", "|gameinfo_path|.")]
        else:
            entries = [(k, v) for k, v in search.items() if isinstance(v, str)]

        mounts: List[Mount] = []
        seen: Dict[Path, int] = {}
        for roles_raw, raw_path in entries:
            roles = tuple(r.strip().lower() for r in roles_raw.split("+") if r.strip())
            if not roles or not (set(roles) & CONTENT_ROLES):
                continue                      # bins, write paths for caches, platform-only entries
            resolved = self._resolve(raw_path)
            if resolved is None:
                continue
            if not resolved.is_dir():
                warnings.append(f"search path does not exist: {raw_path}")
                continue
            if resolved in seen:              # keep the first (highest priority) occurrence
                idx = seen[resolved]
                merged = tuple(dict.fromkeys(mounts[idx].roles + roles))
                mounts[idx] = Mount(mounts[idx].name, resolved, merged, idx)
                continue
            seen[resolved] = len(mounts)
            mounts.append(Mount(resolved.name or str(resolved), resolved, roles, len(mounts)))
        return mounts

    def _resolve(self, raw: str) -> Optional[Path]:
        """Expand engine tokens and make the path absolute."""
        value = raw.strip().strip('"')
        if not value or value.startswith("|all_source_engine_paths|") and value.endswith(".vpk"):
            return None
        value = value.replace("|gameinfo_path|", str(self.mod_dir) + os.sep)
        value = value.replace("|all_source_engine_paths|", str(self.game_dir) + os.sep)
        if value.lower().endswith(".vpk"):
            return None                      # loose-file installs only, for now
        p = Path(value)
        if not p.is_absolute():
            p = self.game_dir / p
        try:
            return Path(os.path.normpath(str(p)))
        except (OSError, ValueError):
            return None

    # -- info ------------------------------------------------------------------
    @property
    def report(self) -> MountReport:
        return self._report if self._report is not None else self.validate()

    @property
    def is_mounted(self) -> bool:
        return bool(self.mounts)

    def title(self) -> str:
        if self.gameinfo is not None:
            name = self.gameinfo.get_str("game")
            if name:
                return name
        return "Source Filmmaker"

    def describe(self) -> str:
        return f"{self.title()} - {len(self.mounts)} mounts at {self.game_dir}"

    def __repr__(self) -> str:
        return f"SFMInstall({str(self.root)!r}, mounts={len(self.mounts)})"
