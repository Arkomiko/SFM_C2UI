# Testing

All automated tests, kept out of `Core/` and `App/` so neither ships with test
code and both stay "folders only" as designed.

    python Testing/run.py                 everything
    python Testing/run.py core            one folder
    python Testing/run.py core/test_vfs   one module

The runner has no dependencies: the engine is pure standard library, so its
tests run anywhere Python does. The editor's tests avoid a window too; the
few checks that need OpenGL live outside the repository.

| Folder | Covers |
|---|---|
| `core/` | The engine: mounts and the VFS, the content index, bridges and dev-kit slots, every format reader (DMX byte-exact, models, materials, textures, maps), sessions, animation, operators and rigs, editing, keys, the motion editor |
| `app/` | The editor without a window: locations and the "inside `App/` only" rule, settings, scene building, the manipulator, render maths |
| `tools/` | The utilities in `Tools/` |
| `fixtures/` | Shared sample data: a fake installation, a small model with flexes, materials, sessions |

`fixtures/` is shared on purpose - a fake SFM installation is needed by both the
bridge tests and the editor tests, and duplicating it would let the two drift
apart.

If Core is ever split into its own repository, `core/` and the fixtures it uses
move with it.
