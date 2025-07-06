#!/usr/bin/env python3
"""
Build Script for Scientific Machine Learning Homework Assistant
Creates standalone executables for Windows (.exe) and Linux

This script uses PyInstaller to create platform-specific executables
that include all dependencies and can run without Python installed.
"""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


# Colors for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

def print_colored(message, color):
    """Print colored message."""
    print(f"{color}{message}{Colors.NC}")

def print_header(title):
    """Print section header."""
    print_colored(f"\n{'='*60}", Colors.BLUE)
    print_colored(f"🏗️  {title}", Colors.BOLD)
    print_colored(f"{'='*60}", Colors.BLUE)

def check_dependencies():
    """Check if required build dependencies are installed."""
    print_header("Checking Build Dependencies")
    
    required_packages = ['PyInstaller', 'PyQt5', 'numpy', 'matplotlib', 'scipy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
            print_colored(f"✅ {package}", Colors.GREEN)
        except ImportError:
            missing_packages.append(package)
            print_colored(f"❌ {package}", Colors.RED)
    
    if missing_packages:
        print_colored(f"\n⚠️  Missing packages: {', '.join(missing_packages)}", Colors.YELLOW)
        print_colored("Installing missing packages...", Colors.YELLOW)
        
        for package in missing_packages:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                             check=True, capture_output=True)
                print_colored(f"✅ Installed {package}", Colors.GREEN)
            except subprocess.CalledProcessError as e:
                print_colored(f"❌ Failed to install {package}: {e}", Colors.RED)
                return False
    
    return True

def create_spec_file():
    """Create PyInstaller spec file for better control."""
    print_header("Creating PyInstaller Specification")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Define the main entry point
main_script = 'src/main_gui.py'

# Additional data files to include
added_files = [
    ('src/homework1/*.py', 'homework1'),
    ('src/homework2/*.py', 'homework2'),
    ('src/homework1/*.json', 'homework1'),
    ('src/homework2/*.json', 'homework2'),
    ('src/homework1/README.md', 'homework1'),
    ('src/homework2/README.md', 'homework2'),
    ('docs/homework/*.pdf', 'docs/homework'),
    ('requirements.txt', '.'),
    ('README.md', '.'),
]

# Hidden imports (modules not automatically detected)
hidden_imports = [
    'PyQt5.QtCore',
    'PyQt5.QtGui', 
    'PyQt5.QtWidgets',
    'numpy',
    'matplotlib',
    'matplotlib.backends.backend_qt5agg',
    'scipy',
    'scipy.stats',
    'scipy.optimize',
    'json',
    'pathlib',
]

a = Analysis(
    [main_script],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='homework-ai',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)
'''
    
    with open('homework-ai.spec', 'w') as f:
        f.write(spec_content)
    
    print_colored("✅ Created homework-ai.spec", Colors.GREEN)

def build_executable():
    """Build the executable using PyInstaller."""
    print_header("Building Executable")
    
    # Get platform info
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    print_colored(f"🖥️  Platform: {system} {arch}", Colors.BLUE)
    print_colored(f"🐍 Python: {sys.version.split()[0]}", Colors.BLUE)
    
    # Create output directory
    output_dir = f"dist/{system}-{arch}"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Run PyInstaller
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            '--noconfirm',
            f'--distpath={output_dir}',
            'homework-ai.spec'
        ]
        
        print_colored(f"🔨 Running: {' '.join(cmd)}", Colors.YELLOW)
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print_colored("✅ Build completed successfully!", Colors.GREEN)
        
        # Show output location
        if system == 'windows':
            executable_name = 'homework-ai.exe'
        else:
            executable_name = 'homework-ai'
            
        executable_path = os.path.join(output_dir, executable_name)
        
        if os.path.exists(executable_path):
            file_size = os.path.getsize(executable_path) / (1024 * 1024)  # MB
            print_colored(f"📦 Executable: {executable_path}", Colors.GREEN)
            print_colored(f"📏 Size: {file_size:.1f} MB", Colors.GREEN)
        else:
            print_colored(f"⚠️  Executable not found at expected location: {executable_path}", Colors.YELLOW)
            
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Build failed: {e}", Colors.RED)
        print_colored(f"Error output: {e.stderr}", Colors.RED)
        return False
    
    return True

def create_installer_scripts():
    """Create platform-specific installer scripts."""
    print_header("Creating Installer Scripts")
    
    system = platform.system().lower()
    
    if system == 'linux':
        create_linux_installer()
    elif system == 'windows':
        create_windows_installer()
    else:
        print_colored(f"⚠️  No installer script for {system}", Colors.YELLOW)

def create_linux_installer():
    """Create Linux installer script."""
    installer_content = '''#!/bin/bash
# Scientific Machine Learning Homework Assistant - Linux Installer

set -e

# Colors
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
BOLD='\\033[1m'
NC='\\033[0m'

