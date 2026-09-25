"""
The bridge contract.

A *bridge* turns one external thing - a Source Filmmaker installation, a Steam
library, a Garry's Mod folder - into content C2UI understands. One folder per
bridge lives in `Core/dev-kit/`, next to the SDK it reads.

Writing a bridge means three methods:

    class MyBridge(SourceBridge):
        ID = "mything"
        NAME = "My Thing"

        def discover(self):          -> candidate paths, best first
        def probe(self, path):       -> ProbeResult: is this really one?
        def mount(self, path):       -> MountSet: its content roots, in order

Rules a bridge must keep:

* **Never raise for a missing or broken installation.** Return a ProbeResult
  saying why. The editor has to keep running when a game is uninstalled.
* **Never write anything.** Bridges read. Anything writable belongs to the App.
* **Never guess a path silently.** `discover()` proposes, the user decides, and
  the chosen path arrives back through `probe()` and `mount()`.
"""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar, List, Optional

from .types import Availability, MountSet, ProbeResult

__all__ = ["SourceBridge", "BridgeInfo"]

log = logging.getLogger("c2ui.bridge")


class SourceBridge(ABC):
    """Base class for everything in `Core/dev-kit/bridge_*`."""

    #: Stable identifier used in settings and by the registry.
    ID: ClassVar[str] = ""
    #: Human readable name, shown in the UI.
    NAME: ClassVar[str] = ""
    #: dev-kit slot this bridge needs, e.g. "sfm_sdk". None when it needs none.
    REQUIRES_SDK: ClassVar[Optional[str]] = None

    def __init__(self, sdk_dir: Optional[Path] = None) -> None:
        #: Where the SDK this bridge needs was placed, when it was placed.
        self.sdk_dir = sdk_dir

    # -- required ---------------------------------------------------------------
    @abstractmethod
    def discover(self) -> List[Path]:
        """Candidate installation paths, best guess first.  May be empty."""

    @abstractmethod
    def probe(self, path) -> ProbeResult:
        """Decide whether `path` really holds this product.

        Must not raise: an unreadable or missing path is a ProbeResult, not an
        exception.
        """

    @abstractmethod
    def mount(self, path) -> MountSet:
        """Build the ordered content roots for an installation at `path`.

        Returns an empty MountSet rather than raising when the installation
        cannot be read.
        """

    # -- provided ---------------------------------------------------------------
    def sdk_available(self) -> bool:
        """True when this bridge needs no SDK, or its slot has been filled."""
        if self.REQUIRES_SDK is None:
            return True
        if self.sdk_dir is None or not self.sdk_dir.is_dir():
            return False
        # a slot holding only its own instructions is still empty
        return any(p.name != "PLACE_SDK_HERE.md" for p in self.sdk_dir.iterdir())

    def availability(self, path=None) -> ProbeResult:
        """Probe, but report a missing SDK slot before blaming the path."""
        if not self.sdk_available():
            return ProbeResult.failed(
                Availability.SDK_MISSING,
                f"{self.NAME}: place the SDK in Core/dev-kit/{self.REQUIRES_SDK}",
            )
        if path is None:
            found = self.discover()
            if not found:
                return ProbeResult.failed(
                    Availability.NOT_CONFIGURED, f"{self.NAME}: no installation configured or found")
            path = found[0]
        return self.probe(path)

    def auto_mount(self) -> MountSet:
        """Discover, probe and mount in one call - used by tests and tooling."""
        result = self.availability()
        if not result.ok or result.root is None:
            return MountSet(self.ID, self.NAME, warnings=[result.detail])
        return self.mount(result.root)

    def __repr__(self) -> str:
        return f"<{type(self).__name__} id={self.ID!r}>"


class BridgeInfo:
    """What the registry knows about a bridge before loading it."""

    __slots__ = ("id", "name", "folder", "entry", "requires_sdk", "error")

    def __init__(self, id: str, name: str, folder: Path, entry: str,
                 requires_sdk: Optional[str] = None, error: str = "") -> None:
        self.id = id
        self.name = name
        self.folder = folder
        self.entry = entry
        self.requires_sdk = requires_sdk
        self.error = error

    @property
    def ok(self) -> bool:
        """True when the manifest and entry point loaded without error."""
        return not self.error

    def __repr__(self) -> str:
        state = "ok" if self.ok else f"error={self.error!r}"
        return f"<BridgeInfo {self.id} {state}>"
