@echo off
REM Run Origin Style Studio without packaging EXE
REM Usage: double-click this file in Windows

python app\origin_style_studio.py
if %errorlevel% neq 0 (
  echo.
  echo Failed to launch. Please ensure Python is installed and added to PATH.
  pause
)
