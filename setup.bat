@echo off
setlocal
cd /d "%~dp0"
echo [C2UI] Creating virtual environment...
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 -m venv .venv
) else (
    python -m venv .venv
)
if not exist ".venv\Scripts\python.exe" (
    echo [C2UI] Failed to create .venv - is Python 3.10+ installed?
    pause
    exit /b 1
)
echo [C2UI] Installing requirements...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
echo [C2UI] Done. Start with run.bat
pause
