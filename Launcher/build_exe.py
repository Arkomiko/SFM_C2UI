"""
Build the launcher into one executable.

    .venv/Scripts/python.exe -m pip install pyinstaller
    .venv/Scripts/python.exe Launcher/build_exe.py

The result is `Launcher/dist/C2UI Launcher.exe`, a single file that needs no
Python on the machine it is copied to - as long as it stays inside the project
folder, which is what it starts.  Everything the build leaves behind (`build`,
`dist`, the spec file) lives under `Launcher/` and is ignored by git: a binary
does not belong in the source tree.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

LAUNCHER = Path(__file__).resolve().parent
ROOT = LAUNCHER.parent
NAME = "C2UI Launcher"

#: Qt brings far more than a window with three buttons; leaving the rest out
#: keeps the executable a third of the size and the start quick
EXCLUDED = ("PySide6.QtQml", "PySide6.QtQuick", "PySide6.QtQuick3D", "PySide6.QtWebEngineCore",
            "PySide6.QtWebEngineWidgets", "PySide6.QtMultimedia", "PySide6.QtMultimediaWidgets",
            "PySide6.Qt3DCore", "PySide6.QtCharts", "PySide6.QtDataVisualization", "PySide6.QtNetwork",
            "PySide6.QtSql", "PySide6.QtTest", "PySide6.QtOpenGL", "PySide6.QtOpenGLWidgets",
            "PySide6.QtPdf", "PySide6.QtPrintSupport", "PySide6.QtSvg", "PySide6.QtDesigner",
            "numpy", "OpenGL", "sqlite3", "unittest", "pydoc", "tkinter")


def main() -> int:
    """Run PyInstaller and report where the executable landed."""
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller is not installed:\n"
              "    .venv/Scripts/python.exe -m pip install pyinstaller")
        return 1
    command = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile", "--windowed",
               "--name", NAME,
               "--distpath", str(LAUNCHER / "dist"),
               "--workpath", str(LAUNCHER / "build"),
               "--specpath", str(LAUNCHER / "build")]
    for module in EXCLUDED:
        command += ["--exclude-module", module]
    command.append(str(LAUNCHER / "launcher.py"))
    print(" ".join(command))
    result = subprocess.run(command, cwd=str(ROOT))
    if result.returncode:
        return result.returncode
    exe = LAUNCHER / "dist" / f"{NAME}.exe"
    if not exe.is_file():                                  # not Windows: PyInstaller drops the suffix
        exe = LAUNCHER / "dist" / NAME
    print(f"\n{exe}  ({exe.stat().st_size / 1024 / 1024:.1f} MB)" if exe.exists() else "\nnothing was built")
    shutil.rmtree(LAUNCHER / "build", ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
