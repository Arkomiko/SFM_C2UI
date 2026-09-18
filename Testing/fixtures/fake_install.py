"""
Build a throwaway Source Filmmaker installation on disk.

Shared by the bridge tests and the editor tests on purpose: one definition of
what an installation looks like, so the two cannot drift apart.

    with fake_sfm() as root:
        ...                      # root/game/usermod/gameinfo.txt exists

The layout mirrors a real install closely enough to exercise every rule the
bridge implements: token expansion, several roles on one entry, a duplicate
path, a `.vpk` entry to skip, and a search path that does not exist.
"""
from __future__ import annotations

import contextlib
import shutil
import tempfile
from pathlib import Path
from typing import Iterator, Optional

GAMEINFO = """"GameInfo"
{{
    game    "{title}"
    type    multiplayer_only

    FileSystem
    {{
        SteamAppId      1840
        ToolsAppId      1840

        SearchPaths
        {{
            Game+Mod                |gameinfo_path|.
            Game                    tf_movies
            Game                    tf
            Game                    |all_source_engine_paths|hl2
            Game                    missing_folder
            Game                    tf/tf2_textures.vpk
            Game                    tf
            GameBin                 bin
            Game+Write              workshop
        }}
    }}
}}
"""

#: Folders created inside every mount so `content_dirs()` has something to find.
CONTENT = ("models", "materials", "sound")


def build(root: Path, title: str = "Fake Filmmaker") -> Path:
    """Create the installation under `root` and return `root`."""
    game = root / "game"
    for mount in ("usermod", "tf_movies", "tf", "hl2", "workshop"):
        for sub in CONTENT:
            (game / mount / sub).mkdir(parents=True, exist_ok=True)
    (game / "bin").mkdir(parents=True, exist_ok=True)
    (game / "sfm.exe").write_bytes(b"not a real executable")
    (game / "usermod" / "gameinfo.txt").write_text(
        GAMEINFO.format(title=title), encoding="utf-8")

    # content used by the virtual file system tests: the same relative path in
    # three mounts, so overriding can be observed
    for mount, marker in (("usermod", b"usermod"), ("tf_movies", b"tf_movies"), ("tf", b"tf")):
        (game / mount / "models" / "shared.mdl").write_bytes(marker)
    (game / "tf" / "models" / "only_in_tf.mdl").write_bytes(b"tf")
    (game / "tf" / "materials" / "brick.vmt").write_text(
        '"LightmappedGeneric"\n{\n\t"$basetexture" "brick/wall"\n}\n', encoding="utf-8")
    (game / "usermod" / "models" / "nested").mkdir(parents=True, exist_ok=True)
    (game / "usermod" / "models" / "nested" / "deep.mdl").write_bytes(b"deep")
    return root


@contextlib.contextmanager
def fake_sfm(title: str = "Fake Filmmaker") -> Iterator[Path]:
    """A temporary installation, removed on exit."""
    temp = Path(tempfile.mkdtemp(prefix="c2ui_fake_sfm_"))
    try:
        yield build(temp, title)
    finally:
        shutil.rmtree(temp, ignore_errors=True)


@contextlib.contextmanager
def empty_dir(prefix: str = "c2ui_tmp_") -> Iterator[Path]:
    """A temporary folder with nothing in it."""
    temp = Path(tempfile.mkdtemp(prefix=prefix))
    try:
        yield temp
    finally:
        shutil.rmtree(temp, ignore_errors=True)


def real_sfm() -> Optional[Path]:
    """The machine's own installation, when there is one.

    Tests that use it must skip cleanly when it is absent - not every machine
    running these tests has Source Filmmaker installed.
    """
    import os
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from Core.Code.registry import BridgeRegistry

    env = os.environ.get("C2UI_SFM_ROOT")
    bridge = BridgeRegistry().load("sfm")
    if bridge is None:
        return None
    if env and bridge.probe(env).ok:
        return Path(env)
    found = bridge.discover()
    return found[0] if found else None
