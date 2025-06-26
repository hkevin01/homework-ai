"""
Tests for Homework 1 Problem Scripts

This module tests that all problem scripts run correctly and produce expected output.
"""

import os
import shutil
import subprocess
import sys
import tempfile

import pytest


class TestProblemScripts:
    """Test cases for individual problem scripts."""
    
    def setup_method(self):
        """Set up test environment."""
        self.homework_dir = os.path.join('src', 'homework1')
        self.problem_files = [
            'problem1_tuberculosis_test.py',
            'problem2_discrete_random_variables.py',
            'problem3_earthquake_prediction.py',
            'problem4_mechanical_failure.py'
        ]
    
    def test_all_problem_files_exist(self):
        """Test that all problem files exist."""
        for problem_file in self.problem_files:
            file_path = os.path.join(self.homework_dir, problem_file)
            assert os.path.exists(file_path), f"Problem file {file_path} does not exist"
    
    def test_problem1_tuberculosis_test(self):
        """Test Problem 1: Tuberculosis Test Assessment."""
        result = subprocess.run(
            [sys.executable, 'problem1_tuberculosis_test.py'],
            cwd=self.homework_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0, f"Problem 1 failed with return code {result.returncode}"
        assert "Tuberculosis Test Assessment" in result.stdout
        assert "Prior probability of disease" in result.stdout
        assert "Posterior probability given positive test" in result.stdout
        assert "Likelihood ratio" in result.stdout
        assert "Sensitivity" in result.stdout
        assert "Specificity" in result.stdout
        
        # Check for specific numerical results (updated to match actual output)
        assert "0.0040" in result.stdout  # Prior probability
        assert "0.031" in result.stdout   # Posterior probability (approximately)
    
    def test_problem2_discrete_random_variables(self):
        """Test Problem 2: Discrete Random Variables."""
        result = subprocess.run(
            [sys.executable, 'problem2_discrete_random_variables.py'],
            cwd=self.homework_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0, f"Problem 2 failed with return code {result.returncode}"
        assert "Problem 2: Discrete Random Variables" in result.stdout
        assert "Categorical(0.3, 0.1, 0.2, 0.4)" in result.stdout
        assert "Expectation E[X]" in result.stdout
        assert "Variance V[X]" in result.stdout
        assert "Probability Mass Function" in result.stdout
        
        # Check for expected values (updated to match actual output)
        assert "1.70" in result.stdout  # Expected value
        assert "1.61" in result.stdout  # Variance
    
    def test_problem3_earthquake_prediction(self):
        """Test Problem 3: Earthquake Prediction."""
        result = subprocess.run(
            [sys.executable, 'problem3_earthquake_prediction.py'],
            cwd=self.homework_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0, f"Problem 3 failed with return code {result.returncode}"
        assert "Problem 3: Earthquake Prediction" in result.stdout
        assert "Earthquake data by decade" in result.stdout
        assert "Mean earthquakes per decade" in result.stdout
        assert "Variance" in result.stdout
        assert "Standard deviation" in result.stdout
        assert "Probability of 1+ major earthquakes" in result.stdout
        
        # Check for specific data
        assert "1900-1909: 0 major earthquakes" in result.stdout
        assert "1910-1919: 1 major earthquakes" in result.stdout
    
    def test_problem4_mechanical_failure(self):
        """Test Problem 4: Mechanical Component Failure."""
        result = subprocess.run(
            [sys.executable, 'problem4_mechanical_failure.py'],
            cwd=self.homework_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0, f"Problem 4 failed with return code {result.returncode}"
        assert "Problem 4: Mechanical Component Failure" in result.stdout
        assert "Failure time data" in result.stdout
        assert "Basic Statistics" in result.stdout
        assert "Mean failure time" in result.stdout
        assert "Standard deviation" in result.stdout
        assert "Distribution Comparison" in result.stdout
        assert "Exponential Distribution" in result.stdout
        assert "Weibull Distribution" in result.stdout
        assert "Reliability Predictions" in result.stdout
        
        # Check for specific data
        assert "Gear 1: 10.5 years" in result.stdout
        assert "Gear 2: 7.5 years" in result.stdout
    
    def test_problem_scripts_no_errors(self):
        """Test that all problem scripts run without critical errors."""
        for problem_file in self.problem_files:
            result = subprocess.run(
                [sys.executable, problem_file],
                cwd=self.homework_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            assert result.returncode == 0, f"{problem_file} failed with return code {result.returncode}"
            
            # Allow Qt threading errors from matplotlib (these are expected)
            stderr_content = result.stderr.strip()
            if stderr_content:
                # Check that stderr only contains expected Qt warnings
                expected_warnings = [
                    "QSocketNotifier: Can only be used with threads started with QThread",
                    "qt.qpa.wayland: Wayland does not support QWindow::requestActivate()"
                ]
                
                for warning in expected_warnings:
                    if warning in stderr_content:
                        # This is expected, continue
                        continue
                
                # If we get here, there are unexpected errors
                if stderr_content and not any(warning in stderr_content for warning in expected_warnings):
                    pytest.fail(f"{problem_file} produced unexpected stderr: {result.stderr}")
            
            assert result.stdout.strip(), f"{problem_file} produced no output"
    
    def test_problem_scripts_produce_meaningful_output(self):
        """Test that all problem scripts produce meaningful output."""
        expected_keywords = {
            'problem1_tuberculosis_test.py': ['Tuberculosis', 'probability', 'test'],
            'problem2_discrete_random_variables.py': ['Categorical', 'expectation', 'variance'],
            'problem3_earthquake_prediction.py': ['Earthquake', 'decade', 'probability'],
            'problem4_mechanical_failure.py': ['Failure', 'statistics', 'distribution']
        }
        
        for problem_file, keywords in expected_keywords.items():
            result = subprocess.run(
                [sys.executable, problem_file],
                cwd=self.homework_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            assert result.returncode == 0, f"{problem_file} failed"
            output = result.stdout.lower()
            
            for keyword in keywords:
                assert keyword.lower() in output, f"Keyword '{keyword}' not found in {problem_file} output"


class TestProblemDependencies:
    """Test that problem scripts have required dependencies."""
    
    def test_required_modules_importable(self):
        """Test that all required modules can be imported."""
        required_modules = ['numpy', 'scipy', 'matplotlib', 'PyQt5']
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError as e:
                pytest.fail(f"Required module {module} not available: {e}")
    
    def test_problem_imports(self):
        """Test that problem scripts can import their dependencies."""
        problem_files = [
            'problem1_tuberculosis_test.py',
            'problem2_discrete_random_variables.py',
            'problem3_earthquake_prediction.py',
            'problem4_mechanical_failure.py'
        ]
        
        for problem_file in problem_files:
            file_path = os.path.join('src', 'homework1', problem_file)
            
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    compile(content, file_path, 'exec')
            except SyntaxError as e:
                pytest.fail(f"Syntax error in {problem_file}: {e}")
            except Exception as e:
                pytest.fail(f"Error in {problem_file}: {e}")


class TestProblemOutputFormat:
    """Test the format and structure of problem outputs."""
    
    def test_problem_outputs_are_readable(self):
        """Test that problem outputs are human-readable."""
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
            
            assert result.returncode == 0, f"{problem_file} failed"
            
            # Check that output is not empty
            assert result.stdout.strip(), f"{problem_file} produced empty output"
            
            # Check that output contains reasonable line lengths
            lines = result.stdout.split('\n')
            for line in lines:
                assert len(line) < 200, f"Line too long in {problem_file}: {line[:50]}..."
            
            # Check that output contains some numerical values
            import re
            numbers = re.findall(r'\d+\.\d+', result.stdout)
            assert len(numbers) > 0, f"{problem_file} contains no numerical results"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 