"""
Start the editor.

    .venv/Scripts/python.exe Tools/Launcher/c2ui.py

Runs from the project folder and writes only inside it: settings under
App/User, caches under App/Cache, the log under App/Temporary.  The
project root holds nothing but folders and the README, so the launcher
lives here and finds the root two folders up.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _logging() -> None:
    from App.Code import locations
    locations.ensure_dirs()
    handlers = [logging.StreamHandler(sys.stderr)]
    try:
        handlers.append(logging.FileHandler(locations.TEMPORARY / "c2ui.log", encoding="utf-8"))
    except OSError:
        pass
    logging.basicConfig(level=logging.INFO, handlers=handlers,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def main() -> int:
    _logging()
    from PySide6.QtGui import QSurfaceFormat
    from PySide6.QtWidgets import QApplication

    from App.Code.main_window import MainWindow
    from App.Code.render.viewport import gl_format
    from App.Code.settings import Settings

    QSurfaceFormat.setDefaultFormat(gl_format())
    app = QApplication(sys.argv)
    app.setApplicationName("C2UI")
    app.setOrganizationName("C2UI")

    settings = Settings.load()
    window = MainWindow(settings)
    window.restore_geometry()
    window.show()
    window.open_content()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
