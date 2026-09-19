"""
Content index.

Walking a mounted installation costs seconds - roughly 28 000 files across six
mounts on a normal Source Filmmaker setup. A UI cannot pay that on every launch,
so the walk happens once and the result is kept in a small SQLite file that the
App stores in `App/Cache/content`.

    index = ContentIndex(cache_dir)
    index.refresh(vfs)                       # scans only when something changed
    index.search("scout", kind="model")
    index.winners(kind="material", limit=50)

The index records *every* copy of a file, one row per mount, and marks the one
that wins by mount priority. That is what makes "which mount is this actually
coming from" answerable without touching the disk. Overrides are not rare and
not evenly spread: a normal install has some six hundred of them, bunched in the
shared texture folders where a movie mount shadows the game it came from.

Core never chooses where the cache lives: the directory is handed in by whoever
owns it, which keeps the engine usable from a read-only installation.
"""
from __future__ import annotations

import logging
import os
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

from Core.API.types import Mount, MountSet

from .vfs import VirtualFileSystem

log = logging.getLogger("c2ui.index")

__all__ = ["ContentEntry", "ContentIndex", "IndexStats", "KINDS", "kind_of"]

SCHEMA_VERSION = 1
DB_NAME = "content.db"

#: file extension -> what the editor calls it
KINDS: Dict[str, str] = {
    ".mdl": "model",
    ".vmt": "material",
    ".vtf": "texture",
    ".wav": "sound",
    ".mp3": "sound",
    ".bsp": "map",
    ".pcf": "particles",
    ".dmx": "element",
    ".vcd": "scene",
}

