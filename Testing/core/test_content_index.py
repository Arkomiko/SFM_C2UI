"""Content index: building, override resolution, querying and invalidation."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Core.Code.content_index import ContentIndex, kind_of
from Core.Code.registry import BridgeRegistry
from Core.Code.vfs import VirtualFileSystem
from fixtures.fake_install import empty_dir, fake_sfm


def _vfs(root):
    bridge = BridgeRegistry().load("sfm")
    assert bridge is not None
    return VirtualFileSystem(bridge.mount(root))


# -------------------------------------------------------------------- kinds
def test_kind_of_maps_known_extensions():
    assert kind_of("scout.mdl") == "model"
    assert kind_of("brick.VMT") == "material"
    assert kind_of("hit.wav") == "sound"
    assert kind_of("session.dmx") == "element"


def test_kind_of_ignores_everything_else():
    assert kind_of("readme.txt") is None
    assert kind_of("noextension") is None
    assert kind_of("") is None


# ------------------------------------------------------------------ building
def test_build_indexes_every_copy():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            stats = index.build(_vfs(root))
            # shared.mdl lives in three mounts: three rows, one winner
            assert stats.files > stats.winners
            assert stats.overridden == stats.files - stats.winners
            assert stats.mounts == 5
            assert stats.rebuilt


def test_the_index_file_lands_in_the_given_folder():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            index.build(_vfs(root))
        assert (cache / "content.db").is_file()


def test_winner_is_the_highest_priority_mount():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            index.build(_vfs(root))
            entry = index.resolve("models/shared.mdl")
            assert entry is not None
            assert entry.mount == "usermod"
            assert entry.winner


def test_overrides_are_ordered_by_priority():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            index.build(_vfs(root))
            found = index.overrides("models/shared.mdl")
            assert [e.mount for e in found] == ["usermod", "tf_movies", "tf"]
            assert [e.winner for e in found] == [True, False, False]


def test_resolve_is_case_insensitive():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            index.build(_vfs(root))
            assert index.resolve("MODELS/SHARED.MDL") is not None
            assert index.resolve(r"models\shared.mdl") is not None


def test_resolve_returns_none_for_unknown_paths():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            index.build(_vfs(root))
            assert index.resolve("models/nope.mdl") is None
            assert index.overrides("models/nope.mdl") == []


def test_entry_path_points_at_the_real_file():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            index.build(_vfs(root))
            entry = index.resolve("models/only_in_tf.mdl")
            assert entry is not None
            assert entry.path.is_file()
            assert entry.path.read_bytes() == b"tf"


# ------------------------------------------------------------------- queries
def test_kinds_counts_visible_files():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            index.build(_vfs(root))
            kinds = index.kinds()
            assert kinds.get("model", 0) >= 3
            assert kinds.get("material", 0) >= 1


def test_count_of_a_kind():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            index.build(_vfs(root))
            assert index.count("model") == index.kinds()["model"]
            assert index.count("model", winners_only=False) > index.count("model")


def test_search_finds_by_substring():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            index.build(_vfs(root))
            found = index.search("only_in")
            assert [e.rel for e in found] == ["models/only_in_tf.mdl"]


def test_search_can_filter_by_kind():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            index.build(_vfs(root))
            assert index.search("shared", kind="material") == []
            assert index.search("shared", kind="model")


def test_search_returns_only_winners_by_default():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            index.build(_vfs(root))
            assert len(index.search("shared")) == 1
            assert len(index.search("shared", winners_only=False)) == 3


def test_winners_pages():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            index.build(_vfs(root))
            first = index.winners(kind="model", limit=1)
            second = index.winners(kind="model", limit=1, offset=1)
            assert len(first) == 1 and len(second) == 1
            assert first[0].rel != second[0].rel


def test_in_folder_lists_only_direct_children():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            index.build(_vfs(root))
            rels = {e.rel for e in index.in_folder("models")}
            assert "models/shared.mdl" in rels
            assert "models/nested/deep.mdl" not in rels      # one level down
            nested = {e.rel for e in index.in_folder("models/nested")}
            assert "models/nested/deep.mdl" in nested


# -------------------------------------------------------------- invalidation
def test_refresh_reuses_a_matching_index():
    with fake_sfm() as root, empty_dir() as cache:
        vfs = _vfs(root)
        with ContentIndex(cache) as index:
            index.build(vfs)
            again = index.refresh(vfs)
            assert not again.rebuilt


def test_refresh_rebuilds_when_the_mounts_change():
    with fake_sfm() as root, empty_dir() as cache:
        vfs = _vfs(root)
        with ContentIndex(cache) as index:
            index.build(vfs)
            vfs.set_mounts(vfs.mounts[:2])          # pretend a mount disappeared
            assert index.refresh(vfs).rebuilt


def test_force_rebuilds_even_when_valid():
    with fake_sfm() as root, empty_dir() as cache:
        vfs = _vfs(root)
        with ContentIndex(cache) as index:
            index.build(vfs)
            assert index.refresh(vfs, force=True).rebuilt


def test_an_index_survives_being_reopened():
    with fake_sfm() as root, empty_dir() as cache:
        vfs = _vfs(root)
        with ContentIndex(cache) as index:
            index.build(vfs)
            expected = index.count()
        with ContentIndex(cache) as reopened:
            assert reopened.count() == expected
            assert reopened.matches(vfs.mounts)
            assert reopened.resolve("models/shared.mdl") is not None


def test_clear_empties_the_index():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            index.build(_vfs(root))
            index.clear()
            assert index.count() == 0
            assert index.resolve("models/shared.mdl") is None


def test_matches_is_false_for_an_empty_index():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            assert not index.matches(_vfs(root).mounts)


def test_verify_reports_a_changed_file():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            index.build(_vfs(root))
            assert index.verify() == []
            target = root / "game" / "tf" / "models" / "only_in_tf.mdl"
            target.write_bytes(b"changed on disk, longer than before")
            stale = index.verify()
            assert [e.rel for e in stale] == ["models/only_in_tf.mdl"]


def test_verify_reports_a_deleted_file():
    with fake_sfm() as root, empty_dir() as cache:
        with ContentIndex(cache) as index:
            index.build(_vfs(root))
            (root / "game" / "tf" / "models" / "only_in_tf.mdl").unlink()
            assert "models/only_in_tf.mdl" in {e.rel for e in index.verify()}


def test_progress_is_reported_per_mount():
    with fake_sfm() as root, empty_dir() as cache:
        seen = []
        with ContentIndex(cache) as index:
            index.build(_vfs(root), progress=lambda name, n: seen.append(name))
        assert seen == ["usermod", "tf_movies", "tf", "hl2", "workshop"]


def test_building_over_no_mounts_is_harmless():
    with empty_dir() as cache:
        with ContentIndex(cache) as index:
            stats = index.build(VirtualFileSystem())
            assert stats.files == 0
            assert index.kinds() == {}
            assert index.search("anything") == []
