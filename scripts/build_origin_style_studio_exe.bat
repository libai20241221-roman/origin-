@echo off
REM Build Origin Style Studio EXE (Windows)
REM Usage: run in repo root after installing pyinstaller

pyinstaller --noconfirm --onefile --windowed --name OriginStyleStudio app\origin_style_studio.py

echo.
echo Build complete. EXE location:
echo dist\OriginStyleStudio.exe
