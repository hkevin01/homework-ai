# 🎓 Scientific Machine Learning Homework Assistant

A comprehensive PyQt5 application for managing and running scientific machine learning homework assignments with an intuitive graphical interface.

## ✨ Features

- 📚 **Multi-Assignment Management**: Handle multiple homework assignments in a tabbed interface
- 🧩 **Individual Problem Execution**: Run specific problems with real-time output
- 📊 **Integrated Plotting**: Built-in matplotlib visualization within the GUI
- ⚡ **Modern Interface**: Clean, responsive PyQt5 interface with proper styling
- 🔄 **Auto-Discovery**: Automatically finds and loads homework assignments
- 📈 **Progress Tracking**: Visual feedback for running processes
- 🎯 **Bayesian Methods**: Advanced probability and inference implementations

## 🏗️ Project Structure

```
homework-ai/
├── run.sh                       # 🚀 Main launcher script
├── README.md                    # 📖 This file
├── requirements.txt             # 📋 Python dependencies
├── STRUCTURE.md                 # 📁 Detailed structure guide
│
├── bin/                         # 🔧 Executable scripts
│   ├── launch_enhanced_gui.py   # Enhanced GUI launcher
│   └── launch_gui.py            # Basic GUI launcher
│
├── src/                         # 💻 Source code
│   ├── homework1/               # Homework 1: Introduction to SciML
│   │   ├── problem1_tuberculosis_test.py
│   │   ├── problem2_discrete_random_variables.py
│   │   ├── problem3_earthquake_prediction.py
│   │   ├── problem4_mechanical_failure.py
│   │   ├── enhanced_gui.py      # Enhanced GUI for HW1
│   │   └── gui_app.py          # Basic GUI for HW1
│   ├── homework2/               # Homework 2: Bayesian Methods
│   │   ├── problem1_bayesian_estimation.py
│   │   ├── metadata.json       # Assignment metadata
│   │   └── README.md           # Assignment description
│   ├── main_gui.py             # Main enhanced GUI application
│   ├── homework_manager.py     # Assignment management logic
│   └── assignment_widget.py    # Individual assignment widgets
│
├── docs/                        # 📚 Documentation and PDFs
│   └── homework/               # Homework assignment PDFs
├── tests/                       # 🧪 Test suite
├── config/                      # ⚙️ Configuration files
├── tools/                       # 🛠️ Development tools
└── scripts/                     # 📜 Utility scripts
```

See [STRUCTURE.md](STRUCTURE.md) for detailed organization information.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd homework-ai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 🖥️ Running the Application

#### Option 1: Main Launcher (Recommended)
```bash
# Make the script executable (first time only)
chmod +x run.sh

# Launch the application
./run.sh                    # Main GUI (default)
./run.sh gui                # Main GUI (explicit)
./run.sh hw1                # Homework 1 specific GUI
./run.sh hw2                # Homework 2 specific GUI
./run.sh demo               # Run demonstration
./run.sh test               # Run test suite
./run.sh install            # Install/update dependencies
./run.sh build              # Build standalone executable
./run.sh clean              # Clean temporary files
./run.sh status             # Show project status
./run.sh help               # Show help
```

#### Option 2: Direct Script Execution
```bash
# Enhanced GUI launcher
python bin/launch_enhanced_gui.py

# Basic GUI launcher
python bin/launch_gui.py

# Direct GUI launch
cd src && python main_gui.py
```

#### Option 3: Individual Homework GUIs
```bash
# For Homework 1
cd src/homework1
python enhanced_gui.py

# Or basic GUI
python gui_app.py
```

## 📚 Available Assignments

### Homework 1: Introduction to Scientific Machine Learning
- **Problem 1**: Tuberculosis Test Analysis (Bayes' Theorem)
- **Problem 2**: Discrete Random Variables
- **Problem 3**: Earthquake Prediction (Probability Models)
- **Problem 4**: Mechanical Failure Analysis

### Homework 2: Advanced Probability and Bayesian Methods
- **Problem 1**: Bayesian Parameter Estimation
- **Problem 2**: Markov Chain Monte Carlo (MCMC)
- **Problem 3**: Gaussian Processes
- **Problem 4**: Variational Inference

## 🎯 Usage Guide

### Main Interface
1. **Overview Tab**: View all available assignments
2. **Assignment Tabs**: Individual assignment interfaces
3. **Problem Execution**: Click "Run Problem" to execute individual problems
4. **Real-time Output**: See results and plots immediately
5. **File Management**: Access assignment files and documentation

### Features in Detail

#### 📊 Visualization
- Integrated matplotlib plots appear directly in the GUI
- Multiple figure tabs for complex visualizations
- Interactive plot controls

#### 🔄 Problem Execution
- Background thread execution prevents GUI freezing
- Real-time output streaming
- Error handling and reporting
- Stop/restart capabilities

#### 📁 Assignment Management
- Automatic discovery of homework folders
- Metadata-driven assignment information
- Extensible structure for new assignments

## 🛠️ Development

### Adding New Assignments

1. **Create assignment folder:**
   ```bash
   mkdir src/homework3
   ```

2. **Add metadata.json:**
   ```json
   {
     "title": "Your Assignment Title",
     "description": "Assignment description",
     "topics": ["Topic 1", "Topic 2"],
     "status": "Available"
   }
   ```

3. **Create problem files:**
   ```bash
   touch src/homework3/problem1_your_problem.py
   ```

4. **Add README.md** with assignment details

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_homework1_problems.py
```

### Code Quality
```bash
# Format code
black src/

# Check style
flake8 src/
```

## 📋 Dependencies

### Core Requirements
- **PyQt5**: GUI framework
- **numpy**: Numerical computing
- **matplotlib**: Plotting and visualization
- **scipy**: Scientific computing

### Advanced Features
- **pandas**: Data manipulation
- **scikit-learn**: Machine learning
- **pymc**: Bayesian modeling
- **emcee**: MCMC sampling

See `requirements.txt` for complete list with versions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-assignment`)
3. Commit your changes (`git commit -am 'Add new assignment'`)
4. Push to the branch (`git push origin feature/new-assignment`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

1. **PyQt5 Installation Problems:**
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install python3-pyqt5
   
   # On macOS with Homebrew
   brew install pyqt5
   ```

2. **Missing Dependencies:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **GUI Won't Start:**
   - Check Python version (3.8+ required)
   - Verify PyQt5 installation
   - Try the simple launcher: `python launch_gui.py`

### Getting Help

- Check the [Issues](https://github.com/your-repo/issues) page
- Review the documentation in `docs/`
- Run individual problems directly for debugging

---

**Happy Learning! 🎓📚** 