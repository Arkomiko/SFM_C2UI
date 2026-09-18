"""
SFMBridge - Python 3 side of the link to the agent running inside sfm.exe.

Built on QTcpSocket so all callbacks land on the GUI thread; no locking needed.

    bridge.connect_to_agent()                       # async, emits connected_changed
    bridge.call("sfm.get_shots", {}, on_result)     # async with callback
    shots = bridge.call_sync("sfm.get_shots")       # blocks (with local event loop) up to timeout
    bridge.events.subscribe("sfm.frame_changed", handler)   # server-pushed events

While no agent is reachable the bridge is in *offline mode*: calls fail fast with
BridgeError and the UI keeps working with placeholder data.
"""
from __future__ import annotations

import logging
from typing import Any, Callable, Dict, Optional

from PySide6.QtCore import QEventLoop, QObject, QTimer, Signal
from PySide6.QtNetwork import QAbstractSocket, QTcpSocket

from . import protocol

log = logging.getLogger("c2ui.bridge")

ResultCallback = Callable[[Any, Optional[Dict[str, Any]]], None]


class BridgeError(RuntimeError):
    def __init__(self, code: int, message: str, data: Any = None) -> None:
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message
        self.data = data


class SFMBridge(QObject):
    connected_changed = Signal(bool)
    event_received = Signal(str, object)        # event name, data
    handshake_done = Signal(dict)

    def __init__(self, events: Any, host: str = protocol.DEFAULT_HOST, port: int = protocol.DEFAULT_PORT,
                 auto_reconnect: bool = True, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.events = events
        self.host = host
        self.port = port
        self.auto_reconnect = auto_reconnect
        self.agent_info: Dict[str, Any] = {}

        self._sock = QTcpSocket(self)
        self._sock.connected.connect(self._on_connected)
        self._sock.disconnected.connect(self._on_disconnected)
        self._sock.readyRead.connect(self._on_ready_read)
        self._sock.errorOccurred.connect(self._on_error)
        self._buffer = b""
        self._next_id = 1
        self._pending: Dict[int, ResultCallback] = {}
        self._connected = False

        self._reconnect = QTimer(self)
        self._reconnect.setInterval(3000)
        self._reconnect.timeout.connect(self._try_reconnect)

    # ---------------------------------------------------------------- state
    @property
    def connected(self) -> bool:
        return self._connected

    def connect_to_agent(self) -> None:
        if self._sock.state() != QAbstractSocket.SocketState.UnconnectedState:
            return
        log.debug("Connecting to SFM agent at %s:%s", self.host, self.port)
        self._sock.connectToHost(self.host, self.port)
        if self.auto_reconnect and not self._reconnect.isActive():
            self._reconnect.start()

    def disconnect_from_agent(self) -> None:
        self._reconnect.stop()
        if self._sock.state() != QAbstractSocket.SocketState.UnconnectedState:
            self._sock.disconnectFromHost()

    def _try_reconnect(self) -> None:
        if self._sock.state() == QAbstractSocket.SocketState.UnconnectedState:
            self._sock.connectToHost(self.host, self.port)

    def flush(self, timeout_ms: int = 300) -> None:
        """Push pending writes out (used right before shutdown)."""
        if self._sock.state() == QAbstractSocket.SocketState.ConnectedState:
            self._sock.flush()
            if self._sock.bytesToWrite():
                self._sock.waitForBytesWritten(timeout_ms)

    # ---------------------------------------------------------------- calls
    def call(self, method: str, params: Optional[Dict[str, Any]] = None,
             callback: Optional[ResultCallback] = None) -> Optional[int]:
        if not self._connected:
            if callback:
                callback(None, {"code": protocol.ERR_INTERNAL, "message": "SFM agent not connected"})
            return None
        req_id = self._next_id
        self._next_id += 1
        if callback:
            self._pending[req_id] = callback
        self._sock.write(protocol.encode(protocol.make_request(req_id, method, params)))
        return req_id

    def call_sync(self, method: str, params: Optional[Dict[str, Any]] = None, timeout_ms: int = 5000) -> Any:
        if not self._connected:
            raise BridgeError(protocol.ERR_INTERNAL, "SFM agent not connected")
        loop = QEventLoop()
        box: Dict[str, Any] = {}

        def _cb(result: Any, error: Optional[Dict[str, Any]]) -> None:
            box["result"], box["error"] = result, error
            loop.quit()

        self.call(method, params, _cb)
        QTimer.singleShot(timeout_ms, loop.quit)
        loop.exec()
        if "error" not in box and "result" not in box:
            raise BridgeError(protocol.ERR_INTERNAL, f"Timeout calling {method}")
        if box.get("error"):
            e = box["error"]
            raise BridgeError(e.get("code", -1), e.get("message", "error"), e.get("data"))
        return box.get("result")

    # ------------------------------------------------------------ socket io
    def _on_connected(self) -> None:
        log.info("Connected to SFM agent at %s:%s", self.host, self.port)
        self._buffer = b""
        self._connected = True
        self.connected_changed.emit(True)
        self.events.publish("sfm.connected", {"host": self.host, "port": self.port})
        self.call(protocol.HANDSHAKE_METHOD, {"client": "C2UI", "protocol": protocol.PROTOCOL_VERSION}, self._on_hello)

    def _on_hello(self, result: Any, error: Optional[Dict[str, Any]]) -> None:
        if error:
            log.warning("Agent handshake failed: %s", error)
            return
        self.agent_info = result or {}
        log.info("Agent: %s", self.agent_info)
        self.handshake_done.emit(self.agent_info)

    def _on_disconnected(self) -> None:
        was = self._connected
        self._connected = False
        self.agent_info = {}
        for cb in list(self._pending.values()):
            cb(None, {"code": protocol.ERR_INTERNAL, "message": "disconnected"})
        self._pending.clear()
        if was:
            log.warning("SFM agent disconnected")
            self.connected_changed.emit(False)
            self.events.publish("sfm.disconnected", {})

    def _on_error(self, err: QAbstractSocket.SocketError) -> None:
        if err == QAbstractSocket.SocketError.ConnectionRefusedError:
            log.debug("SFM agent not reachable (connection refused)")
        else:
            log.debug("Socket error: %s", self._sock.errorString())

    def _on_ready_read(self) -> None:
        self._buffer += bytes(self._sock.readAll())
        while b"\n" in self._buffer:
            line, self._buffer = self._buffer.split(b"\n", 1)
            if not line.strip():
                continue
            try:
                msg = protocol.decode(line)
            except ValueError:
                log.warning("Bad message from agent: %r", line[:200])
                continue
            self._dispatch(msg)

    def _dispatch(self, msg: Dict[str, Any]) -> None:
        if "event" in msg:
            name, data = msg["event"], msg.get("data")
            self.event_received.emit(name, data)
            self.events.publish(f"sfm.{name}" if not name.startswith("sfm.") else name, data)
            return
        req_id = msg.get("id")
        cb = self._pending.pop(req_id, None)
        if cb is None:
            return
        try:
            cb(msg.get("result"), msg.get("error"))
        except Exception:  # noqa: BLE001
            log.exception("Bridge callback failed for request %s", req_id)
