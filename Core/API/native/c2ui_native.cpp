// c2ui_native - Win32 helpers for the C2UI host (pybind11 module).
//
// Mirrors Core/API/win32.py one-to-one so Core/API/native.py can pick whichever
// implementation is available.  Build with CMake (see CMakeLists.txt).

#define WIN32_LEAN_AND_MEAN
#define NOMINMAX
#include <windows.h>
#include <tlhelp32.h>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <string>
#include <vector>

namespace py = pybind11;

namespace {

std::wstring windowTextW(HWND hwnd) {
    wchar_t buf[512] = {0};
    GetWindowTextW(hwnd, buf, 512);
    return buf;
}

std::wstring classNameW(HWND hwnd) {
    wchar_t buf[256] = {0};
    GetClassNameW(hwnd, buf, 256);
    return buf;
}

std::string toUtf8(const std::wstring& s) {
    if (s.empty()) return {};
    int n = WideCharToMultiByte(CP_UTF8, 0, s.c_str(), (int)s.size(), nullptr, 0, nullptr, nullptr);
    std::string out(n, '\0');
    WideCharToMultiByte(CP_UTF8, 0, s.c_str(), (int)s.size(), &out[0], n, nullptr, nullptr);
    return out;
}

std::wstring toWide(const std::string& s) {
    if (s.empty()) return {};
    int n = MultiByteToWideChar(CP_UTF8, 0, s.c_str(), (int)s.size(), nullptr, 0);
    std::wstring out(n, L'\0');
    MultiByteToWideChar(CP_UTF8, 0, s.c_str(), (int)s.size(), &out[0], n);
    return out;
}

std::wstring lower(std::wstring s) {
    for (auto& c : s) c = (wchar_t)towlower(c);
    return s;
}

struct EnumCtx {
    std::vector<py::dict> out;
    DWORD pid;
    bool visibleOnly;
};

BOOL CALLBACK enumProc(HWND hwnd, LPARAM lparam) {
    auto* ctx = reinterpret_cast<EnumCtx*>(lparam);
    if (ctx->visibleOnly && !IsWindowVisible(hwnd)) return TRUE;
    DWORD pid = 0;
    GetWindowThreadProcessId(hwnd, &pid);
    if (ctx->pid != 0 && pid != ctx->pid) return TRUE;
    RECT r{};
    GetWindowRect(hwnd, &r);
    py::dict d;
    d["hwnd"] = (std::uintptr_t)hwnd;
    d["pid"] = (unsigned long)pid;
    d["title"] = toUtf8(windowTextW(hwnd));
    d["class"] = toUtf8(classNameW(hwnd));
    d["rect"] = py::make_tuple(r.left, r.top, r.right - r.left, r.bottom - r.top);
    ctx->out.push_back(std::move(d));
    return TRUE;
}

} // namespace

PYBIND11_MODULE(c2ui_native, m) {
    m.doc() = "C2UI native Win32 helpers";

    m.def("is_window", [](std::uintptr_t hwnd) { return hwnd && IsWindow((HWND)hwnd) != 0; });
    m.def("window_text", [](std::uintptr_t hwnd) { return toUtf8(windowTextW((HWND)hwnd)); });
    m.def("class_name", [](std::uintptr_t hwnd) { return toUtf8(classNameW((HWND)hwnd)); });
    m.def("window_pid", [](std::uintptr_t hwnd) {
        DWORD pid = 0;
        GetWindowThreadProcessId((HWND)hwnd, &pid);
        return (unsigned long)pid;
    });
    m.def("window_rect", [](std::uintptr_t hwnd) {
        RECT r{};
        GetWindowRect((HWND)hwnd, &r);
        return py::make_tuple(r.left, r.top, r.right - r.left, r.bottom - r.top);
    });
    m.def("enum_top_windows", [](py::object pid, bool visibleOnly) {
        EnumCtx ctx{{}, pid.is_none() ? 0 : pid.cast<DWORD>(), visibleOnly};
        EnumWindows(enumProc, reinterpret_cast<LPARAM>(&ctx));
        py::list out;
        for (auto& d : ctx.out) out.append(d);
        return out;
    }, py::arg("pid") = py::none(), py::arg("visible_only") = true);
    m.def("find_window", [](const std::string& titleSubstr, py::object pid) -> py::object {
        EnumCtx ctx{{}, pid.is_none() ? 0 : pid.cast<DWORD>(), false};
        EnumWindows(enumProc, reinterpret_cast<LPARAM>(&ctx));
        auto needle = lower(toWide(titleSubstr));
        for (auto& d : ctx.out) {
            auto title = lower(toWide(d["title"].cast<std::string>()));
            if (title.find(needle) != std::wstring::npos) return d["hwnd"];
        }
        return py::none();
    }, py::arg("title_substr"), py::arg("pid") = py::none());
    m.def("make_child_style", [](std::uintptr_t h) {
        HWND hwnd = (HWND)h;
        LONG style = GetWindowLongW(hwnd, GWL_STYLE);
        style &= ~(WS_CAPTION | WS_THICKFRAME | WS_SYSMENU | WS_MINIMIZEBOX | WS_MAXIMIZEBOX | WS_POPUP);
        style |= WS_CHILD | WS_VISIBLE;
        SetWindowLongW(hwnd, GWL_STYLE, style);
        LONG ex = GetWindowLongW(hwnd, GWL_EXSTYLE);
        ex &= ~WS_EX_APPWINDOW;
        ex |= WS_EX_TOOLWINDOW;
        SetWindowLongW(hwnd, GWL_EXSTYLE, ex);
        SetWindowPos(hwnd, nullptr, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED | SWP_NOACTIVATE);
    });
    m.def("set_parent", [](std::uintptr_t hwnd, py::object parent) {
        HWND p = parent.is_none() ? nullptr : (HWND)parent.cast<std::uintptr_t>();
        return (std::uintptr_t)SetParent((HWND)hwnd, p);
    }, py::arg("hwnd"), py::arg("parent_hwnd") = py::none());
    m.def("move_window", [](std::uintptr_t hwnd, int x, int y, int w, int h, bool repaint) {
        MoveWindow((HWND)hwnd, x, y, w, h, repaint ? TRUE : FALSE);
    }, py::arg("hwnd"), py::arg("x"), py::arg("y"), py::arg("w"), py::arg("h"), py::arg("repaint") = true);
    m.def("show_window", [](std::uintptr_t hwnd, bool show) {
        ShowWindow((HWND)hwnd, show ? SW_SHOWNA : SW_HIDE);
    }, py::arg("hwnd"), py::arg("show") = true);
    m.def("process_exists", [](unsigned long pid) {
        HANDLE h = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, FALSE, pid);
        if (!h) return false;
        DWORD code = 0;
        BOOL ok = GetExitCodeProcess(h, &code);
        CloseHandle(h);
        return ok && code == STILL_ACTIVE;
    });
    m.def("find_process", [](const std::string& exeName) {
        std::vector<unsigned long> pids;
        HANDLE snap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
        if (snap == INVALID_HANDLE_VALUE) return pids;
        PROCESSENTRY32W e{};
        e.dwSize = sizeof(e);
        auto needle = lower(toWide(exeName));
        if (Process32FirstW(snap, &e)) {
            do {
                if (lower(e.szExeFile) == needle) pids.push_back(e.th32ProcessID);
            } while (Process32NextW(snap, &e));
        }
        CloseHandle(snap);
        return pids;
    });
    m.attr("IS_NATIVE") = true;
}
