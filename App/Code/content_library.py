"""
The editor's view of mounted content.

Ties the pieces together: pick a bridge, mount an installation, put a virtual
file system over it and keep a content index in `App/Cache/content` so the walk
is paid once rather than on every launch.

    library = ContentLibrary()
    library.open("sfm")                  # discovers, mounts, indexes
    library.search("scout", kind="model")
    library.read("materials/brick.vmt")

Everything reports rather than raises: an uninstalled game, a moved folder or a
corrupt cache all leave the editor running.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional

from Core.API import Availability, MountSet, ProbeResult
from Core.Code.content_index import ContentEntry, ContentIndex, IndexStats
from Core.Code.registry import BridgeRegistry
from Core.Code.vfs import VirtualFileSystem

from . import locations

log = logging.getLogger("c2ui.library")

__all__ = ["ContentLibrary", "LibraryState"]


@dataclass
class LibraryState:
    """What the editor can tell the user about the content it has."""

    source_id: str = ""
    title: str = ""
    root: Optional[Path] = None
    availability: Availability = Availability.NOT_CONFIGURED
    detail: str = ""
    mounts: int = 0
    stats: Optional[IndexStats] = None
    warnings: List[str] = field(default_factory=list)

    @property
    def ready(self) -> bool:
        """True when the installation is usable and something is mounted."""
        return self.availability.usable and self.mounts > 0

    def summary(self) -> str:
        """One line for the status bar."""
        if not self.ready:
            return self.detail or "no content mounted"
        counted = self.stats.winners if self.stats else 0
        return f"{self.title}: {counted} files across {self.mounts} mounts"


class ContentLibrary:
    """Mounted content plus its index, as the editor sees it."""

    def __init__(self, cache_dir: Optional[Path] = None,
                 registry: Optional[BridgeRegistry] = None) -> None:
        self.cache_dir = Path(cache_dir) if cache_dir else locations.CONTENT_CACHE
        self.registry = registry or BridgeRegistry()
        self.vfs = VirtualFileSystem()
        self.index = ContentIndex(self.cache_dir)
        self.state = LibraryState()
        self._mount_set: Optional[MountSet] = None

    # ---------------------------------------------------------------- opening
    def open(self, source_id: str = "sfm", path=None,
             progress: Optional[Callable[[str, int], None]] = None,
             force_rescan: bool = False) -> LibraryState:
        """Mount an installation and make its content queryable."""
        bridge = self.registry.load(source_id)
        if bridge is None:
            self.state = LibraryState(
                source_id=source_id, availability=Availability.INVALID,
                detail=f"no bridge named '{source_id}'")
            return self.state

        probe: ProbeResult = bridge.probe(path) if path else bridge.availability()
        if not probe.ok or probe.root is None:
            self.state = LibraryState(
                source_id=source_id, availability=probe.availability, detail=probe.detail)
            log.info("Content not available: %s", probe.detail)
            return self.state

        mounts = bridge.mount(probe.root)
        self._mount_set = mounts
        self.vfs.set_mounts(mounts)

        stats = self._index_safely(progress, force_rescan)
        self.state = LibraryState(
            source_id=source_id, title=mounts.title, root=mounts.root,
            availability=Availability.AVAILABLE, mounts=len(mounts),
            stats=stats, warnings=list(mounts.warnings),
        )
        log.info("Content library open: %s", self.state.summary())
        return self.state

    def _index_safely(self, progress, force: bool) -> Optional[IndexStats]:
        """A broken cache must cost a rescan, never a failed start."""
        try:
            return self.index.refresh(self.vfs, progress=progress, force=force)
        except Exception:                        # noqa: BLE001 - sqlite, disk, anything
            log.warning("Content index unusable, rebuilding from scratch", exc_info=True)
        try:
            self.index.clear()
            return self.index.build(self.vfs, progress=progress)
        except Exception:                        # noqa: BLE001
            log.exception("Content index could not be built; falling back to direct scanning")
            return None

    def close(self) -> None:
        """Close the index database."""
        self.index.close()

    def rescan(self, progress: Optional[Callable[[str, int], None]] = None) -> Optional[IndexStats]:
        """Force a fresh walk - the "rescan content" action."""
        if not self.vfs:
            return None
        return self.index.build(self.vfs, progress=progress)

    # ---------------------------------------------------------------- queries
    @property
    def ready(self) -> bool:
        """True when content is mounted."""
        return self.state.ready

    def kinds(self) -> Dict[str, int]:
        """File kind to count."""
        return self.index.kinds() if self.ready else {}

    def search(self, text: str, kind: Optional[str] = None, limit: int = 200) -> List[ContentEntry]:
        """Files whose path contains `text`."""
        return self.index.search(text, kind, limit) if self.ready else []

    def browse(self, folder: str = "", kind: Optional[str] = None,
               limit: int = 500) -> List[ContentEntry]:
        """Files in a folder."""
        return self.index.in_folder(folder, kind, limit) if self.ready else []

    def page(self, kind: Optional[str] = None, limit: int = 200, offset: int = 0) -> List[ContentEntry]:
        """A page of visible files."""
        return self.index.winners(kind, limit, offset) if self.ready else []

    def resolve(self, rel: str) -> Optional[Path]:
        """Where a content path actually is - index first, disk as a fallback."""
        entry = self.index.resolve(rel) if self.ready else None
        if entry is not None and entry.path.is_file():
            return entry.path
        return self.vfs.resolve(rel)

    def overrides(self, rel: str) -> List[ContentEntry]:
        """Every mount's copy of a file, winner first."""
        return self.index.overrides(rel) if self.ready else []

    def read_bytes(self, rel: str) -> Optional[bytes]:
        """A file's bytes through the mounts, or None."""
        path = self.resolve(rel)
        if path is None:
            return None
        try:
            return path.read_bytes()
        except OSError:
            log.warning("Could not read %s", path, exc_info=True)
            return None

    def read_text(self, rel: str) -> Optional[str]:
        """A file's text through the mounts, or None."""
        return self.vfs.read_text(rel) if self.vfs else None

    def disk_source(self) -> "DiskSource":
        """A reader that never touches the index, safe to use from another
        thread.  The SQLite connection belongs to the thread that opened it;
        the virtual file system is plain Python and resolves the same paths."""
        return DiskSource(self.vfs)

    def __repr__(self) -> str:
        return f"<ContentLibrary {self.state.summary()}>"


class DiskSource:
    """Content reads through the mounts alone - see ContentLibrary.disk_source."""

    def __init__(self, vfs: VirtualFileSystem) -> None:
        self.vfs = vfs

    def resolve(self, rel: str) -> Optional[Path]:
        """Where the file is on disk, or None."""
        return self.vfs.resolve(rel)

    def read_bytes(self, rel: str) -> Optional[bytes]:
        """A file's bytes through the mounts, or None."""
        return self.vfs.read_bytes(rel)

    def read_text(self, rel: str) -> Optional[str]:
        """A file's text through the mounts, or None."""
        return self.vfs.read_text(rel)
