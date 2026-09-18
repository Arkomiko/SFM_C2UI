"""Start and locate the original sfm.exe process (optional - SFM may be absent)."""
from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path
from typing import List, Optional

from Core.Library import paths

log = logging.getLogger("c2ui.launcher")


class SFMLauncher:
    def __init__(self, exe: Optional[str | Path] = None) -> None:
        self._exe: Optional[Path] = Path(exe) if exe else paths.sfm_exe()
        self._proc: Optional[subprocess.Popen] = None

    # -- configuration ----------------------------------------------------------
    @property
    def exe(self) -> Optional[Path]:
        return self._exe

    def set_exe(self, exe: Optional[str | Path]) -> None:
        """Re-point at another sfm.exe (called when the user edits the SFM path)."""
        self._exe = Path(exe) if exe else None

    def available(self) -> bool:
        return bool(self._exe and self._exe.is_file())

    # -- process ----------------------------------------------------------------
    def launch(self, args: Optional[List[str]] = None, env: Optional[dict] = None) -> Optional[subprocess.Popen]:
        if not self.available():
            log.error("sfm.exe not found at %s", self._exe or "(not configured)")
            return None
        if self.is_running():
            log.info("SFM already running (pid %s)", self.pid)
            return self._proc
        assert self._exe is not None
        cmd = [str(self._exe)] + list(args or [])
        full_env = dict(os.environ)
        if env:
            full_env.update(env)
        full_env["C2UI_SDK_ROOT"] = str(paths.SDK_ROOT)
        log.info("Launching SFM: %s", " ".join(cmd))
        try:
            self._proc = subprocess.Popen(cmd, cwd=str(self._exe.parent), env=full_env)
        except OSError:
            log.exception("Failed to launch SFM")
            self._proc = None
        return self._proc

    def is_running(self) -> bool:
        return self._proc is not None and self._proc.poll() is None

    @property
    def pid(self) -> Optional[int]:
        return self._proc.pid if self.is_running() else None

    def terminate(self) -> None:
        if self.is_running() and self._proc is not None:
            log.info("Terminating SFM (pid %s)", self._proc.pid)
            self._proc.terminate()
