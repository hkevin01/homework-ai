#!/usr/bin/env python3
"""
Simple GUI Test Runner

This script runs basic tests on the Homework 1 GUI application
to verify functionality without complex Qt threading issues.
"""

import os
import subprocess
import sys
import time


def test_gui_launch():
    """Test that the GUI can be launched without errors."""
    print("🧪 Testing GUI Launch...")
    
    try:
        # Try to launch the GUI in a subprocess
        process = subprocess.Popen(
            [sys.executable, "src/homework1/gui_app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a few seconds for the GUI to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ GUI launched successfully")
            # Terminate the process
            process.terminate()
            process.wait(timeout=5)
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ GUI failed to launch")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing GUI launch: {e}")
        return False

def test_problem_files():
    """Test that all problem files exist and are valid Python."""
    print("🧪 Testing Problem Files...")
    
    problem_files = [
        'src/homework1/problem1_tuberculosis_test.py',
        'src/homework1/problem2_discrete_random_variables.py',
        'src/homework1/problem3_earthquake_prediction.py',
        'src/homework1/problem4_mechanical_failure.py'
    ]
    
    all_valid = True
    
    for file_path in problem_files:
        if not os.path.exists(file_path):
            print(f"❌ Problem file not found: {file_path}")
            all_valid = False
            continue
            
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                compile(content, file_path, 'exec')
            print(f"✅ {file_path} - Valid Python")
        except SyntaxError as e:
            print(f"❌ {file_path} - Syntax error: {e}")
            all_valid = False
        except Exception as e:
            print(f"❌ {file_path} - Error: {e}")
            all_valid = False
    
    return all_valid

def test_individual_problems():
    """Test that individual problems can run without the GUI."""
    print("🧪 Testing Individual Problems...")
    
    problem_files = [
        'problem1_tuberculosis_test.py',
        'problem2_discrete_random_variables.py',
        'problem3_earthquake_prediction.py',
        'problem4_mechanical_failure.py'
    ]
    
    all_successful = True
    
    for problem_file in problem_files:
        try:
            print(f"Testing {problem_file}...")
            result = subprocess.run(
                [sys.executable, problem_file],
                cwd='src/homework1',
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"✅ {problem_file} - Ran successfully")
                if result.stdout.strip():
                    print(f"   Output: {result.stdout.strip()[:100]}...")
            else:
                print(f"❌ {problem_file} - Failed with return code {result.returncode}")
                print(f"   Error: {result.stderr}")
                all_successful = False
                
        except subprocess.TimeoutExpired:
            print(f"❌ {problem_file} - Timed out")
            all_successful = False
        except Exception as e:
            print(f"❌ {problem_file} - Error: {e}")
            all_successful = False
    
    return all_successful

def test_dependencies():
    """Test that all required dependencies are available."""
    print("🧪 Testing Dependencies...")
    
    required_modules = [
        'PyQt5',
        'numpy',
        'scipy',
        'matplotlib'
    ]
    
    all_available = True
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} - Available")
        except ImportError:
            print(f"❌ {module} - Not available")
            all_available = False
    
    return all_available

def main():
    """Run all tests."""
    print("🚀 Starting Homework 1 GUI Tests")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Problem Files", test_problem_files),
        ("Individual Problems", test_individual_problems),
        ("GUI Launch", test_gui_launch)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! GUI should work correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 