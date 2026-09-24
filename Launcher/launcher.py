"""
The launcher window: what starts C2UI on a machine that has no Python of its own.

    .venv/Scripts/python.exe Launcher/launcher.py        from a checkout
    "C2UI Launcher.exe"                                  the built one

Deliberately plain and deliberately temporary - the owner asked for exactly
three buttons while the editor is the only thing there is to start.  It is
built into a single executable by `build_exe.py`, so it must find the project
around itself rather than relying on the working directory, and it must be
able to say why a start failed rather than closing silently.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

__all__ = ["LauncherWindow", "project_root", "python_for", "main"]

TITLE = "C2UI - Launcher [Dev-mode]"
DESCRIPTION = "Описание: Временный вид у лаунчера, он потом переписан будет!"

#: the folders that mark the project root, so the exe can sit anywhere under it
MARKERS = ("App", "Core", "Launcher")

STYLE = """
QWidget#root { background: #17181c; }
QLabel#title { color: #f2f4f8; }
QLabel#description { color: #98a0ad; }
QFrame#rule { background: #2a2d34; max-height: 1px; border: none; }
QPushButton {
    background: #23262d; color: #e8ebf0; border: 1px solid #333842;
    border-radius: 4px; padding: 10px 18px; min-width: 150px;
}
QPushButton:hover { background: #2c3039; border-color: #3d4450; }
QPushButton:pressed { background: #1d2026; }
QPushButton:disabled { background: #1c1e23; color: #5b616b; border-color: #26292f; }
QPushButton#quit { min-width: 110px; }
"""


def project_root(start: Optional[Path] = None) -> Optional[Path]:
    """The C2UI folder around this file (or around the executable), or None.

    A frozen launcher sits in `Launcher/dist`, a checkout's in `Launcher`, and
    someone may copy the exe to the project root itself; all three are found by
    walking up until a folder holds App, Core and Launcher.
    """
    here = (Path(start) if start is not None else Path(
        sys.executable if getattr(sys, "frozen", False) else __file__).parent).resolve()
    for folder in (here, *here.parents):
        if all((folder / name).is_dir() for name in MARKERS):
            return folder
    return None


def python_for(root: Path) -> Optional[Path]:
    """The interpreter that can run the editor: the project's own virtual
    environment first, then whatever Python is on the PATH."""
    for candidate in (root / ".venv" / "Scripts" / "pythonw.exe", root / ".venv" / "Scripts" / "python.exe",
                      root / ".venv" / "bin" / "python"):
        if candidate.is_file():
            return candidate
    from shutil import which
    found = which("pythonw") or which("python") or which("python3")
    return Path(found) if found else None


def dark_title_bar(window: QWidget) -> bool:
    """Ask Windows for a dark title bar, so the frame matches the window.

    Windows 10 1809 and up; anywhere else the light frame simply stays.
    """
    if sys.platform != "win32":
        return False
    try:
        import ctypes
        handle = int(window.winId())
        for attribute in (20, 19):          # DWMWA_USE_IMMERSIVE_DARK_MODE, and the number it had before 1903
            value = ctypes.c_int(1)
            if ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    handle, attribute, ctypes.byref(value), ctypes.sizeof(value)) == 0:
                return True
    except Exception:                       # noqa: BLE001 - a light frame is not a failure
        pass
    return False


class LauncherWindow(QWidget):
    """Title, one line of description, and the three buttons."""

    def __init__(self) -> None:
        super().__init__()
        self.root = project_root()
        self.setObjectName("root")
        self.setWindowTitle(TITLE)
        self.setFixedSize(560, 300)
        self.setStyleSheet(STYLE)

        title = QLabel(TITLE)
        title.setObjectName("title")
        title.setAlignment(Qt.AlignHCenter)
        font = QFont(title.font())
        font.setPointSize(17)
        font.setWeight(QFont.DemiBold)
        title.setFont(font)

        description = QLabel(DESCRIPTION)
        description.setObjectName("description")
        description.setAlignment(Qt.AlignHCenter)
        description.setWordWrap(True)

        rule = QFrame()
        rule.setObjectName("rule")
        rule.setFrameShape(QFrame.HLine)

        self.core_button = QPushButton("Запустить Core")
        self.core_button.clicked.connect(self.start_core)
        self.app_button = QPushButton("Запустить App")
        self.app_button.setEnabled(False)                      # there is no App yet
        self.app_button.setToolTip("App ещё нет")
        quit_button = QPushButton("Выйти")
        quit_button.setObjectName("quit")
        quit_button.clicked.connect(self.close)

        buttons = QHBoxLayout()
        buttons.setSpacing(12)
        buttons.addStretch(1)
        buttons.addWidget(self.core_button)
        buttons.addWidget(self.app_button)
        buttons.addWidget(quit_button)
        buttons.addStretch(1)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(14)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(rule)
        layout.addStretch(1)
        layout.addLayout(buttons)

        if self.root is None:
            self.core_button.setEnabled(False)
            description.setText(DESCRIPTION + "\n\nПроект не найден: положите лаунчер внутрь папки C2UI_SDK.")

    def showEvent(self, event) -> None:
        super().showEvent(event)
        dark_title_bar(self)                           # the window handle exists only once shown

    # -- starting things -------------------------------------------------------------
    def start_core(self) -> None:
        """Start the editor in its own process and close the launcher."""
        command = self.core_command()
        if command is None:
            QMessageBox.critical(self, TITLE, "Не найден Python для запуска редактора.\n"
                                              "Создайте .venv в папке проекта:\n\n"
                                              "python -m venv .venv\n"
                                              ".venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt")
            return
        try:
            subprocess.Popen(command, cwd=str(self.root), close_fds=True,
                             creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except OSError as exc:
            QMessageBox.critical(self, TITLE, f"Редактор не запустился:\n{exc}")
            return
        self.close()

    def core_command(self) -> Optional[List[str]]:
        """What to run to get the editor, or None when no interpreter is around."""
        if self.root is None:
            return None
        interpreter = python_for(self.root)
        if interpreter is None:
            return None
        return [str(interpreter), str(self.root / "Launcher" / "c2ui.py")]


def main(argv: Optional[List[str]] = None) -> int:
    """Show the launcher; returns the process exit code."""
    app = QApplication(list(sys.argv if argv is None else argv))
    app.setApplicationName("C2UI Launcher")
    app.setOrganizationName("C2UI")
    window = LauncherWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")
    raise SystemExit(main())
