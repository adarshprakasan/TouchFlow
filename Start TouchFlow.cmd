@echo off
cd /d "%~dp0"
python companion\touchflow.py
if errorlevel 1 pause
