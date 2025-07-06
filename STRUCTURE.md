# 📁 Project Structure

This document describes the organized structure of the Scientific Machine Learning Homework Assistant project.

## 🏗️ Directory Organization

```
homework-ai/                     # 📦 Root directory
├── run.sh                       # 🚀 Main launcher script
├── README.md                    # 📖 Project documentation
├── requirements.txt             # 📋 Python dependencies
├── PROJECT_SUMMARY.md           # 📊 Project accomplishments
├── CHANGELOG.md                 # 📝 Version history
├── .gitignore                   # 🚫 Git ignore rules
│
├── bin/                         # 🔧 Executable scripts
│   ├── launch_enhanced_gui.py   # Enhanced GUI launcher
│   ├── launch_gui.py            # Basic GUI launcher
│   └── simple_gui.py            # Simple GUI fallback
│
├── src/                         # 💻 Source code
│   ├── main_gui.py              # Main application
│   ├── homework_manager.py      # Assignment management
│   ├── assignment_widget.py     # Assignment UI components
│   ├── enhanced_homework_gui.py # Enhanced main GUI
│   │
│   ├── homework1/               # 📚 Assignment 1
│   │   ├── problem1_tuberculosis_test.py
│   │   ├── problem2_discrete_random_variables.py
│   │   ├── problem3_earthquake_prediction.py
│   │   ├── problem4_mechanical_failure.py
│   │   ├── enhanced_gui.py      # HW1-specific GUI
│   │   ├── gui_app.py           # HW1 basic GUI
│   │   ├── metadata.json        # Assignment metadata
│   │   └── README.md            # Assignment description
│   │
│   └── homework2/               # 📚 Assignment 2
│       ├── problem1_bayesian_estimation.py
│       ├── metadata.json
│       └── README.md
│
├── tests/                       # 🧪 Test suite
│   ├── test_homework1_problems.py
│   ├── test_gui_functionality.py
│   └── run_comprehensive_tests.py
│
├── docs/                        # 📚 Documentation
│   ├── index.md                 # Documentation index
│   ├── homework/                # Assignment PDFs
│   └── lectures/                # Lecture materials
│
├── config/                      # ⚙️ Configuration files
│   ├── .editorconfig            # Editor configuration
│   ├── .prettierrc              # Code formatting
│   └── .cursorrules             # Cursor AI rules
│
├── tools/                       # 🛠️ Development tools
│   ├── run_enhanced_gui.sh      # Legacy shell script
│   └── run_gui.sh               # Legacy shell script
│
├── scripts/                     # 📜 Utility scripts
│   └── README.md                # Scripts documentation
│
├── assignments/                 # 📋 Assignment templates
│   └── README.md                # Assignment guidelines
│
├── .github/                     # 🐙 GitHub configuration
│   └── workflows/               # CI/CD workflows
│
├── .copilot/                    # 🤖 AI assistant config
│
└── poeopenaiwrapper/            # 🔌 External wrapper
    └── [external project files]
```

## 🚀 Quick Start

### Main Launcher (Recommended)
```bash
./run.sh                    # Launch main GUI
./run.sh gui                # Launch main GUI (explicit)
./run.sh hw1                # Launch Homework 1 GUI
./run.sh demo               # Run demonstration
./run.sh test               # Run tests
./run.sh install            # Install dependencies
./run.sh clean              # Clean temp files
./run.sh help               # Show help
```

### Direct Execution
```bash
# Enhanced GUI
python bin/launch_enhanced_gui.py

# Basic GUI
python bin/launch_gui.py

# Specific homework
cd src/homework1 && python enhanced_gui.py
```

## 📁 File Organization Logic

### `/bin/` - Executables
- Contains all launcher scripts and executable Python files
- Scripts that users run directly to start the application

### `/src/` - Source Code
- Core application code organized by functionality
- Each homework assignment has its own subdirectory
- Shared components (GUI framework, managers) at root level

### `/config/` - Configuration
- Editor and development tool configurations
- Keeps the root directory clean of dotfiles

### `/tools/` - Development Tools
- Utility scripts for development and maintenance
- Legacy scripts and development helpers

### `/tests/` - Test Suite
- Unit tests, integration tests, and test utilities
- Organized to mirror the src/ structure

### `/docs/` - Documentation
- User guides, API documentation, and reference materials
- Assignment PDFs and lecture materials

## 🎯 Benefits of This Structure

### ✅ Clean Root Directory
- Only essential files at the root level
- Easy to understand project overview
- Professional appearance

### ✅ Logical Organization
- Related files grouped together
- Clear separation of concerns
- Easy navigation and maintenance

### ✅ Scalable Design
- Easy to add new homework assignments
- Simple to extend with new tools
- Maintainable as project grows

### ✅ Development Friendly
- Clear separation of code and configuration
- Organized test structure
- Consistent naming conventions

## 🔧 Maintenance Guidelines

### Adding New Assignments
1. Create `src/homeworkN/` directory
2. Add problem files following naming convention
3. Create `metadata.json` and `README.md`
4. Update main documentation

### Adding New Tools
1. Place executable scripts in `bin/`
2. Place development tools in `tools/`
3. Update the main `run.sh` script if needed

### Configuration Changes
1. Keep configuration files in `config/`
2. Create symlinks if tools expect files at root
3. Document any special requirements

This structure provides a professional, maintainable, and user-friendly organization for the Scientific Machine Learning Homework Assistant project.
