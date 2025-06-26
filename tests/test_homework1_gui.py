"""
Tests for Homework 1 GUI Application

This module contains comprehensive tests for the PyQt GUI application,
including unit tests for individual components and integration tests.
"""

import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, Mock, patch

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

# Import the GUI components
from homework1.gui_app import Homework1GUI, ProblemRunner


class TestProblemRunner(unittest.TestCase):
    """Test cases for the ProblemRunner class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test_problem.py')
        
        # Create a simple test Python file
        with open(self.test_file, 'w') as f:
            f.write("""
import sys
print("Test problem output")
print("This is a test")
sys.exit(0)
""")
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)
    
    def test_problem_runner_initialization(self):
        """Test ProblemRunner initialization."""
        runner = ProblemRunner(self.test_file)
        self.assertIsNotNone(runner)
        self.assertEqual(runner.problem_file, self.test_file)
    
    def test_problem_runner_output_signal(self):
        """Test that ProblemRunner emits output signals."""
        runner = ProblemRunner(self.test_file)
        mock_output_handler = Mock()
        runner.output_received.connect(mock_output_handler)
        
        # Run the problem
        runner.run()
        runner.wait(5000)  # Wait up to 5 seconds
        
        # Check if output was received
        self.assertTrue(mock_output_handler.called)
    
    def test_problem_runner_finished_signal(self):
        """Test that ProblemRunner emits finished signal."""
        runner = ProblemRunner(self.test_file)
        mock_finished_handler = Mock()
        runner.finished.connect(mock_finished_handler)
        
        # Run the problem
        runner.run()
        runner.wait(5000)  # Wait up to 5 seconds
        
        # Check if finished signal was emitted
        self.assertTrue(mock_finished_handler.called)
    
    def test_problem_runner_error_handling(self):
        """Test ProblemRunner error handling with non-existent file."""
        runner = ProblemRunner("non_existent_file.py")
        mock_error_handler = Mock()
        runner.error_occurred.connect(mock_error_handler)
        
        # Run the problem
        runner.run()
        runner.wait(5000)  # Wait up to 5 seconds
        
        # Check if error was handled
        self.assertTrue(mock_error_handler.called)


class TestHomework1GUI(unittest.TestCase):
    """Test cases for the Homework1GUI class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        
        self.gui = Homework1GUI()
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.gui.close()
    
    def test_gui_initialization(self):
        """Test GUI initialization."""
        self.assertIsNotNone(self.gui)
        self.assertEqual(self.gui.windowTitle(), 
                        "Homework 1 - Introduction to Scientific Machine Learning")
    
    def test_gui_has_tabs(self):
        """Test that GUI has the expected tabs."""
        tab_widget = self.gui.tab_widget
        self.assertIsNotNone(tab_widget)
        
        # Check that we have 4 tabs (one for each problem)
        self.assertEqual(tab_widget.count(), 4)
        
        # Check tab titles
        expected_titles = [
            'Problem 1: Tuberculosis Test',
            'Problem 2: Discrete Random Variables',
            'Problem 3: Earthquake Prediction',
            'Problem 4: Mechanical Failure'
        ]
        
        for i, expected_title in enumerate(expected_titles):
            self.assertEqual(tab_widget.tabText(i), expected_title)
    
    def test_problem_descriptions_exist(self):
        """Test that problem descriptions are properly set."""
        # Get the first tab
        first_tab = self.gui.tab_widget.widget(0)
        
        # Find the description text edit
        desc_text = None
        for child in first_tab.findChildren(QApplication.instance().findChild):
            if hasattr(child, 'toPlainText'):
                desc_text = child
                break
        
        if desc_text:
            description = desc_text.toPlainText()
            self.assertIn("Tuberculosis Test Assessment", description)
            self.assertIn("Bayesian probability", description)
    
    def test_gui_controls_exist(self):
        """Test that GUI controls (buttons) exist."""
        # Get the first tab
        first_tab = self.gui.tab_widget.widget(0)
        
        # Find buttons
        buttons = first_tab.findChildren(QApplication.instance().findChild)
        run_button = None
        clear_button = None
        
        for button in buttons:
            if hasattr(button, 'text'):
                if "Run Problem" in button.text():
                    run_button = button
                elif "Clear Output" in button.text():
                    clear_button = button
        
        self.assertIsNotNone(run_button, "Run Problem button not found")
        self.assertIsNotNone(clear_button, "Clear Output button not found")
    
    def test_gui_output_area_exists(self):
        """Test that GUI has an output text area."""
        # Get the first tab
        first_tab = self.gui.tab_widget.widget(0)
        
        # Find the output text edit
        output_text = None
        for child in first_tab.findChildren(QApplication.instance().findChild):
            if hasattr(child, 'toPlainText') and hasattr(child, 'setPlainText'):
                output_text = child
                break
        
        self.assertIsNotNone(output_text, "Output text area not found")
        self.assertTrue(output_text.isReadOnly(), "Output area should be read-only")


