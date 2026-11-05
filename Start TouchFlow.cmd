@echo off
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
  py -3 companion\touchflow.py
) else (
  python companion\touchflow.py
)
if errorlevel 1 (
  echo.
  echo TouchFlow could not start. Install Python 3.12 or newer with Tk support,
  echo or download the portable Windows ZIP from GitHub Releases.
  pause
)
