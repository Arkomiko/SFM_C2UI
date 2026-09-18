"""
Win32 helpers (ctypes) - the pure-Python fallback for Core/API/native.

Used by the host to embed foreign windows (the SFM viewport HWND) and to inspect
the sfm.exe process.  Every function is a no-op / returns defaults on non-Windows.
"""
from __future__ import annotations

import ctypes
import logging
import sys
from ctypes import wintypes
from typing import Dict, List, Optional

log = logging.getLogger("c2ui.win32")

IS_WINDOWS = sys.platform == "win32"

GWL_STYLE = -16
GWL_EXSTYLE = -20
WS_CHILD = 0x40000000
WS_POPUP = 0x80000000
WS_CAPTION = 0x00C00000
WS_THICKFRAME = 0x00040000
WS_SYSMENU = 0x00080000
WS_MINIMIZEBOX = 0x00020000
WS_MAXIMIZEBOX = 0x00010000
WS_VISIBLE = 0x10000000
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
SWP_NOZORDER = 0x0004
SWP_NOACTIVATE = 0x0010
SWP_FRAMECHANGED = 0x0020
SWP_SHOWWINDOW = 0x0040
SW_HIDE = 0
SW_SHOW = 5
SW_SHOWNA = 8

if IS_WINDOWS:
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    _WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.GetWindowLongW.restype = ctypes.c_long
    user32.SetWindowLongW.restype = ctypes.c_long
    user32.SetParent.restype = wintypes.HWND
    user32.GetParent.restype = wintypes.HWND
else:  # pragma: no cover
    user32 = kernel32 = None


def is_window(hwnd: int) -> bool:
    return bool(IS_WINDOWS and hwnd and user32.IsWindow(wintypes.HWND(hwnd)))


def window_text(hwnd: int) -> str:
    if not IS_WINDOWS:
        return ""
    buf = ctypes.create_unicode_buffer(512)
    user32.GetWindowTextW(wintypes.HWND(hwnd), buf, 512)
    return buf.value


def class_name(hwnd: int) -> str:
    if not IS_WINDOWS:
        return ""
    buf = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(wintypes.HWND(hwnd), buf, 256)
    return buf.value


def window_pid(hwnd: int) -> int:
    if not IS_WINDOWS:
        return 0
    pid = wintypes.DWORD(0)
    user32.GetWindowThreadProcessId(wintypes.HWND(hwnd), ctypes.byref(pid))
    return int(pid.value)


def window_rect(hwnd: int) -> tuple[int, int, int, int]:
    if not IS_WINDOWS:
        return (0, 0, 0, 0)
    r = wintypes.RECT()
    user32.GetWindowRect(wintypes.HWND(hwnd), ctypes.byref(r))
    return (r.left, r.top, r.right - r.left, r.bottom - r.top)


def enum_top_windows(pid: Optional[int] = None, visible_only: bool = True) -> List[Dict[str, object]]:
    """List top-level windows, optionally only those owned by ``pid``."""
    result: List[Dict[str, object]] = []
    if not IS_WINDOWS:
        return result

    @_WNDENUMPROC
    def _cb(hwnd, _lparam):
        if visible_only and not user32.IsWindowVisible(hwnd):
            return True
        wp = window_pid(hwnd)
        if pid is not None and wp != pid:
            return True
        result.append({"hwnd": int(hwnd), "pid": wp, "title": window_text(hwnd), "class": class_name(hwnd),
                       "rect": window_rect(hwnd)})
        return True

    user32.EnumWindows(_cb, 0)
    return result


def find_window(title_substr: str, pid: Optional[int] = None) -> Optional[int]:
    needle = title_substr.lower()
    for w in enum_top_windows(pid, visible_only=False):
        if needle in str(w["title"]).lower():
            return int(w["hwnd"])  # type: ignore[arg-type]
    return None


def make_child_style(hwnd: int) -> None:
    """Strip caption/frame and mark the window as a child so it embeds cleanly."""
    if not IS_WINDOWS:
        return
    h = wintypes.HWND(hwnd)
    style = user32.GetWindowLongW(h, GWL_STYLE)
    style &= ~(WS_CAPTION | WS_THICKFRAME | WS_SYSMENU | WS_MINIMIZEBOX | WS_MAXIMIZEBOX | WS_POPUP)
    style |= WS_CHILD | WS_VISIBLE
    user32.SetWindowLongW(h, GWL_STYLE, style)
    ex = user32.GetWindowLongW(h, GWL_EXSTYLE)
    ex &= ~WS_EX_APPWINDOW
    ex |= WS_EX_TOOLWINDOW
    user32.SetWindowLongW(h, GWL_EXSTYLE, ex)
    user32.SetWindowPos(h, None, 0, 0, 0, 0, 0x0001 | 0x0002 | SWP_NOZORDER | SWP_FRAMECHANGED | SWP_NOACTIVATE)


def set_parent(hwnd: int, parent_hwnd: Optional[int]) -> int:
    """Reparent ``hwnd`` under ``parent_hwnd`` (None = desktop).  Returns previous parent."""
    if not IS_WINDOWS:
        return 0
    prev = user32.SetParent(wintypes.HWND(hwnd), wintypes.HWND(parent_hwnd) if parent_hwnd else None)
    return int(prev or 0)


def move_window(hwnd: int, x: int, y: int, w: int, h: int, repaint: bool = True) -> None:
    if IS_WINDOWS:
        user32.MoveWindow(wintypes.HWND(hwnd), int(x), int(y), int(w), int(h), wintypes.BOOL(repaint))


def show_window(hwnd: int, show: bool = True) -> None:
    if IS_WINDOWS:
        user32.ShowWindow(wintypes.HWND(hwnd), SW_SHOWNA if show else SW_HIDE)


def process_exists(pid: int) -> bool:
    if not IS_WINDOWS:
        return False
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    h = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
    if not h:
        return False
    code = wintypes.DWORD(0)
    ok = kernel32.GetExitCodeProcess(h, ctypes.byref(code))
    kernel32.CloseHandle(h)
    return bool(ok) and code.value == 259          # STILL_ACTIVE


def find_process(exe_name: str) -> List[int]:
    """PIDs of running processes whose image name matches (case-insensitive)."""
    pids: List[int] = []
    if not IS_WINDOWS:
        return pids
    TH32CS_SNAPPROCESS = 0x00000002

    class PROCESSENTRY32W(ctypes.Structure):
        _fields_ = [("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD), ("th32ProcessID", wintypes.DWORD),
                    ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)), ("th32ModuleID", wintypes.DWORD),
                    ("cntThreads", wintypes.DWORD), ("th32ParentProcessID", wintypes.DWORD),
                    ("pcPriClassBase", ctypes.c_long), ("dwFlags", wintypes.DWORD), ("szExeFile", ctypes.c_wchar * 260)]

    snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snap == wintypes.HANDLE(-1).value:
        return pids
    entry = PROCESSENTRY32W()
    entry.dwSize = ctypes.sizeof(PROCESSENTRY32W)
    needle = exe_name.lower()
    if kernel32.Process32FirstW(snap, ctypes.byref(entry)):
        while True:
            if entry.szExeFile.lower() == needle:
                pids.append(int(entry.th32ProcessID))
            if not kernel32.Process32NextW(snap, ctypes.byref(entry)):
                break
    kernel32.CloseHandle(snap)
    return pids
