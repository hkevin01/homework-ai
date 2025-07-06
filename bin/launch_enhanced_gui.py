#!/usr/bin/env python3
"""
Enhanced Homework GUI Launcher

This script launches the enhanced homework GUI with detailed problem explanations,
solutions, and interactive execution capabilities.
"""

import os
import sys
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent
project_root = current_dir.parent
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

def check_and_install_dependencies():
    """Check and optionally install required dependencies."""
    required_packages = {
        'PyQt5': 'PyQt5>=5.15.0',
        'numpy': 'numpy>=1.21.0',
        'matplotlib': 'matplotlib>=3.5.0',
        'scipy': 'scipy>=1.7.0'
    }
    
    missing = []
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
        except ImportError:
            missing.append(pip_name)
    
    if missing:
        print("❌ Missing required dependencies:")
        for dep in missing:
            print(f"   - {dep}")
        
        response = input("\nWould you like to install missing dependencies? (y/n): ")
        if response.lower() in ['y', 'yes']:
            import subprocess
            try:
                cmd = [sys.executable, '-m', 'pip', 'install'] + missing
                subprocess.check_call(cmd)
                print("✅ Dependencies installed successfully!")
                return True
            except subprocess.CalledProcessError:
                print("❌ Failed to install dependencies automatically.")
                print("Please run: pip install -r requirements.txt")
                return False
        else:
            print("Please install missing dependencies manually:")
            print("pip install -r requirements.txt")
            return False
    
    return True

def launch_enhanced_gui():
    """Launch the enhanced homework GUI."""
    try:
        # Import and configure PyQt5
        from PyQt5.QtCore import Qt
        from PyQt5.QtWidgets import QApplication

        # Set high DPI settings for better display
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        
        # Import the main application
        from main_gui import MainApplication

        # Create and show the main window
        window = MainApplication()
        window.show()
        
        print("🚀 Enhanced Homework GUI launched successfully!")
        print("📚 Navigate through assignments and explore problems in detail.")
        
        return app.exec_()
        
    except Exception as e:
        print(f"❌ Failed to launch enhanced GUI: {e}")
        return None

def launch_homework1_gui():
    """Fallback to homework1 specific GUI."""
    try:
        hw1_dir = src_dir / "homework1"
        if hw1_dir.exists():
            original_cwd = os.getcwd()
            os.chdir(hw1_dir)
            sys.path.insert(0, str(hw1_dir))
            
            try:
                from enhanced_gui import main
                print("🚀 Launching Homework 1 Enhanced GUI...")
                result = main()
                os.chdir(original_cwd)
                return result
            except ImportError:
                try:
                    from gui_app import main
                    print("🚀 Launching Homework 1 Basic GUI...")
                    result = main()
                    os.chdir(original_cwd)
                    return result
                except ImportError:
                    os.chdir(original_cwd)
                    return None
    except Exception as e:
        print(f"❌ Failed to launch homework1 GUI: {e}")
        return None

def run_demo_problem():
    """Run a demonstration problem if GUIs fail."""
    try:
        print("🧪 Running demonstration problem...")
        
        # Try to run homework2 problem1 (Bayesian estimation)
        hw2_dir = src_dir / "homework2"
        problem_file = hw2_dir / "problem1_bayesian_estimation.py"
        
        if problem_file.exists():
            print(f"Running: {problem_file}")
            os.chdir(hw2_dir)
            
            # Import and run the problem
            sys.path.insert(0, str(hw2_dir))
            
            # Execute the problem file
            with open(problem_file, 'r') as f:
                code = f.read()
            
            # Create a safe execution environment
            exec_globals = {
                '__file__': str(problem_file),
                '__name__': '__main__'
            }
            
            exec(code, exec_globals)
            return 0
            
        else:
            # Fallback to homework1 problem
            hw1_dir = src_dir / "homework1"
            problem_file = hw1_dir / "problem1_tuberculosis_test.py"
            
            if problem_file.exists():
                print(f"Running: {problem_file}")
                os.chdir(hw1_dir)
                
                with open(problem_file, 'r') as f:
                    code = f.read()
                
                exec_globals = {
                    '__file__': str(problem_file),
                    '__name__': '__main__'
                }
                
                exec(code, exec_globals)
                return 0
    
    except Exception as e:
        print(f"❌ Demo problem failed: {e}")
        return 1

def print_welcome():
    """Print welcome message and usage instructions."""
    print("🎓" + "="*60 + "🎓")
    print("    Scientific Machine Learning Homework Assistant")
    print("         Enhanced PyQt5 GUI with Detailed Explanations")
    print("🎓" + "="*60 + "🎓")
    print()
    print("✨ Features:")
    print("   📚 Multi-assignment management with tabbed interface")
    print("   🧩 Detailed problem descriptions and solutions")
    print("   ⚡ Interactive problem execution with live output")
    print("   📊 Integrated matplotlib visualizations")
    print("   💡 Step-by-step solution explanations")
    print("   🔍 Source code viewing and analysis")
    print()

def main():
    """Main launcher function."""
    print_welcome()
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_and_install_dependencies():
        print("\n❌ Cannot proceed without required dependencies.")
        return 1
    
    print("✅ All dependencies available")
    print()
    
    # Try to launch enhanced GUI
    print("🚀 Launching Enhanced Homework GUI...")
    result = launch_enhanced_gui()
    if result is not None:
        return result
    
    print("⚠️  Enhanced GUI failed, trying Homework 1 GUI...")
    result = launch_homework1_gui()
    if result is not None:
        return result
    
    print("⚠️  GUI launch failed, running demonstration...")
    return run_demo_problem()

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for using the Homework Assistant!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
