@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  .venv\Scripts\python.exe companion\touchflow.py
) else (
  where py >nul 2>nul
  if not errorlevel 1 (
    py -3 companion\touchflow.py
  ) else (
    python companion\touchflow.py
  )
)
if errorlevel 1 (
  echo.
  echo TouchFlow could not start. Install Python 3.12 or newer with Tk support.
  echo Install source dependencies with: py -3 -m pip install -r requirements.txt
  echo Or download the portable Windows ZIP from GitHub Releases.
  pause
)
