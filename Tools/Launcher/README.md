# Launcher

`c2ui.py` starts the editor; `requirements.txt` lists what the window needs
(the engine in `Core/` needs nothing).

    python -m venv .venv
    .venv/Scripts/python.exe -m pip install -r Tools/Launcher/requirements.txt
    .venv/Scripts/python.exe Tools/Launcher/c2ui.py

A packaged launcher - one executable that carries its own Python and updates
itself - is planned here.
