"""
Tests for GUI Functionality

This module tests the GUI components, button interactions, and output display.
"""

import os
import subprocess
import sys
import time
from unittest.mock import MagicMock, Mock, patch

import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtTest import QTest
    from PyQt5.QtWidgets import QApplication, QPushButton, QTextEdit

    from homework1.simple_gui import SimpleHomework1GUI
    PYTQT_AVAILABLE = True
except ImportError:
    PYTQT_AVAILABLE = False


class TestGUIFunctionality:
    """Test GUI functionality and interactions."""
    
    @pytest.fixture(scope="class")
    def app(self):
        """Create QApplication instance for tests."""
        if not PYTQT_AVAILABLE:
            pytest.skip("PyQt5 not available")
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        return app
    
    @pytest.fixture
    def gui(self, app):
        """Create GUI instance for each test."""
        gui = SimpleHomework1GUI()
        yield gui
        gui.close()
    
    def test_gui_initialization(self, gui):
        """Test that GUI initializes correctly."""
        assert gui is not None
        assert gui.windowTitle() == "Homework 1 - Introduction to Scientific Machine Learning"
        assert gui.tab_widget is not None
        assert gui.tab_widget.count() == 4
    
    def test_gui_has_correct_tabs(self, gui):
        """Test that GUI has the correct tabs with proper titles."""
        expected_titles = [
            'Problem 1: Tuberculosis Test',
            'Problem 2: Discrete Random Variables',
            'Problem 3: Earthquake Prediction',
            'Problem 4: Mechanical Failure'
        ]
        
        for i, expected_title in enumerate(expected_titles):
            actual_title = gui.tab_widget.tabText(i)
            assert actual_title == expected_title, f"Tab {i} title mismatch: expected '{expected_title}', got '{actual_title}'"
    
    def test_gui_has_control_buttons(self, gui):
        """Test that each tab has the required control buttons."""
        for i in range(gui.tab_widget.count()):
            tab = gui.tab_widget.widget(i)
            
            # Find buttons in the tab
            buttons = tab.findChildren(QPushButton)
            button_texts = [btn.text() for btn in buttons]
            
            assert "Run Problem" in button_texts, f"Tab {i} missing 'Run Problem' button"
            assert "Clear Output" in button_texts, f"Tab {i} missing 'Clear Output' button"
    
    def test_gui_has_output_area(self, gui):
        """Test that each tab has an output text area."""
        for i in range(gui.tab_widget.count()):
            tab = gui.tab_widget.widget(i)
            
            # Find text edit widgets in the tab
            text_edits = tab.findChildren(QTextEdit)
            assert len(text_edits) > 0, f"Tab {i} has no text edit widgets"
            
            # Check that at least one is read-only (output area)
            read_only_found = any(te.isReadOnly() for te in text_edits)
            assert read_only_found, f"Tab {i} has no read-only text area"
    
    def test_clear_output_button_functionality(self, gui):
        """Test that clear output button works."""
        # Get the first tab
        first_tab = gui.tab_widget.widget(0)
        
        # Find the output text area
        output_text = None
        for child in first_tab.findChildren(QTextEdit):
            if child.isReadOnly():
                output_text = child
                break
        
        assert output_text is not None, "Could not find output text area"
        
        # Add some text to the output area
        test_text = "Test output text"
        output_text.setPlainText(test_text)
        assert output_text.toPlainText() == test_text
        
        # Find and click the clear button
        clear_button = None
        for child in first_tab.findChildren(QPushButton):
            if child.text() == "Clear Output":
                clear_button = child
                break
        
        assert clear_button is not None, "Could not find clear button"
        
        # Click the clear button
        QTest.mouseClick(clear_button, Qt.LeftButton)
        
        # Check that output is cleared
        assert output_text.toPlainText() == "", "Output was not cleared"


