"""
Tests for Output Population in GUI

This module specifically tests that solution output is properly populated
when running problems through the GUI.
"""

import os
import re
import subprocess
import sys
import time

import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtTest import QTest
    from PyQt5.QtWidgets import QApplication, QPushButton, QTextEdit

    from homework1.simple_gui import SimpleHomework1GUI
    PYTQT_AVAILABLE = True
except ImportError:
    PYTQT_AVAILABLE = False


class TestOutputPopulation:
    """Test that output is properly populated when running problems."""
    
    @pytest.fixture(scope="class")
    def app(self):
        """Create QApplication instance for tests."""
        if not PYTQT_AVAILABLE:
            pytest.skip("PyQt5 not available")
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        return app
    
    def test_problem1_output_population(self, app):
        """Test that Problem 1 output is populated in GUI."""
        if not PYTQT_AVAILABLE:
            pytest.skip("PyQt5 not available")
        
        gui = SimpleHomework1GUI()
        
        try:
            # Get the first tab (Problem 1)
            tab = gui.tab_widget.widget(0)
            
            # Find the output text area
            output_text = None
            for child in tab.findChildren(QTextEdit):
                if child.isReadOnly():
                    output_text = child
                    break
            
            assert output_text is not None, "Could not find output text area"
            
            # Clear any existing output
            output_text.clear()
            assert output_text.toPlainText() == ""
            
            # Find and click the run button
            run_button = None
            for child in tab.findChildren(QPushButton):
                if child.text() == "Run Problem":
                    run_button = child
                    break
            
            assert run_button is not None, "Could not find run button"
            
            # Click the run button
            QTest.mouseClick(run_button, Qt.LeftButton)
            
            # Wait for output to be populated
            time.sleep(5)
            
            # Check that output has been populated
            output_content = output_text.toPlainText()
            assert output_content.strip() != "", "Output was not populated"
            
            # Check for expected content
            assert "Tuberculosis Test Assessment" in output_content
            assert "Prior probability of disease" in output_content
            assert "Posterior probability given positive test" in output_content
            
            # Check for numerical results
            assert re.search(r'\d+\.\d+', output_content), "No numerical results found"
            
        finally:
            gui.close()
    
    def test_problem2_output_population(self, app):
        """Test that Problem 2 output is populated in GUI."""
        if not PYTQT_AVAILABLE:
            pytest.skip("PyQt5 not available")
        
        gui = SimpleHomework1GUI()
        
        try:
            # Get the second tab (Problem 2)
            tab = gui.tab_widget.widget(1)
            
            # Find the output text area
            output_text = None
            for child in tab.findChildren(QTextEdit):
                if child.isReadOnly():
                    output_text = child
                    break
            
            assert output_text is not None, "Could not find output text area"
            
            # Clear any existing output
            output_text.clear()
            assert output_text.toPlainText() == ""
            
            # Find and click the run button
            run_button = None
            for child in tab.findChildren(QPushButton):
                if child.text() == "Run Problem":
                    run_button = child
                    break
            
            assert run_button is not None, "Could not find run button"
            
            # Click the run button
            QTest.mouseClick(run_button, Qt.LeftButton)
            
            # Wait for output to be populated
            time.sleep(5)
            
            # Check that output has been populated
            output_content = output_text.toPlainText()
            assert output_content.strip() != "", "Output was not populated"
            
            # Check for expected content
            assert "Problem 2: Discrete Random Variables" in output_content
            assert "Categorical(0.3, 0.1, 0.2, 0.4)" in output_content
            assert "Expectation E[X]" in output_content
            assert "Variance V[X]" in output_content
            
            # Check for numerical results
            assert re.search(r'\d+\.\d+', output_content), "No numerical results found"
            
        finally:
            gui.close()
    
    def test_problem3_output_population(self, app):
        """Test that Problem 3 output is populated in GUI."""
        if not PYTQT_AVAILABLE:
            pytest.skip("PyQt5 not available")
        
        gui = SimpleHomework1GUI()
        
        try:
            # Get the third tab (Problem 3)
            tab = gui.tab_widget.widget(2)
            
            # Find the output text area
            output_text = None
            for child in tab.findChildren(QTextEdit):
                if child.isReadOnly():
                    output_text = child
                    break
            
            assert output_text is not None, "Could not find output text area"
            
            # Clear any existing output
            output_text.clear()
            assert output_text.toPlainText() == ""
            
            # Find and click the run button
            run_button = None
            for child in tab.findChildren(QPushButton):
                if child.text() == "Run Problem":
                    run_button = child
                    break
            
            assert run_button is not None, "Could not find run button"
            
            # Click the run button
            QTest.mouseClick(run_button, Qt.LeftButton)
            
            # Wait for output to be populated
            time.sleep(5)
            
            # Check that output has been populated
            output_content = output_text.toPlainText()
            assert output_content.strip() != "", "Output was not populated"
            
            # Check for expected content
            assert "Problem 3: Earthquake Prediction" in output_content
            assert "Earthquake data by decade" in output_content
            assert "Mean earthquakes per decade" in output_content
            
            # Check for numerical results
            assert re.search(r'\d+\.\d+', output_content), "No numerical results found"
            
        finally:
            gui.close()
    
    def test_problem4_output_population(self, app):
        """Test that Problem 4 output is populated in GUI."""
        if not PYTQT_AVAILABLE:
            pytest.skip("PyQt5 not available")
        
        gui = SimpleHomework1GUI()
        
        try:
            # Get the fourth tab (Problem 4)
            tab = gui.tab_widget.widget(3)
            
            # Find the output text area
            output_text = None
            for child in tab.findChildren(QTextEdit):
                if child.isReadOnly():
                    output_text = child
                    break
            
            assert output_text is not None, "Could not find output text area"
            
            # Clear any existing output
            output_text.clear()
            assert output_text.toPlainText() == ""
            
            # Find and click the run button
            run_button = None
            for child in tab.findChildren(QPushButton):
                if child.text() == "Run Problem":
                    run_button = child
                    break
            
            assert run_button is not None, "Could not find run button"
            
            # Click the run button
            QTest.mouseClick(run_button, Qt.LeftButton)
            
            # Wait for output to be populated
            time.sleep(5)
            
            # Check that output has been populated
            output_content = output_text.toPlainText()
            assert output_content.strip() != "", "Output was not populated"
            
            # Check for expected content
            assert "Problem 4: Mechanical Component Failure" in output_content
            assert "Failure time data" in output_content
            assert "Basic Statistics" in output_content
            assert "Distribution Comparison" in output_content
            
            # Check for numerical results
            assert re.search(r'\d+\.\d+', output_content), "No numerical results found"
            
        finally:
            gui.close()