echo -e "${BLUE}${BOLD}🎓 Scientific Machine Learning Homework Assistant${NC}"
echo -e "${BLUE}Linux Installation Script${NC}"
echo -e "${BLUE}==============================================${NC}"

# Get system info
SYSTEM=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)
INSTALL_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons"

echo -e "${BLUE}📋 Installation Details:${NC}"
echo -e "   Platform: $SYSTEM $ARCH"
echo -e "   Install Directory: $INSTALL_DIR"
echo -e "   Desktop Entry: $DESKTOP_DIR"

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR"

# Find the executable
EXECUTABLE="homework-ai"
if [ -f "dist/$SYSTEM-$ARCH/$EXECUTABLE" ]; then
    EXEC_PATH="dist/$SYSTEM-$ARCH/$EXECUTABLE"
elif [ -f "dist/$EXECUTABLE" ]; then
    EXEC_PATH="dist/$EXECUTABLE"
else
    echo -e "${RED}❌ Executable not found${NC}"
    exit 1
fi

# Copy executable
echo -e "${YELLOW}📦 Installing executable...${NC}"
cp "$EXEC_PATH" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/$EXECUTABLE"

# Create desktop entry
echo -e "${YELLOW}🖥️  Creating desktop entry...${NC}"
cat > "$DESKTOP_DIR/homework-ai.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Scientific ML Homework Assistant
Comment=PyQt application for scientific machine learning homework
Exec=$INSTALL_DIR/$EXECUTABLE
Icon=homework-ai
Terminal=false
Categories=Education;Science;
EOF

# Create simple icon (if not exists)
if [ ! -f "$ICON_DIR/homework-ai.png" ]; then
    echo -e "${YELLOW}🎨 Creating application icon...${NC}"
    # Create a simple text-based icon using ImageMagick if available
    if command -v convert >/dev/null 2>&1; then
        convert -size 64x64 xc:lightblue -font DejaVu-Sans-Bold -pointsize 12 -fill darkblue -annotate +5+30 "ML\\nHW" "$ICON_DIR/homework-ai.png" 2>/dev/null || true
    fi
fi

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
fi

echo -e "${GREEN}✅ Installation completed successfully!${NC}"
echo -e "${GREEN}🚀 You can now run the application by:${NC}"
echo -e "   • Typing: homework-ai"
echo -e "   • Finding it in your applications menu"
echo -e "   • Running: $INSTALL_DIR/$EXECUTABLE"

# Offer to add to PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo -e "${YELLOW}💡 Tip: Add $INSTALL_DIR to your PATH for easier access${NC}"
    echo -e "   Add this line to your ~/.bashrc or ~/.zshrc:"
    echo -e "   export PATH=\"\\$PATH:$INSTALL_DIR\""
fi
'''
    
    with open('install-linux.sh', 'w') as f:
        f.write(installer_content)
    
    os.chmod('install-linux.sh', 0o755)
    print_colored("✅ Created install-linux.sh", Colors.GREEN)

def create_windows_installer():
    """Create Windows installer batch script."""
    installer_content = '''@echo off
REM Scientific Machine Learning Homework Assistant - Windows Installer

echo ====================================================
echo 🎓 Scientific Machine Learning Homework Assistant
echo Windows Installation Script
echo ====================================================

REM Get system info
set ARCH=%PROCESSOR_ARCHITECTURE%
set INSTALL_DIR=%USERPROFILE%\\AppData\\Local\\HomeworkAI
set EXECUTABLE=homework-ai.exe

echo 📋 Installation Details:
echo    Platform: Windows %ARCH%
echo    Install Directory: %INSTALL_DIR%

REM Create install directory
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Find and copy executable
if exist "dist\\windows-%ARCH%\\%EXECUTABLE%" (
    echo 📦 Installing executable...
    copy "dist\\windows-%ARCH%\\%EXECUTABLE%" "%INSTALL_DIR%\\" > nul
) else if exist "dist\\%EXECUTABLE%" (
    echo 📦 Installing executable...
    copy "dist\\%EXECUTABLE%" "%INSTALL_DIR%\\" > nul
) else (
    echo ❌ Executable not found
    pause
    exit /b 1
)

REM Create start menu shortcut
echo 🖥️ Creating start menu shortcut...
set SHORTCUT_DIR=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs
echo Set oWS = WScript.CreateObject("WScript.Shell") > createshortcut.vbs
echo sLinkFile = "%SHORTCUT_DIR%\\Scientific ML Homework Assistant.lnk" >> createshortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> createshortcut.vbs
echo oLink.TargetPath = "%INSTALL_DIR%\\%EXECUTABLE%" >> createshortcut.vbs
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> createshortcut.vbs
echo oLink.Description = "Scientific Machine Learning Homework Assistant" >> createshortcut.vbs
echo oLink.Save >> createshortcut.vbs
cscript createshortcut.vbs > nul
del createshortcut.vbs

