#!/usr/bin/env python3
"""
Simple test script to verify the GUI execute functionality
"""

import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

def test_problem_execution():
    """Test that problem files can be executed directly."""
    print("🧪 Testing problem execution...")
    
    # Test homework1 problem1
    hw1_dir = src_dir / "homework1"
    problem1_file = hw1_dir / "problem1_tuberculosis_test.py"
    
    if problem1_file.exists():
        print(f"✅ Found test file: {problem1_file}")
        
        # Try to execute it
        try:
            original_cwd = os.getcwd()
            os.chdir(hw1_dir)
            
            import subprocess
            result = subprocess.run(
                [sys.executable, "problem1_tuberculosis_test.py"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            os.chdir(original_cwd)
            
            if result.returncode == 0:
                print("✅ Problem executed successfully!")
                print("Output preview:")
                print(result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout)
                return True
            else:
                print(f"❌ Problem execution failed with code {result.returncode}")
                print("Error:", result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print("⚠️  Problem execution timed out")
            return False
        except Exception as e:
            print(f"❌ Error executing problem: {e}")
            return False
    else:
        print(f"❌ Test file not found: {problem1_file}")
        return False

def test_gui_imports():
    """Test that GUI components can be imported."""
    print("🧪 Testing GUI imports...")
    
    try:
        from PyQt5.QtCore import QThread
        from assignment_widget import ProblemRunner
        print("✅ PyQt5 and custom widgets imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 GUI Execute Functionality Test")
    print("=" * 40)
    
    success = True
    
    # Test imports
    success &= test_gui_imports()
    
    # Test problem execution
    success &= test_problem_execution()
    
    if success:
        print("\n✅ All tests passed! Execute functionality should work.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        sys.exit(1)