#: only these folders are walked - the rest of an installation is not content
CONTENT_ROOTS: Tuple[str, ...] = (
    "models", "materials", "sound", "maps", "particles", "elements", "scenes",
)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS mounts (
    priority INTEGER PRIMARY KEY,
    name     TEXT NOT NULL,
    path     TEXT NOT NULL,
    roles    TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS files (
    id         INTEGER PRIMARY KEY,
    rel        TEXT    NOT NULL,
    rel_lower  TEXT    NOT NULL,
    name_lower TEXT    NOT NULL,
    kind       TEXT    NOT NULL,
    ext        TEXT    NOT NULL,
    priority   INTEGER NOT NULL,
    size       INTEGER NOT NULL,
    mtime      REAL    NOT NULL,
    winner     INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS files_rel    ON files(rel_lower);
CREATE INDEX IF NOT EXISTS files_kind   ON files(kind, winner);
CREATE INDEX IF NOT EXISTS files_name   ON files(name_lower);
"""


@dataclass(frozen=True)
class ContentEntry:
    """One indexed file."""

    rel: str
    kind: str
    mount: str
    mount_path: Path
    priority: int
    size: int
    mtime: float
    winner: bool

    @property
    def path(self) -> Path:
        return self.mount_path / self.rel

    @property
    def name(self) -> str:
        return self.rel.rsplit("/", 1)[-1]

    def __str__(self) -> str:
        return self.rel


@dataclass
class IndexStats:
    """What a scan did."""

    files: int = 0
    winners: int = 0
    overridden: int = 0
    mounts: int = 0
    seconds: float = 0.0
    rebuilt: bool = False

    def summary(self) -> str:
        if not self.rebuilt:
            return f"index reused: {self.winners} files across {self.mounts} mounts"
        return (f"indexed {self.files} files ({self.winners} visible, "
                f"{self.overridden} overridden) from {self.mounts} mounts in {self.seconds:.1f}s")


def kind_of(name: str) -> Optional[str]:
    """What the editor calls this file, or None when it is not content."""
    dot = name.rfind(".")
    return KINDS.get(name[dot:].lower()) if dot >= 0 else None


class ContentIndex:
    """A queryable index of everything in a mounted installation."""

    def __init__(self, cache_dir, db_name: str = DB_NAME) -> None:
        self.cache_dir = Path(cache_dir)
        self.db_path = self.cache_dir / db_name
        self._db: Optional[sqlite3.Connection] = None
        self._mount_paths: Dict[int, Tuple[str, Path]] = {}

    # ------------------------------------------------------------------ lifetime
    def open(self) -> sqlite3.Connection:
        if self._db is not None:
            return self._db
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        try:
            self._connect()
        except sqlite3.DatabaseError:
            # The cache is regenerable by definition, so a file that is not a
            # database - truncated by a crash, half-written, replaced by junk -
            # is deleted rather than reported. Losing it only costs a rescan.
            log.warning("Content index at %s is unreadable; starting a new one", self.db_path)
            self._discard_file()
            self._connect()
        stored = self._meta("schema")
        if stored is None:
            self._set_meta("schema", str(SCHEMA_VERSION))
        elif stored != str(SCHEMA_VERSION):
            log.info("Content index schema changed (%s -> %s), discarding", stored, SCHEMA_VERSION)
            self.clear()
            self._set_meta("schema", str(SCHEMA_VERSION))
        self._load_mount_paths()
        return self._db

    def _connect(self) -> None:
        """Open the file and make sure it really is our database."""
        db = sqlite3.connect(str(self.db_path))
        db.row_factory = sqlite3.Row
        try:
            db.executescript(_SCHEMA)
        except sqlite3.DatabaseError:
            db.close()
            raise
        self._db = db

    def _discard_file(self) -> None:
        if self._db is not None:
            try:
                self._db.close()
            except sqlite3.Error:
                pass
            self._db = None
        for suffix in ("", "-wal", "-shm"):
            candidate = self.db_path.with_name(self.db_path.name + suffix)
            try:
                candidate.unlink(missing_ok=True)
            except OSError:
                log.debug("Could not remove %s", candidate, exc_info=True)

    def close(self) -> None:
        if self._db is not None:
            self._db.close()
            self._db = None

    def __enter__(self) -> "ContentIndex":
        self.open()
        return self

    def __exit__(self, *_exc) -> None:
        self.close()

    def clear(self) -> None:
        """Throw the index away.  Always safe: the next scan rebuilds it."""
        db = self._db if self._db is not None else self.open()
        db.executescript("DELETE FROM files; DELETE FROM mounts; DELETE FROM meta;")
        db.commit()
        self._mount_paths.clear()

    # ------------------------------------------------------------------ building
    def refresh(self, vfs: VirtualFileSystem,
                progress: Optional[Callable[[str, int], None]] = None,
                force: bool = False) -> IndexStats:
        """Scan only when the mounts changed - otherwise reuse what is stored."""
        self.open()
        if not force and self.matches(vfs.mounts):
            stats = self.stats()
            stats.rebuilt = False
            log.info("Content index reused (%d files)", stats.winners)
            return stats
        return self.build(vfs, progress)

    def build(self, vfs: VirtualFileSystem,
              progress: Optional[Callable[[str, int], None]] = None) -> IndexStats:
        """Walk every mount and rewrite the index."""
        db = self.open()
        started = time.time()
        mounts = vfs.mounts

        db.execute("DELETE FROM files")
        db.execute("DELETE FROM mounts")
        db.executemany(
            "INSERT INTO mounts (priority, name, path, roles) VALUES (?, ?, ?, ?)",
            [(m.priority, m.name, str(m.path), "+".join(m.roles)) for m in mounts],
        )

        total = 0
        for mount in mounts:
            if progress is not None:
                progress(mount.name, total)
            rows = list(_scan_mount(mount))
            if rows:
                db.executemany(
                    "INSERT INTO files (rel, rel_lower, name_lower, kind, ext, priority, size, mtime)"
                    " VALUES (?, ?, ?, ?, ?, ?, ?, ?)", rows)
            total += len(rows)

        self._mark_winners(db)
        self._set_meta("signature", _signature(mounts))
        self._set_meta("built", str(time.time()))
        db.commit()
        self._load_mount_paths()

        stats = self.stats()
        stats.seconds = time.time() - started
        stats.rebuilt = True
        log.info("Content index built: %s", stats.summary())
        return stats

    @staticmethod
    def _mark_winners(db: sqlite3.Connection) -> None:
        """Flag the copy of each path that wins by mount priority.

        Done once at build time so every later query is a plain indexed lookup
        instead of a correlated sub-select.
        """
        db.execute("UPDATE files SET winner = 0")
        db.execute(
            "UPDATE files SET winner = 1 WHERE id IN ("
            "  SELECT id FROM (SELECT id, MIN(priority) FROM files GROUP BY rel_lower)"
            ")"
        )

    # ------------------------------------------------------------- validation
    def matches(self, mounts: Sequence[Mount]) -> bool:
        """True when the stored index was built from exactly these mounts."""
        if self._meta("signature") is None:
            return False
        if self.count() == 0:
            return False
        return self._meta("signature") == _signature(mounts)

    def built_at(self) -> Optional[float]:
        raw = self._meta("built")
        try:
            return float(raw) if raw else None
        except ValueError:
            return None

    def verify(self, limit: Optional[int] = None) -> List[ContentEntry]:
        """Re-stat indexed files and report the ones that changed on disk.

        Used by an explicit "rescan" rather than on startup: it touches the file
        system, which is the cost the index exists to avoid.
        """
        stale: List[ContentEntry] = []
        for entry in self._iter_all(limit):
            try:
                st = entry.path.stat()
            except OSError:
                stale.append(entry)
                continue
            if st.st_size != entry.size or abs(st.st_mtime - entry.mtime) > 1e-6:
                stale.append(entry)
        return stale

    # ------------------------------------------------------------------ queries
    def count(self, kind: Optional[str] = None, winners_only: bool = True) -> int:
        db = self.open()
        sql = "SELECT COUNT(*) FROM files WHERE 1=1"
        args: List[object] = []
        if winners_only:
            sql += " AND winner = 1"
        if kind:
            sql += " AND kind = ?"
            args.append(kind)
        return int(db.execute(sql, args).fetchone()[0])

    def kinds(self) -> Dict[str, int]:
        """How many visible files of each kind - what a content browser shows."""
        db = self.open()
        rows = db.execute(
            "SELECT kind, COUNT(*) AS n FROM files WHERE winner = 1 GROUP BY kind ORDER BY n DESC")
        return {row["kind"]: row["n"] for row in rows}

    def resolve(self, rel: str) -> Optional[ContentEntry]:
        """The winning entry for a path, without touching the disk."""
        db = self.open()
        row = db.execute(
            "SELECT * FROM files WHERE rel_lower = ? AND winner = 1 LIMIT 1",
            (rel.replace("\\", "/").lower(),)).fetchone()
        return self._entry(row) if row else None

    def overrides(self, rel: str) -> List[ContentEntry]:
        """Every mount holding this path, best first."""
        db = self.open()
        rows = db.execute(
            "SELECT * FROM files WHERE rel_lower = ? ORDER BY priority",
            (rel.replace("\\", "/").lower(),))
        return [self._entry(r) for r in rows]

    def search(self, text: str, kind: Optional[str] = None, limit: int = 200,
               winners_only: bool = True) -> List[ContentEntry]:
        """Substring search over paths, shortest match first."""
        db = self.open()
        needle = f"%{text.replace('\\', '/').lower()}%"
        sql = "SELECT * FROM files WHERE rel_lower LIKE ?"
        args: List[object] = [needle]
        if winners_only:
            sql += " AND winner = 1"
        if kind:
            sql += " AND kind = ?"
            args.append(kind)
        sql += " ORDER BY LENGTH(rel), rel LIMIT ?"
        args.append(limit)
        return [self._entry(r) for r in db.execute(sql, args)]

    def winners(self, kind: Optional[str] = None, limit: int = 200,
                offset: int = 0) -> List[ContentEntry]:
        """A page of visible files - what the content browser scrolls through."""
        db = self.open()
        sql = "SELECT * FROM files WHERE winner = 1"
        args: List[object] = []
        if kind:
            sql += " AND kind = ?"
            args.append(kind)
        sql += " ORDER BY rel LIMIT ? OFFSET ?"
        args.extend([limit, offset])
        return [self._entry(r) for r in db.execute(sql, args)]

    def in_folder(self, folder: str, kind: Optional[str] = None,
                  limit: int = 500) -> List[ContentEntry]:
        """Visible files directly inside a folder, merged across mounts."""
        prefix = folder.replace("\\", "/").strip("/").lower()
        prefix = f"{prefix}/" if prefix else ""
        db = self.open()
        sql = ("SELECT * FROM files WHERE winner = 1 AND rel_lower LIKE ?"
               " AND INSTR(SUBSTR(rel_lower, ?), '/') = 0")
        args: List[object] = [f"{prefix}%", len(prefix) + 1]
        if kind:
            sql += " AND kind = ?"
            args.append(kind)
        sql += " ORDER BY rel LIMIT ?"
        args.append(limit)
        return [self._entry(r) for r in db.execute(sql, args)]

    def stats(self) -> IndexStats:
        db = self.open()
        files = int(db.execute("SELECT COUNT(*) FROM files").fetchone()[0])
        winners = int(db.execute("SELECT COUNT(*) FROM files WHERE winner = 1").fetchone()[0])
        mounts = int(db.execute("SELECT COUNT(*) FROM mounts").fetchone()[0])
        return IndexStats(files=files, winners=winners, overridden=files - winners, mounts=mounts)

    # ------------------------------------------------------------------ internals
    def _entry(self, row: sqlite3.Row) -> ContentEntry:
        name, path = self._mount_paths.get(row["priority"], ("?", Path(".")))
        return ContentEntry(
            rel=row["rel"], kind=row["kind"], mount=name, mount_path=path,
            priority=row["priority"], size=row["size"], mtime=row["mtime"],
            winner=bool(row["winner"]),
        )

    def _iter_all(self, limit: Optional[int] = None) -> Iterator[ContentEntry]:
        db = self.open()
        sql = "SELECT * FROM files ORDER BY id"
        if limit is not None:
            sql += f" LIMIT {int(limit)}"
        for row in db.execute(sql):
            yield self._entry(row)

    def _load_mount_paths(self) -> None:
        self._mount_paths = {
            row["priority"]: (row["name"], Path(row["path"]))
            for row in self.open().execute("SELECT priority, name, path FROM mounts")
        }

    def _meta(self, key: str) -> Optional[str]:
        row = self.open().execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else None

    def _set_meta(self, key: str, value: str) -> None:
        self.open().execute(
            "INSERT INTO meta (key, value) VALUES (?, ?)"
            " ON CONFLICT(key) DO UPDATE SET value = excluded.value", (key, value))

    def __repr__(self) -> str:
        return f"<ContentIndex {self.db_path}>"


# ---------------------------------------------------------------------------
#  Scanning
# ---------------------------------------------------------------------------
def _scan_mount(mount: Mount) -> Iterable[Tuple[str, str, str, str, str, int, int, float]]:
    """Walk one mount's content folders with os.scandir - faster than glob."""
    base = mount.path
    for root_name in CONTENT_ROOTS:
        root = base / root_name
        if not root.is_dir():
            continue
        yield from _walk(root, root_name, mount.priority)


def _walk(folder: Path, rel_prefix: str, priority: int):
    stack = [(folder, rel_prefix)]
    while stack:
        current, prefix = stack.pop()
        try:
            entries = list(os.scandir(current))
        except OSError:
            log.debug("Cannot read %s", current, exc_info=True)
            continue
        for entry in entries:
            try:
                if entry.is_dir(follow_symlinks=False):
                    stack.append((Path(entry.path), f"{prefix}/{entry.name}"))
                    continue
                if not entry.is_file(follow_symlinks=False):
                    continue
                kind = kind_of(entry.name)
                if kind is None:
                    continue
                stat = entry.stat()
            except OSError:
                continue
            rel = f"{prefix}/{entry.name}"
            dot = entry.name.rfind(".")
            ext = entry.name[dot:].lower() if dot >= 0 else ""
            yield (rel, rel.lower(), entry.name.lower(), kind, ext,
                   priority, stat.st_size, stat.st_mtime)


def _signature(mounts: Sequence[Mount]) -> str:
    """Identifies a mount set: rebuild the index when this changes."""
    return "|".join(f"{m.priority}:{m.name}:{m.path}" for m in sorted(mounts, key=lambda x: x.priority))
