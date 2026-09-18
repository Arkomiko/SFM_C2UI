"""
Types every program built on C2UI shares.

These are the words App, the tools and third-party plugins use to talk about
external content. They are deliberately plain data: no behaviour, no Qt, no
engine imports, so anything can depend on them.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

__all__ = ["Availability", "Mount", "MountSet", "ProbeResult", "CONTENT_DIRS"]

#: Sub-folders that make a content root worth mounting, in reporting order.
CONTENT_DIRS: Tuple[str, ...] = (
    "models", "materials", "sound", "maps", "particles", "scripts", "elements",
)


class Availability(Enum):
    """Why a source can or cannot be used right now.

    Every bridge reports one of these instead of raising, so the editor can show
    the reason and keep running.
    """

    AVAILABLE = "available"
    NOT_CONFIGURED = "not_configured"   # nobody has said where it is
    NOT_FOUND = "not_found"             # a path was given but nothing is there
    INVALID = "invalid"                 # something is there, but not this product
    SDK_MISSING = "sdk_missing"         # the bridge needs an SDK slot that is empty

    @property
    def usable(self) -> bool:
        return self is Availability.AVAILABLE


@dataclass(frozen=True)
class Mount:
    """One content root.

    Mounts are ordered: :attr:`priority` 0 wins when the same file exists in
    several of them, exactly like the engine's own search paths.
    """

    name: str                                   # folder name, e.g. "usermod"
    path: Path
    priority: int
    roles: Tuple[str, ...] = ()                 # game / mod / write ...
    source_id: str = ""                         # which bridge produced it

    @property
    def writable(self) -> bool:
        return "write" in self.roles or "mod" in self.roles

    def has(self, sub: str) -> bool:
        return (self.path / sub).is_dir()

    def content_dirs(self) -> List[str]:
        return [d for d in CONTENT_DIRS if self.has(d)]

    def __str__(self) -> str:
        return f"{self.name} ({self.path})"


@dataclass
class MountSet:
    """Everything one bridge found in one installation."""

    source_id: str                              # "sfm", "gmod", ...
    title: str                                  # human name of the installation
    root: Optional[Path] = None
    mounts: List[Mount] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        return bool(self.mounts)

    def __len__(self) -> int:
        return len(self.mounts)

    def __iter__(self):
        return iter(self.mounts)

    def by_name(self, name: str) -> Optional[Mount]:
        lowered = name.lower()
        return next((m for m in self.mounts if m.name.lower() == lowered), None)

    def writable(self) -> Optional[Mount]:
        return next((m for m in self.mounts if m.writable), None)

    def summary(self) -> str:
        if not self.mounts:
            return f"{self.title}: nothing mounted"
        return f"{self.title}: {len(self.mounts)} mounts from {self.root}"


@dataclass
class ProbeResult:
    """The answer to "is there a usable installation at this path?"."""

    availability: Availability
    root: Optional[Path] = None
    title: str = ""
    detail: str = ""                            # why, when it is not usable

    @property
    def ok(self) -> bool:
        return self.availability.usable

    def __bool__(self) -> bool:
        return self.ok

    @classmethod
    def available(cls, root: Path, title: str) -> "ProbeResult":
        return cls(Availability.AVAILABLE, root, title)

    @classmethod
    def failed(cls, availability: Availability, detail: str, root: Optional[Path] = None) -> "ProbeResult":
        return cls(availability, root, "", detail)


def order_mounts(mounts: Sequence[Mount]) -> List[Mount]:
    """Sort by priority and renumber, so merged sets stay consistent."""
    ordered = sorted(mounts, key=lambda m: m.priority)
    return [
        Mount(m.name, m.path, i, m.roles, m.source_id)
        for i, m in enumerate(ordered)
    ]
