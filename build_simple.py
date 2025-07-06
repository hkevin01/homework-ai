#!/usr/bin/env python3
"""
Simple Build Script for Scientific Machine Learning Homework Assistant
Creates standalone executables using PyInstaller
"""

import os
import platform
import subprocess
import sys


def main():
    """Build standalone executable."""
    print("🏗️ Building Scientific ML Homework Assistant")
    print("=" * 50)
    
    # Check PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'PyInstaller'])
    
    # Get platform info
    system = platform.system().lower()
    
    # Define executable name
    exe_name = 'homework-ai.exe' if system == 'windows' else 'homework-ai'
    
    # PyInstaller command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name', 'homework-ai',
        '--add-data', 'src/homework1:homework1',
        '--add-data', 'src/homework2:homework2',
        '--hidden-import', 'PyQt5.QtCore',
        '--hidden-import', 'PyQt5.QtGui',
        '--hidden-import', 'PyQt5.QtWidgets',
        '--hidden-import', 'matplotlib.backends.backend_qt5agg',
        'src/main_gui.py'
    ]
    
    print(f"🔨 Building for {system}...")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Build complete! Executable: dist/{exe_name}")
        print(f"📂 Size: {os.path.getsize(f'dist/{exe_name}') / 1024 / 1024:.1f} MB")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
