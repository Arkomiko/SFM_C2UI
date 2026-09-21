"""
Bridge registry.

Bridges live in `Core/dev-kit/bridge_*`, each with a `bridge.json` manifest and
a module holding one :class:`SourceBridge` subclass. They are loaded by file
path rather than imported as packages, which is what lets `dev-kit` keep its
hyphen and what makes adding a bridge a matter of dropping in a folder.

    registry = BridgeRegistry()
    registry.discover()             -> [BridgeInfo, ...]
    bridge = registry.load("sfm")   -> SourceBridge

A bridge that fails to load is recorded with its error instead of raising: one
broken integration must never stop the editor.
"""
from __future__ import annotations

import importlib.util
import inspect
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional

from Core.API.bridge import BridgeInfo, SourceBridge

from .locations import DEV_KIT

__all__ = ["BridgeRegistry"]

log = logging.getLogger("c2ui.registry")

MANIFEST = "bridge.json"
BRIDGE_PREFIX = "bridge_"


class BridgeRegistry:
    """Finds and loads the bridges in `Core/dev-kit`."""

    def __init__(self, dev_kit: Optional[Path] = None) -> None:
        self.dev_kit = Path(dev_kit) if dev_kit else DEV_KIT
        self._found: Dict[str, BridgeInfo] = {}
        self._loaded: Dict[str, SourceBridge] = {}

    # -- discovery --------------------------------------------------------------
    def discover(self) -> List[BridgeInfo]:
        """Scan dev-kit for bridge folders and read their manifests."""
        self._found.clear()
        if not self.dev_kit.is_dir():
            log.warning("dev-kit not found at %s", self.dev_kit)
            return []
        for folder in sorted(self.dev_kit.iterdir()):
            if not folder.is_dir() or not folder.name.startswith(BRIDGE_PREFIX):
                continue
            if self._is_reserved(folder):
                log.debug("Bridge slot '%s' is reserved but not implemented yet", folder.name)
                continue
            info = self._read_manifest(folder)
            if info.id in self._found:
                info.error = f"duplicate bridge id '{info.id}'"
            self._found[info.id or folder.name] = info
        log.info("Bridges found: %s", ", ".join(sorted(self._found)) or "(none)")
        return list(self._found.values())

    @staticmethod
    def _is_reserved(folder: Path) -> bool:
        """A folder kept for a bridge nobody has written yet.

        Reserved slots hold nothing but placeholders, so they are skipped in
        silence: only a folder that *tries* to be a bridge and fails is an error
        worth reporting.
        """
        placeholders = {".gitkeep", "readme.md", "place_sdk_here.md"}
        return all(entry.name.lower() in placeholders for entry in folder.iterdir())

    def _read_manifest(self, folder: Path) -> BridgeInfo:
        fallback_id = folder.name[len(BRIDGE_PREFIX):] or folder.name
        manifest = folder / MANIFEST
        if not manifest.is_file():
            return BridgeInfo(fallback_id, fallback_id, folder, "bridge.py",
                              error=f"{MANIFEST} is missing")
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            return BridgeInfo(fallback_id, fallback_id, folder, "bridge.py",
                              error=f"{MANIFEST} is invalid ({exc})")
        return BridgeInfo(
            id=str(data.get("id") or fallback_id),
            name=str(data.get("name") or fallback_id),
            folder=folder,
            entry=str(data.get("entry") or "bridge.py"),
            requires_sdk=data.get("requires_sdk") or None,
        )

    def info(self, bridge_id: str) -> Optional[BridgeInfo]:
        """The manifest of a bridge by id, or None."""
        if not self._found:
            self.discover()
        return self._found.get(bridge_id)

    def available(self) -> List[BridgeInfo]:
        """Bridges whose manifests loaded."""
        if not self._found:
            self.discover()
        return [i for i in self._found.values() if i.ok]

    # -- loading ----------------------------------------------------------------
    def load(self, bridge_id: str) -> Optional[SourceBridge]:
        """Instantiate a bridge.  Returns None and records the error on failure."""
        if bridge_id in self._loaded:
            return self._loaded[bridge_id]
        info = self.info(bridge_id)
        if info is None:
            log.error("No bridge named '%s'", bridge_id)
            return None
        if not info.ok:
            log.error("Bridge '%s' is unusable: %s", bridge_id, info.error)
            return None

        entry = info.folder / info.entry
        if not entry.is_file():
            info.error = f"entry '{info.entry}' not found"
            log.error("Bridge '%s': %s", bridge_id, info.error)
            return None

        try:
            cls = self._load_class(info, entry)
        except Exception as exc:                     # noqa: BLE001 - any bridge bug
            info.error = f"{type(exc).__name__}: {exc}"
            log.exception("Bridge '%s' failed to load", bridge_id)
            return None
        if cls is None:
            info.error = "no SourceBridge subclass in the entry module"
            log.error("Bridge '%s': %s", bridge_id, info.error)
            return None

        sdk_dir = self.dev_kit / info.requires_sdk if info.requires_sdk else None
        try:
            bridge = cls(sdk_dir=sdk_dir)
        except Exception as exc:                     # noqa: BLE001
            info.error = f"{type(exc).__name__}: {exc}"
            log.exception("Bridge '%s' could not be constructed", bridge_id)
            return None
        self._loaded[bridge_id] = bridge
        log.debug("Bridge loaded: %s", bridge_id)
        return bridge

    def _load_class(self, info: BridgeInfo, entry: Path):
        module_name = f"c2ui_bridges.{info.id}"
        spec = importlib.util.spec_from_file_location(
            module_name, entry, submodule_search_locations=[str(info.folder)])
        if spec is None or spec.loader is None:
            raise ImportError(f"cannot import {entry}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
        except Exception:
            sys.modules.pop(module_name, None)
            raise
        for _name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, SourceBridge) and obj is not SourceBridge and obj.ID:
                return obj
        return None

    def load_all(self) -> Dict[str, SourceBridge]:
        """Load every discoverable bridge, skipping the broken ones."""
        for info in self.available():
            self.load(info.id)
        return dict(self._loaded)

    def __repr__(self) -> str:
        return f"<BridgeRegistry {len(self._found)} found, {len(self._loaded)} loaded>"
