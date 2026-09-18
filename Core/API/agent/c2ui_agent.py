# -*- coding: utf-8 -*-
"""
C2UI agent - runs INSIDE sfm.exe (Python 2.7.5, PySide 1.x / Qt 4.8).

Started from game/usermod/scripts/sfm/sfm_init.py (see install_agent.py) or from
the SFM Scripts menu.  Opens a JSON-RPC server on 127.0.0.1:<port> using
QtNetwork.QTcpServer so every handler runs on SFM's GUI thread, where the
`sfm` / `sfmApp` / `vs` modules and the Qt4 widgets may be touched safely.

    from the host:   {"id": 1, "method": "c2ui.windows", "params": {}}

Standalone test mode (no SFM):  python.exe c2ui_agent.py --standalone
creates a dummy QApplication with a fake "Primary Viewport" widget so the
detach / embed / QSS flow can be exercised without launching SFM.

KEEP THIS FILE PYTHON 2.7 COMPATIBLE.
"""
from __future__ import print_function

import json
import os
import sys
import time
import traceback

AGENT_VERSION = "0.2.1"
DEFAULT_PORT = 41794

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
_API_DIR = os.path.dirname(_HERE)
if _API_DIR not in sys.path:
    sys.path.insert(0, _API_DIR)

import protocol  # noqa: E402  (shared 2/3 wire format)

try:
    from PySide import QtCore, QtGui, QtNetwork
except ImportError:  # pragma: no cover - only outside SFM / without PySide
    QtCore = QtGui = QtNetwork = None

# SFM modules exist only inside sfm.exe
try:
    import sfm          # noqa: F401
    import sfmApp       # noqa: F401
    import vs           # noqa: F401
    INSIDE_SFM = True
except ImportError:
    sfm = sfmApp = vs = None
    INSIDE_SFM = False


def _log(msg):
    print("[C2UI agent] " + msg)


def _to_int(value):
    """winId() may come back as int/long, a PyCObject/PyCapsule (PySide 1.x) or a string."""
    try:
        return int(value)
    except (TypeError, ValueError):
        pass
    tname = type(value).__name__
    try:
        import ctypes
        if tname == "PyCObject":
            fn = ctypes.pythonapi.PyCObject_AsVoidPtr
            fn.restype = ctypes.c_void_p
            fn.argtypes = [ctypes.py_object]
            return int(fn(value) or 0)
        if tname == "PyCapsule":
            fn = ctypes.pythonapi.PyCapsule_GetPointer
            fn.restype = ctypes.c_void_p
            fn.argtypes = [ctypes.py_object, ctypes.c_char_p]
            return int(fn(value, None) or 0)
    except Exception:  # noqa: BLE001
        pass
    try:
        return int(str(value), 0)
    except (TypeError, ValueError):
        return 0


def _prop(w, name, default=None):
    """Read a Qt property / call a getter safely on QWidget *or* plain-QObject wrappers."""
    try:
        if hasattr(w, name):
            v = getattr(w, name)
            return v() if callable(v) else v
        v = w.property(name)
        return default if v is None else v
    except Exception:  # noqa: BLE001
        return default


def _widget_info(w, with_hwnd=True):
    try:
        geo = _prop(w, "frameGeometry", None) or _prop(w, "geometry", None)
        is_window = bool(_prop(w, "isWindow", False))
        native = is_window
        try:
            native = native or bool(w.testAttribute(QtCore.Qt.WA_NativeWindow))
        except Exception:  # noqa: BLE001
            pass
        info = {
            "class": w.metaObject().className(),
            "wrapper": type(w).__name__,
            "objectName": unicode(w.property("objectName") or u""),  # noqa: F821
            "title": unicode(w.property("windowTitle") or u""),      # noqa: F821
            "visible": bool(_prop(w, "isVisible", _prop(w, "visible", False))),
            "topLevel": is_window,
            "geometry": [geo.x(), geo.y(), geo.width(), geo.height()] if geo is not None else None,
            "native": native,
        }
        if with_hwnd and native and hasattr(w, "winId"):
            info["hwnd"] = _to_int(w.winId())
        return info
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc), "class": getattr(getattr(w, "metaObject", lambda: None)(), "className", lambda: "?")()}


