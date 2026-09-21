# App

The C2UI editor itself.

| Folder | Lifetime |
|---|---|
| `Code/` | The editor's source |
| `Data/` | Ships with the program, read-only |
| `User/` | Belongs to the user - **never deleted automatically** |
| `Cache/` | Regenerable, shared by every session, survives restarts |
| `Temporary/` | Session scratch, cleared on start |
| `Legal/` | Licences |

This folder contains **only folders**. Anything loose here is a mistake.
Everything the editor writes goes under `User/`, `Cache/` or `Temporary/`;
nothing is written anywhere else on the machine.

## Code

| Module | Does |
|---|---|
| `main_window.py` | The window: panels, menus, session load/save, selection, playback, undo |
| `content_library.py` | Mounts an installation through `Core.API` and keeps its index in `Cache/content` |
| `locations.py` | Every writable path, all inside this folder |
| `settings.py` | User settings as JSON under `User/Settings` |
| `export.py` | Renders the sequence to an image sequence or a movie (MJPEG AVI natively, H.264 MP4 through Qt Multimedia) |
| `render/scene.py` | From content to draw items: models, poses, the map, lights |
| `render/renderer.py` | Draws a scene with the GL 3.3 shaders in `render/shaders.py` |
| `render/gl_resources.py` | Meshes and textures on the GPU |
| `render/viewport.py` | The QOpenGLWidget: SFM camera controls, picking, the manipulator |
| `render/camera.py`, `render/manipulator.py`, `render/math3d.py` | Camera, gizmo, matrices |
| `ui/session_tree.py` | Shots, scenes and animation sets |
| `ui/timeline.py` | Clips, the time cursor, the time selection |
| `ui/graph_editor.py` | Curves and keys of the selected element |
| `ui/inspector.py` | An element's attributes, editable |
| `ui/docking.py` | Panels that dock the UE5 way |
| `ui/export_dialog.py` | What to export, how big, how fast, which part |
