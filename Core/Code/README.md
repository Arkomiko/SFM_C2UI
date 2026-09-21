# Code

Engine source code.

Everything public about these modules is declared in `Core/API`; App, the tools
and plugins import that contract, never these modules directly. That is what
lets the engine change without breaking anything built on it.

| Module | Does |
|---|---|
| `vfs.py` | Layered file system over the mounts: the highest-priority copy of a path wins |
| `content_index.py` | SQLite index of every mounted file, built once and reused |
| `keyvalues.py` | Valve KeyValues (`gameinfo.txt`, `.vmt`) |
| `registry.py` | Finds and loads the bridges in `dev-kit/` |
| `transform.py` | Vectors, quaternions, 3x4 matrices in Source's conventions |
| `pose.py` | Bind poses and skinning matrices for a model's skeleton |
| `flex.py` | Flex controllers to vertex deltas |
| `animation.py` | Evaluates a session's channels and logs at a time |
| `operators.py` | Expressions, pack operators, rig constraints and IK |
| `expression.py` | SFM's expression language |
| `editing.py` | The undo stack and the elementary commands |
| `keys.py` | Editing a log's keys: move, insert, delete, per component |
| `motion.py` | The time selection and offsets applied over it |
| `locations.py` | Where Core's own folders are |
| `formats/` | Readers: `binary` (bounds-checked cursors), `dmx` (binary 1–5 and keyvalues2), `mdl` / `vvd` / `vtx` / `studio` (models), `vmt` (materials), `vtf` (textures), `bsp` (maps) |
