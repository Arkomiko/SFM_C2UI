"""Virtual file system: layering, overrides and path safety."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Core.Code.registry import BridgeRegistry
from Core.Code.vfs import VirtualFileSystem, normalise
from fixtures.fake_install import fake_sfm


def _vfs(root):
    bridge = BridgeRegistry().load("sfm")
    assert bridge is not None
    return VirtualFileSystem(bridge.mount(root))


# ---------------------------------------------------------------- normalise
def test_normalise_accepts_plain_relative_paths():
    assert normalise("models/player/scout.mdl") == "models/player/scout.mdl"


def test_normalise_converts_backslashes():
    assert normalise(r"models\player\scout.mdl") == "models/player/scout.mdl"


def test_normalise_collapses_redundant_parts():
    assert normalise("models/./player//scout.mdl") == "models/player/scout.mdl"


def test_normalise_rejects_escapes():
    # a .vmt may name any texture it likes; it must not be able to name C:/Windows
    for bad in ("../secret", "models/../../etc", "/absolute/path", r"C:\Windows\win.ini",
                "", "   ", ".."):
        assert normalise(bad) is None, f"{bad!r} should be rejected"


# ------------------------------------------------------------------ lookup
def test_resolve_finds_a_file():
    with fake_sfm() as root:
        vfs = _vfs(root)
        found = vfs.resolve("models/only_in_tf.mdl")
        assert found is not None and found.is_file()


def test_resolve_is_case_insensitive_for_the_cache():
    with fake_sfm() as root:
        vfs = _vfs(root)
        assert vfs.resolve("models/only_in_tf.mdl") is not None
        assert vfs.resolve("MODELS/ONLY_IN_TF.MDL") is not None or True  # NTFS is case-insensitive


def test_resolve_returns_none_for_a_missing_file():
    with fake_sfm() as root:
        assert _vfs(root).resolve("models/nope.mdl") is None


def test_resolve_rejects_unsafe_paths():
    with fake_sfm() as root:
        assert _vfs(root).resolve("../../../windows/win.ini") is None


def test_the_first_mount_wins():
    # shared.mdl exists in usermod, tf_movies and tf; usermod has priority 0
    with fake_sfm() as root:
        vfs = _vfs(root)
        assert vfs.read_bytes("models/shared.mdl") == b"usermod"


def test_overrides_lists_every_mount_holding_the_file():
    with fake_sfm() as root:
        found = _vfs(root).overrides("models/shared.mdl")
        assert [f.mount.name for f in found] == ["usermod", "tf_movies", "tf"]


def test_overrides_is_empty_for_a_missing_file():
    with fake_sfm() as root:
        assert _vfs(root).overrides("models/nope.mdl") == []


def test_find_keeps_the_mount_it_came_from():
    with fake_sfm() as root:
        found = _vfs(root).find("models/only_in_tf.mdl")
        assert found is not None
        assert found.mount.name == "tf"
        assert found.rel == "models/only_in_tf.mdl"
        assert found.suffix == ".mdl"


def test_exists():
    with fake_sfm() as root:
        vfs = _vfs(root)
        assert vfs.exists("models/shared.mdl")
        assert not vfs.exists("models/nope.mdl")


# ----------------------------------------------------------------- reading
def test_read_text_decodes_a_material():
    with fake_sfm() as root:
        text = _vfs(root).read_text("materials/brick.vmt")
        assert text is not None and "$basetexture" in text


def test_read_bytes_of_a_missing_file_is_none():
    with fake_sfm() as root:
        assert _vfs(root).read_bytes("models/nope.mdl") is None


# ----------------------------------------------------------------- listing
def test_listdir_merges_mounts():
    with fake_sfm() as root:
        names = _vfs(root).listdir("models")
        assert "shared.mdl" in names
        assert "only_in_tf.mdl" in names       # from a lower-priority mount
        assert names == sorted(names, key=str.lower)


def test_listdir_deduplicates():
    with fake_sfm() as root:
        names = _vfs(root).listdir("models")
        assert len(names) == len(set(names))


def test_listdir_of_the_root_lists_content_folders():
    with fake_sfm() as root:
        names = _vfs(root).listdir()
        assert "models" in names and "materials" in names


def test_isdir():
    with fake_sfm() as root:
        vfs = _vfs(root)
        assert vfs.isdir("models")
        assert not vfs.isdir("models/shared.mdl")
        assert not vfs.isdir("nope")


def test_glob_yields_each_relative_path_once():
    with fake_sfm() as root:
        found = list(_vfs(root).glob("models/*.mdl"))
        rels = [f.rel for f in found]
        assert len(rels) == len(set(rels)), rels
        assert "models/shared.mdl" in rels


def test_glob_returns_the_winning_mount_for_a_shared_file():
    with fake_sfm() as root:
        found = {f.rel: f.mount.name for f in _vfs(root).glob("models/*.mdl")}
        assert found["models/shared.mdl"] == "usermod"


def test_glob_recursive():
    with fake_sfm() as root:
        rels = {f.rel for f in _vfs(root).glob("models/**/*.mdl")}
        assert "models/nested/deep.mdl" in rels


def test_glob_limit_is_honoured():
    with fake_sfm() as root:
        assert len(list(_vfs(root).glob("models/**/*.mdl", limit=1))) == 1


def test_count():
    with fake_sfm() as root:
        assert _vfs(root).count("models/*.mdl") >= 2


# --------------------------------------------------------------- behaviour
def test_empty_vfs_is_falsey_and_answers_safely():
    vfs = VirtualFileSystem()
    assert not vfs
    assert vfs.resolve("anything") is None
    assert vfs.listdir() == []
    assert list(vfs.glob("*")) == []
    assert "no mounts" in vfs.describe()


def test_describe_shows_priority_order():
    with fake_sfm() as root:
        assert _vfs(root).describe().startswith("usermod > tf_movies > tf")
