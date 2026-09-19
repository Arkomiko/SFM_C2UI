"""
The winner invariant.

Which copy of a file wins decides what the editor actually loads, and the flag
is set by one UPDATE that leans on SQLite's bare-column behaviour beside MIN().
That behaviour is documented, but it is load-bearing here, so it gets its own
tests rather than being trusted.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Core.API.types import Mount
from Core.Code.content_index import ContentIndex
from Core.Code.vfs import VirtualFileSystem
from fixtures.fake_install import empty_dir


def _layered(base: Path, layers):
    """Build mounts named a, b, c... each holding the given relative files."""
    mounts = []
    for priority, (name, files) in enumerate(layers):
        root = base / name
        for rel in files:
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(name.encode())
        mounts.append(Mount(name=name, path=root, priority=priority, roles=("game",), source_id="test"))
    return VirtualFileSystem(mounts)


def _winner_report(index: ContentIndex):
    """(paths without exactly one winner, paths whose winner is not the top mount)."""
    db = index.open()
    stray = [r["rel_lower"] for r in db.execute(
        "SELECT rel_lower FROM files GROUP BY rel_lower HAVING SUM(winner) != 1")]
    wrong = [r["rel_lower"] for r in db.execute(
        "SELECT f.rel_lower FROM files f WHERE f.winner = 1 AND f.priority >"
        " (SELECT MIN(priority) FROM files WHERE rel_lower = f.rel_lower)")]
    return stray, wrong


def test_every_path_has_exactly_one_winner():
    with empty_dir() as base, empty_dir() as cache:
        vfs = _layered(base, [
            ("a", ["models/one.mdl", "models/shared.mdl"]),
            ("b", ["models/shared.mdl", "models/two.mdl"]),
            ("c", ["models/shared.mdl", "models/two.mdl", "models/three.mdl"]),
        ])
        with ContentIndex(cache) as index:
            index.build(vfs)
            stray, wrong = _winner_report(index)
            assert stray == [], stray
            assert wrong == [], wrong


def test_the_winner_is_always_the_highest_priority_mount():
    with empty_dir() as base, empty_dir() as cache:
        vfs = _layered(base, [
            ("a", ["models/shared.mdl"]),
            ("b", ["models/shared.mdl"]),
            ("c", ["models/shared.mdl"]),
        ])
        with ContentIndex(cache) as index:
            index.build(vfs)
            entry = index.resolve("models/shared.mdl")
            assert entry is not None
            assert entry.mount == "a"
            assert entry.path.read_bytes() == b"a"


def test_a_file_only_in_the_lowest_mount_still_wins():
    with empty_dir() as base, empty_dir() as cache:
        vfs = _layered(base, [
            ("a", ["models/one.mdl"]),
            ("b", []),
            ("c", ["models/deep.mdl"]),
        ])
        with ContentIndex(cache) as index:
            index.build(vfs)
            entry = index.resolve("models/deep.mdl")
            assert entry is not None and entry.mount == "c" and entry.winner


def test_winner_survives_many_copies():
    with empty_dir() as base, empty_dir() as cache:
        layers = [(chr(ord("a") + i), ["models/shared.mdl"]) for i in range(8)]
        vfs = _layered(base, layers)
        with ContentIndex(cache) as index:
            index.build(vfs)
            assert index.count("model") == 1                       # one visible
            assert index.count("model", winners_only=False) == 8    # eight copies
            stray, wrong = _winner_report(index)
            assert not stray and not wrong
            assert index.resolve("models/shared.mdl").mount == "a"


def test_rebuilding_does_not_leave_old_winners_behind():
    with empty_dir() as base, empty_dir() as cache:
        vfs = _layered(base, [
            ("a", ["models/shared.mdl"]),
            ("b", ["models/shared.mdl"]),
        ])
        with ContentIndex(cache) as index:
            index.build(vfs)
            assert index.resolve("models/shared.mdl").mount == "a"

            # the top mount disappears; the next one must take over
            vfs.set_mounts(vfs.mounts[1:])
            index.build(vfs)
            stray, wrong = _winner_report(index)
            assert not stray and not wrong
            assert index.resolve("models/shared.mdl").mount == "b"
            assert index.count("model", winners_only=False) == 1


def test_overrides_and_resolve_agree():
    with empty_dir() as base, empty_dir() as cache:
        vfs = _layered(base, [
            ("a", ["materials/x.vmt"]),
            ("b", ["materials/x.vmt"]),
            ("c", ["materials/x.vmt"]),
        ])
        with ContentIndex(cache) as index:
            index.build(vfs)
            chain = index.overrides("materials/x.vmt")
            assert [o.mount for o in chain] == ["a", "b", "c"]
            assert sum(o.winner for o in chain) == 1
            assert chain[0].winner
            assert index.resolve("materials/x.vmt").mount == chain[0].mount


def test_index_and_vfs_pick_the_same_file():
    with empty_dir() as base, empty_dir() as cache:
        vfs = _layered(base, [
            ("a", ["models/one.mdl"]),
            ("b", ["models/one.mdl", "models/two.mdl"]),
            ("c", ["models/two.mdl", "models/three.mdl"]),
        ])
        with ContentIndex(cache) as index:
            index.build(vfs)
            for rel in ("models/one.mdl", "models/two.mdl", "models/three.mdl"):
                from_index = index.resolve(rel)
                from_disk = vfs.find(rel)
                assert from_index is not None and from_disk is not None, rel
                assert from_index.mount == from_disk.mount.name, rel
                assert from_index.path == from_disk.path, rel
