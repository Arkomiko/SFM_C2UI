"""
Start the engine on its own, without the editor.

    python Launcher/core.py                     open the shell
    python Launcher/core.py find scout.mdl      run one command and leave

Temporary: once App can be started headless this goes away and the editor
becomes the only entry point.  It exists because `Core` is a library - it
mounts an installation, indexes it, reads its formats and evaluates its
sessions, and none of that needs a window.  Nothing here imports `App`; the
launcher plays App's part by choosing where the index is cached, which is
the one thing Core never decides for itself.

Needs no packages at all: the engine is standard library only.

Commands:

    mount [id] [path]    mount an installation (sfm by default) and index it
    rescan               build the index again from scratch
    mounts               the mounts in priority order
    stats                what the index holds
    kinds                file kinds and their counts
    find <text> [kind]   search the index
    ls <folder> [kind]   list a folder
    read <path>          where a content path resolves to, and its size
    model <path>         load a model: bones, meshes, materials, flexes
    material <path>      a material: shader, parameters, textures
    texture <path>       a texture: format, size, mip count
    map <name>           a map: faces, props, lights, sky
    session <path.dmx>   a session: shots, models, sound
    eval <path.dmx> <s>  evaluate a session at a time and show what moved
    help, quit
"""
from __future__ import annotations

import logging
import shlex
import sys
import time
from pathlib import Path
from typing import List, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Core.API import Availability, MountSet                        # noqa: E402
from Core.API.dmx import Time                                      # noqa: E402
from Core.API.session import GameModel, ProjectedLight, Session    # noqa: E402
from Core.Code.animation import Evaluator                          # noqa: E402
from Core.Code.content_index import ContentIndex                   # noqa: E402
from Core.Code.formats import (FormatError, load_dmx, load_material, load_model,  # noqa: E402
                               parse_vtf)
from Core.Code.formats.bsp import map_path, parse_bsp              # noqa: E402
from Core.Code.registry import BridgeRegistry                      # noqa: E402
from Core.Code.sound import active_sound_clips                     # noqa: E402
from Core.Code.vfs import VirtualFileSystem                        # noqa: E402

#: where the index is cached - the editor's own folder, so both share one scan
CACHE_DIR = PROJECT_ROOT / "App" / "Cache" / "content"

log = logging.getLogger("c2ui.core")


