"""
Application-wide event bus.

A tiny publish/subscribe layer on top of a Qt signal so that events published from
worker threads (e.g. the SFM bridge) are delivered on the GUI thread.

    bus.subscribe("sfm.connected", lambda payload: ...)
    bus.publish("sfm.connected", {"port": 41794})

Topic names are dotted strings.  A subscriber to "sfm" receives every topic that
starts with "sfm." (prefix matching), which is handy for logging/debugging.
"""
from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any, Callable, DefaultDict, List

from PySide6.QtCore import QObject, Qt, Signal

log = logging.getLogger("c2ui.events")

Handler = Callable[[Any], None]


class EventBus(QObject):
    _event = Signal(str, object)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._subs: DefaultDict[str, List[Handler]] = defaultdict(list)
        # Queued connection => always dispatched on the receiver (GUI) thread.
        self._event.connect(self._dispatch, Qt.ConnectionType.QueuedConnection)

    # -- public API -------------------------------------------------------------
    def subscribe(self, topic: str, handler: Handler) -> Callable[[], None]:
        """Subscribe handler to topic; returns an unsubscribe callable."""
        self._subs[topic].append(handler)

        def _unsub() -> None:
            try:
                self._subs[topic].remove(handler)
            except ValueError:
                pass

        return _unsub

    def publish(self, topic: str, payload: Any = None) -> None:
        """Thread-safe: may be called from any thread."""
        self._event.emit(topic, payload)

    def publish_sync(self, topic: str, payload: Any = None) -> None:
        """Dispatch immediately on the calling thread (GUI thread only)."""
        self._dispatch(topic, payload)

    # -- internals --------------------------------------------------------------
    def _dispatch(self, topic: str, payload: Any) -> None:
        handlers: List[Handler] = []
        # snapshot: a handler may (un)subscribe while we are dispatching
        for key, subs in list(self._subs.items()):
            if key == topic or key == "*" or topic.startswith(key + "."):
                handlers.extend(subs)
        for h in handlers:
            try:
                h(payload)
            except Exception:  # noqa: BLE001 - never let one subscriber kill the bus
                log.exception("Event handler for %r failed", topic)
