# Core/API/native - optional C++ module (pybind11)

`c2ui_native.cpp` implements the same functions as `Core/API/win32.py`
(window enumeration, SetParent / style changes for embedding the SFM viewport,
process lookup).  `Core/API/native.py` imports the compiled module when it exists
and silently falls back to the ctypes implementation otherwise, so a compiler is
**never required** to run C2UI.

## Build

Requires Visual Studio Build Tools (MSVC) or clang-cl + CMake 3.18+:

    Core\API\native\build.bat

or manually:

    .venv\Scripts\python.exe -m pip install pybind11
    cmake -S Core/API/native -B Core/API/native/build -DPython_EXECUTABLE=.venv/Scripts/python.exe
    cmake --build Core/API/native/build --config Release

The resulting `c2ui_native.*.pyd` is written to `Core/API/`.

Note: the host is 64-bit Python; `-A Win32` in build.bat is only attempted first
for toolchains that default to it and is not required.
