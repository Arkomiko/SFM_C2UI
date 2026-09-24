# Launcher

How C2UI is started.

## The window

`launcher.py` is what a person opens: a title, a line of description and three
buttons - start Core, start App (greyed out, there is no App yet) and quit.
Temporary by design; it will be rewritten when App exists.

    .venv/Scripts/python.exe Launcher/launcher.py

Built into one executable that needs no Python on the machine:

    .venv/Scripts/python.exe -m pip install pyinstaller
    .venv/Scripts/python.exe Launcher/build_exe.py      ->  Launcher/dist/C2UI Launcher.exe

The executable finds the project by walking up from wherever it sits until it
sees `App`, `Core` and `Launcher` together, so it works from `Launcher/dist`,
from `Launcher/` or from the project root - but it has to stay inside the
project, which is what it starts.  `build/`, `dist/` and the spec file are
ignored by git: a binary does not belong in the source tree.

## The editor

`c2ui.py` opens the editor, which is what the launcher's "Запустить Core"
starts; `requirements.txt` lists what that window needs (the engine in `Core/`
needs nothing beyond the standard library).

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
