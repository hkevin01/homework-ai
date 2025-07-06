# 🎓 Scientific Machine Learning Homework Assistant

A comprehensive PyQt5 desktop application for managing and executing scientific machine learning homework assignments with interactive problem solving, visualization, and standalone executable generation.

## ✨ Key Features

- 📚 **Multi-Assignment Management**: Tabbed interface for multiple homework sets
- 🧩 **Interactive Problem Solving**: Run individual problems with real-time output
- 📊 **Integrated Visualizations**: Built-in matplotlib plotting within the GUI
- ⚡ **Modern Interface**: Clean, responsive PyQt5 design with professional styling
- 🔄 **Auto-Discovery**: Automatically detects and loads homework assignments
- 🏗️ **Executable Building**: Create standalone .exe/.binary files for distribution
- 📈 **Progress Tracking**: Visual feedback and status reporting
- 🎯 **Educational Focus**: Detailed explanations and learning objectives

## 🚀 Quick Start

```bash
# Clone and run
git clone https://github.com/hkevin01/homework-ai.git
cd homework-ai
./run.sh
```

## 📦 One-Command Operations

- `./run.sh` - Launch main GUI
- `./run.sh build` - Create standalone executable
- `./run.sh demo` - Run demonstration
- `./run.sh test` - Run test suite
- `./run.sh status` - Show project info

## 🏗️ Build Executables

### Linux/macOS
```bash
./run.sh build
```

### Windows
```cmd
build_windows.bat
```

Creates standalone executables that run without Python installed!

## 📚 Current Assignments

### Homework 1: Introduction to Scientific ML
- **Problem 1**: Tuberculosis Test Analysis (Bayes' Theorem)
- **Problem 2**: Discrete Random Variables
- **Problem 3**: Earthquake Prediction Models
- **Problem 4**: Mechanical Failure Analysis

### Homework 2: Advanced Probability & Bayesian Methods
- **Problem 1**: Bayesian Parameter Estimation
- More problems coming soon...

## 🔧 Technical Stack

- **GUI Framework**: PyQt5
- **Scientific Computing**: NumPy, SciPy, Matplotlib
- **Build System**: PyInstaller for cross-platform executables
- **Architecture**: Modular design with homework manager and assignment widgets

## 📁 Project Structure

```
homework-ai/
├── run.sh                    # 🚀 Main launcher
├── build_windows.bat         # 🪟 Windows build script
├── BUILD_GUIDE.md           # 📖 Complete build documentation
│
├── src/                     # 💻 Source code
│   ├── main_gui.py          # Main application
│   ├── homework_manager.py  # Assignment management
│   ├── assignment_widget.py # UI components
│   └── homework*/           # Assignment implementations
│
├── bin/                     # 🔧 Launcher scripts
├── docs/                    # 📚 Documentation & PDFs
├── tests/                   # 🧪 Test suite
└── config/                  # ⚙️ Configuration files
```

## 🎯 Features in Detail

### Interactive Problem Execution
- Execute individual homework problems
- Real-time output capture and display
- Interactive parameter adjustment
- Integrated matplotlib plotting

### Professional GUI
- Modern tabbed interface
- Assignment overview with detailed descriptions
- Problem-specific execution environments
- Status tracking and progress indicators

### Educational Enhancement
- Detailed problem descriptions and learning objectives
- Step-by-step solution explanations
- Source code viewing and analysis
- Theory integration with practical implementation

### Cross-Platform Distribution
- Linux, Windows, macOS support
- Standalone executable generation
- No Python installation required for end users
- Professional application packaging

## 🔬 Scientific Applications

This tool is designed for educational environments teaching:
- **Probabilistic Machine Learning**
- **Bayesian Inference**
- **Statistical Modeling**
- **Scientific Computing with Python**
- **Data Analysis and Visualization**

## 📈 Development Status

- ✅ Core GUI framework
- ✅ Assignment management system
- ✅ Problem execution engine
- ✅ Build system for executables
- ✅ Comprehensive documentation
- 🔄 Additional homework assignments (ongoing)
- 🔄 Advanced visualization features (planned)

## 🤝 Contributing

This is an educational project. Feel free to:
- Add new homework assignments
- Improve the GUI interface
- Enhance problem implementations
- Add new scientific computing examples

## 📄 License

Educational use - See LICENSE file for details.

---

**Built with ❤️ for scientific education and machine learning exploration**