class TestOutputContentValidation:
    """Test that output content is valid and complete."""
    
    def test_problem_outputs_contain_required_sections(self):
        """Test that problem outputs contain all required sections."""
        problem_files = [
            'problem1_tuberculosis_test.py',
            'problem2_discrete_random_variables.py',
            'problem3_earthquake_prediction.py',
            'problem4_mechanical_failure.py'
        ]
        
        required_sections = {
            'problem1_tuberculosis_test.py': [
                'Tuberculosis Test Assessment',
                'Prior probability of disease',
                'Posterior probability given positive test',
                'Likelihood ratio',
                'Sensitivity',
                'Specificity'
            ],
            'problem2_discrete_random_variables.py': [
                'Problem 2: Discrete Random Variables',
                'Categorical(0.3, 0.1, 0.2, 0.4)',
                'Expectation E[X]',
                'Variance V[X]',
                'Probability Mass Function'
            ],
            'problem3_earthquake_prediction.py': [
                'Problem 3: Earthquake Prediction',
                'Earthquake data by decade',
                'Mean earthquakes per decade',
                'Variance',
                'Standard deviation'
            ],
            'problem4_mechanical_failure.py': [
                'Problem 4: Mechanical Component Failure',
                'Failure time data',
                'Basic Statistics',
                'Mean failure time',
                'Standard deviation',
                'Distribution Comparison'
            ]
        }
        
        for problem_file, sections in required_sections.items():
            result = subprocess.run(
                [sys.executable, problem_file],
                cwd=os.path.join('src', 'homework1'),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            assert result.returncode == 0, f"{problem_file} failed to run"
            output = result.stdout
            
            for section in sections:
                assert section in output, f"Section '{section}' not found in {problem_file} output"
    
    def test_problem_outputs_contain_numerical_results(self):
        """Test that problem outputs contain numerical results."""
        problem_files = [
            'problem1_tuberculosis_test.py',
            'problem2_discrete_random_variables.py',
            'problem3_earthquake_prediction.py',
            'problem4_mechanical_failure.py'
        ]
        
        for problem_file in problem_files:
            result = subprocess.run(
                [sys.executable, problem_file],
                cwd=os.path.join('src', 'homework1'),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            assert result.returncode == 0, f"{problem_file} failed to run"
            output = result.stdout
            
            # Check for decimal numbers
            decimal_numbers = re.findall(r'\d+\.\d+', output)
            assert len(decimal_numbers) > 0, f"{problem_file} contains no decimal numbers"
            
            # Check for integers
            integers = re.findall(r'\b\d+\b', output)
            assert len(integers) > 0, f"{problem_file} contains no integers"
    
    def test_problem_outputs_are_formatted_correctly(self):
        """Test that problem outputs are properly formatted."""
        problem_files = [
            'problem1_tuberculosis_test.py',
            'problem2_discrete_random_variables.py',
            'problem3_earthquake_prediction.py',
            'problem4_mechanical_failure.py'
        ]
        
        for problem_file in problem_files:
            result = subprocess.run(
                [sys.executable, problem_file],
                cwd=os.path.join('src', 'homework1'),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            assert result.returncode == 0, f"{problem_file} failed to run"
            output = result.stdout
            
            # Check that output is not empty
            assert output.strip(), f"{problem_file} produced empty output"
            
            # Check that output has reasonable line lengths
            lines = output.split('\n')
            for line in lines:
                if line.strip():  # Skip empty lines
                    assert len(line) < 200, f"Line too long in {problem_file}: {line[:50]}..."
            
            # Check that output contains some structure (headers, separators, etc.)
            assert '=' in output or '-' in output or ':' in output, f"{problem_file} lacks formatting structure"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 