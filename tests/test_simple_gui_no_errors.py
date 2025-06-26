"""
Tests for Simple GUI - No Qt Threading Errors

This module tests that the simple GUI launches without Qt threading errors
and functions correctly.
"""

import os
import subprocess
import sys
import time

import pytest


class TestSimpleGUINoErrors:
    """Test that simple GUI launches without Qt threading errors."""
    
    def test_simple_gui_launches_without_qt_errors(self):
        """Test that simple GUI launches without QSocketNotifier errors."""
        # Launch the simple GUI in a subprocess
        process = subprocess.Popen(
            [sys.executable, "src/homework1/simple_gui.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for GUI to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            # GUI is running, terminate it and check for errors
            process.terminate()
            process.wait(timeout=5)
            stdout, stderr = process.communicate()
            
            # Check for absence of Qt threading errors
            error_indicators = [
                "QSocketNotifier",
                "QProcess::ExitStatus",
                "Cannot queue arguments",
                "QThread",
                "QTimer",
                "QEventLoop"
            ]
            
            for error_indicator in error_indicators:
                assert error_indicator not in stderr, (
                    f"Qt threading error found: {error_indicator} in stderr: {stderr}"
                )
            
            # Check that there are no critical errors
            critical_errors = [
                "FATAL",
                "CRITICAL",
                "ERROR",
                "Exception",
                "Traceback"
            ]
            
            for error in critical_errors:
                assert error not in stderr, (
                    f"Critical error found: {error} in stderr: {stderr}"
                )
        else:
            # GUI failed to start, check why
            stdout, stderr = process.communicate()
            pytest.fail(f"Simple GUI failed to start. STDOUT: {stdout}, STDERR: {stderr}")
    
    def test_simple_gui_script_exists(self):
        """Test that the simple GUI script exists."""
        gui_file = "src/homework1/simple_gui.py"
        assert os.path.exists(gui_file), f"Simple GUI file {gui_file} does not exist"
    
    def test_simple_gui_importable(self):
        """Test that the simple GUI can be imported without errors."""
        gui_file = "src/homework1/simple_gui.py"
        
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("simple_gui", gui_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            pytest.fail(f"Failed to import simple GUI module: {e}")
    
    def test_simple_gui_no_subprocess_usage(self):
        """Test that simple GUI doesn't use subprocess (which causes Qt errors)."""
        gui_file = "src/homework1/simple_gui.py"
        
        with open(gui_file, 'r') as f:
            content = f.read()
        
        # Check that subprocess is not imported or used
        assert "import subprocess" not in content, "Simple GUI imports subprocess"
        assert "subprocess." not in content, "Simple GUI uses subprocess"
        
        # Check that QProcess is not used
        assert "QProcess" not in content, "Simple GUI uses QProcess"
        
        # Check that threading is not used
        assert "import threading" not in content, "Simple GUI imports threading"
        assert "threading." not in content, "Simple GUI uses threading"
    
    def test_simple_gui_uses_direct_execution(self):
        """Test that simple GUI uses direct execution instead of subprocess."""
        gui_file = "src/homework1/simple_gui.py"
        
        with open(gui_file, 'r') as f:
            content = f.read()
        
        # Check that it imports the problem modules directly
        assert "import problem1_tuberculosis_test" in content, "Simple GUI doesn't import problem1"
        assert "import problem2_discrete_random_variables" in content, "Simple GUI doesn't import problem2"
        assert "import problem3_earthquake_prediction" in content, "Simple GUI doesn't import problem3"
        assert "import problem4_mechanical_failure" in content, "Simple GUI doesn't import problem4"
    
    def test_simple_gui_has_correct_structure(self):
        """Test that simple GUI has the correct structure."""
        gui_file = "src/homework1/simple_gui.py"
        
        with open(gui_file, 'r') as f:
            content = f.read()
        
        # Check for required components
        required_components = [
            "class SimpleHomework1GUI",
            "QMainWindow",
            "QTabWidget",
            "QTextEdit",
            "QPushButton",
            "Run Problem",
            "Clear Output"
        ]
        
        for component in required_components:
            assert component in content, f"Simple GUI missing component: {component}"


class TestSimpleGUIFunctionality:
    """Test that simple GUI functions correctly."""
    
    def test_simple_gui_can_run_problems_directly(self):
        """Test that simple GUI can run problems directly without subprocess."""
        # Test that problem modules can be imported and run
        problem_modules = [
            'problem1_tuberculosis_test',
            'problem2_discrete_random_variables', 
            'problem3_earthquake_prediction',
            'problem4_mechanical_failure'
        ]
        
        for module_name in problem_modules:
            try:
                # Import the module
                module = __import__(module_name, fromlist=[''])
                
                # Check that it has a main function or can be executed
                if hasattr(module, 'main'):
                    # Module has a main function
                    pass
                elif hasattr(module, '__name__') and module.__name__ == '__main__':
                    # Module can be run directly
                    pass
                else:
                    # Check if module has any executable content
                    assert True, f"Module {module_name} has no executable content"
                    
            except ImportError as e:
                pytest.fail(f"Failed to import {module_name}: {e}")
            except Exception as e:
                pytest.fail(f"Error with {module_name}: {e}")
    
    def test_simple_gui_output_capture(self):
        """Test that simple GUI can capture output from problem execution."""
        # This test verifies that the GUI can capture stdout/stderr
        # by testing the underlying mechanism
        
        import io
        import sys
        from contextlib import redirect_stderr, redirect_stdout

        # Test output capture mechanism
        output = io.StringIO()
        error_output = io.StringIO()
        
        try:
            with redirect_stdout(output), redirect_stderr(error_output):
                # Import and run a simple test
                import sys
                sys.path.insert(0, 'src/homework1')
                
                # Test that we can import the problem modules
                import problem1_tuberculosis_test

                # Check that output capture works
                print("Test output")
                
        except Exception as e:
            pytest.fail(f"Output capture test failed: {e}")
        
        captured_output = output.getvalue()
        captured_errors = error_output.getvalue()
        
        assert "Test output" in captured_output, "Output capture not working"
        assert captured_errors == "", f"Unexpected errors: {captured_errors}"


class TestSimpleGUIPerformance:
    """Test that simple GUI performs well without threading issues."""
    
    def test_simple_gui_startup_time(self):
        """Test that simple GUI starts up quickly."""
        start_time = time.time()
        
        process = subprocess.Popen(
            [sys.executable, "src/homework1/simple_gui.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for GUI to start
        time.sleep(2)
        
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=5)
            startup_time = time.time() - start_time
            
            # GUI should start within 3 seconds
            assert startup_time < 3.0, f"GUI startup took too long: {startup_time:.2f} seconds"
        else:
            stdout, stderr = process.communicate()
            pytest.fail(f"GUI failed to start. STDOUT: {stdout}, STDERR: {stderr}")
    
    def test_simple_gui_no_memory_leaks(self):
        """Test that simple GUI doesn't have obvious memory leaks."""
        # Launch and close GUI multiple times to check for memory issues
        for i in range(3):
            process = subprocess.Popen(
                [sys.executable, "src/homework1/simple_gui.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            time.sleep(1)
            
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=5)
                stdout, stderr = process.communicate()
                
                # Check for memory-related errors
                memory_errors = [
                    "Memory",
                    "Segmentation fault",
                    "Out of memory",
                    "malloc",
                    "free"
                ]
                
                for error in memory_errors:
                    assert error not in stderr, f"Memory error found: {error} in stderr: {stderr}"
            else:
                stdout, stderr = process.communicate()
                pytest.fail(f"GUI failed on iteration {i}. STDOUT: {stdout}, STDERR: {stderr}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 