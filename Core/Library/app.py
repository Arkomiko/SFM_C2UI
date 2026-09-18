"""
C2UIApplication - composition root.

Creates the QApplication and wires the managers together in a fixed order:

    Settings -> Locale -> Theme -> PanelRegistry -> Context -> Window -> Layout
             -> Workspace -> Bridge/Launcher -> Plugins

Everything else reaches the managers through ``app.<name>``.
"""
from __future__ import annotations

import logging
import sys
from typing import Any, Dict, Optional

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QApplication, QMessageBox

from Core.API.bridge import SFMBridge
from Core.API.launcher import SFMLauncher
from Core.API.session import SFMSession

from . import __version__, paths
from .context_manager import ActionDef, ContextManager
from .events import EventBus
from .layout_manager import LayoutManager
from .localization import get_locale_manager, tr
from .logging_setup import setup_logging
from .panels.registry import get_panel_registry
from .plugin_loader import PluginLoader
from .settings import Settings
from .theme_manager import ThemeManager
from .ui.main_window import C2UIMainWindow
from .workspace_manager import WorkspaceManager

log = logging.getLogger("c2ui.app")


class C2UIApplication:
    def __init__(self, args: Optional[Dict[str, Any]] = None) -> None:
        self.args = args or {}
        paths.ensure_user_dirs()
        self.settings = Settings()
        setup_logging(self.args.get("log_level") or self.settings.get("dev.log_level", "INFO"))
        log.info("SFM - C2UI v%s  (SDK: %s)", __version__, paths.SDK_ROOT)

        QCoreApplication.setOrganizationName("C2UI")
        QCoreApplication.setApplicationName("SFM-C2UI")
        QCoreApplication.setApplicationVersion(__version__)
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        self.qapp = QApplication.instance() or QApplication(sys.argv)
        self.qapp.setStyle("Fusion")             # neutral base style -> QSS behaves predictably
        self._load_fonts()

        self.events = EventBus()
        self.locale = get_locale_manager()
        self.locale.set_language(self.args.get("lang") or self.settings.get("ui.language", "en"))

        self.theme = ThemeManager(self.qapp, hot_reload=bool(self.settings.get("dev.hot_reload_themes", True)))
        self.theme.set_font_scale(float(self.settings.get("ui.font_scale", 1.0)))

        self.panels = get_panel_registry()
        from .panels import builtin  # noqa: F401  (registers built-in panels on import)

        self.context = ContextManager()
        self.window = C2UIMainWindow(self)
        self.context.attach_host(self.window)
        self.layout = LayoutManager(self, self.window, self.panels)
        self.workspace = WorkspaceManager(self)

        self.launcher = SFMLauncher(self.settings.get("sfm.exe") or None)
        self.bridge = SFMBridge(self.events, port=int(self.settings.get("sfm.agent_port", 41794)))
        self.sfm = SFMSession(self, self.launcher, self.bridge)
        self.plugins = PluginLoader(self)

        self._register_core_actions()
        self._connect_signals()

    # ------------------------------------------------------------------ run
    def run(self) -> int:
        self.workspace.discover()
        ws_id = self.args.get("workspace") or self.settings.get("ui.workspace", "UnrealEditor")
        theme_override = self.args.get("theme") or None
        if not self.workspace.activate(ws_id, theme_override=theme_override,
                                       restore_user_layout=not self.args.get("safe_mode")):
            QMessageBox.critical(None, "C2UI", tr("error.no_workspace"))
            return 1

        if not self.args.get("safe_mode"):
            self.plugins.discover()
            self.plugins.load_all()

        self.window.show()
        self.window.retranslate()
        self._update_sfm_availability(self.sfm.available)

        if not self.args.get("no_sfm") and self.sfm.available:
            if self.settings.get("sfm.auto_launch"):
                self.launch_sfm()
            elif self.settings.get("sfm.auto_connect", True):
                self.bridge.connect_to_agent()
        return self.qapp.exec()

    def shutdown(self) -> None:
        log.info("Shutting down")
        self.layout.prepare_shutdown()
        if self.workspace.current and self.settings.get("ui.restore_last_layout", True):
            self.workspace.save_layout("last")
        self.plugins.unload_all()
        self.sfm.shutdown()
        self.bridge.disconnect_from_agent()
        self.settings.flush()

    # ------------------------------------------------------------- switching
    def switch_workspace(self, workspace_id: str) -> None:
        if self.workspace.current and self.workspace.current.id == workspace_id:
            return
        self.workspace.activate(workspace_id)
        self.window.retranslate()

    def switch_theme(self, theme_id: str) -> None:
        if self.theme.apply(theme_id):
            self.settings.set("ui.theme", theme_id)

    def switch_language(self, code: str) -> None:
        if self.locale.set_language(code):
            self.settings.set("ui.language", code)
            self.context.retranslate()
            self.window.retranslate()

    # ------------------------------------------------------------------- sfm
    def launch_sfm(self) -> None:
        if not self.sfm.available:
            self.window.show_message(tr("status.sfm_not_configured"), 8000)
            self.open_preferences("sfm")
            return
        if self.sfm.launch():
            self.window.show_message(tr("status.sfm_launched", pid=self.launcher.pid))
        else:
            self.window.show_message(tr("status.sfm_launch_failed"))

    def install_agent(self) -> None:
        try:
            info = self.sfm.install_agent()
            self.window.show_message(tr("status.agent_installed", path=info["init"]), 8000)
        except (RuntimeError, OSError) as exc:
            log.warning("Agent install failed: %s", exc)
            self.window.show_message(tr("status.agent_install_failed", error=str(exc)), 8000)

    def uninstall_agent(self) -> None:
        try:
            self.sfm.uninstall_agent()
            self.window.show_message(tr("status.agent_uninstalled"))
        except (RuntimeError, OSError) as exc:
            log.warning("Agent uninstall failed: %s", exc)
            self.window.show_message(tr("status.agent_install_failed", error=str(exc)), 8000)

    def dump_sfm_api(self) -> None:
        def _cb(result, error):
            if error:
                log.warning("api_dir failed: %s", error)
                return
            for mod, names in (result or {}).items():
                log.info("%s: %s", mod, ", ".join(names) if names else "(not available)")
            self.layout.open_panel("output_log")
        self.sfm_call("c2ui.api_dir", {}, _cb)

    def sfm_call(self, method: str, params: Optional[Dict[str, Any]] = None, callback=None) -> None:
        """Fire-and-forget call that degrades gracefully when SFM is absent/offline."""
        if not self.bridge.connected:
            self.window.show_message(
                tr("status.sfm_offline_action") if self.sfm.available else tr("status.sfm_not_configured"))
            return
        self.bridge.call(method, params, callback)

    # ------------------------------------------------------------- internals
    def _load_fonts(self) -> None:
        from PySide6.QtGui import QFontDatabase
        n = 0
        if paths.FONTS_DIR.is_dir():
            for f in list(paths.FONTS_DIR.glob("*.ttf")) + list(paths.FONTS_DIR.glob("*.otf")):
                if QFontDatabase.addApplicationFont(str(f)) >= 0:
                    n += 1
        if n:
            log.info("Loaded %d bundled font file(s)", n)

    def _connect_signals(self) -> None:
        self.theme.theme_changed.connect(self._on_theme_changed)
        self.context.context_changed.connect(self._on_context_changed)
        self.bridge.connected_changed.connect(self._on_bridge_changed)
        self.sfm.status_message.connect(lambda text: self.window.show_message(text, 6000))
        self.sfm.agent_ready.connect(self._on_agent_ready)
        self.sfm.availability_changed.connect(self._update_sfm_availability)
        self.window.banner.dismissed.connect(lambda: self.settings.set("ui.show_sfm_banner", False))
        self.workspace.workspace_changed.connect(lambda ws: self.window.set_workspace_status(ws.display_name()))
        self.events.subscribe("sfm.state_changed", self._on_sfm_state)

    def _on_theme_changed(self, theme: Any) -> None:
        for panel in self.layout.panels().values():
            panel.on_theme_changed(theme)
        for dock in self.layout.docks().values():
            dock.retranslate()
        self.context.refresh_icons()        # cheap: re-render icons, keep the widgets
        self.window.retheme()
        self.events.publish_sync("ui.theme_changed", theme.id)

    def _on_context_changed(self, context_id: str) -> None:
        preset = self.context.preset(context_id)
        if preset:
            self.window.set_context_status(preset.name())
            for pid in preset.hide_panels:
                self.layout.close_panel(pid)
            for pid in preset.show_panels:
                self.layout.open_panel(pid, raise_=False)
        for panel in self.layout.panels().values():
            panel.on_context_changed(context_id)
        self.events.publish_sync("ui.context_changed", context_id)

    def _on_sfm_state(self, payload: Dict[str, Any]) -> None:
        state = (payload or {}).get("state", payload) or {}
        frame = state.get("frame")
        doc = state.get("session")
        parts = []
        if doc:
            parts.append(str(doc))
        if frame is not None:
            parts.append(tr("status.frame", frame=frame))
        if state.get("playing"):
            parts.append(tr("status.playing"))
        if parts:
            self.window.set_context_status("  ".join(parts))

    SFM_ACTIONS = ("sfm.launch", "sfm.connect", "sfm.install_agent", "sfm.uninstall_agent")

    def _update_sfm_availability(self, available: bool) -> None:
        """SFM is optional: enable/disable everything that needs it and explain why."""
        hint = self.sfm.requirement_hint()
        for aid in self.SFM_ACTIONS:
            act = self.context.action(aid)
            if act is None:
                continue
            act.setEnabled(available if aid != "sfm.connect" else (available and not self.bridge.connected))
            act.setToolTip(hint if not available else "")
        self.window.set_sfm_status(self.bridge.connected, "" if available else tr("status.sfm_not_configured"))
        if available:
            self.window.banner.hide_message()
        elif self.settings.get("ui.show_sfm_banner", True):
            self.window.banner.show_message(
                tr("banner.sfm_missing"), kind="warning", icon="info",
                action_text=tr("banner.sfm_action"), action=lambda: self.open_preferences("sfm"),
            )
        self.events.publish_sync("sfm.availability_changed", available)

    def open_preferences(self, page: str = "sfm") -> None:
        from .ui.preferences import PreferencesDialog
        dlg = PreferencesDialog(self, self.window, page)
        dlg.exec()

    def _on_agent_ready(self, info: Dict[str, Any]) -> None:
        inside = info.get("inside_sfm", False)
        self.window.set_sfm_status(True, f"agent v{info.get('agent', '?')}" + ("" if inside else " [standalone]"))

    def _on_bridge_changed(self, connected: bool) -> None:
        self.window.set_sfm_status(connected, f":{self.bridge.port}" if connected else "")
        for panel in self.layout.panels().values():
            panel.on_sfm_connected(connected)
        for aid in ("transport.play_pause", "transport.stop", "transport.prev_frame", "transport.next_frame",
                    "transport.to_start", "transport.to_end", "sfm.disconnect", "sfm.embed_viewport",
                    "sfm.release_viewport", "sfm.sync_theme", "sfm.api_dir"):
            self.context.set_enabled(aid, connected)
        self.context.set_enabled("sfm.connect", not connected)

    def _register_core_actions(self) -> None:
        A = ActionDef
        w = self.window
        acts = [
            A("file.new", "action.file.new", "file_new", "Ctrl+N", callback=lambda: self.sfm_call("sfm.new_session")),
            A("file.open", "action.file.open", "folder_open", "Ctrl+O", callback=lambda: self.sfm_call("sfm.open_session")),
            A("file.save", "action.file.save", "save", "Ctrl+S", callback=lambda: self.sfm_call("sfm.save_session")),
            A("file.save_as", "action.file.save_as", "save_as", "Ctrl+Shift+S", callback=lambda: self.sfm_call("sfm.save_session_as")),
            A("file.export_movie", "action.file.export_movie", "render", "Ctrl+M", callback=lambda: self.sfm_call("sfm.export_movie")),
            A("app.exit", "action.app.exit", "close", "Alt+F4", callback=w.close),

            A("edit.undo", "action.edit.undo", "undo", "Ctrl+Z", callback=lambda: self.sfm_call("sfm.undo")),
            A("edit.redo", "action.edit.redo", "redo", "Ctrl+Y", callback=lambda: self.sfm_call("sfm.redo")),
            A("edit.preferences", "action.edit.preferences", "settings", "Ctrl+,", callback=self._show_preferences),

            A("window.save_layout", "action.window.save_layout", "save", "", callback=w.save_layout_as),
            A("window.reset_layout", "action.window.reset_layout", "reset", "", callback=self.workspace.reset_layout),
            A("window.fullscreen", "action.window.fullscreen", "fullscreen", "F11", checkable=True, callback=self._toggle_fullscreen),
            A("window.output_log", "action.window.output_log", "log", "Ctrl+`", callback=lambda: self.layout.toggle_panel("output_log")),

            A("sfm.launch", "action.sfm.launch", "launch", "", callback=self.launch_sfm),
            A("sfm.connect", "action.sfm.connect", "link", "", callback=self.bridge.connect_to_agent),
            A("sfm.disconnect", "action.sfm.disconnect", "unlink", "", enabled=False, callback=self.bridge.disconnect_from_agent),
            A("sfm.install_agent", "action.sfm.install_agent", "import", "", category="SFM", callback=self.install_agent),
            A("sfm.uninstall_agent", "action.sfm.uninstall_agent", "delete", "", category="SFM", callback=self.uninstall_agent),
            A("sfm.embed_viewport", "action.sfm.embed_viewport", "viewport", "", enabled=False, category="SFM", callback=self.sfm.embed_viewport),
            A("sfm.release_viewport", "action.sfm.release_viewport", "dock_float", "", enabled=False, category="SFM", callback=self.sfm.release_viewport),
            A("sfm.sync_theme", "action.sfm.sync_theme", "theme", "", checkable=True, enabled=False, category="SFM",
              checked=bool(self.settings.get("sfm.sync_theme", True)), callback=self.sfm.sync_theme),
            A("sfm.api_dir", "action.sfm.api_dir", "log", "", enabled=False, category="SFM", callback=self.dump_sfm_api),

            A("transport.to_start", "action.transport.to_start", "skip_start", "Home", enabled=False, callback=lambda: self.sfm_call("sfm.transport", {"cmd": "to_start"})),
            A("transport.prev_frame", "action.transport.prev_frame", "step_back", "Left", enabled=False, callback=lambda: self.sfm_call("sfm.transport", {"cmd": "prev_frame"})),
            A("transport.play_pause", "action.transport.play_pause", "play", "Space", enabled=False, callback=lambda: self.sfm_call("sfm.transport", {"cmd": "play_pause"})),
            A("transport.stop", "action.transport.stop", "stop", "Escape", enabled=False, callback=lambda: self.sfm_call("sfm.transport", {"cmd": "stop"})),
            A("transport.next_frame", "action.transport.next_frame", "step_forward", "Right", enabled=False, callback=lambda: self.sfm_call("sfm.transport", {"cmd": "next_frame"})),
            A("transport.to_end", "action.transport.to_end", "skip_end", "End", enabled=False, callback=lambda: self.sfm_call("sfm.transport", {"cmd": "to_end"})),

            A("help.about", "action.help.about", "info", "", callback=self._show_about),
            A("help.docs", "action.help.docs", "help", "F1", callback=self._open_docs),

            # selection / context-menu actions (bound to real SFM operations in Stage 3)
            A("sel.rename", "action.sel.rename", "rename", "F2", category="Selection", callback=lambda: self.sfm_call("sfm.rename_selected")),
            A("sel.duplicate", "action.sel.duplicate", "duplicate", "Ctrl+D", category="Selection", callback=lambda: self.sfm_call("sfm.duplicate_selected")),
            A("sel.delete", "action.sel.delete", "delete", "Delete", category="Selection", callback=lambda: self.sfm_call("sfm.delete_selected")),
            A("sel.properties", "action.sel.properties", "details", "", category="Selection", callback=lambda: self.layout.open_panel("details")),
            A("content.open", "action.content.open", "folder_open", "", category="Content", callback=self._content_open),
            A("content.reveal", "action.content.reveal", "folder", "", category="Content", callback=self._content_reveal),
            A("content.import", "action.content.import", "import", "", category="Content", callback=lambda: self.sfm_call("sfm.import_asset")),
            A("clip.split", "action.clip.split", "split", "Ctrl+K", category="Timeline", callback=lambda: self.sfm_call("sfm.split_clip")),
            A("clip.delete", "action.clip.delete", "delete", "", category="Timeline", callback=lambda: self.sfm_call("sfm.delete_clip")),
        ]
        self.context.register_actions(acts)

    # ---------------------------------------------------------- simple slots
    def _toggle_fullscreen(self, checked: bool) -> None:
        if checked:
            self.window.showFullScreen()
        else:
            self.window.showNormal()
            self.window.showMaximized()

    def _show_preferences(self) -> None:
        self.open_preferences("appearance")

    def _show_about(self) -> None:
        QMessageBox.about(
            self.window, "SFM - C2UI",
            f"<b>SFM - C2UI</b> v{__version__}<br>{tr('about.tagline')}<br><br>"
            f"SDK: {paths.SDK_ROOT}<br>SFM: {paths.sfm_root() or tr('status.sfm_not_configured')}<br>"
            f"PySide6: {__import__('PySide6').__version__}  Python: {sys.version.split()[0]}",
        )

    def _open_docs(self) -> None:
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(paths.SDK_ROOT / "README.md")))

    def _selected_paths(self) -> list:
        return [s["path"] for s in self.context.selection if isinstance(s, dict) and s.get("path")]

    def _content_open(self) -> None:
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices
        for p in self._selected_paths():
            QDesktopServices.openUrl(QUrl.fromLocalFile(p))

    def _content_reveal(self) -> None:
        import subprocess
        for p in self._selected_paths()[:1]:
            subprocess.Popen(["explorer", "/select,", p.replace("/", "\\")])
