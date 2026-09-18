@echo off
setlocal
cd /d "%~dp0"
set PY=%~dp0..\..\..\.venv\Scripts\python.exe
if not exist "%PY%" set PY=python
"%PY%" -m pip install pybind11 >nul
cmake -S . -B build -DPython_EXECUTABLE="%PY%" -A Win32 2>nul || cmake -S . -B build -DPython_EXECUTABLE="%PY%"
if errorlevel 1 (echo [C2UI] CMake configure failed - is Visual Studio Build Tools installed? & exit /b 1)
cmake --build build --config Release
if errorlevel 1 (echo [C2UI] build failed & exit /b 1)
echo [C2UI] c2ui_native built into Core\API
