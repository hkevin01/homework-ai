"""
Enhanced PyQt GUI for Homework 1 with Integrated Figure Display

This enhanced version includes a tab system for displaying figures within the same window,
avoiding the need to open separate figure windows.
"""

import io
import os
import sys
from typing import Dict, List, Optional, Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSplitter,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class FigureTabWidget(QWidget):
    """Widget for displaying matplotlib figures in tabs."""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Initialize the figure tab widget."""
        super().__init__(parent)
        self.figures: Dict[str, Figure] = {}
        self.canvases: Dict[str, FigureCanvas] = {}
        self.init_ui()
    
    def init_ui(self) -> None:
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Create tab widget for figures
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Add placeholder for no figures
        self.add_placeholder_tab()
    
    def add_placeholder_tab(self) -> None:
        """Add a placeholder tab when no figures are available."""
        placeholder_widget = QWidget()
        placeholder_layout = QVBoxLayout(placeholder_widget)
        
        placeholder_label = QLabel("No figures available yet.\nRun a problem to see visualizations.")
        placeholder_label.setAlignment(Qt.AlignCenter)
        placeholder_label.setFont(QFont("Arial", 12))
        placeholder_layout.addWidget(placeholder_label)
        
        self.tab_widget.addTab(placeholder_widget, "No Figures")
    
    def clear_figures(self) -> None:
        """Clear all figures and reset to placeholder."""
        self.figures.clear()
        self.canvases.clear()
        self.tab_widget.clear()
        self.add_placeholder_tab()
    
    def add_figure(self, title: str, figure: Figure) -> None:
        """Add a new figure to the tab widget."""
        # Remove placeholder if it exists
        if self.tab_widget.count() == 1 and self.tab_widget.tabText(0) == "No Figures":
            self.tab_widget.clear()
        
        # Create canvas for the figure
        canvas = FigureCanvas(figure)
        canvas.setMinimumSize(400, 300)
        
        # Create scroll area for the canvas
        scroll_area = QScrollArea()
        scroll_area.setWidget(canvas)
        scroll_area.setWidgetResizable(True)
        
        # Add to tab widget
        self.tab_widget.addTab(scroll_area, title)
        
        # Store references
        self.figures[title] = figure
        self.canvases[title] = canvas
        
        # Update the canvas
        canvas.draw()


class ProblemTabWidget(QWidget):
    """Widget for a single problem tab with integrated figure display."""
    
    def __init__(self, problem_data: Dict[str, any], parent: Optional[QWidget] = None) -> None:
        """Initialize the problem tab widget."""
        super().__init__(parent)
        self.problem_data = problem_data
        self.output_text: Optional[QTextEdit] = None
        self.figure_tabs: Optional[FigureTabWidget] = None
        self.init_ui()
    
    def init_ui(self) -> None:
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Create main splitter
        main_splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(main_splitter)
        
        # Left side: Problem description and controls
        left_widget = self.create_left_panel()
        main_splitter.addWidget(left_widget)
        
        # Right side: Output and figures
        right_widget = self.create_right_panel()
        main_splitter.addWidget(right_widget)
        
        # Set splitter proportions (40% left, 60% right)
        main_splitter.setSizes([400, 600])
    
    def create_left_panel(self) -> QWidget:
        """Create the left panel with problem description and controls."""
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Problem description
        desc_group = QGroupBox("Problem Description")
        desc_layout = QVBoxLayout(desc_group)
        
        desc_text = QTextEdit()
        desc_text.setPlainText(self.problem_data["description"])
        desc_text.setReadOnly(True)
        desc_text.setMaximumHeight(200)
        desc_layout.addWidget(desc_text)
        left_layout.addWidget(desc_group)
        
        # Learning objectives
        obj_group = QGroupBox("Learning Objectives")
        obj_layout = QVBoxLayout(obj_group)
        
        for objective in self.problem_data["learning_objectives"]:
            obj_label = QLabel(f"• {objective}")
            obj_label.setWordWrap(True)
            obj_layout.addWidget(obj_label)
        
        left_layout.addWidget(obj_group)
        
        # Control buttons
        button_group = QGroupBox("Controls")
        button_layout = QHBoxLayout(button_group)
        
        run_button = QPushButton("Run Problem")
        run_button.clicked.connect(self.run_problem)
        button_layout.addWidget(run_button)
        
        clear_button = QPushButton("Clear Output")
        clear_button.clicked.connect(self.clear_output)
        button_layout.addWidget(clear_button)
        
        left_layout.addWidget(button_group)
        left_layout.addStretch()
        
        return left_widget
    
    def create_right_panel(self) -> QWidget:
        """Create the right panel with output and figure tabs."""
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Create tab widget for output and figures
        right_tab_widget = QTabWidget()
        right_layout.addWidget(right_tab_widget)
        
        # Output tab
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        
        output_label = QLabel("Problem Output:")
        output_label.setFont(QFont("Arial", 12, QFont.Bold))
        output_layout.addWidget(output_label)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Courier", 10))
        output_layout.addWidget(self.output_text)
        
        right_tab_widget.addTab(output_widget, "Output")
        
        # Figures tab
        self.figure_tabs = FigureTabWidget()
        right_tab_widget.addTab(self.figure_tabs, "Figures")
        
        return right_widget
    
    def run_problem(self) -> None:
        """Run the problem and capture output and figures."""
        try:
            # Clear previous output and figures
            self.clear_output()
            
            # Set matplotlib to use non-interactive backend for capturing
            matplotlib.use("Agg")
            
            # Capture stdout and stderr using StringIO
            import io
            from contextlib import redirect_stderr, redirect_stdout
            
            output_buffer = io.StringIO()
            error_buffer = io.StringIO()
            
            # Add src/homework1 to path for imports
            import sys
            sys.path.insert(0, os.path.join("src", "homework1"))
            
            # Import and run the problem module directly
            problem_file = self.problem_data["file"]
            module_name = problem_file.replace(".py", "")
            
            try:
                with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
                    # Import the module
                    module = __import__(module_name, fromlist=[""])
                    
                    # If the module has a main function, call it
                    if hasattr(module, "main"):
                        module.main()
                    # Otherwise, the module should execute when imported
                    
            except ImportError as e:
                error_msg = f"Failed to import {module_name}: {str(e)}"
                if self.output_text:
                    self.output_text.setPlainText(error_msg)
                QMessageBox.critical(self, "Import Error", error_msg)
                return
            except Exception as e:
                error_msg = f"Error executing {module_name}: {str(e)}"
                if self.output_text:
                    self.output_text.setPlainText(error_msg)
                QMessageBox.critical(self, "Execution Error", error_msg)
                return
            
            # Get captured output
            stdout_content = output_buffer.getvalue()
            stderr_content = error_buffer.getvalue()
            
            # Display output
            if self.output_text:
                if stdout_content:
                    self.output_text.setPlainText(stdout_content)
                else:
                    self.output_text.setPlainText("Problem executed successfully (no output generated)")
            
            # Generate and display figures
            self.generate_problem_figures()
            
            # Show success message
            QMessageBox.information(self, "Success", f"Problem {self.problem_data['title']} completed successfully!")
                
        except Exception as e:
            error_msg = f"Error running {self.problem_data['file']}: {str(e)}"
            if self.output_text:
                self.output_text.setPlainText(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
    
    def clear_output(self) -> None:
        """Clear the output display and figures."""
        if self.output_text:
            self.output_text.clear()
        if self.figure_tabs:
            self.figure_tabs.clear_figures()
    
    def generate_problem_figures(self) -> None:
        """Generate figures specific to the problem."""
        problem_file = self.problem_data["file"]
        
        if "problem1_tuberculosis_test" in problem_file:
            self.generate_tuberculosis_figures()
        elif "problem2_discrete_random_variables" in problem_file:
            self.generate_discrete_variables_figures()
        elif "problem3_earthquake_prediction" in problem_file:
            self.generate_earthquake_figures()
        elif "problem4_mechanical_failure" in problem_file:
            self.generate_mechanical_failure_figures()
    
    def generate_tuberculosis_figures(self) -> None:
        """Generate figures for tuberculosis test problem."""
        # Prior vs Posterior Probability
        fig1 = Figure(figsize=(8, 6))
        ax1 = fig1.add_subplot(111)
        
        categories = ["Disease Present", "Disease Absent"]
        prior_probs = [0.004, 0.996]
        posterior_probs = [0.0311, 0.9689]
        
        x = np.arange(len(categories))
        width = 0.35
        
        ax1.bar(x - width/2, prior_probs, width, label="Prior Probability", alpha=0.8)
        ax1.bar(x + width/2, posterior_probs, width, label="Posterior Probability", alpha=0.8)
        
        ax1.set_xlabel("Disease Status")
        ax1.set_ylabel("Probability")
        ax1.set_title("Prior vs Posterior Probabilities")
        ax1.set_xticks(x)
        ax1.set_xticklabels(categories)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        self.figure_tabs.add_figure("Prior vs Posterior", fig1)
        
        # Test Performance Metrics
        fig2 = Figure(figsize=(8, 6))
        ax2 = fig2.add_subplot(111)
        
        metrics = ["Sensitivity", "Specificity", "PPV", "NPV"]
        values = [0.80, 0.90, 0.0311, 0.9996]
        colors = ["green", "blue", "orange", "red"]
        
        bars = ax2.bar(metrics, values, color=colors, alpha=0.7)
        ax2.set_ylabel("Probability")
        ax2.set_title("Test Performance Metrics")
        ax2.set_ylim(0, 1)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f"{value:.4f}", ha="center", va="bottom")
        
        ax2.grid(True, alpha=0.3)
        
        self.figure_tabs.add_figure("Test Performance", fig2)
    
    def generate_discrete_variables_figures(self) -> None:
        """Generate figures for discrete random variables problem."""
        # Probability Mass Function
        fig1 = Figure(figsize=(10, 6))
        ax1 = fig1.add_subplot(111)
        
        x_values = [0, 1, 2, 3]
        probabilities = [0.3, 0.1, 0.2, 0.4]
        
        bars = ax1.bar(x_values, probabilities, alpha=0.7, color="skyblue", edgecolor="navy")
        ax1.set_xlabel("X Values")
        ax1.set_ylabel("Probability P(X = x)")
        ax1.set_title("Probability Mass Function")
        ax1.set_xticks(x_values)
        ax1.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, prob in zip(bars, probabilities):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f"{prob:.2f}", ha="center", va="bottom")
        
        self.figure_tabs.add_figure("Probability Mass Function", fig1)
        
        # Cumulative Distribution Function
        fig2 = Figure(figsize=(10, 6))
        ax2 = fig2.add_subplot(111)
        
        cumulative_probs = np.cumsum(probabilities)
        
        ax2.step(x_values, cumulative_probs, where="post", marker="o", linewidth=2, markersize=8)
        ax2.set_xlabel("X Values")
        ax2.set_ylabel("Cumulative Probability F(X ≤ x)")
        ax2.set_title("Cumulative Distribution Function")
        ax2.set_xticks(x_values)
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 1.1)
        
        self.figure_tabs.add_figure("Cumulative Distribution", fig2)
    
    def generate_earthquake_figures(self) -> None:
        """Generate figures for earthquake prediction problem."""
        # Earthquake data by decade
        fig1 = Figure(figsize=(12, 6))
        ax1 = fig1.add_subplot(111)
        
        decades = [f"{1900+i*10}-{1909+i*10}" for i in range(12)]
        earthquake_counts = [0, 1, 2, 0, 3, 2, 1, 2, 1, 2, 1, 0]
        
        bars = ax1.bar(decades, earthquake_counts, alpha=0.7, color="orange", edgecolor="darkorange")
        ax1.set_xlabel("Decade")
        ax1.set_ylabel("Number of Major Earthquakes")
        ax1.set_title("Major Earthquakes by Decade (1900-2019)")
        ax1.tick_params(axis="x", rotation=45)
        ax1.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, count in zip(bars, earthquake_counts):
            if count > 0:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                        str(count), ha="center", va="bottom")
        
        self.figure_tabs.add_figure("Earthquakes by Decade", fig1)
        
        # Poisson distribution fit
        fig2 = Figure(figsize=(10, 6))
        ax2 = fig2.add_subplot(111)
        
        lambda_param = 1.25  # Mean earthquakes per decade
        x = np.arange(0, 6)
        poisson_probs = [np.exp(-lambda_param) * lambda_param**k / np.math.factorial(k) for k in x]
        
        bars = ax2.bar(x, poisson_probs, alpha=0.7, color="lightgreen", edgecolor="darkgreen")
        ax2.set_xlabel("Number of Earthquakes")
        ax2.set_ylabel("Probability")
        ax2.set_title(f"Poisson Distribution (λ = {lambda_param})")
        ax2.set_xticks(x)
        ax2.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, prob in zip(bars, poisson_probs):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f"{prob:.3f}", ha="center", va="bottom")
        
        self.figure_tabs.add_figure("Poisson Distribution", fig2)
    
    def generate_mechanical_failure_figures(self) -> None:
        """Generate figures for mechanical failure problem."""
        # Failure time data
        fig1 = Figure(figsize=(10, 6))
        ax1 = fig1.add_subplot(111)
        
        gear_names = ["Gear 1", "Gear 2", "Gear 3", "Gear 4", "Gear 5"]
        failure_times = [10.5, 7.5, 12.0, 8.2, 15.1]
        
        bars = ax1.bar(gear_names, failure_times, alpha=0.7, color="lightcoral", edgecolor="darkred")
        ax1.set_xlabel("Gear Component")
        ax1.set_ylabel("Failure Time (years)")
        ax1.set_title("Mechanical Component Failure Times")
        ax1.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, time in zip(bars, failure_times):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f"{time:.1f}", ha="center", va="bottom")
        
        self.figure_tabs.add_figure("Failure Times", fig1)
        
        # Distribution comparison
        fig2 = Figure(figsize=(12, 6))
        ax2 = fig2.add_subplot(111)
        
        # Generate sample data for distributions
        x = np.linspace(0, 20, 100)
        mean_failure_time = np.mean(failure_times)
        
        # Exponential distribution
        exp_pdf = (1/mean_failure_time) * np.exp(-x/mean_failure_time)
        ax2.plot(x, exp_pdf, label="Exponential", linewidth=2, color="blue")
        
        # Weibull distribution (shape=2, scale=mean_failure_time)
        weibull_pdf = (2/mean_failure_time) * (x/mean_failure_time) * np.exp(-(x/mean_failure_time)**2)
        ax2.plot(x, weibull_pdf, label="Weibull", linewidth=2, color="red")
        
        ax2.set_xlabel("Time (years)")
        ax2.set_ylabel("Probability Density")
        ax2.set_title("Failure Time Distribution Comparison")
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        self.figure_tabs.add_figure("Distribution Comparison", fig2)


class EnhancedHomework1GUI(QMainWindow):
    """Enhanced GUI window for Homework 1 with integrated figure display."""
    
    def __init__(self) -> None:
        """Initialize the enhanced GUI."""
        super().__init__()
        self.problem_tabs: List[ProblemTabWidget] = []
        self.init_ui()
    
    def init_ui(self) -> None:
        """Initialize the user interface."""
        self.setWindowTitle("Homework 1 - Enhanced Scientific Machine Learning GUI")
        self.setGeometry(100, 100, 1400, 900)
        
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
        self.statusBar().showMessage("Ready - Enhanced GUI with Integrated Figures")
    
    def create_header(self) -> QFrame:
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
        subtitle_label = QLabel("Enhanced Interactive Problem Solver with Integrated Visualizations")
        subtitle_label.setFont(QFont("Arial", 12))
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)
        
        return header_frame
    
    def add_problem_tabs(self) -> None:
        """Add tabs for each problem."""
        problems = [
            {
                "title": "Problem 1: Tuberculosis Test",
                "file": "problem1_tuberculosis_test.py",
                "description": self.get_problem1_description(),
                "learning_objectives": [
                    "Understand Bayesian probability and Bayes' theorem",
                    "Calculate prior and posterior probabilities",
                    "Evaluate medical test accuracy and usefulness",
                    "Interpret likelihood ratios and odds ratios"
                ]
            },
            {
                "title": "Problem 2: Discrete Random Variables",
                "file": "problem2_discrete_random_variables.py",
                "description": self.get_problem2_description(),
                "learning_objectives": [
                    "Work with categorical random variables",
                    "Calculate expectation and variance",
                    "Visualize probability mass functions",
                    "Use scipy.stats for statistical analysis"
                ]
            },
            {
                "title": "Problem 3: Earthquake Prediction",
                "file": "problem3_earthquake_prediction.py",
                "description": self.get_problem3_description(),
                "learning_objectives": [
                    "Model rare events using Poisson processes",
                    "Analyze time series data",
                    "Make probabilistic predictions",
                    "Evaluate model fit and assumptions"
                ]
            },
            {
                "title": "Problem 4: Mechanical Failure",
                "file": "problem4_mechanical_failure.py",
                "description": self.get_problem4_description(),
                "learning_objectives": [
                    "Analyze failure time distributions",
                    "Fit exponential and Weibull distributions",
                    "Perform reliability analysis",
                    "Compare distribution fits using goodness-of-fit tests"
                ]
            }
        ]
        
        for problem in problems:
            problem_tab = ProblemTabWidget(problem)
            self.problem_tabs.append(problem_tab)
            self.tab_widget.addTab(problem_tab, problem["title"])
    
    def get_problem1_description(self) -> str:
        """Get description for Problem 1."""
        return """A medical test for tuberculosis has a sensitivity of 80% and specificity of 90%. 
