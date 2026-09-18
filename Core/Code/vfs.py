"""
Virtual file system over mounted content roots.

Source games layer their content: the same relative path may exist in several
mounts, and the first one wins. `usermod/models/x.mdl` overrides
`tf/models/x.mdl` without either knowing about the other. The VFS gives that
behaviour one place to live.

    vfs = VirtualFileSystem(mount_set)
    vfs.resolve("models/player/scout.mdl")     -> Path | None
    vfs.overrides("materials/x.vmt")           -> every mount that has it
    vfs.glob("models/**/*.mdl", limit=100)     -> VirtualFile entries
    vfs.read_bytes("scripts/game_sounds.txt")

Paths are always relative, `/`-separated and case-insensitive, because that is
how Valve's own paths are written. A path that tries to escape its mount
(`..`, absolute, a drive letter) is rejected.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Union

from Core.API.types import Mount, MountSet

__all__ = ["VirtualFile", "VirtualFileSystem", "normalise"]

log = logging.getLogger("c2ui.vfs")


def normalise(rel: str) -> Optional[str]:
    """Clean a content-relative path, or None when it is unsafe.

    Rejects absolute paths, drive letters and anything that climbs out of its
    mount - a `.vmt` may name any texture it likes, and it must not be able to
    name `C:/Windows`.
    """
    if not rel:
        return None
    text = str(rel).replace("\\", "/").strip()
    if not text or text.startswith("/") or ":" in text.split("/", 1)[0]:
        return None
    parts: List[str] = []
    for part in PurePosixPath(text).parts:
        if part in (".", ""):
            continue
        if part == "..":
            return None
        parts.append(part)
    return "/".join(parts) if parts else None


@dataclass(frozen=True)
class VirtualFile:
    """A file found in a mount, with the mount it came from."""

    rel: str
    path: Path
    mount: Mount

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def suffix(self) -> str:
        return self.path.suffix.lower()

    def read_bytes(self) -> bytes:
        return self.path.read_bytes()

    def __str__(self) -> str:
        return self.rel


class VirtualFileSystem:
    """Read-only view over ordered mounts.

    Never writes: everything the editor produces belongs in `App/`, not in a
    mounted installation.
    """

    def __init__(self, mounts: Union[MountSet, Sequence[Mount], None] = None) -> None:
        self._mounts: List[Mount] = []
        #: rel path (lowercase) -> resolved Path, for the winning mount only
        self._cache: Dict[str, Optional[Path]] = {}
        if mounts is not None:
            self.set_mounts(mounts)

    # -- mounts -----------------------------------------------------------------
    def set_mounts(self, mounts: Union[MountSet, Sequence[Mount]]) -> None:
        source = list(mounts) if not isinstance(mounts, MountSet) else list(mounts.mounts)
        self._mounts = sorted(source, key=lambda m: m.priority)
        self._cache.clear()

    @property
    def mounts(self) -> List[Mount]:
        return list(self._mounts)

    def __bool__(self) -> bool:
        return bool(self._mounts)

    # -- resolution -------------------------------------------------------------
    def resolve(self, rel: str) -> Optional[Path]:
        """The winning file for `rel`, or None when no mount has it."""
        key = normalise(rel)
        if key is None:
            return None
        lowered = key.lower()
        if lowered in self._cache:
            return self._cache[lowered]
        found: Optional[Path] = None
        for mount in self._mounts:
            candidate = mount.path / key
            if candidate.is_file():
                found = candidate
                break
        self._cache[lowered] = found
        return found

    def find(self, rel: str) -> Optional[VirtualFile]:
        """Like :meth:`resolve`, but keeps the mount the file came from."""
        key = normalise(rel)
        if key is None:
            return None
        for mount in self._mounts:
            candidate = mount.path / key
            if candidate.is_file():
                return VirtualFile(key, candidate, mount)
        return None

    def overrides(self, rel: str) -> List[VirtualFile]:
        """Every mount holding `rel`, best first.

        More than one entry means a mount is overriding another - worth showing
        the user when content behaves unexpectedly.
        """
        key = normalise(rel)
        if key is None:
            return []
        out: List[VirtualFile] = []
        for mount in self._mounts:
            candidate = mount.path / key
            if candidate.is_file():
                out.append(VirtualFile(key, candidate, mount))
        return out

    def exists(self, rel: str) -> bool:
        return self.resolve(rel) is not None

    # -- reading ----------------------------------------------------------------
    def read_bytes(self, rel: str) -> Optional[bytes]:
        path = self.resolve(rel)
        if path is None:
            return None
        try:
            return path.read_bytes()
        except OSError:
            log.warning("Could not read %s", path, exc_info=True)
            return None

    def read_text(self, rel: str, encodings: Iterable[str] = ("utf-8", "cp1252", "latin-1")) -> Optional[str]:
        raw = self.read_bytes(rel)
        if raw is None:
            return None
        for enc in encodings:
            try:
                return raw.decode(enc)
            except UnicodeDecodeError:
                continue
        return raw.decode("latin-1", "replace")

    # -- listing ----------------------------------------------------------------
    def listdir(self, rel: str = "") -> List[str]:
        """Entry names directly under `rel`, merged across mounts, deduplicated."""
        key = "" if not rel else normalise(rel)
        if key is None:
            return []
        seen: Dict[str, None] = {}
        for mount in self._mounts:
            folder = mount.path / key if key else mount.path
            if not folder.is_dir():
                continue
            try:
                for entry in os.scandir(folder):
                    seen.setdefault(entry.name, None)
            except OSError:
                continue
        return sorted(seen, key=str.lower)

    def isdir(self, rel: str) -> bool:
        key = normalise(rel)
        if key is None:
            return False
        return any((m.path / key).is_dir() for m in self._mounts)

    def glob(self, pattern: str, limit: Optional[int] = None) -> Iterator[VirtualFile]:
        """Match `pattern` across every mount, winning mount first.

        The same relative path is yielded once, from the mount that wins it, so
        a caller listing models never sees the overridden copies.
        """
        clean = normalise(pattern)
        if clean is None:
            return
        seen: set[str] = set()
        count = 0
        for mount in self._mounts:
            if not mount.path.is_dir():
                continue
            try:
                for path in mount.path.glob(clean):
                    if not path.is_file():
                        continue
                    try:
                        rel = path.relative_to(mount.path).as_posix()
                    except ValueError:
                        continue
                    lowered = rel.lower()
                    if lowered in seen:
                        continue
                    seen.add(lowered)
                    yield VirtualFile(rel, path, mount)
                    count += 1
                    if limit is not None and count >= limit:
                        return
            except OSError:
                log.debug("glob failed under %s", mount.path, exc_info=True)

    def count(self, pattern: str, limit: Optional[int] = None) -> int:
        """How many distinct files match - used for content statistics."""
        total = 0
        for _ in self.glob(pattern, limit):
            total += 1
        return total

    # -- diagnostics ------------------------------------------------------------
    def describe(self) -> str:
        if not self._mounts:
            return "no mounts"
        return " > ".join(m.name for m in self._mounts)

    def __repr__(self) -> str:
        return f"<VirtualFileSystem {len(self._mounts)} mounts: {self.describe()}>"