class RpcError(Exception):
    def __init__(self, code, message, data=None):
        Exception.__init__(self, message)
        self.code = code
        self.data = data


# =============================================================================
class C2UIAgent(QtCore.QObject if QtCore else object):
    """JSON-RPC server + method table."""

    def __init__(self, port=DEFAULT_PORT, parent=None):
        if QtCore:
            QtCore.QObject.__init__(self, parent)
        self.port = port
        self.server = None
        self.clients = {}            # socket -> buffer
        self.started = time.time()
        self.exec_namespace = {"sfm": sfm, "sfmApp": sfmApp, "vs": vs, "agent": self, "QtGui": QtGui, "QtCore": QtCore}
        self._detached = {}          # id(widget) -> (widget, parent, flags, geometry)
        self._orig_qss = None
        self._last_state = {}
        self._poll = None
        self.methods = {
            "c2ui.hello": self.m_hello,
            "c2ui.ping": lambda p: "pong",
            "c2ui.api_dir": self.m_api_dir,
            "c2ui.windows": self.m_windows,
            "c2ui.find_widget": self.m_find_widget,
            "c2ui.detach_widget": self.m_detach_widget,
            "c2ui.restore_widget": self.m_restore_widget,
            "c2ui.restore_all": self.m_restore_all,
            "c2ui.set_widget_visible": self.m_set_widget_visible,
            "c2ui.apply_qss": self.m_apply_qss,
            "c2ui.reset_qss": self.m_reset_qss,
            "c2ui.main_window": self.m_main_window,
            "c2ui.actions": self.m_actions,
            "c2ui.trigger_action": self.m_trigger_action,
            "c2ui.dismiss_modal": self.m_dismiss_modal,
            "c2ui.show_tab_window": lambda p: self._call_app("ShowTabWindow", p.get("name", "Primary Viewport")),
            "c2ui.shutdown": self.m_shutdown,
            "sfm.exec": self.m_exec,
            "sfm.eval": self.m_eval,
            "sfm.get_state": self.m_get_state,
            "sfm.transport": self.m_transport,
            "sfm.set_frame": self.m_set_frame,
            "sfm.new_session": lambda p: self._trigger(["New"]) if not p.get("path") else self._call_app("NewDocument", p["path"]),
            "sfm.open_session": lambda p: self._call_app("OpenDocument", p["path"]) if p.get("path") else self._trigger(["Open..."]),
            "sfm.save_session": lambda p: self._call_app("SaveDocument") if sfmApp else self._trigger(["Save"]),
            "sfm.save_session_as": lambda p: self._trigger(["Save As..."]),
            "sfm.export_movie": lambda p: self._trigger(["Movie...", "Export Movie..."]),
            "sfm.undo": lambda p: self._trigger(["Undo"]),
            "sfm.redo": lambda p: self._trigger(["Redo"]),
            "sfm.close_session": lambda p: self._call_app("CloseDocument"),
            "sfm.game_command": lambda p: self._call_app("ExecuteGameCommand", p.get("cmd", "")),
        }
        self._play_hint = {"frame": None, "t": 0.0, "playing": False, "our_set": 0.0}

    # ------------------------------------------------------------ server
    def start(self):
        if QtNetwork is None:
            _log("PySide not available - agent cannot start")
            return False
        self.server = QtNetwork.QTcpServer(self)
        self.server.newConnection.connect(self._on_new_connection)
        if not self.server.listen(QtNetwork.QHostAddress(QtNetwork.QHostAddress.LocalHost), self.port):
            _log("listen failed on port %d: %s" % (self.port, self.server.errorString()))
            return False
        _log("listening on 127.0.0.1:%d (inside SFM: %s)" % (self.port, INSIDE_SFM))
        self._write_discovery_file()
        self._poll = QtCore.QTimer(self)
        self._poll.setInterval(250)
        self._poll.timeout.connect(self._poll_state)
        self._poll.start()
        return True

    def stop(self):
        if self._poll:
            self._poll.stop()
        for sock in list(self.clients.keys()):
            sock.disconnectFromHost()
        if self.server:
            self.server.close()
        self.m_restore_all({})
        self.m_reset_qss({})
        _log("stopped")

    def _write_discovery_file(self):
        try:
            base = os.environ.get("C2UI_USER_DIR") or os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "C2UI")
            if not os.path.isdir(base):
                os.makedirs(base)
            with open(os.path.join(base, "agent.json"), "w") as fh:
                json.dump({"port": self.port, "pid": os.getpid(), "inside_sfm": INSIDE_SFM, "started": self.started}, fh)
        except Exception:  # noqa: BLE001
            traceback.print_exc()

    def _on_new_connection(self):
        while self.server.hasPendingConnections():
            sock = self.server.nextPendingConnection()
            self.clients[sock] = b""
            sock.readyRead.connect(lambda s=sock: self._on_ready_read(s))
            sock.disconnected.connect(lambda s=sock: self._on_disconnected(s))
            _log("client connected (%d total)" % len(self.clients))
        if self._poll is not None and not self._poll.isActive():
            self._last_state = {}
            self._poll.start()

    def _on_disconnected(self, sock):
        self.clients.pop(sock, None)
        sock.deleteLater()
        _log("client disconnected (%d left)" % len(self.clients))

    def _on_ready_read(self, sock):
        data = bytes(sock.readAll())
        buf = self.clients.get(sock, b"") + data
        while b"\n" in buf:
            line, buf = buf.split(b"\n", 1)
            if line.strip():
                self._handle_line(sock, line)
        self.clients[sock] = buf

    def _handle_line(self, sock, line):
        try:
            msg = protocol.decode(line)
        except ValueError:
            self._send(sock, protocol.make_error(None, protocol.ERR_PARSE, "bad json"))
            return
        req_id = msg.get("id")
        method = msg.get("method")
        params = msg.get("params") or {}
        fn = self.methods.get(method)
        if fn is None:
            self._send(sock, protocol.make_error(req_id, protocol.ERR_METHOD_NOT_FOUND, "unknown method: %s" % method))
            return
        try:
            result = fn(params)
            self._send(sock, protocol.make_result(req_id, result))
        except RpcError as exc:
            self._send(sock, protocol.make_error(req_id, exc.code, str(exc), exc.data))
        except Exception as exc:  # noqa: BLE001
            self._send(sock, protocol.make_error(req_id, protocol.ERR_INTERNAL, "%s: %s" % (exc.__class__.__name__, exc),
                                                 traceback.format_exc()))

    def _send(self, sock, obj):
        try:
            sock.write(protocol.encode(obj))
        except Exception:  # noqa: BLE001
            traceback.print_exc()

    def broadcast(self, event, data=None):
        payload = protocol.encode(protocol.make_event(event, data))
        for sock in list(self.clients.keys()):
            try:
                sock.write(payload)
            except Exception:  # noqa: BLE001
                pass

    # ------------------------------------------------------------ helpers
    def _app(self):
        return QtGui.QApplication.instance()

    def _all_widgets(self):
        return list(self._app().allWidgets()) if self._app() else []

    def _find(self, params):
        """Locate a widget.  Priority: hwnd -> exact objectName -> exact windowTitle ->
        class name -> substring match (case-insensitive).  Optional "class" narrows."""
        hwnd = params.get("hwnd")
        name = params.get("name") or params.get("title") or ""
        name_l = name.lower()
        cls = (params.get("class") or "").lower()
        top_only = bool(params.get("top_level", False))
        exact, by_class, fuzzy = None, None, None
        for w in self._all_widgets():
            try:
                if top_only and not _prop(w, "isWindow", False):
                    continue
                wcls = w.metaObject().className()
                if cls and cls not in wcls.lower():
                    continue
                if hwnd:
                    if hasattr(w, "winId") and (_prop(w, "isWindow", False) or w.testAttribute(QtCore.Qt.WA_NativeWindow))                             and _to_int(w.winId()) == hwnd:
                        return w
                    continue
                oname = unicode(w.property("objectName") or u"")   # noqa: F821
                title = unicode(w.property("windowTitle") or u"")  # noqa: F821
                if name and (oname == name or title == name):
                    if exact is None or (hasattr(w, "winId") and not hasattr(exact, "winId")):
                        exact = w
                elif name and name_l == wcls.lower():
                    by_class = by_class or w
                elif name and (name_l in oname.lower() or name_l in title.lower()):
                    fuzzy = fuzzy or w
                elif not name and cls:
                    by_class = by_class or w
            except Exception:  # noqa: BLE001
                continue
        return exact or by_class or fuzzy

    def _call_app(self, name, *args):
        if sfmApp is None:
            raise RpcError(protocol.ERR_SFM, "not inside SFM (standalone agent)")
        fn = getattr(sfmApp, name, None)
        if fn is None:
            raise RpcError(protocol.ERR_METHOD_NOT_FOUND, "sfmApp.%s not available" % name)
        return _jsonable(fn(*args))

    def _try_app(self, names, *args):
        """Call the first sfmApp.<name> that exists; None when none does."""
        if sfmApp is None:
            return None
        for n in names:
            fn = getattr(sfmApp, n, None)
            if fn is not None:
                try:
                    return fn(*args)
                except Exception:  # noqa: BLE001
                    continue
        return None

    # ------------------------------------------------------------ actions
    def _action_index(self):
        """text (without &) -> QAction and objectName -> QAction, across the whole app.
        SFM attaches most commands to CQTabbedToolButtons / menus rather than the main window."""
        by_text, by_name = {}, {}

        def add(a):
            try:
                t = unicode(a.text()).replace("&", "").strip()  # noqa: F821
                n = unicode(a.objectName())                      # noqa: F821
            except Exception:  # noqa: BLE001
                return
            if t and t not in by_text:
                by_text[t] = a
            if n and n != "QFunctorAction" and n not in by_name:
                by_name[n] = a

        mw = None
        if sfmApp is not None:
            try:
                mw = sfmApp.GetMainWindow()
            except Exception:  # noqa: BLE001
                mw = None
        if mw is not None:
            for a in mw.findChildren(QtGui.QAction):
                add(a)
        for w in self._all_widgets():
            try:
                for a in w.actions():
                    add(a)
            except Exception:  # noqa: BLE001
                continue
        return by_text, by_name

    def _trigger(self, texts):
        by_text, by_name = self._action_index()
        for t in texts:
            a = by_text.get(t) or by_name.get(t)
            if a is not None:
                a.trigger()
                return t
        raise RpcError(protocol.ERR_METHOD_NOT_FOUND, "no SFM action named %s" % " / ".join(texts))

    def m_actions(self, p):
        flt = (p.get("filter") or "").lower()
        by_text, by_name = self._action_index()
        out = []
        for t, a in sorted(by_text.items()):
            if flt and flt not in t.lower():
                continue
            try:
                out.append({"text": t, "shortcut": unicode(a.shortcut().toString()), "objectName": unicode(a.objectName()),  # noqa: F821
                            "checkable": bool(a.isCheckable()), "checked": bool(a.isChecked()), "enabled": bool(a.isEnabled())})
            except Exception:  # noqa: BLE001
                continue
        return out

    def m_trigger_action(self, p):
        names = [p[k] for k in ("text", "name") if p.get(k)]
        if not names:
            raise RpcError(protocol.ERR_INVALID_PARAMS, "text or name required")
        return self._trigger(names)

    def m_dismiss_modal(self, p):
        app = self._app()
        m = app.activeModalWidget() if app else None
        if m is None:
            return None
        info = _widget_info(m, with_hwnd=False)
        try:
            if p.get("accept") and hasattr(m, "accept"):
                m.accept()
            elif hasattr(m, "reject"):
                m.reject()
            else:
                m.close()
        except Exception:  # noqa: BLE001
            traceback.print_exc()
        return info

    # ------------------------------------------------------------ methods
    def m_hello(self, p):
        return {
            "agent": AGENT_VERSION,
            "protocol": protocol.PROTOCOL_VERSION,
            "pid": os.getpid(),
            "python": sys.version.split()[0],
            "qt": QtCore.qVersion(),
            "inside_sfm": INSIDE_SFM,
            "uptime": time.time() - self.started,
            "client": p.get("client"),
            "main_hwnd": self.m_main_window({}).get("hwnd"),
        }

    def m_api_dir(self, p):
        mods = {"sfm": sfm, "sfmApp": sfmApp, "vs": vs}
        out = {}
        for name, mod in mods.items():
            out[name] = sorted(n for n in dir(mod) if not n.startswith("_")) if mod is not None else None
        return out

    def m_windows(self, p):
        top_only = bool(p.get("top_level", False))
        flt = (p.get("filter") or "").lower()
        result = []
        for w in self._all_widgets():
            try:
                info = _widget_info(w, with_hwnd=True)
                if "error" in info:
                    continue
                if top_only and not info["topLevel"]:
                    continue
                hay = (info["objectName"] + " " + info["title"] + " " + info["class"]).lower()
                if flt and flt not in hay:
                    continue
                if not top_only and not flt and not info["topLevel"] and not info["title"] and not info["objectName"]:
                    continue      # skip anonymous children unless asked for
                result.append(info)
            except Exception:  # noqa: BLE001
                continue
        return result

    def m_main_window(self, p):
        w = None
        if sfmApp is not None:
            w = self._try_app(["GetMainWindow"])
        if w is None:
            for tl in self._app().topLevelWidgets():
                if isinstance(tl, QtGui.QMainWindow):
                    w = tl
                    break
        if w is None:
            return {}
        try:
            if not w.testAttribute(QtCore.Qt.WA_NativeWindow) and not w.isWindow():
                return _widget_info(w, with_hwnd=False)
        except Exception:  # noqa: BLE001
            pass
        return _widget_info(w)

    def m_find_widget(self, p):
        w = self._find(p)
        return _widget_info(w) if w is not None else None

    def m_detach_widget(self, p):
        """Make a child widget a frameless top-level window so it gets its own HWND
        the host can embed.  Returns the hwnd."""
        w = self._find(p)
        if w is None:
            raise RpcError(protocol.ERR_INVALID_PARAMS, "widget not found: %r" % p)
        if not hasattr(w, "setWindowFlags"):
            raise RpcError(protocol.ERR_SFM, "widget %s is wrapped as %s - cannot detach" % (w.metaObject().className(), type(w).__name__))
        key = id(w)
        if key not in self._detached:
            self._detached[key] = (w, w.parentWidget(), int(w.windowFlags()), w.geometry())
            w.setParent(None)
            flags = QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint
            if p.get("tool", True):
                flags |= QtCore.Qt.Tool
            w.setWindowFlags(QtCore.Qt.WindowFlags(flags))
            w.setAttribute(QtCore.Qt.WA_NativeWindow, True)
            size = p.get("size") or [max(64, w.width()), max(64, w.height())]
            w.resize(int(size[0]), int(size[1]))
            w.move(-32000, -32000) if p.get("offscreen", False) else None
            w.show()
        hwnd = _to_int(w.winId())
        _log("detached %s hwnd=%d" % (w.metaObject().className(), hwnd))
        return {"hwnd": hwnd, "info": _widget_info(w)}

    def m_restore_widget(self, p):
        w = self._find(p)
        if w is None:
            raise RpcError(protocol.ERR_INVALID_PARAMS, "widget not found: %r" % p)
        return self._restore(id(w))

    def _restore(self, key):
        entry = self._detached.pop(key, None)
        if entry is None:
            return False
        w, parent, flags, geo = entry
        try:
            w.setWindowFlags(QtCore.Qt.WindowFlags(flags))
            w.setParent(parent)
            w.setGeometry(geo)
            w.show()
            if parent is not None and parent.layout() is not None:
                parent.layout().addWidget(w)
        except Exception:  # noqa: BLE001
            traceback.print_exc()
            return False
        return True

    def m_restore_all(self, p):
        n = 0
        for key in list(self._detached.keys()):
            if self._restore(key):
                n += 1
        return n

    def m_set_widget_visible(self, p):
        w = self._find(p)
        if w is None:
            raise RpcError(protocol.ERR_INVALID_PARAMS, "widget not found: %r" % p)
        w.setVisible(bool(p.get("visible", True)))
        return True

    def m_apply_qss(self, p):
        app = self._app()
        if self._orig_qss is None:
            self._orig_qss = unicode(app.styleSheet())  # noqa: F821
        app.setStyleSheet(p.get("qss") or "")
        return {"length": len(p.get("qss") or "")}

    def m_reset_qss(self, p):
        app = self._app()
        if app is not None and self._orig_qss is not None:
            app.setStyleSheet(self._orig_qss)
            self._orig_qss = None
        return True

    def m_shutdown(self, p):
        QtCore.QTimer.singleShot(0, self.stop)
        return True

    def m_exec(self, p):
        code = p.get("code") or ""
        out = _capture_stdout()
        try:
            try:
                result = eval(compile(code, "<c2ui>", "eval"), self.exec_namespace)
            except SyntaxError:
                exec(compile(code, "<c2ui>", "exec"), self.exec_namespace)
                result = None
        finally:
            printed = out.stop()
        text = printed
        if result is not None:
            text = (text + "\n" if text else "") + repr(result)
        return text

    def m_eval(self, p):
        return _jsonable(eval(p.get("expr") or "None", self.exec_namespace))

    def m_get_state(self, p):
        return self._state()

    def _state(self):
        st = {"inside_sfm": INSIDE_SFM, "has_document": False}
        if sfmApp is None:
            st["frame"] = int(self.exec_namespace.get("_fake_frame", 0))
            st["fps"] = 24
            return st
        try:
            st["has_document"] = bool(self._try_app(["HasDocument"]))
            st["fps"] = self._try_app(["GetFramesPerSecond"])
            st["frame"] = self._try_app(["GetHeadTimeInFrames", "GetCurrentFrame"])
            st["time"] = self._try_app(["GetHeadTimeInSeconds"])
            mode = self._try_app(["GetTimelineMode"])
            st["timeline_mode"] = int(mode) if mode is not None else None
            root = self._try_app(["GetDocumentRoot"])
            if root is not None:
                st["session"] = _safe_name(root)
            shot = self._try_app(["GetShotAtCurrentTime"])
            if shot is not None:
                st["shot"] = _safe_name(shot)
            # "playing" is meaningless without a loaded session
            st["playing"] = self._update_play_hint(st.get("frame")) if st["has_document"] else False
        except Exception as exc:  # noqa: BLE001
            st["error"] = str(exc)
        return st

    def _update_play_hint(self, frame):
        """SFM exposes no 'is playing' query: infer it from the head moving on its own
        (needs the 250 ms poll, i.e. a connected client)."""
        h = self._play_hint
        now = time.time()
        if h["frame"] is None:
            h["frame"], h["t"] = frame, now
        elif frame != h["frame"]:
            if now - h["our_set"] > 0.6:
                h["playing"] = True
            h["frame"], h["t"] = frame, now
        elif now - h["t"] > 0.5:
            h["playing"] = False
        return h["playing"]

    def _poll_state(self):
        """Timer callback: push a state_changed event to clients when the state changes."""
        if not self.clients:
            return
        try:
            st = self._state()
        except Exception:  # noqa: BLE001
            return
        if st != self._last_state:
            changed = dict((k, v) for k, v in st.items() if self._last_state.get(k) != v)
            self._last_state = st
            self.broadcast("state_changed", {"state": st, "changed": changed})

    def m_transport(self, p):
        cmd = p.get("cmd")
        if cmd == "play_pause":
            self._play_hint["playing"] = not self._play_hint["playing"]
            self._play_hint["our_set"] = time.time()
            return self._trigger(["Toggle Play"])
        if cmd == "stop":
            if self._play_hint["playing"]:
                self._play_hint["playing"] = False
                self._play_hint["our_set"] = time.time()
                return self._trigger(["Toggle Play"])
            return "already stopped"
        mapping = {
            "to_start": ["Jump To Sequence Top"],
            "prev_frame": ["Jump to Previous Frame"],
            "next_frame": ["Jump to Next Frame"],
            "to_end": ["Jump To Sequence Bottom"],
            "prev_clip": ["Jump to Clip Top"],
            "next_clip": ["Jump to Next Clip Top"],
            "record": ["Record Game"],
        }
        if cmd in mapping:
            self._play_hint["our_set"] = time.time()      # a jump is not "playing"
            return self._trigger(mapping[cmd])
        raise RpcError(protocol.ERR_INVALID_PARAMS, "unknown transport cmd %r" % cmd)

    def m_set_frame(self, p):
        frame = int(p.get("frame", 0))
        if sfmApp is None:
            self.exec_namespace["_fake_frame"] = frame
            return frame
        self._play_hint["our_set"] = time.time()
        for n in ("SetHeadTimeInFrames", "SetCurrentFrame"):
            fn = getattr(sfmApp, n, None)
            if fn is not None:
                fn(frame)
                return frame
        raise RpcError(protocol.ERR_METHOD_NOT_FOUND, "no frame setter on sfmApp")


