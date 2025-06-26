"""
Simplified PyQt GUI for Homework 1

This is a simplified version that avoids Qt threading issues
by using a different approach for running problems.
"""

import os
import subprocess
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class SimpleHomework1GUI(QMainWindow):
    """Simplified GUI window for Homework 1."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Homework 1 - Introduction to Scientific Machine Learning")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Create tab widget for problems
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Add problem tabs
        self.add_problem_tabs()
        
        # Create status bar
        self.statusBar().showMessage("Ready")
        
    def create_header(self):
        """Create the header section."""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Box)
        header_frame.setStyleSheet("QFrame { background-color: #f0f0f0; border: 2px solid #ccc; }")
        
        layout = QVBoxLayout(header_frame)
        
        # Title
        title_label = QLabel("Homework 1: Introduction to Scientific Machine Learning")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Interactive Problem Solver and Analysis Tool")
        subtitle_label.setFont(QFont("Arial", 12))
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)
        
        return header_frame
    
    def add_problem_tabs(self):
        """Add tabs for each problem."""
        problems = [
            {
                'title': 'Problem 1: Tuberculosis Test',
                'file': 'problem1_tuberculosis_test.py',
                'description': self.get_problem1_description(),
                'learning_objectives': [
                    "Understand Bayesian probability and Bayes' theorem",
                    "Calculate prior and posterior probabilities",
                    "Evaluate medical test accuracy and usefulness",
                    "Interpret likelihood ratios and odds ratios"
                ]
            },
            {
                'title': 'Problem 2: Discrete Random Variables',
                'file': 'problem2_discrete_random_variables.py',
                'description': self.get_problem2_description(),
                'learning_objectives': [
                    "Work with categorical random variables",
                    "Calculate expectation and variance",
                    "Visualize probability mass functions",
                    "Use scipy.stats for statistical analysis"
                ]
            },
            {
                'title': 'Problem 3: Earthquake Prediction',
                'file': 'problem3_earthquake_prediction.py',
                'description': self.get_problem3_description(),
                'learning_objectives': [
                    "Model rare events using Poisson processes",
                    "Analyze time series data",
                    "Make probabilistic predictions",
                    "Evaluate model fit and assumptions"
                ]
            },
            {
                'title': 'Problem 4: Mechanical Failure',
                'file': 'problem4_mechanical_failure.py',
                'description': self.get_problem4_description(),
                'learning_objectives': [
                    "Analyze failure time distributions",
                    "Fit exponential and Weibull distributions",
                    "Perform reliability analysis",
                    "Compare distribution fits using goodness-of-fit tests"
                ]
            }
        ]
        
        for problem in problems:
            tab = self.create_problem_tab(problem)
            self.tab_widget.addTab(tab, problem['title'])
    
    def create_problem_tab(self, problem):
        """Create a tab for a specific problem."""
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        
        # Create splitter for description and output
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Left side: Problem description and controls
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Problem description
        desc_group = QGroupBox("Problem Description")
        desc_layout = QVBoxLayout(desc_group)
        
        desc_text = QTextEdit()
        desc_text.setPlainText(problem['description'])
        desc_text.setReadOnly(True)
        desc_text.setMaximumHeight(200)
        desc_layout.addWidget(desc_text)
        left_layout.addWidget(desc_group)
        
        # Learning objectives
        obj_group = QGroupBox("Learning Objectives")
        obj_layout = QVBoxLayout(obj_group)
        
        for objective in problem['learning_objectives']:
            obj_label = QLabel(f"• {objective}")
            obj_label.setWordWrap(True)
            obj_layout.addWidget(obj_label)
        
        left_layout.addWidget(obj_group)
        
        # Control buttons
        button_group = QGroupBox("Controls")
        button_layout = QHBoxLayout(button_group)
        
        run_button = QPushButton("Run Problem")
        run_button.clicked.connect(lambda: self.run_problem_simple(problem['file']))
        button_layout.addWidget(run_button)
        
        clear_button = QPushButton("Clear Output")
        clear_button.clicked.connect(lambda: self.clear_output())
        button_layout.addWidget(clear_button)
        
        left_layout.addWidget(button_group)
        left_layout.addStretch()
        splitter.addWidget(left_widget)
        
        # Right side: Output display
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        output_label = QLabel("Problem Output:")
        output_label.setFont(QFont("Arial", 12, QFont.Bold))
        right_layout.addWidget(output_label)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Courier", 10))
        right_layout.addWidget(self.output_text)
        
        splitter.addWidget(right_widget)
        
        # Set splitter proportions
        splitter.setSizes([400, 800])
        
        return tab_widget
    
    def get_problem1_description(self):
        """Get detailed description for Problem 1."""
        return """Problem 1: Tuberculosis Test Assessment

This problem explores Bayesian probability in the context of medical testing. We are tasked with assessing the usefulness of a tuberculosis test.

