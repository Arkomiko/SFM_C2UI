#!/usr/bin/env python3
"""
SFM - C2UI  (Source Film Maker - Custom to User Interface)
Application entry point.

    python main.py [--workspace UnrealEditor] [--theme ue5_dark] [--lang ru]
                   [--safe-mode] [--no-sfm] [--log-level DEBUG]
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

SDK_ROOT = Path(__file__).resolve().parent
if str(SDK_ROOT) not in sys.path:
    sys.path.insert(0, str(SDK_ROOT))

MIN_PY = (3, 10)


def _check_environment() -> None:
    if sys.version_info < MIN_PY:
        sys.exit(f"C2UI requires Python {MIN_PY[0]}.{MIN_PY[1]}+ (found {sys.version.split()[0]}).")
    try:
        import PySide6  # noqa: F401
    except ImportError:
        venv_py = SDK_ROOT / ".venv" / "Scripts" / "python.exe"
        hint = f"  {venv_py} main.py" if venv_py.is_file() else "  setup.bat   (creates .venv and installs requirements.txt)"
        sys.exit("PySide6 is not installed for this interpreter.\nRun C2UI with:\n" + hint)


def parse_args(argv: list[str]) -> dict:
    p = argparse.ArgumentParser(prog="C2UI", description="Modern UI shell for Source Filmmaker")
    p.add_argument("--workspace", "-w", help="workspace id (folder name in Workspaces/)")
    p.add_argument("--theme", "-t", help="theme id (file name in Themes/ without .json)")
    p.add_argument("--lang", "-l", help="language code (file name in Locales/)")
    p.add_argument("--safe-mode", action="store_true", help="skip plugins and saved user layouts")
    p.add_argument("--no-sfm", action="store_true", help="do not launch / connect to sfm.exe")
    p.add_argument("--log-level", default=None, help="DEBUG, INFO, WARNING, ERROR")
    ns = p.parse_args(argv)
    return {"workspace": ns.workspace, "theme": ns.theme, "lang": ns.lang, "safe_mode": ns.safe_mode,
            "no_sfm": ns.no_sfm, "log_level": ns.log_level}


def main(argv: list[str] | None = None) -> int:
    _check_environment()
    os.chdir(SDK_ROOT)
    args = parse_args(sys.argv[1:] if argv is None else argv)
    from Core.Library.app import C2UIApplication
    return C2UIApplication(args).run()


if __name__ == "__main__":
    sys.exit(main())
