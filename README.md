# SFM - C2UI  (Source Film Maker - Custom to User Interface)

A modern, flexible, open UI shell and launcher for **Source Filmmaker**.
The default workspace mimics **Unreal Engine 5**; more workspaces (Windows Fluent,
Adobe After Effects, DaVinci Resolve) are built on the same JSON-driven system.

```
Host   : Python 3.10+  +  PySide6 (Qt 6)          -> this repository (C2UI_SDK)
Bridge : JSON-RPC over localhost TCP
Agent  : Python 2.7 + PySide 1.2 (Qt 4) *inside* sfm.exe  (Core/API/agent, Stage 2)
Native : optional C++ / pybind11 module for Win32 window embedding (Core/API/native)
```

## Quick start

```bat
setup.bat        :: creates .venv and installs PySide6
run.bat          :: starts C2UI  (run.bat --workspace UWP --lang ru --safe-mode ...)
```

**C2UI does not require Source Filmmaker to run.** It starts as a standalone editor
shell; SFM-backed features (launching SFM, the embedded viewport, live panels) stay
disabled until you point it at an installation:

*Preferences -> Source Filmmaker -> SFM folder* (or the banner's **Set SFM path**
button). Pick the folder that contains `game\sfm.exe`; `Detect` scans your Steam
libraries. The path is stored in `sfm.root` and can also be forced with the
`C2UI_SFM_ROOT` environment variable.

`main.py` options: `--workspace <id>` `--theme <id>` `--lang <code>` `--safe-mode` `--no-sfm` `--log-level DEBUG`

## Directory structure

```
C2UI_SDK/
├── Core/
│   ├── API/             C++/Python bindings, IPC and the bridge to the original SFM SDK
│   ├── Library/         core logic: ThemeManager, LayoutManager, ContextManager, WorkspaceManager,
│   │                    panels/ (registry + built-ins), ui/ (main window, docks), plugin loader
│   └── Scripts/         user plugins, macros and custom Python scripts (see Core/Scripts/README.md)
├── Workspaces/
│   ├── UnrealEditor/    default UE5-style layout, contexts, menu, toolbar
│   ├── UWP/             Windows 10/11 modern style (stub)
│   └── AAE/             Adobe After Effects style (stub)
├── Themes/              JSON token files + base.qss template
├── Locales/             i18n (en.json, ru.json, ...)
├── Assets/              icons (monochrome SVG, tinted per theme), fonts
└── main.py              application entry point
```

## The SFM bridge (Stage 2)

C2UI (Python 3 / Qt 6) talks to the original SFM (Python 2.7 / Qt 4.8) over a small
JSON-RPC link, because the two Qt versions cannot share a process:

```
C2UI host  ──TCP 127.0.0.1:41794──►  c2ui_agent.py  (runs inside sfm.exe)
SFMBridge (QTcpSocket)   JSON lines   QtNetwork.QTcpServer, SFM GUI thread
      ▲                                     │  sfm / sfmApp / vs  +  Qt4 widget tree
      └── state_changed events ◄────────────┘
```

* **Agent** (`Core/API/agent/c2ui_agent.py`) exposes `c2ui.*` (windows, detach/embed,
  QSS) and `sfm.*` (exec, state, transport, sessions). Install it once with
  `python Core/API/agent/install_agent.py` (adds a marked, reversible hook to SFM's
  `usermod/scripts/sfm/sfm_init.py`); C2UI also auto-installs it before launching SFM.
* **Bridge** (`Core/API/bridge.py`) + **SFMSession** (`Core/API/session.py`) drive
  launch → connect → **embed the SFM viewport** (its HWND is reparented into the
  Viewport panel via `QWindow.fromWinId`) → **push the C2UI theme into SFM** (`Themes/sfm_native.qss`).
* **Native** (`Core/API/native.py`): Win32 helpers (SetParent, window/process lookup).
  Pure-ctypes `win32.py` is used by default; an optional pybind11 build
  (`Core/API/native/`) is a drop-in speedup — **no compiler is required**.

Everything degrades gracefully when SFM is missing *or* not running: actions are
disabled with a tooltip explaining why, panels show empty states, and nothing throws.
Test the whole flow without SFM: `game\sdktools\python\2.7\win32\python.exe Core\API\agent\c2ui_agent.py --standalone --port 41795`.

## The four managers

| Manager | Input | Responsibility |
|---|---|---|
| **ThemeManager** | `Themes/*.json` + `Themes/base.qss` | tokens -> QSS, QPalette, fonts, tinted icons, hot reload, theme inheritance (`"base"`) |
| **LayoutManager** | `Workspaces/<ws>/layout.json` | builds the QDockWidget tree (split / tabify / sizes), open/close/toggle panels, captures user layouts (`%LOCALAPPDATA%\C2UI\layouts`) |
| **ContextManager** | `Workspaces/<ws>/contexts.json` | action registry, editor modes (contexts), shortcut overrides, context menus, shared selection |
| **WorkspaceManager** | `Workspaces/<ws>/workspace.json` | discovers workspaces and activates them: locale overrides -> theme -> contexts -> menus/toolbars -> layout |

Panels are `C2UIPanel` subclasses registered in the `PanelRegistry` (`Core/Library/panels`).
Built-ins: `viewport`, `outliner`, `details`, `content_browser`, `output_log`, `timeline`, `place_actors`.

## Extending

* **New theme** - copy `Themes/ue5_dark.json`, change `id`/`name`, override tokens (or set `"base": "ue5_dark"` and override only a few).  Themes hot-reload while the app runs.
* **New workspace** - copy `Workspaces/UnrealEditor`, edit `workspace.json` and `layout.json`.
* **New panel / action** - write a plugin in `Core/Scripts/` (see the README there and `example_hello`).
* **New language** - add `Locales/<code>.json` with the same keys as `en.json`.

User data lives outside the SDK tree in `%LOCALAPPDATA%\C2UI` (override with `C2UI_USER_DIR`).
Set `C2UI_SFM_ROOT` if the SDK is not located next to `SourceFilmmaker/game`.

## Roadmap

See [ROADMAP.md](ROADMAP.md).