class TestGUIIntegration(unittest.TestCase):
    """Integration tests for the GUI application."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.test_problem_file = os.path.join(self.test_dir, 'test_problem.py')
        
        # Create a simple test problem file
        with open(self.test_problem_file, 'w') as f:
            f.write("""
import sys
print("=== Test Problem Output ===")
print("This is a test problem for GUI testing")
print("It should display in the GUI output area")
print("=== End Test ===")
sys.exit(0)
""")
        
        self.gui = Homework1GUI()
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)
        self.gui.close()
    
    @patch('homework1.gui_app.ProblemRunner')
    def test_run_problem_integration(self, mock_runner_class):
        """Test running a problem through the GUI."""
        # Mock the ProblemRunner
        mock_runner = Mock()
        mock_runner_class.return_value = mock_runner
        
        # Get the first tab and find the run button
        first_tab = self.gui.tab_widget.widget(0)
        run_button = None
        
        for child in first_tab.findChildren(QApplication.instance().findChild):
            if hasattr(child, 'text') and "Run Problem" in child.text():
                run_button = child
                break
        
        self.assertIsNotNone(run_button, "Run button not found")
        
        # Click the run button
        QTest.mouseClick(run_button, Qt.LeftButton)
        
        # Check that ProblemRunner was created and started
        mock_runner_class.assert_called_once()
        mock_runner.start.assert_called_once()
    
    def test_gui_responsiveness(self):
        """Test that GUI remains responsive during operations."""
        # Get the first tab
        first_tab = self.gui.tab_widget.widget(0)
        
        # Find buttons
        buttons = first_tab.findChildren(QApplication.instance().findChild)
        
        # Test that we can interact with buttons
        for button in buttons:
            if hasattr(button, 'text') and button.text():
                # Check that button is enabled
                self.assertTrue(button.isEnabled(), 
                              f"Button '{button.text()}' should be enabled")


class TestProblemFiles(unittest.TestCase):
    """Test that problem files exist and are valid."""
    
    def test_problem_files_exist(self):
        """Test that all problem files exist."""
        problem_files = [
            'src/homework1/problem1_tuberculosis_test.py',
            'src/homework1/problem2_discrete_random_variables.py',
            'src/homework1/problem3_earthquake_prediction.py',
            'src/homework1/problem4_mechanical_failure.py'
        ]
        
        for file_path in problem_files:
            self.assertTrue(os.path.exists(file_path), 
                          f"Problem file {file_path} does not exist")
    
    def test_problem_files_are_valid_python(self):
        """Test that problem files contain valid Python code."""
        problem_files = [
            'src/homework1/problem1_tuberculosis_test.py',
            'src/homework1/problem2_discrete_random_variables.py',
            'src/homework1/problem3_earthquake_prediction.py',
            'src/homework1/problem4_mechanical_failure.py'
        ]
        
        for file_path in problem_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    compile(content, file_path, 'exec')
            except SyntaxError as e:
                self.fail(f"Syntax error in {file_path}: {e}")


def run_gui_tests():
    """Run all GUI tests."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestProblemRunner))
    test_suite.addTest(unittest.makeSuite(TestHomework1GUI))
    test_suite.addTest(unittest.makeSuite(TestGUIIntegration))
    test_suite.addTest(unittest.makeSuite(TestProblemFiles))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_gui_tests()
    sys.exit(0 if success else 1) 