Given Information:
• Prior probability of disease: 0.4% of population has tuberculosis
• Test sensitivity: 80% true positive rate (P(positive|disease) = 0.80)
• Test specificity: 90% true negative rate (P(negative|no disease) = 0.90)

Key Questions:
A. Find the prior probability P(B|I) - the base rate of tuberculosis
B. Calculate the posterior probability P(B|A,I) - probability of disease given positive test
C. Analyze the test's usefulness using likelihood ratios and odds ratios

This problem demonstrates:
• Application of Bayes' theorem
• Understanding of medical test accuracy
• Interpretation of diagnostic test results
• Decision-making under uncertainty

The solution shows how even a seemingly accurate test can have limited predictive value when the disease is rare in the population."""
    
    def get_problem2_description(self):
        """Get detailed description for Problem 2."""
        return """Problem 2: Practice with Discrete Random Variables

This problem focuses on categorical random variables and their properties. We work with a specific categorical distribution.

Given Distribution:
X ~ Categorical(0.3, 0.1, 0.2, 0.4)
Values: {0, 1, 2, 3}

Key Questions:
A. Calculate the expectation E[X]
B. Calculate the variance V[X]
C. Plot the probability mass function of X

This problem demonstrates:
• Properties of categorical random variables
• Calculation of expected values and variance
• Visualization of probability distributions
• Use of scipy.stats for statistical analysis

The categorical distribution is fundamental in machine learning for:
• Classification problems
• Categorical data modeling
• Multinomial distributions
• Discrete choice models

The solution provides both analytical calculations and computational verification using Python's scientific computing libraries."""
    
    def get_problem3_description(self):
        """Get detailed description for Problem 3."""
        return """Problem 3: Earthquake Prediction in Southern California

This problem applies Poisson processes to model rare events - major earthquakes in Southern California. We analyze historical data to make probabilistic predictions.

Given Data:
• Historical earthquake counts by decade (1900-2019)
• Major earthquakes defined as magnitude ≥ 6.5
• Focus on Southern California region

Key Questions:
A. Analyze earthquake statistics (mean, variance, patterns)
B. Fit a Poisson model to the data
C. Predict probability of major earthquakes in the next decade

This problem demonstrates:
• Poisson process modeling for rare events
• Time series analysis of count data
• Probabilistic forecasting
• Model validation and interpretation

The Poisson distribution is ideal for modeling:
• Rare events over time
• Count data with low rates
• Events that occur independently
• Natural disasters and accidents

The solution shows how statistical models can inform risk assessment and planning for natural disasters."""
    
    def get_problem4_description(self):
        """Get detailed description for Problem 4."""
        return """Problem 4: Mechanical Component Failure Analysis

This problem explores reliability analysis and failure time distributions. We analyze data from mechanical component testing to understand failure patterns.

Given Data:
• Failure times for 10 mechanical gears (in years)
• Components tested until failure
• Need to determine appropriate probability distribution

Key Questions:
A. Calculate basic statistics of failure times
B. Fit exponential and Weibull distributions
C. Compare distribution fits and predict reliability

This problem demonstrates:
• Reliability analysis and survival modeling
• Distribution fitting and comparison
• Goodness-of-fit testing
• Reliability prediction and planning

The exponential distribution assumes:
• Constant failure rate (memoryless property)
• Random failures with no aging effects

The Weibull distribution allows for:
• Increasing or decreasing failure rates
• Aging effects and wear-out patterns
• More flexible modeling of real-world systems

This analysis is crucial for:
• Maintenance planning
• Warranty analysis
• Quality control
• System design and optimization"""
    
    def run_problem_simple(self, problem_file):
        """Run a problem using a simple approach without threading."""
        try:
            # Clear previous output
            self.output_text.clear()
            
            # Update status
            self.statusBar().showMessage(f"Running {problem_file}...")
            
            # Change to the homework1 directory
            current_dir = os.getcwd()
            homework_dir = os.path.join(current_dir, 'src', 'homework1')
            
            # Run the problem file
            result = subprocess.run(
                [sys.executable, problem_file],
                cwd=homework_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.output_text.append(result.stdout)
                self.statusBar().showMessage(f"{problem_file} completed successfully")
            else:
                error_msg = f"Error running {problem_file}:\n{result.stderr}"
                self.output_text.append(error_msg)
                self.statusBar().showMessage(f"Error running {problem_file}")
                
        except subprocess.TimeoutExpired:
            error_msg = f"Execution of {problem_file} timed out after 30 seconds"
            self.output_text.append(error_msg)
            self.statusBar().showMessage("Execution timed out")
        except Exception as e:
            error_msg = f"Error running {problem_file}: {str(e)}"
            self.output_text.append(error_msg)
            self.statusBar().showMessage("Error occurred")
    
    def clear_output(self):
        """Clear the output display."""
        self.output_text.clear()
        self.statusBar().showMessage("Output cleared")


def main():
    """Main function to run the simplified GUI application."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the main window
    window = SimpleHomework1GUI()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 