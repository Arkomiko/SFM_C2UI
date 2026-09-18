"""Bridge registry: discovery, reserved slots and failure handling."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Core.Code.registry import BridgeRegistry
from fixtures.fake_install import empty_dir

GOOD_BRIDGE = '''
from Core.API import Availability, MountSet, ProbeResult, SourceBridge


class ToyBridge(SourceBridge):
    ID = "toy"
    NAME = "Toy"

    def discover(self):
        return []

    def probe(self, path):
        return ProbeResult.failed(Availability.NOT_FOUND, "toy")

    def mount(self, path):
        return MountSet(self.ID, self.NAME)
'''


def _make(folder: Path, name: str, manifest, module: str = GOOD_BRIDGE):
    d = folder / name
    d.mkdir(parents=True, exist_ok=True)
    if manifest is not None:
        (d / "bridge.json").write_text(json.dumps(manifest), encoding="utf-8")
    if module is not None:
        (d / "bridge.py").write_text(module, encoding="utf-8")
    return d


def test_reserved_slot_is_not_reported_as_an_error():
    # a folder holding only placeholders is planned work, not a broken bridge
    with empty_dir() as dev_kit:
        d = dev_kit / "bridge_planned"
        d.mkdir()
        (d / ".gitkeep").write_text("", encoding="utf-8")
        assert BridgeRegistry(dev_kit).discover() == []


def test_reserved_slot_with_a_readme_is_still_reserved():
    with empty_dir() as dev_kit:
        d = dev_kit / "bridge_planned"
        d.mkdir()
        (d / "README.md").write_text("later", encoding="utf-8")
        assert BridgeRegistry(dev_kit).discover() == []


def test_missing_manifest_is_an_error_when_code_is_present():
    with empty_dir() as dev_kit:
        _make(dev_kit, "bridge_broken", manifest=None)
        infos = BridgeRegistry(dev_kit).discover()
        assert len(infos) == 1
        assert not infos[0].ok
        assert "bridge.json" in infos[0].error


def test_invalid_manifest_is_reported():
    with empty_dir() as dev_kit:
        d = _make(dev_kit, "bridge_bad", manifest={"id": "bad"})
        (d / "bridge.json").write_text("{ not json", encoding="utf-8")
        infos = BridgeRegistry(dev_kit).discover()
        assert not infos[0].ok
        assert "invalid" in infos[0].error


def test_a_good_bridge_loads():
    with empty_dir() as dev_kit:
        _make(dev_kit, "bridge_toy", {"id": "toy", "name": "Toy", "entry": "bridge.py"})
        registry = BridgeRegistry(dev_kit)
        bridge = registry.load("toy")
        assert bridge is not None
        assert bridge.ID == "toy"
        assert bridge.mount("anything").source_id == "toy"


def test_bridges_are_cached_between_loads():
    with empty_dir() as dev_kit:
        _make(dev_kit, "bridge_toy", {"id": "toy", "name": "Toy"})
        registry = BridgeRegistry(dev_kit)
        assert registry.load("toy") is registry.load("toy")


def test_a_module_that_raises_on_import_is_recorded_not_raised():
    with empty_dir() as dev_kit:
        _make(dev_kit, "bridge_boom", {"id": "boom", "name": "Boom"},
              module="raise RuntimeError('boom')\n")
        registry = BridgeRegistry(dev_kit)
        assert registry.load("boom") is None
        assert "boom" in registry.info("boom").error.lower()


def test_a_module_without_a_bridge_class_is_reported():
    with empty_dir() as dev_kit:
        _make(dev_kit, "bridge_empty", {"id": "empty", "name": "Empty"},
              module="x = 1\n")
        registry = BridgeRegistry(dev_kit)
        assert registry.load("empty") is None
        assert "SourceBridge" in registry.info("empty").error


def test_a_missing_entry_file_is_reported():
    with empty_dir() as dev_kit:
        _make(dev_kit, "bridge_gone", {"id": "gone", "name": "Gone", "entry": "nope.py"},
              module=None)
        registry = BridgeRegistry(dev_kit)
        assert registry.load("gone") is None
        assert "not found" in registry.info("gone").error


def test_one_broken_bridge_does_not_stop_the_others():
    with empty_dir() as dev_kit:
        _make(dev_kit, "bridge_toy", {"id": "toy", "name": "Toy"})
        _make(dev_kit, "bridge_boom", {"id": "boom", "name": "Boom"},
              module="raise RuntimeError('boom')\n")
        loaded = BridgeRegistry(dev_kit).load_all()
        assert "toy" in loaded
        assert "boom" not in loaded


def test_unknown_id_returns_none():
    with empty_dir() as dev_kit:
        assert BridgeRegistry(dev_kit).load("nope") is None


def test_missing_dev_kit_is_survivable():
    registry = BridgeRegistry(Path("Z:/no/such/dev-kit"))
    assert registry.discover() == []
    assert registry.load("sfm") is None


def test_the_real_dev_kit_exposes_sfm_and_no_errors():
    infos = BridgeRegistry().discover()
    by_id = {i.id: i for i in infos}
    assert "sfm" in by_id
    broken = [f"{i.id}: {i.error}" for i in infos if not i.ok]
    assert not broken, broken
