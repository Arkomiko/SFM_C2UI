"""The SFM bridge: probing an installation and expanding its search paths."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Core.API import Availability
from Core.Code.registry import BridgeRegistry
from fixtures.fake_install import empty_dir, fake_sfm


def _bridge():
    bridge = BridgeRegistry().load("sfm")
    assert bridge is not None, "the sfm bridge should load from Core/dev-kit"
    return bridge


# ----------------------------------------------------------------- registry
def test_registry_finds_the_sfm_bridge():
    infos = BridgeRegistry().discover()
    ids = {i.id for i in infos}
    assert "sfm" in ids, f"expected an 'sfm' bridge, found {ids}"
    info = next(i for i in infos if i.id == "sfm")
    assert info.ok, info.error
    assert info.name == "Source Filmmaker"


def test_registry_reports_unknown_bridge_without_raising():
    assert BridgeRegistry().load("does_not_exist") is None


def test_bridge_declares_it_needs_no_sdk():
    bridge = _bridge()
    assert bridge.REQUIRES_SDK is None
    assert bridge.sdk_available() is True


# -------------------------------------------------------------------- probe
def test_probe_accepts_the_install_folder():
    with fake_sfm("Fake Filmmaker") as root:
        result = _bridge().probe(root)
        assert result.ok, result.detail
        assert result.root == root
        assert result.title == "Fake Filmmaker"


def test_probe_accepts_the_game_folder():
    with fake_sfm() as root:
        result = _bridge().probe(root / "game")
        assert result.ok, result.detail
        assert result.root == root


def test_probe_accepts_sfm_exe():
    with fake_sfm() as root:
        result = _bridge().probe(root / "game" / "sfm.exe")
        assert result.ok, result.detail
        assert result.root == root


def test_probe_rejects_a_folder_without_game():
    with empty_dir() as folder:
        result = _bridge().probe(folder)
        assert not result.ok
        assert result.availability is Availability.INVALID
        assert "game" in result.detail.lower()


def test_probe_rejects_a_game_folder_without_gameinfo():
    with empty_dir() as folder:
        (folder / "game" / "usermod").mkdir(parents=True)
        result = _bridge().probe(folder)
        assert not result.ok
        assert "gameinfo" in result.detail.lower()


def test_probe_reports_missing_path():
    result = _bridge().probe(Path("Z:/definitely/not/here"))
    assert not result.ok
    assert result.availability in (Availability.NOT_FOUND, Availability.INVALID)


def test_probe_of_nothing_is_not_configured():
    result = _bridge().probe("")
    assert not result.ok
    assert result.availability is Availability.NOT_CONFIGURED


def test_probe_never_raises_on_junk():
    for junk in ("", "   ", "\\\\?\\bad", "C:", "%%%"):
        result = _bridge().probe(junk)
        assert not result.ok


# -------------------------------------------------------------------- mount
def test_mount_resolves_search_paths_in_order():
    with fake_sfm() as root:
        mounts = _bridge().mount(root)
        assert mounts, mounts.warnings
        names = [m.name for m in mounts]
        assert names == ["usermod", "tf_movies", "tf", "hl2", "workshop"], names
        assert [m.priority for m in mounts] == [0, 1, 2, 3, 4]


def test_mount_expands_gameinfo_path_token():
    with fake_sfm() as root:
        mounts = _bridge().mount(root)
        assert mounts.mounts[0].path == root / "game" / "usermod"


def test_mount_expands_all_source_engine_paths_token():
    with fake_sfm() as root:
        hl2 = mounts_by_name(_bridge().mount(root), "hl2")
        assert hl2.path == root / "game" / "hl2"


def test_mount_skips_vpk_entries():
    with fake_sfm() as root:
        mounts = _bridge().mount(root)
        assert not any(str(m.path).lower().endswith(".vpk") for m in mounts)


def test_mount_skips_non_content_roles():
    # "GameBin bin" must not become a content mount
    with fake_sfm() as root:
        assert mounts_by_name_opt(_bridge().mount(root), "bin") is None


def test_mount_collapses_duplicate_paths_keeping_priority():
    # tf appears twice in the fixture; it must stay at its first position
    with fake_sfm() as root:
        mounts = _bridge().mount(root)
        tf = [m for m in mounts if m.name == "tf"]
        assert len(tf) == 1
        assert tf[0].priority == 2


def test_mount_warns_about_a_missing_search_path():
    with fake_sfm() as root:
        mounts = _bridge().mount(root)
        assert any("missing_folder" in w for w in mounts.warnings), mounts.warnings


def test_mount_records_roles_and_writable_mount():
    with fake_sfm() as root:
        mounts = _bridge().mount(root)
        assert "mod" in mounts.mounts[0].roles
        writable = mounts.writable()
        assert writable is not None
        assert writable.name in ("usermod", "workshop")


def test_mount_reports_content_dirs():
    with fake_sfm() as root:
        mounts = _bridge().mount(root)
        assert "models" in mounts.mounts[0].content_dirs()


def test_mount_of_a_bad_path_returns_empty_set_not_an_exception():
    mounts = _bridge().mount("Z:/nope")
    assert len(mounts) == 0
    assert mounts.warnings


def test_mount_tags_every_mount_with_the_source_id():
    with fake_sfm() as root:
        mounts = _bridge().mount(root)
        assert {m.source_id for m in mounts} == {"sfm"}


def test_mount_set_helpers():
    with fake_sfm("Fake Filmmaker") as root:
        mounts = _bridge().mount(root)
        assert mounts.by_name("TF") is not None      # case-insensitive
        assert mounts.by_name("nope") is None
        assert "Fake Filmmaker" in mounts.summary()
        assert bool(mounts) is True


# ------------------------------------------------------------------ helpers
def mounts_by_name(mount_set, name):
    found = mount_set.by_name(name)
    assert found is not None, f"no mount named {name}: {[m.name for m in mount_set]}"
    return found


def mounts_by_name_opt(mount_set, name):
    return mount_set.by_name(name)
