"""
Native helper loader.

    from Core.API import native
    native.enum_top_windows(pid)

Prefers the compiled pybind11 module (Core/API/c2ui_native*.pyd) and falls back to
the ctypes implementation in win32.py.  Both expose the same functions.
"""
from __future__ import annotations

import logging

log = logging.getLogger("c2ui.native")

try:
    from . import c2ui_native as _impl  # type: ignore[attr-defined]
    IS_NATIVE = True
    log.info("Using compiled c2ui_native module")
except ImportError:
    from . import win32 as _impl
    IS_NATIVE = False

is_window = _impl.is_window
window_text = _impl.window_text
class_name = _impl.class_name
window_pid = _impl.window_pid
window_rect = _impl.window_rect
enum_top_windows = _impl.enum_top_windows
find_window = _impl.find_window
make_child_style = _impl.make_child_style
set_parent = _impl.set_parent
move_window = _impl.move_window
show_window = _impl.show_window
process_exists = _impl.process_exists
find_process = _impl.find_process

__all__ = ["IS_NATIVE", "is_window", "window_text", "class_name", "window_pid", "window_rect", "enum_top_windows",
           "find_window", "make_child_style", "set_parent", "move_window", "show_window", "process_exists",
           "find_process"]