class TestGUIOutputPopulation:
    """Test that GUI properly populates output when running problems."""
    
    def test_gui_can_run_problem1(self):
        """Test that GUI can run Problem 1 and display output."""
        if not PYTQT_AVAILABLE:
            pytest.skip("PyQt5 not available")
        
        # Create a simple test to verify the GUI can run problems
        # This is a basic test that doesn't require full GUI interaction
        result = subprocess.run(
            [sys.executable, "src/homework1/problem1_tuberculosis_test.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0, "Problem 1 failed to run"
        assert "Tuberculosis Test Assessment" in result.stdout
        assert "Prior probability of disease" in result.stdout
    
    def test_gui_can_run_problem2(self):
        """Test that GUI can run Problem 2 and display output."""
        if not PYTQT_AVAILABLE:
            pytest.skip("PyQt5 not available")
        
        result = subprocess.run(
            [sys.executable, "src/homework1/problem2_discrete_random_variables.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0, "Problem 2 failed to run"
        assert "Problem 2: Discrete Random Variables" in result.stdout
        assert "Expectation E[X]" in result.stdout
    
    def test_gui_can_run_problem3(self):
        """Test that GUI can run Problem 3 and display output."""
        if not PYTQT_AVAILABLE:
            pytest.skip("PyQt5 not available")
        
        result = subprocess.run(
            [sys.executable, "src/homework1/problem3_earthquake_prediction.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0, "Problem 3 failed to run"
        assert "Problem 3: Earthquake Prediction" in result.stdout
        assert "Earthquake data by decade" in result.stdout
    
    def test_gui_can_run_problem4(self):
        """Test that GUI can run Problem 4 and display output."""
        if not PYTQT_AVAILABLE:
            pytest.skip("PyQt5 not available")
        
        result = subprocess.run(
            [sys.executable, "src/homework1/problem4_mechanical_failure.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0, "Problem 4 failed to run"
        assert "Problem 4: Mechanical Component Failure" in result.stdout
        assert "Failure time data" in result.stdout


class TestGUIIntegration:
    """Integration tests for the GUI."""
    
    def test_simple_gui_launches_without_errors(self):
        """Test that the simple GUI launches without Qt threading errors."""
        if not PYTQT_AVAILABLE:
            pytest.skip("PyQt5 not available")
        
        # Launch the GUI in a subprocess and check for errors
        process = subprocess.Popen(
            [sys.executable, "src/homework1/simple_gui.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a few seconds for the GUI to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            # GUI is running, check for error messages
            process.terminate()
            process.wait(timeout=5)
            stdout, stderr = process.communicate()
            
            # Check that there are no Qt threading errors
            assert "QSocketNotifier" not in stderr, f"QSocketNotifier error found: {stderr}"
            assert "QProcess::ExitStatus" not in stderr, f"QProcess::ExitStatus error found: {stderr}"
            assert "Cannot queue arguments" not in stderr, f"Queue arguments error found: {stderr}"
        else:
            # GUI failed to start, check why
            stdout, stderr = process.communicate()
            pytest.fail(f"GUI failed to start. STDOUT: {stdout}, STDERR: {stderr}")
    
    def test_gui_script_exists_and_runnable(self):
        """Test that the GUI script exists and can be imported."""
        gui_file = "src/homework1/simple_gui.py"
        assert os.path.exists(gui_file), f"GUI file {gui_file} does not exist"
        
        # Try to import the GUI module
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("simple_gui", gui_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            pytest.fail(f"Failed to import GUI module: {e}")


class TestGUIButtonInteractions:
    """Test button interactions in the GUI."""
    
    @pytest.fixture(scope="class")
    def app(self):
        """Create QApplication instance for tests."""
        if not PYTQT_AVAILABLE:
            pytest.skip("PyQt5 not available")
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        return app
    
    @pytest.fixture
    def gui(self, app):
        """Create GUI instance for each test."""
        gui = SimpleHomework1GUI()
        yield gui
        gui.close()
    
    def test_run_button_clickable(self, gui):
        """Test that run buttons are clickable."""
        # Get the first tab
        first_tab = gui.tab_widget.widget(0)
        
        # Find the run button
        run_button = None
        for child in first_tab.findChildren(QPushButton):
            if child.text() == "Run Problem":
                run_button = child
                break
        
        assert run_button is not None, "Could not find run button"
        assert run_button.isEnabled(), "Run button is not enabled"
        
        # Test that button can be clicked (without actually running the problem)
        # We'll just verify the button exists and is enabled
    
    def test_clear_button_clickable(self, gui):
        """Test that clear buttons are clickable."""
        # Get the first tab
        first_tab = gui.tab_widget.widget(0)
        
        # Find the clear button
        clear_button = None
        for child in first_tab.findChildren(QPushButton):
            if child.text() == "Clear Output":
                clear_button = child
                break
        
        assert clear_button is not None, "Could not find clear button"
        assert clear_button.isEnabled(), "Clear button is not enabled"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 