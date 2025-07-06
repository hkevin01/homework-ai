#!/bin/bash
# Scientific Machine Learning Homework Assistant
# Main launcher script

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Project directories
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$PROJECT_ROOT/src"
BIN_DIR="$PROJECT_ROOT/bin"

echo -e "${BLUE}${BOLD}🎓 Scientific Machine Learning Homework Assistant${NC}"
echo -e "${BLUE}======================================================${NC}"
echo

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python() {
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}❌ Python not found. Please install Python 3.8 or higher.${NC}"
        exit 1
    fi
    
    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    echo -e "${GREEN}✅ Found Python $PYTHON_VERSION${NC}"
    
    if $PYTHON_CMD -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
        echo -e "${GREEN}✅ Python version is compatible${NC}"
    else
        echo -e "${RED}❌ Python 3.8 or higher required. Found $PYTHON_VERSION${NC}"
        exit 1
    fi
}

# Function to check and install dependencies
check_dependencies() {
    echo -e "${YELLOW}🔍 Checking dependencies...${NC}"
    
    if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
        if $PYTHON_CMD -c "import PyQt5, numpy, matplotlib, scipy" 2>/dev/null; then
            echo -e "${GREEN}✅ All required dependencies are installed${NC}"
        else
            echo -e "${YELLOW}⚠️  Some dependencies are missing${NC}"
            read -p "Install missing dependencies? (y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo -e "${YELLOW}📦 Installing dependencies...${NC}"
                $PYTHON_CMD -m pip install -r "$PROJECT_ROOT/requirements.txt"
                echo -e "${GREEN}✅ Dependencies installed${NC}"
            else
                echo -e "${RED}❌ Cannot proceed without required dependencies${NC}"
                exit 1
            fi
        fi
    else
        echo -e "${RED}❌ requirements.txt not found${NC}"
        exit 1
    fi
}

# Function to show usage
show_usage() {
    echo -e "${BOLD}Usage:${NC}"
    echo "  ./run.sh [OPTION]"
    echo
    echo -e "${BOLD}Options:${NC}"
    echo "  gui           Launch the main GUI application (default)"
    echo "  hw1           Launch Homework 1 specific GUI"
    echo "  demo          Run a demonstration problem"
    echo "  test          Run the test suite"
    echo "  install       Install/update dependencies"
    echo "  clean         Clean temporary files"
    echo "  help          Show this help message"
    echo
    echo -e "${BOLD}Examples:${NC}"
    echo "  ./run.sh              # Launch main GUI"
    echo "  ./run.sh gui          # Launch main GUI"
    echo "  ./run.sh hw1          # Launch Homework 1 GUI"
    echo "  ./run.sh demo         # Run demonstration"
}

# Function to launch main GUI
launch_gui() {
    echo -e "${BLUE}🚀 Launching Enhanced Homework GUI...${NC}"
    cd "$PROJECT_ROOT"
    $PYTHON_CMD "$BIN_DIR/launch_enhanced_gui.py"
}

# Function to launch homework 1 GUI
launch_hw1() {
    echo -e "${BLUE}🚀 Launching Homework 1 GUI...${NC}"
    if [ -f "$SRC_DIR/homework1/enhanced_gui.py" ]; then
        cd "$SRC_DIR/homework1"
        $PYTHON_CMD enhanced_gui.py
    elif [ -f "$SRC_DIR/homework1/gui_app.py" ]; then
        cd "$SRC_DIR/homework1"
        $PYTHON_CMD gui_app.py
    else
        echo -e "${RED}❌ Homework 1 GUI not found${NC}"
        exit 1
    fi
}

# Function to run demo
run_demo() {
    echo -e "${BLUE}🧪 Running demonstration problem...${NC}"
    
    # Try homework2 problem1 first
    if [ -f "$SRC_DIR/homework2/problem1_bayesian_estimation.py" ]; then
        cd "$SRC_DIR/homework2"
        $PYTHON_CMD problem1_bayesian_estimation.py
    # Fallback to homework1 problem1
    elif [ -f "$SRC_DIR/homework1/problem1_tuberculosis_test.py" ]; then
        cd "$SRC_DIR/homework1"
        $PYTHON_CMD problem1_tuberculosis_test.py
    else
        echo -e "${RED}❌ No demonstration problems found${NC}"
        exit 1
    fi
}

# Function to run tests
run_tests() {
    echo -e "${BLUE}🧪 Running test suite...${NC}"
    cd "$PROJECT_ROOT"
    if [ -d "tests" ]; then
        $PYTHON_CMD -m pytest tests/ -v
    else
        echo -e "${RED}❌ Tests directory not found${NC}"
        exit 1
    fi
}

# Function to install dependencies
install_deps() {
    echo -e "${YELLOW}📦 Installing/updating dependencies...${NC}"
    $PYTHON_CMD -m pip install --upgrade pip
    $PYTHON_CMD -m pip install -r "$PROJECT_ROOT/requirements.txt"
    echo -e "${GREEN}✅ Dependencies updated${NC}"
}

# Function to clean temporary files
clean_temp() {
    echo -e "${YELLOW}🧹 Cleaning temporary files...${NC}"
    
    # Remove Python cache files
    find "$PROJECT_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$PROJECT_ROOT" -type f -name "*.pyc" -delete 2>/dev/null || true
    find "$PROJECT_ROOT" -type f -name "*.pyo" -delete 2>/dev/null || true
    
    # Remove pytest cache
    rm -rf "$PROJECT_ROOT/.pytest_cache" 2>/dev/null || true
    
    # Remove matplotlib cache
    rm -rf ~/.matplotlib 2>/dev/null || true
    
    echo -e "${GREEN}✅ Temporary files cleaned${NC}"
}

# Main script logic
main() {
    # Change to project directory
    cd "$PROJECT_ROOT"
    
    # Check Python
    check_python
    
    # Parse command line arguments
    case "${1:-gui}" in
        "gui"|"")
            check_dependencies
            launch_gui
            ;;
        "hw1")
            check_dependencies
            launch_hw1
            ;;
        "demo")
            check_dependencies
            run_demo
            ;;
        "test")
            check_dependencies
            run_tests
            ;;
        "install")
            install_deps
            ;;
        "clean")
            clean_temp
            ;;
        "help"|"-h"|"--help")
            show_usage
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $1${NC}"
            echo
            show_usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
