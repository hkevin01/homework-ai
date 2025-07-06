@echo off
REM Build script for Windows - Scientific ML Homework Assistant

echo ================================================
echo 🏗️ Building Scientific ML Homework Assistant
echo Windows Executable Builder
echo ================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing PyInstaller...
    python -m pip install PyInstaller
) else (
    echo ✅ PyInstaller found
)

REM Create dist directory if it doesn't exist
if not exist "dist" mkdir "dist"

echo 🔨 Building Windows executable...

REM Run PyInstaller
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name homework-ai ^
    --distpath dist ^
    --workpath build ^
    --specpath . ^
    --add-data "src\homework1;homework1" ^
    --add-data "src\homework2;homework2" ^
    --hidden-import PyQt5.QtCore ^
    --hidden-import PyQt5.QtGui ^
    --hidden-import PyQt5.QtWidgets ^
    --hidden-import matplotlib.backends.backend_qt5agg ^
    --hidden-import numpy ^
    --hidden-import scipy ^
    src\main_gui.py

if exist "dist\homework-ai.exe" (
    echo ✅ Build successful!
    echo 📦 Executable: dist\homework-ai.exe
    
    REM Get file size
    for %%I in (dist\homework-ai.exe) do echo 📏 Size: %%~zI bytes
    
    echo.
    echo 🚀 To run the executable:
    echo    dist\homework-ai.exe
    echo.
    echo 💡 You can also create shortcuts or move to a different location
) else (
    echo ❌ Build failed - executable not found
    pause
    exit /b 1
)

REM Clean up build artifacts
echo 🧹 Cleaning build artifacts...
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo ✅ Build process completed!
pause