# =============================================================================
def _safe_name(obj):
    for attr in ("name", "GetName"):
        try:
            v = getattr(obj, attr)
            return unicode(v() if callable(v) else v)  # noqa: F821
        except Exception:  # noqa: BLE001
            continue
    return repr(obj)


def _jsonable(value, depth=0):
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    try:
        basestring_ = basestring  # noqa: F821
    except NameError:
        basestring_ = str
    if isinstance(value, basestring_):
        return value
    if depth > 3:
        return repr(value)
    if isinstance(value, dict):
        return dict((str(k), _jsonable(v, depth + 1)) for k, v in value.items())
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(v, depth + 1) for v in value]
    return repr(value)


class _capture_stdout(object):
    def __init__(self):
        self._old = sys.stdout
        self._buf = []
        sys.stdout = self

    def write(self, s):
        self._buf.append(s)
        try:
            self._old.write(s)
        except Exception:  # noqa: BLE001
            pass

    def flush(self):
        pass

    def stop(self):
        sys.stdout = self._old
        return "".join(self._buf).rstrip("\n")


_agent = None


def start(port=None):
    """Entry point used by sfm_init.py.  Idempotent."""
    global _agent
    if _agent is not None:
        return _agent
    port = int(port or os.environ.get("C2UI_AGENT_PORT") or DEFAULT_PORT)
    _agent = C2UIAgent(port)
    if not _agent.start():
        _agent = None
    return _agent