class CoreShell:
    """The engine with an installation mounted, and commands over it."""

    def __init__(self, cache_dir: Path = CACHE_DIR) -> None:
        self.registry = BridgeRegistry()
        self.vfs = VirtualFileSystem()
        self.index = ContentIndex(cache_dir)
        self.mounts: Optional[MountSet] = None

    # -- mounting ----------------------------------------------------------------
    def mount(self, source_id: str = "sfm", path: Optional[str] = None, force: bool = False) -> None:
        """Find an installation, mount it and index what it holds."""
        bridge = self.registry.load(source_id)
        if bridge is None:
            names = ", ".join(i.id for i in self.registry.available()) or "none"
            print(f"no bridge named {source_id!r}; available: {names}")
            return
        probe = bridge.probe(Path(path)) if path else bridge.availability()
        if not probe.ok or probe.root is None:
            print(f"{bridge.NAME}: {probe.detail or probe.availability.name}")
            return
        self.mounts = bridge.mount(probe.root)
        self.vfs.set_mounts(self.mounts)
        print(f"{self.mounts.title}: {len(self.mounts)} mounts from {self.mounts.root}")
        for warning in self.mounts.warnings:
            print(f"  warning: {warning}")
        started = time.perf_counter()
        stats = self.index.build(self.vfs) if force else self.index.refresh(self.vfs)
        print(f"  {stats.summary()} ({time.perf_counter() - started:.1f} s)")

    def ready(self) -> bool:
        """True when something is mounted; prints what to do when not."""
        if self.mounts is None:
            print("nothing is mounted yet - run `mount`")
            return False
        return True

    # -- the index ---------------------------------------------------------------
    def cmd_mounts(self) -> None:
        """Every mount in priority order."""
        if not self.ready():
            return
        for mount in self.vfs.mounts:
            folders = ", ".join(mount.content_dirs()) or "-"
            print(f"  {mount.priority:3d} {mount.name:24s} {mount.path}  [{folders}]")

    def cmd_stats(self) -> None:
        """What the index holds."""
        if not self.ready():
            return
        stats = self.index.stats()
        built = self.index.built_at()
        when = time.strftime("%Y-%m-%d %H:%M", time.localtime(built)) if built else "never"
        print(f"  {stats.summary()}  (built {when})")
        print(f"  database {self.index.db_path}")

    def cmd_kinds(self) -> None:
        """File kinds and how many of each are visible."""
        if not self.ready():
            return
        for kind, count in sorted(self.index.kinds().items(), key=lambda kv: -kv[1]):
            print(f"  {count:8d}  {kind}")

    def cmd_find(self, text: str, kind: Optional[str] = None, limit: int = 40) -> None:
        """Search the index for a path."""
        if not self.ready():
            return
        found = self.index.search(text, kind, limit)
        for entry in found:
            print(f"  {entry.rel}")
        print(f"  {len(found)} shown")

    def cmd_ls(self, folder: str = "", kind: Optional[str] = None, limit: int = 60) -> None:
        """List a folder of the mounted content."""
        if not self.ready():
            return
        for entry in self.index.in_folder(folder, kind, limit):
            print(f"  {entry.rel}")

    def cmd_read(self, rel: str) -> None:
        """Where a content path resolves to, and how big it is."""
        if not self.ready():
            return
        path = self.vfs.resolve(rel)
        if path is None:
            print(f"  {rel}: not found")
            return
        print(f"  {path}  ({path.stat().st_size} bytes)")
        overrides = self.index.overrides(rel)
        if len(overrides) > 1:
            print("  also in:")
            for entry in overrides[1:]:
                print(f"    {entry.mount_name}: {entry.path}")

    # -- formats -----------------------------------------------------------------
    def cmd_model(self, rel: str) -> None:
        """Load a model through the whole mdl / vvd / vtx path."""
        if not self.ready():
            return
        started = time.perf_counter()
        model = load_model(self.vfs, rel)
        print(f"  {model.summary()}  ({time.perf_counter() - started:.2f} s)")
        print(f"  material dirs: {', '.join(model.material_dirs) or '-'}")
        for mesh in model.meshes[:12]:
            flexes = f", {len(mesh.flexes)} flexes" if mesh.flexes else ""
            print(f"    {mesh.material:44s} {mesh.vertex_count:6d} verts, {mesh.triangle_count:6d} tris{flexes}")
        if len(model.meshes) > 12:
            print(f"    ... {len(model.meshes) - 12} more")
        if model.flex_controllers:
            names = ", ".join(c.name for c in model.flex_controllers[:8])
            print(f"  flex controllers: {len(model.flex_controllers)} ({names}...)")
        for warning in model.warnings[:5]:
            print(f"  warning: {warning}")

    def cmd_material(self, rel: str) -> None:
        """Read a material and show what a renderer would take from it."""
        if not self.ready():
            return
        material = load_material(self.vfs, rel)
        if material is None:
            print(f"  {rel}: not found")
            return
        print(f"  {material.summary()}")
        for key in sorted(material.params):
            print(f"    {key:28s} {material.params[key]}")
        for warning in material.warnings:
            print(f"  warning: {warning}")

    def cmd_texture(self, rel: str) -> None:
        """Parse a texture header."""
        if not self.ready():
            return
        data = self.vfs.read_bytes(rel if rel.endswith(".vtf") else f"materials/{rel}.vtf")
        if data is None:
            print(f"  {rel}: not found")
            return
        vtf = parse_vtf(data, rel)
        print(f"  {vtf.width}x{vtf.height} {vtf.format_name} v{vtf.version[0]}.{vtf.version[1]}, "
              f"{len(vtf.mips)} mips, flags {vtf.flags:#x}{', cubemap' if vtf.is_cubemap else ''}")
        for warning in vtf.warnings[:5]:
            print(f"  warning: {warning}")

    def cmd_map(self, name: str) -> None:
        """Parse a map and show what the renderer would get from it."""
        if not self.ready():
            return
        rel = map_path(name)
        data = self.vfs.read_bytes(rel)
        if data is None:
            print(f"  {rel}: not found")
            return
        started = time.perf_counter()
        bsp = parse_bsp(data, rel)
        lo, hi = bsp.bounds
        print(f"  {rel}: version {bsp.version}, {len(bsp.faces)} faces, {len(bsp.static_props)} props, "
              f"{len(bsp.entities)} entities, {len(bsp.world_lights)} lights ({time.perf_counter() - started:.1f} s)")
        print(f"  sky {bsp.sky_name or '-'}, sun {'yes' if bsp.sky_light else 'no'}, "
              f"tonemap {'yes' if bsp.tone_map else 'no'}, pak {len(bsp.pak_files())} files")
        print(f"  bounds {tuple(round(v) for v in lo)} .. {tuple(round(v) for v in hi)}")
        for warning in bsp.warnings[:5]:
            print(f"  warning: {warning}")

    # -- sessions ----------------------------------------------------------------
    def cmd_session(self, path: str) -> None:
        """Open a session and show its shots, models and sound."""
        session = Session(load_dmx(Path(path)))
        clip = session.active_clip
        print(f"  {session.summary()}")
        print(f"  {session.frame_rate:g} fps, movie {session.movie_size[0]}x{session.movie_size[1]}")
        if clip is None:
            return
        print(f"  sequence {clip.time_frame.duration.seconds:.2f} s on map {clip.map_name or '-'}")
        for shot in clip.shots:
            frame = shot.time_frame
            models = len(shot.game_models()) if shot.scene is not None else 0
            camera = shot.camera.name if shot.camera is not None else "-"
            print(f"    {shot.name:16s} {frame.start.seconds:7.2f} +{frame.duration.seconds:6.2f}  "
                  f"camera {camera:28s} {models} models")
        sounds = active_sound_clips(clip)
        missing = [s.path for s in sounds if self.vfs.resolve(s.path) is None] if self.mounts else []
        print(f"  sound: {len(sounds)} clips that play" + (f", {len(missing)} missing" if missing else ""))

    def cmd_eval(self, path: str, seconds: str) -> None:
        """Evaluate a session at a time, then report what the engine computed."""
        session = Session(load_dmx(Path(path)))
        clip = session.active_clip
        if clip is None:
            print("  the session has no active clip")
            return
        at = Time.from_seconds(float(seconds))
        evaluator = Evaluator()
        started = time.perf_counter()
        evaluator.evaluate(clip, at)
        shot = clip.shot_at(at)
        print(f"  {at.seconds:.3f} s: {evaluator.channels_run} channels, {evaluator.operators_run} operators "
              f"({time.perf_counter() - started:.2f} s)")
        if shot is None:
            print("  no shot plays at that moment")
            return
        print(f"  shot {shot.name}")
        if shot.scene is None:
            return
        for node, world, visible in shot.scene.walk_visibility():
            if isinstance(node, GameModel) and visible:
                where = tuple(round(v, 1) for v in (world[3], world[7], world[11]))
                print(f"    {node.name:36s} {node.model_name:48s} at {where}")
            elif isinstance(node, ProjectedLight) and visible:
                print(f"    light {node.name:30s} intensity {node.intensity:.2f} "
                      f"colour {tuple(round(c, 2) for c in node.color)}")
        for error in evaluator.errors[:5]:
            print(f"  error: {error}")

    # -- the shell ---------------------------------------------------------------
    COMMANDS = {
        "mount": "mount", "rescan": None, "mounts": "cmd_mounts", "stats": "cmd_stats",
        "kinds": "cmd_kinds", "find": "cmd_find", "ls": "cmd_ls", "read": "cmd_read",
        "model": "cmd_model", "material": "cmd_material", "texture": "cmd_texture",
        "map": "cmd_map", "session": "cmd_session", "eval": "cmd_eval",
    }

    def run(self, words: List[str]) -> None:
        """Run one command; unknown ones print the help."""
        if not words:
            return
        name, args = words[0].lower(), words[1:]
        if name in ("help", "?"):
            print(__doc__)
            return
        if name == "rescan":
            self.mount(force=True) if self.mounts is None else self._rescan()
            return
        method = self.COMMANDS.get(name)
        if method is None:
            print(f"unknown command {name!r}; try `help`")
            return
        try:
            getattr(self, method)(*args)
        except TypeError as exc:
            print(f"  {name}: {exc}")
        except (FormatError, ValueError) as exc:
            print(f"  {name}: {exc}")
        except OSError as exc:
            print(f"  {name}: {exc}")

    def _rescan(self) -> None:
        started = time.perf_counter()
        stats = self.index.build(self.vfs)
        print(f"  {stats.summary()} ({time.perf_counter() - started:.1f} s)")


def main(argv: Optional[List[str]] = None) -> int:
    """Open the shell, or run the one command given on the command line."""
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    argv = list(sys.argv[1:] if argv is None else argv)
    shell = CoreShell()
    if argv:
        shell.mount()
        shell.run(argv)
        return 0
    print(f"C2UI core - {PROJECT_ROOT}\ntype `help` for the commands, `quit` to leave")
    shell.mount()
    while True:
        try:
            line = input("core> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if line.lower() in ("quit", "exit"):
            return 0
        try:
            shell.run(shlex.split(line))
        except ValueError as exc:                     # an unbalanced quote in the line
            print(f"  {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
