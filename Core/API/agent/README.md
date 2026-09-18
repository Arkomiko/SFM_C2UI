# Core/API/agent - code that runs INSIDE sfm.exe (Python 2.7.5 / PySide 1.x / Qt 4.8)

| file | purpose |
|---|---|
| `c2ui_agent.py` | JSON-RPC server on `127.0.0.1:41794` (`QtNetwork.QTcpServer`, GUI thread). Exposes `sfm`, `sfmApp`, `vs`, the Qt4 widget tree and window handles. |
| `install_agent.py` | Writes the auto-start hook into `game/usermod/scripts/sfm/sfm_init.py` (marked block, original backed up as `sfm_init.py.c2ui.bak`) and a manual starter under `mainmenu/C2UI/`. `--uninstall`, `--status`. |

The wire format lives in `../protocol.py` (shared with the Python 3 host).
**Keep everything here Python 2.7 compatible** (no f-strings, no annotations).

## RPC methods

| method | params | result |
|---|---|---|
| `c2ui.hello` | `{client}` | agent/python/qt versions, pid, `inside_sfm`, `main_hwnd` |
| `c2ui.ping` | | `"pong"` |
| `c2ui.api_dir` | | `dir()` of `sfm`, `sfmApp`, `vs` (runtime introspection) |
| `c2ui.windows` | `{top_level?, filter?}` | widget list: class, objectName, title, geometry, hwnd |
| `c2ui.find_widget` | `{name|title|class|hwnd}` | one widget info |
| `c2ui.detach_widget` | `{name, size?, tool?}` | makes the widget a frameless top-level window -> `{hwnd}` (host embeds it) |
| `c2ui.restore_widget` / `c2ui.restore_all` | | put detached widgets back |
| `c2ui.set_widget_visible` | `{name, visible}` | |
| `c2ui.apply_qss` / `c2ui.reset_qss` | `{qss}` | restyle SFM's own Qt widgets (`Themes/sfm_native.qss`) |
| `c2ui.main_window` | | SFM main window info |
| `sfm.exec` / `sfm.eval` | `{code}` / `{expr}` | run Python inside SFM (stdout captured) |
| `sfm.get_state` | | `{has_document, fps, frame, time, timeline_mode, session, shot}` |
| `sfm.transport` | `{cmd: play_pause|stop|to_start|prev_frame|next_frame|to_end}` | |
| `sfm.set_frame` | `{frame}` | |
| `sfm.new_session` `sfm.open_session` `sfm.save_session` `sfm.save_session_as` `sfm.export_movie` `sfm.undo` `sfm.redo` | | thin wrappers over `sfmApp.*` |

Events pushed to every client: `state_changed` `{state, changed}` (polled 4x/s).

## Standalone test (no SFM needed)

    game\sdktools\python\2.7\win32\python.exe Core\API\agent\c2ui_agent.py --standalone --port 41795

opens a fake Qt4 window with a "Primary Viewport" frame; point the host at port 41795
(`sfm.agent_port` in `%LOCALAPPDATA%\C2UI\settings.json`) to exercise embed / QSS / exec.

Disable the hook without uninstalling: set env `C2UI_DISABLE_AGENT=1` before starting SFM.