def stop():
    global _agent
    if _agent is not None:
        _agent.stop()
        _agent = None


# ------------------------------------------------------------------ standalone
def _standalone(port):
    app = QtGui.QApplication.instance() or QtGui.QApplication(sys.argv)
    win = QtGui.QMainWindow()
    win.setObjectName("SFMMainWindow_fake")
    win.setWindowTitle("Fake SFM (C2UI agent standalone)")
    central = QtGui.QWidget(win)
    lay = QtGui.QVBoxLayout(central)
    label = QtGui.QLabel("fake Animation Set Editor", central)
    label.setObjectName("AnimationSetEditor")
    label.setWindowTitle("Animation Set Editor")
    lay.addWidget(label)
    vp = QtGui.QFrame(central)
    vp.setObjectName("PrimaryViewport")
    vp.setWindowTitle("Primary Viewport")
    vp.setMinimumSize(320, 200)
    vp.setStyleSheet("background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #204060, stop:1 #102030); color: white;")
    vl = QtGui.QVBoxLayout(vp)
    vl.addWidget(QtGui.QLabel("FAKE PRIMARY VIEWPORT (Qt 4.8 / Python 2.7)", vp))
    lay.addWidget(vp)
    win.setCentralWidget(central)
    win.resize(640, 480)
    win.show()
    agent = start(port)
    if agent is None:
        return 1
    app.aboutToQuit.connect(agent.stop)
    return app.exec_()


if __name__ == "__main__":
    _port = DEFAULT_PORT
    for i, a in enumerate(sys.argv):
        if a == "--port" and i + 1 < len(sys.argv):
            _port = int(sys.argv[i + 1])
    if "--standalone" in sys.argv:
        sys.exit(_standalone(_port))
    else:
        start(_port)
