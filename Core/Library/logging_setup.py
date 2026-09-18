"""Logging bootstrap: console + rotating file + in-app sink for the Output Log panel."""
from __future__ import annotations

import logging
import logging.handlers
import sys
from collections import deque
from typing import Deque, Optional, Tuple

from PySide6.QtCore import QObject, Signal

from . import paths

LOG_FORMAT = "%(asctime)s %(levelname)-7s %(name)s: %(message)s"
DATE_FORMAT = "%H:%M:%S"


class QtLogSink(QObject, logging.Handler):
    """logging.Handler that re-emits records as a Qt signal (GUI-thread safe)."""

    record_emitted = Signal(str, str, str)   # level, logger name, formatted message

    def __init__(self) -> None:
        QObject.__init__(self)
        logging.Handler.__init__(self)
        self.setFormatter(logging.Formatter("%(asctime)s [%(name)s] %(message)s", DATE_FORMAT))
        self.backlog: Deque[Tuple[str, str, str]] = deque(maxlen=2000)
        self.total = 0          # records ever emitted (backlog is bounded)

    def emit(self, record: logging.LogRecord) -> None:  # type: ignore[override]
        try:
            msg = self.format(record)
        except Exception:  # noqa: BLE001
            msg = record.getMessage()
        item = (record.levelname, record.name, msg)
        self.backlog.append(item)
        self.total += 1
        self.record_emitted.emit(*item)


_sink: Optional[QtLogSink] = None


def get_sink() -> QtLogSink:
    global _sink
    if _sink is None:
        _sink = QtLogSink()
    return _sink


def setup_logging(level: str = "INFO") -> None:
    paths.ensure_user_dirs()
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    if root.handlers:
        return  # already configured (e.g. tests)

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    root.addHandler(console)

    file_handler = logging.handlers.RotatingFileHandler(
        paths.USER_LOGS_DIR / "c2ui.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    root.addHandler(file_handler)

    root.addHandler(get_sink())
    logging.getLogger("c2ui").info("Logging initialised (level=%s, dir=%s)", level, paths.USER_LOGS_DIR)
