@echo off
REM Root launcher for Origin Style Studio

if exist app\origin_style_studio.py (
  python app\origin_style_studio.py
) else (
  echo.
  echo [ERROR] app\origin_style_studio.py not found.
  echo Please make sure you are in the repository root directory.
  pause
)
