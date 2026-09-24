# Launcher

How C2UI is started. Two entry points for now; the packaged launcher - one
executable that carries its own Python and updates itself - will live here too.

## The editor

`c2ui.py` opens the window; `requirements.txt` lists what that window needs
(the engine in `Core/` needs nothing beyond the standard library).

    python -m venv .venv
    .venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
    .venv/Scripts/python.exe Launcher/c2ui.py

## The engine alone

`core.py` starts `Core` without the editor: it mounts an installation,
indexes it, and gives a small shell over the engine - models, materials,
textures, maps, sessions and their evaluation.

    python Launcher/core.py                          the shell
    python Launcher/core.py model models/player/hwm/heavy.mdl
    python Launcher/core.py map afd_warehouse
    python Launcher/core.py eval <session.dmx> 6.0

**Temporary.** It exists while the editor is the only way to see anything;
once `App` can be started headless, the editor becomes the single entry point
and this goes. Nothing in it imports `App` - it only picks where the index is
cached (`App/Cache/content`, the same scan the editor uses), which is the one
thing `Core` never decides for itself.