The prevalence of tuberculosis in the population is 0.4%.

Calculate:
A. The prior probability of disease
B. The posterior probability of disease given a positive test result
C. The likelihood ratio and odds ratio
D. The positive predictive value (PPV) and negative predictive value (NPV)

This problem demonstrates Bayesian reasoning in medical diagnosis."""
    
    def get_problem2_description(self) -> str:
        """Get description for Problem 2."""
        return """Consider a discrete random variable X with the following probability mass function:
P(X = 0) = 0.3, P(X = 1) = 0.1, P(X = 2) = 0.2, P(X = 3) = 0.4

Calculate:
A. The expectation E[X]
B. The variance V[X]
C. Plot the probability mass function
D. Calculate the cumulative distribution function

This problem explores discrete probability distributions and their properties."""
    
    def get_problem3_description(self) -> str:
        """Get description for Problem 3."""
        return """Analyze major earthquake data from 1900-2019, with earthquakes occurring in the following decades:
1900-1909: 0, 1910-1919: 1, 1920-1929: 2, 1930-1939: 0, 1940-1949: 3,
1950-1959: 2, 1960-1969: 1, 1970-1979: 2, 1980-1989: 1, 1990-1999: 2,
2000-2009: 1, 2010-2019: 0

Model this as a Poisson process and:
A. Calculate the mean and variance
B. Fit a Poisson distribution to the data
C. Predict the probability of 1+ and 2+ earthquakes in the next decade
D. Evaluate the model fit

This problem demonstrates modeling rare events with Poisson processes."""
    
    def get_problem4_description(self) -> str:
        """Get description for Problem 4."""
        return """Analyze failure time data for mechanical components:
Gear 1: 10.5 years, Gear 2: 7.5 years, Gear 3: 12.0 years,
Gear 4: 8.2 years, Gear 5: 15.1 years

Perform reliability analysis:
A. Calculate basic statistics (mean, standard deviation)
B. Fit exponential and Weibull distributions
C. Compare distribution fits using goodness-of-fit tests
D. Make reliability predictions for future components

This problem explores reliability engineering and survival analysis."""


def main() -> None:
    """Main function to run the enhanced GUI application."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show the main window
    window = EnhancedHomework1GUI()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 