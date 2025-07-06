#!/usr/bin/env python3
"""
Simple Launcher for Homework GUI

This script provides a simple way to launch the homework GUI application
with proper error handling and fallback options.
"""

import os
import sys
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent
project_root = current_dir.parent
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

def check_dependencies():
    """Check if required dependencies are installed."""
    missing = []
    
    try:
        import PyQt5
    except ImportError:
        missing.append("PyQt5")
    
    try:
        import numpy
    except ImportError:
        missing.append("numpy")
    
    try:
        import matplotlib
    except ImportError:
        missing.append("matplotlib")
    
    try:
        import scipy
    except ImportError:
        missing.append("scipy")
    
    return missing

def launch_enhanced_gui():
    """Try to launch the enhanced GUI."""
    try:
        from enhanced_homework_gui import main
        return main()
    except Exception as e:
        print(f"Failed to launch enhanced GUI: {e}")
        return None

def launch_homework1_gui():
    """Fallback to homework1 GUI."""
    try:
        # Change to homework1 directory
        hw1_dir = src_dir / "homework1"
        if hw1_dir.exists():
            os.chdir(hw1_dir)
            sys.path.insert(0, str(hw1_dir))
            
            # Try enhanced GUI first
            try:
                from enhanced_gui import main
                return main()
            except:
                # Fall back to simple GUI
                from gui_app import main
                return main()
    except Exception as e:
        print(f"Failed to launch homework1 GUI: {e}")
        return None

def main():
    """Main launcher function."""
    print("🎓 Scientific Machine Learning Homework Assistant")
    print("=" * 50)
    
    # Check dependencies
    missing_deps = check_dependencies()
    if missing_deps:
        print("❌ Missing required dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\nPlease install missing dependencies:")
        print("pip install -r requirements.txt")
        return 1
    
    print("✅ All dependencies found")
    print("🚀 Launching GUI application...")
    
    # Try to launch enhanced GUI first
    result = launch_enhanced_gui()
    if result is not None:
        return result
    
    print("⚠️  Enhanced GUI failed, trying homework1 GUI...")
    result = launch_homework1_gui()
    if result is not None:
        return result
    
    # If all else fails, run a simple problem
    print("⚠️  GUI launch failed, running simple demonstration...")
    try:
        # Run homework1 problem1 as demonstration
        hw1_dir = src_dir / "homework1"
        if hw1_dir.exists():
            problem_file = hw1_dir / "problem1_tuberculosis_test.py"
            if problem_file.exists():
                print(f"Running {problem_file}...")
                os.chdir(hw1_dir)
                exec(open(problem_file).read())
                return 0
    except Exception as e:
        print(f"Failed to run demonstration: {e}")
    
    print("❌ Could not launch any GUI or demonstration")
    print("Please check the installation and try again.")
    return 1

if __name__ == "__main__":
    sys.exit(main())
