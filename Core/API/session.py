"""
SFMSession - everything C2UI knows about the *optional* Source Filmmaker install.

C2UI ships as a standalone shell: SFM may be missing entirely.  This class owns

* **where** SFM is (settings -> env -> auto-detect), and whether it is usable
* the process (:class:`SFMLauncher`) and the RPC link (:class:`SFMBridge`)
* the workflow launch -> agent connects -> embed viewport / sync theme -> release

Every SFM-dependent feature asks :attr:`available` first, so the UI can stay alive
and simply tell the user to point C2UI at their SFM installation.
"""
from __future__ import annotations

import ctypes
import dataclasses
import logging
import time
from ctypes import wintypes
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PySide6.QtCore import QObject, QTimer, Signal

from Core.API import native
from Core.API.agent import install_agent
from Core.API.bridge import SFMBridge
from Core.API.launcher import SFMLauncher
from Core.Library import paths

log = logging.getLogger("c2ui.session")

VIEWPORT_LOOKUP_DEFAULT = "Primary Viewport"


class SFMSession(QObject):
    availability_changed = Signal(bool)   # SFM install found / lost
    viewport_ready = Signal(int)          # hwnd of the detached SFM viewport
    viewport_released = Signal()
    agent_ready = Signal(dict)            # handshake info
    status_message = Signal(str)

    def __init__(self, app: Any, launcher: SFMLauncher, bridge: SFMBridge, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.app = app
        self.launcher = launcher
        self.bridge = bridge
        self.viewport_hwnd: Optional[int] = None
        self._available = False
        self._theme_pushed = False
        self._babysit = QTimer(self)
        self._babysit.setInterval(1000)
        self._babysit.timeout.connect(self._babysit_startup)
        self._babysit_until = 0.0
        bridge.handshake_done.connect(self._on_handshake)
        bridge.connected_changed.connect(self._on_connected_changed)
        app.theme.theme_changed.connect(self._on_theme_changed)
        self.resolve_path()

    # ===================================================== installation path
    def resolve_path(self, announce: bool = False) -> bool:
        """Apply the configured SFM root (settings -> env -> auto-detect).

        Returns True when a usable installation is available.  Safe to call at any
        time; emits :attr:`availability_changed` when the answer changes.
        """
        configured = str(self.app.settings.get("sfm.root", "") or "")
        if configured:
            ok, result = paths.set_sfm_root(configured)
            if not ok:
                log.warning("Configured SFM path is not usable (%s): %s", result, configured)
                paths.set_sfm_root(None)
        else:
            paths.set_sfm_root(None)        # fall back to env / auto-detection

        available = paths.sfm_is_installed()
        root = paths.sfm_root()
        # Remember an auto-detected root so the user sees it in Preferences.
        if available and not configured and root is not None:
            self.app.settings.set("sfm.root", str(root))

        exe_override = str(self.app.settings.get("sfm.exe", "") or "")
        self.launcher.set_exe(Path(exe_override) if exe_override else paths.sfm_exe())

        if available != self._available:
            self._available = available
            log.info("SFM installation %s (%s)", "available" if available else "NOT available", root or "-")
            self.availability_changed.emit(available)
        elif announce:
            self.availability_changed.emit(available)
        return available

    def set_path(self, candidate) -> Tuple[bool, str]:
        """Point C2UI at an SFM install (Preferences).  Returns ``(ok, root_or_reason)``."""
        if not candidate:
            self.app.settings.set("sfm.root", "")
            self.resolve_path(announce=True)
            return True, ""
        ok, result = paths.validate_sfm_root(candidate)
        if not ok:
            return False, result
        self.app.settings.set("sfm.root", result)
        self.resolve_path(announce=True)
        return True, result

    @property
    def available(self) -> bool:
        """True when an SFM installation is configured *and* sfm.exe exists."""
        return self._available

    @property
    def root(self) -> Optional[Path]:
        return paths.sfm_root()

    def requirement_hint(self) -> str:
        """Why SFM features are unavailable (empty string when everything is fine)."""
        if self._available:
            return ""
        configured = str(self.app.settings.get("sfm.root", "") or "")
        if configured:
            return f"sfm.exe not found under {configured}"
        return "SFM installation not configured"

    # ------------------------------------------------------------- queries
    @property
    def connected(self) -> bool:
        return self.bridge.connected

    def sfm_pids(self) -> List[int]:
        return native.find_process("sfm.exe")

    def sfm_running(self) -> bool:
        return self.launcher.is_running() or bool(self.sfm_pids())

    def agent_installed(self) -> bool:
        return install_agent.is_installed()

    # ------------------------------------------------------------- actions
    def launch(self) -> bool:
        if not self.resolve_path():
            self.status_message.emit(self.requirement_hint())
            return False
        settings = self.app.settings
        if settings.get("sfm.auto_install_agent", True) and not self.agent_installed():
            try:
                install_agent.install()
            except OSError:
                log.exception("Agent auto-install failed")
        env = {"C2UI_AGENT_PORT": str(self.bridge.port)}
        proc = self.launcher.launch(settings.get("sfm.launch_args", []), env=env)
        if proc is None:
            return False
        self.bridge.connect_to_agent()
        if settings.get("sfm.auto_dismiss_startup_dialogs", True):
            self._babysit_until = time.time() + 120
            self._babysit.start()
        return True

    def install_agent(self) -> Dict[str, str]:
        if not self.available:
            raise RuntimeError(self.requirement_hint())
        return install_agent.install()

    def uninstall_agent(self) -> Dict[str, str]:
        if not self.available:
            raise RuntimeError(self.requirement_hint())
        return install_agent.uninstall()

    def embed_viewport(self, lookup: Optional[str] = None) -> None:
        if not self.bridge.connected:
            self.status_message.emit("SFM agent not connected")
            return
        lookup = lookup or self.app.settings.get("sfm.viewport_lookup", VIEWPORT_LOOKUP_DEFAULT)
        vp = self.app.layout.panel("viewport")
        size = [max(320, vp.width()), max(200, vp.height())] if vp is not None else [1280, 720]
        self.bridge.call("c2ui.detach_widget", {"name": lookup, "tool": True, "size": size}, self._on_detached)

    def _on_detached(self, result: Any, error: Optional[Dict[str, Any]]) -> None:
        if error:
            log.warning("Viewport detach failed: %s", error.get("message"))
            self.status_message.emit(f"Viewport: {error.get('message')}")
            return
        hwnd = int((result or {}).get("hwnd") or 0)
        if not hwnd or not native.is_window(hwnd):
            log.warning("Agent returned invalid viewport hwnd %r", hwnd)
            self.status_message.emit("Viewport: invalid window handle")
            return
        self.viewport_hwnd = hwnd
        log.info("SFM viewport hwnd=%d ready for embedding", hwnd)
        self.viewport_ready.emit(hwnd)

    def release_viewport(self) -> None:
        if self.viewport_hwnd is None:
            return
        self.viewport_released.emit()
        if self.bridge.connected:
            self.bridge.call("c2ui.restore_all", {}, lambda r, e: log.debug("restore_all -> %s %s", r, e))
        self.viewport_hwnd = None

    def sync_theme(self, enable: Optional[bool] = None) -> None:
        if enable is not None:
            self.app.settings.set("sfm.sync_theme", bool(enable))
        if not self.bridge.connected:
            return
        if not self.app.settings.get("sfm.sync_theme", True):
            if self._theme_pushed:
                self.bridge.call("c2ui.reset_qss", {})
                self._theme_pushed = False
            return
        theme = self.app.theme.current
        if theme is None:
            return
        native_theme = dataclasses.replace(theme, qss="sfm_native.qss")
        try:
            qss = self.app.theme.build_qss(native_theme)
        except (FileNotFoundError, OSError):
            log.warning("Themes/sfm_native.qss missing - theme sync skipped")
            return
        self.bridge.call("c2ui.apply_qss", {"qss": qss}, lambda r, e: log.debug("apply_qss -> %s %s", r, e))
        self._theme_pushed = True

    def reset_theme(self) -> None:
        if self.bridge.connected:
            self.bridge.call("c2ui.reset_qss", {})
        self._theme_pushed = False

    def shutdown(self) -> None:
        self._babysit.stop()
        if self.bridge.connected:
            if self.viewport_hwnd is not None:
                self.bridge.call("c2ui.restore_all", {})
            if self._theme_pushed:
                self.bridge.call("c2ui.reset_qss", {})
            self.bridge.flush()
        self.viewport_hwnd = None

    # ------------------------------------------------------------- slots
    def _on_handshake(self, info: Dict[str, Any]) -> None:
        self.agent_ready.emit(info)
        inside = info.get("inside_sfm", False)
        self.status_message.emit(
            f"SFM agent v{info.get('agent')} (Qt {info.get('qt')}, {'SFM' if inside else 'standalone'})")
        settings = self.app.settings
        if settings.get("sfm.sync_theme", True):
            QTimer.singleShot(50, self.sync_theme)
        if settings.get("sfm.embed_viewport_on_connect", True):
            QTimer.singleShot(200, self.embed_viewport)

    def _on_connected_changed(self, connected: bool) -> None:
        if not connected:
            self._theme_pushed = False
            if self.viewport_hwnd is not None:
                self.viewport_hwnd = None
                self.viewport_released.emit()

    def _on_theme_changed(self, _theme: Any) -> None:
        if self.bridge.connected and self.app.settings.get("sfm.sync_theme", True):
            self.sync_theme()

    # --------------------------------------------------------- startup dialog
    def _babysit_startup(self) -> None:
        """SFM shows a modal "Missing Mods In Search Paths" box on many installs before
        the agent can run.  Click its *Continue* button so the launch does not stall -
        by posting a click to the button, never by moving the user's mouse."""
        if time.time() > self._babysit_until or not self.launcher.is_running():
            self._babysit.stop()
            return
        hwnd = native.find_window("Missing Mods", self.launcher.pid)
        if not hwnd:
            return
        if _click_button_by_text(hwnd, ("Continue", "&Continue")):
            log.info("Dismissed SFM 'Missing Mods' dialog")
            self._babysit.stop()


# --------------------------------------------------------------------------- win32
if hasattr(ctypes, "windll"):
    _user32 = ctypes.windll.user32
    _ENUMCHILD = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
else:                                   # pragma: no cover - non-Windows
    _user32 = None
    _ENUMCHILD = None

BM_CLICK = 0x00F5


def _click_button_by_text(dialog_hwnd: int, captions: Tuple[str, ...]) -> bool:
    """Send BM_CLICK to the child button whose caption matches (no cursor movement)."""
    if _user32 is None:
        return False
    wanted = {c.replace("&", "").strip().lower() for c in captions}
    found: List[int] = []

    @_ENUMCHILD
    def _cb(child, _lparam):
        buf = ctypes.create_unicode_buffer(128)
        _user32.GetWindowTextW(child, buf, 128)
        if buf.value.replace("&", "").strip().lower() in wanted:
            found.append(int(child))
            return False
        return True

    try:
        _user32.EnumChildWindows(wintypes.HWND(dialog_hwnd), _cb, 0)
        if found:
            _user32.SendMessageW(wintypes.HWND(found[0]), BM_CLICK, 0, 0)
            return True
    except OSError:
        log.debug("Could not click dialog button", exc_info=True)
    return False