REM Create desktop shortcut
echo 🖥️ Creating desktop shortcut...
echo Set oWS = WScript.CreateObject("WScript.Shell") > createshortcut.vbs
echo sLinkFile = "%USERPROFILE%\\Desktop\\Scientific ML Homework Assistant.lnk" >> createshortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> createshortcut.vbs
echo oLink.TargetPath = "%INSTALL_DIR%\\%EXECUTABLE%" >> createshortcut.vbs
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> createshortcut.vbs
echo oLink.Description = "Scientific Machine Learning Homework Assistant" >> createshortcut.vbs
echo oLink.Save >> createshortcut.vbs
cscript createshortcut.vbs > nul
del createshortcut.vbs

echo ✅ Installation completed successfully!
echo 🚀 You can now run the application by:
echo    • Double-clicking the desktop shortcut
echo    • Finding it in the Start Menu
echo    • Running: %INSTALL_DIR%\\%EXECUTABLE%

pause
'''
    
    with open('install-windows.bat', 'w') as f:
        f.write(installer_content)
    
    print_colored("✅ Created install-windows.bat", Colors.GREEN)

def create_build_all_script():
    """Create a script to build for multiple platforms."""
    build_all_content = '''#!/bin/bash
# Build script for all platforms
# Run this on different platforms to create platform-specific builds

echo "🏗️ Building Scientific ML Homework Assistant for all platforms"
echo "=============================================================="

PLATFORMS=("linux-x86_64" "windows-amd64" "darwin-x86_64")
CURRENT_PLATFORM=$(python3 -c "import platform; print(f'{platform.system().lower()}-{platform.machine().lower()}')")

echo "📍 Current platform: $CURRENT_PLATFORM"

# Build for current platform
echo "🔨 Building for current platform..."
python3 build_executable.py

# Show instructions for other platforms
echo ""
echo "📋 To build for other platforms:"
echo "--------------------------------"

if [[ "$CURRENT_PLATFORM" != "linux"* ]]; then
    echo "🐧 For Linux:"
    echo "   1. Run on a Linux machine:"
    echo "   2. python3 build_executable.py"
    echo "   3. ./install-linux.sh"
fi

if [[ "$CURRENT_PLATFORM" != "windows"* ]]; then
    echo "🪟 For Windows:"
    echo "   1. Run on a Windows machine:"
    echo "   2. python build_executable.py"
    echo "   3. install-windows.bat"
fi

if [[ "$CURRENT_PLATFORM" != "darwin"* ]]; then
    echo "🍎 For macOS:"
    echo "   1. Run on a macOS machine:"
    echo "   2. python3 build_executable.py"
    echo "   3. Create .app bundle manually"
fi

echo ""
echo "✅ Build process completed for $CURRENT_PLATFORM"
'''

    with open('build-all.sh', 'w') as f:
        f.write(build_all_content)
    
    os.chmod('build-all.sh', 0o755)
    print_colored("✅ Created build-all.sh", Colors.GREEN)

def cleanup():
    """Clean up temporary build files."""
    print_header("Cleaning Up")
    
    cleanup_dirs = ['build', '__pycache__']
    cleanup_files = ['homework-ai.spec']
    
    for directory in cleanup_dirs:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print_colored(f"🗑️  Removed {directory}/", Colors.YELLOW)
    
    for file in cleanup_files:
        if os.path.exists(file):
            os.remove(file)
            print_colored(f"🗑️  Removed {file}", Colors.YELLOW)

def main():
    """Main build process."""
    print_colored("🎓 Scientific Machine Learning Homework Assistant", Colors.BOLD)
    print_colored("Executable Build Script", Colors.BLUE)
    print_colored("=" * 50, Colors.BLUE)
    
    # Change to project directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    try:
        # Step 1: Check dependencies
        if not check_dependencies():
            print_colored("❌ Dependency check failed", Colors.RED)
            return 1
        
        # Step 2: Create spec file
        create_spec_file()
        
        # Step 3: Build executable
        if not build_executable():
            print_colored("❌ Build failed", Colors.RED)
            return 1
        
        # Step 4: Create installer scripts
        create_installer_scripts()
        
        # Step 5: Create build-all script
        create_build_all_script()
        
        # Step 6: Cleanup
        cleanup()
        
        print_header("🎉 Build Complete!")
        print_colored("✅ Executable build completed successfully!", Colors.GREEN)
        print_colored("📦 Check the dist/ directory for your executable", Colors.GREEN)
        print_colored("🚀 Run the appropriate installer script to install system-wide", Colors.GREEN)
        
        return 0
        
    except Exception as e:
        print_colored(f"❌ Build failed with error: {e}", Colors.RED)
        return 1

if __name__ == "__main__":
    sys.exit(main())
