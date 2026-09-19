"""ContentLibrary: mounting, indexing and degrading without an installation."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from App.Code.content_library import ContentLibrary
from Core.API import Availability
from fixtures.fake_install import empty_dir, fake_sfm


def _library(cache):
    return ContentLibrary(cache_dir=cache)


# ------------------------------------------------------------------ opening
def test_open_mounts_and_indexes():
    with fake_sfm("Fake Filmmaker") as root, empty_dir() as cache:
        lib = _library(cache)
        state = lib.open("sfm", root)
        try:
            assert state.ready, state.detail
            assert state.title == "Fake Filmmaker"
            assert state.mounts == 5
            assert state.stats is not None and state.stats.winners > 0
            assert "Fake Filmmaker" in state.summary()
        finally:
            lib.close()


def test_open_writes_the_index_into_the_given_cache_folder():
    with fake_sfm() as root, empty_dir() as cache:
        lib = _library(cache)
        lib.open("sfm", root)
        lib.close()
        assert (cache / "content.db").is_file()


def test_second_open_reuses_the_index():
    with fake_sfm() as root, empty_dir() as cache:
        first = _library(cache)
        first.open("sfm", root)
        first.close()

        second = _library(cache)
        state = second.open("sfm", root)
        try:
            assert state.ready
            assert state.stats is not None and not state.stats.rebuilt, "the stored index should be reused"
        finally:
            second.close()


def test_rescan_forces_a_fresh_walk():
    with fake_sfm() as root, empty_dir() as cache:
        lib = _library(cache)
        lib.open("sfm", root)
        try:
            stats = lib.rescan()
            assert stats is not None and stats.rebuilt
        finally:
            lib.close()


def test_warnings_from_the_bridge_reach_the_state():
    # the fixture lists a search path that does not exist
    with fake_sfm() as root, empty_dir() as cache:
        lib = _library(cache)
        state = lib.open("sfm", root)
        try:
            assert any("missing_folder" in w for w in state.warnings), state.warnings
        finally:
            lib.close()


# -------------------------------------------------------------- no content
def test_a_missing_installation_is_reported_not_raised():
    with empty_dir() as cache:
        lib = _library(cache)
        state = lib.open("sfm", Path("Z:/definitely/not/here"))
        try:
            assert not state.ready
            assert state.availability in (Availability.NOT_FOUND, Availability.INVALID)
            assert state.detail
        finally:
            lib.close()


def test_an_unknown_bridge_is_reported_not_raised():
    with empty_dir() as cache:
        lib = _library(cache)
        state = lib.open("no_such_source")
        try:
            assert not state.ready
            assert "no bridge" in state.detail
        finally:
            lib.close()


def test_queries_are_safe_before_anything_is_mounted():
    with empty_dir() as cache:
        lib = _library(cache)
        try:
            assert lib.search("anything") == []
            assert lib.browse() == []
            assert lib.page() == []
            assert lib.kinds() == {}
            assert lib.overrides("models/x.mdl") == []
            assert lib.resolve("models/x.mdl") is None
            assert lib.read_bytes("models/x.mdl") is None
            assert lib.rescan() is None
        finally:
            lib.close()


def test_a_corrupt_cache_is_rebuilt_instead_of_failing():
    with fake_sfm() as root, empty_dir() as cache:
        (cache / "content.db").write_bytes(b"this is not a database")
        lib = _library(cache)
        state = lib.open("sfm", root)
        try:
            assert state.ready, state.detail
            assert state.stats is not None and state.stats.winners > 0
        finally:
            lib.close()


# ------------------------------------------------------------------ queries
def test_search_and_kinds():
    with fake_sfm() as root, empty_dir() as cache:
        lib = _library(cache)
        lib.open("sfm", root)
        try:
            assert lib.kinds().get("model", 0) >= 3
            found = lib.search("only_in", kind="model")
            assert [e.rel for e in found] == ["models/only_in_tf.mdl"]
        finally:
            lib.close()


def test_browse_lists_direct_children_only():
    with fake_sfm() as root, empty_dir() as cache:
        lib = _library(cache)
        lib.open("sfm", root)
        try:
            rels = {e.rel for e in lib.browse("models")}
            assert "models/shared.mdl" in rels
            assert "models/nested/deep.mdl" not in rels
        finally:
            lib.close()


def test_resolve_and_read_use_the_winning_mount():
    with fake_sfm() as root, empty_dir() as cache:
        lib = _library(cache)
        lib.open("sfm", root)
        try:
            assert lib.read_bytes("models/shared.mdl") == b"usermod"
            overrides = lib.overrides("models/shared.mdl")
            assert [o.mount for o in overrides] == ["usermod", "tf_movies", "tf"]
        finally:
            lib.close()


def test_resolve_falls_back_to_disk_for_a_file_added_after_indexing():
    with fake_sfm() as root, empty_dir() as cache:
        lib = _library(cache)
        lib.open("sfm", root)
        try:
            late = root / "game" / "usermod" / "models" / "added_later.mdl"
            late.write_bytes(b"late")
            # not in the index, but the VFS still finds it on disk
            assert lib.resolve("models/added_later.mdl") == late
        finally:
            lib.close()


def test_read_text_decodes_a_material():
    with fake_sfm() as root, empty_dir() as cache:
        lib = _library(cache)
        lib.open("sfm", root)
        try:
            text = lib.read_text("materials/brick.vmt")
            assert text is not None and "$basetexture" in text
        finally:
            lib.close()
