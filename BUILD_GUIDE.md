# 🏗️ Building Standalone Executables

This guide explains how to create standalone executables for the Scientific Machine Learning Homework Assistant that can run without Python being installed on the target system.

## 🚀 Quick Build

### Linux/macOS
```bash
./run.sh build
```

### Windows
```cmd
build_windows.bat
```

## 📋 Requirements

- Python 3.8 or higher
- All project dependencies installed (`./run.sh install`)
- PyInstaller (automatically installed during build)

## 🖥️ Platform-Specific Instructions

### 🐧 Linux

#### Option 1: Using run.sh (Recommended)
```bash
# Build executable
./run.sh build

# The executable will be created at:
# dist/homework-ai
```

#### Option 2: Manual PyInstaller
```bash
# Install PyInstaller
pip install PyInstaller

# Build executable
pyinstaller --onefile --windowed \
    --name homework-ai \
    --add-data "src/homework1:homework1" \
    --add-data "src/homework2:homework2" \
    --hidden-import PyQt5.QtCore \
    --hidden-import PyQt5.QtGui \
    --hidden-import PyQt5.QtWidgets \
    --hidden-import matplotlib.backends.backend_qt5agg \
    src/main_gui.py
```

### 🪟 Windows

#### Option 1: Using batch script (Recommended)
```cmd
REM Double-click or run from command prompt
build_windows.bat
```

#### Option 2: Manual PyInstaller
```cmd
REM Install PyInstaller
python -m pip install PyInstaller

REM Build executable
python -m PyInstaller --onefile --windowed ^
    --name homework-ai ^
    --add-data "src\homework1;homework1" ^
    --add-data "src\homework2;homework2" ^
    --hidden-import PyQt5.QtCore ^
    --hidden-import PyQt5.QtGui ^
    --hidden-import PyQt5.QtWidgets ^
    --hidden-import matplotlib.backends.backend_qt5agg ^
    src\main_gui.py
```

### 🍎 macOS

#### Using run.sh
```bash
# Build executable
./run.sh build

# The executable will be created at:
# dist/homework-ai
```

#### Creating .app Bundle (Optional)
```bash
# After building with PyInstaller, create app bundle
mkdir -p "Scientific ML Homework Assistant.app/Contents/MacOS"
mkdir -p "Scientific ML Homework Assistant.app/Contents/Resources"

# Copy executable
cp dist/homework-ai "Scientific ML Homework Assistant.app/Contents/MacOS/"

# Create Info.plist
cat > "Scientific ML Homework Assistant.app/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>homework-ai</string>
    <key>CFBundleIdentifier</key>
    <string>com.homeworkai.sciml</string>
    <key>CFBundleName</key>
    <string>Scientific ML Homework Assistant</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
</dict>
</plist>
EOF
```

## 📦 Output

After building, you'll find:

- **Linux/macOS**: `dist/homework-ai` (executable binary)
- **Windows**: `dist/homework-ai.exe` (executable)

### 📏 Expected Sizes
- **Linux**: ~80-120 MB
- **Windows**: ~90-130 MB  
- **macOS**: ~85-125 MB

*Size varies based on included dependencies and Python version*

## 🚀 Distribution

### Making it Portable

1. **Copy the executable** to any location
2. **No Python required** on target machines
3. **All dependencies included** in the executable

### Installation Options

#### Linux
```bash
# Copy to user bin directory
cp dist/homework-ai ~/.local/bin/

# Or system-wide (requires sudo)
sudo cp dist/homework-ai /usr/local/bin/

# Create desktop entry
cat > ~/.local/share/applications/homework-ai.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Scientific ML Homework Assistant
Comment=Scientific Machine Learning Homework Assistant
Exec=homework-ai
Icon=homework-ai
Terminal=false
Categories=Education;Science;
EOF
```

#### Windows
```cmd
REM Copy to a permanent location
copy dist\homework-ai.exe "C:\Program Files\HomeworkAI\"

REM Create desktop shortcut (manually or via script)
```

## 🐛 Troubleshooting

### Common Issues

#### Missing Dependencies
```bash
# Add missing imports to the build command
--hidden-import package_name
```

#### Large Executable Size
```bash
# Use --exclude-module to remove unused packages
--exclude-module tkinter
--exclude-module test
```

#### GUI Not Showing (Windows)
- Ensure `--windowed` flag is used
- For debugging, temporarily remove `--windowed` to see console output

#### Import Errors
- Add problematic modules to `--hidden-import`
- Check if all data files are included with `--add-data`

### 🔍 Debugging

#### Console Mode (for debugging)
```bash
# Remove --windowed to see error messages
pyinstaller --onefile \
    --name homework-ai-debug \
    src/main_gui.py
```

#### Verbose Output
```bash
# Add debugging flags
pyinstaller --onefile --windowed \
    --debug all \
    --log-level DEBUG \
    src/main_gui.py
```

## ✅ Testing

### Basic Test
```bash
# Run the executable
./dist/homework-ai          # Linux/macOS
dist\homework-ai.exe         # Windows
```

### Full Test
1. Copy executable to a different machine
2. Ensure target machine doesn't have Python
3. Run executable and test all features:
   - GUI launches correctly
   - Assignments load
   - Problems execute
   - Plots display correctly

## 📋 Build Script Options

The integrated build system supports several options:

```bash
./run.sh build              # Standard build
./run.sh build --debug      # Debug build (future feature)
./run.sh build --clean      # Clean build (future feature)
```

## 🎯 Advanced Customization

### Custom Icons
```bash
# Add icon to build (Windows)
--icon=assets/icon.ico

# Add icon to build (Linux/macOS)
--icon=assets/icon.png
```

### Custom Build Scripts
You can modify the build parameters by editing:
- `run.sh` (Linux/macOS)
- `build_windows.bat` (Windows)

### Multiple Versions
```bash
# Build different variants
pyinstaller --onefile --name homework-ai-lite src/main_gui.py  # Minimal
pyinstaller --onefile --name homework-ai-full src/main_gui.py  # Full featured
```

---

## 📞 Support

If you encounter issues building executables:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Ensure all dependencies are installed
3. Try building in a clean Python environment
4. Check PyInstaller documentation for platform-specific issues

**Happy Building!** 🚀
