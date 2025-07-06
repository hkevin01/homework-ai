"""
Assignment Widget for Individual Homework Assignments

This module provides a detailed widget for displaying and interacting
with individual homework assignments.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QProcess, Qt, QThread, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSplitter,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ProblemRunner(QThread):
    """Thread for running problem solutions without blocking the GUI."""
    
    output_received = pyqtSignal(str)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self, problem_file: str, working_dir: str):
        super().__init__()
        self.problem_file = problem_file
        self.working_dir = working_dir
        self.process = None
        self.is_running = False
    
    def run(self):
        """Run the problem file and capture output."""
        self.is_running = True
        try:
            # Change to the working directory
            original_cwd = os.getcwd()
            os.chdir(self.working_dir)
            
            # Run the Python file
            self.process = subprocess.Popen(
                [sys.executable, self.problem_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read output line by line
            while self.is_running and self.process.poll() is None:
                if self.process.stdout:
                    line = self.process.stdout.readline()
                    if line:
                        self.output_received.emit(line.rstrip())
            
            # Get any remaining output
            if self.process.stdout:
                remaining_output = self.process.stdout.read()
                if remaining_output:
                    self.output_received.emit(remaining_output.rstrip())
            
            # Get stderr if there are errors
            if self.process.stderr:
                error_output = self.process.stderr.read()
                if error_output:
                    self.output_received.emit(f"⚠️ Warnings/Errors:\n{error_output.rstrip()}")
            
            # Wait for process to complete
            if self.is_running:
                self.process.wait()
                
                if self.process.returncode == 0:
                    self.output_received.emit("\n✅ Problem completed successfully!")
                else:
                    self.error_occurred.emit(f"Process exited with code {self.process.returncode}")
            
            # Restore original working directory
            os.chdir(original_cwd)
                
        except Exception as e:
            self.error_occurred.emit(f"Error running problem: {str(e)}")
        finally:
            self.is_running = False
            if self.process:
                try:
                    self.process.terminate()
                    self.process.wait(timeout=5)
                except:
                    pass
            self.finished.emit()
    
    def stop(self):
        """Stop the running process."""
        self.is_running = False
        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=3)
                if self.process.poll() is None:
                    self.process.kill()
            except:
                pass


class FigureWidget(QWidget):
    """Widget for displaying matplotlib figures."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figures = {}
        self.current_figure = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Create tab widget for multiple figures
        self.figure_tabs = QTabWidget()
        layout.addWidget(self.figure_tabs)
        
        # Add placeholder
        self.add_placeholder()
    
    def add_placeholder(self):
        """Add placeholder when no figures are available."""
        placeholder = QLabel("No figures available.\nRun a problem to see visualizations.")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setFont(QFont("Arial", 12))
        self.figure_tabs.addTab(placeholder, "No Figures")
    
    def clear_figures(self):
        """Clear all figures."""
        self.figures.clear()
        self.figure_tabs.clear()
        self.add_placeholder()
    
    def add_figure(self, title: str, figure: Figure):
        """Add a new figure to the widget."""
        # Remove placeholder if it exists
        if (self.figure_tabs.count() == 1 and 
            isinstance(self.figure_tabs.widget(0), QLabel)):
            self.figure_tabs.clear()
        
        # Create canvas
        canvas = FigureCanvas(figure)
        canvas.setMinimumSize(400, 300)
        
        # Add to tabs
        self.figure_tabs.addTab(canvas, title)
        self.figures[title] = figure
        
        # Switch to new figure
        self.figure_tabs.setCurrentWidget(canvas)


class ProblemWidget(QWidget):
    """Widget for displaying and running individual problems with detailed explanations."""
    
    def __init__(self, problem_data: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.problem_data = problem_data
        self.problem_runner = None
        self.solution_text = ""
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Create tab widget for different views
        self.problem_tabs = QTabWidget()
        layout.addWidget(self.problem_tabs)
        
        # Create different tabs
        self.create_question_tab()
        self.create_solution_tab()
        self.create_execution_tab()
        
    def create_question_tab(self):
        """Create the question/problem description tab."""
        question_widget = QWidget()
        layout = QVBoxLayout(question_widget)
        
        # Problem header
        header_group = QGroupBox(f"📋 Problem {self.problem_data['number']}: {self.problem_data['title']}")
        header_layout = QVBoxLayout(header_group)
        
        # Problem description
        desc_text = QTextEdit()
        desc_text.setReadOnly(True)
        
        # Enhanced problem description with extracted docstring
        problem_description = self.extract_problem_description()
        desc_text.setHtml(problem_description)
        
        header_layout.addWidget(desc_text)
        layout.addWidget(header_group)
        
        # Learning objectives
        if self.problem_data.get('learning_objectives'):
            obj_group = QGroupBox("🎯 Learning Objectives")
            obj_layout = QVBoxLayout(obj_group)
            
            for obj in self.problem_data['learning_objectives']:
                obj_label = QLabel(f"• {obj}")
                obj_label.setWordWrap(True)
                obj_label.setFont(QFont("Arial", 10))
                obj_layout.addWidget(obj_label)
            
            layout.addWidget(obj_group)
        
        self.problem_tabs.addTab(question_widget, "📋 Question")
    
    def create_solution_tab(self):
        """Create the solution explanation tab."""
        solution_widget = QWidget()
        layout = QVBoxLayout(solution_widget)
        
        # Solution explanation
        solution_group = QGroupBox("💡 Solution Approach")
        solution_layout = QVBoxLayout(solution_group)
        
        self.solution_text_widget = QTextEdit()
        self.solution_text_widget.setReadOnly(True)
        
        # Extract and display solution approach
        solution_content = self.extract_solution_approach()
        self.solution_text_widget.setHtml(solution_content)
        
        solution_layout.addWidget(self.solution_text_widget)
        layout.addWidget(solution_group)
        
        # Code snippets
        code_group = QGroupBox("💻 Key Code Concepts")
        code_layout = QVBoxLayout(code_group)
        
        self.code_concepts_widget = QTextEdit()
        self.code_concepts_widget.setReadOnly(True)
        self.code_concepts_widget.setFont(QFont("Courier", 9))
        
        # Extract key code concepts
        code_content = self.extract_code_concepts()
        self.code_concepts_widget.setHtml(code_content)
        
        code_layout.addWidget(self.code_concepts_widget)
        layout.addWidget(code_group)
        
        self.problem_tabs.addTab(solution_widget, "💡 Solution")
    
    def create_execution_tab(self):
        """Create the execution and results tab."""
        execution_widget = QWidget()
        layout = QVBoxLayout(execution_widget)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.run_button = QPushButton("▶️ Run Problem")
        self.run_button.clicked.connect(self.run_problem)
        button_layout.addWidget(self.run_button)
        
        self.stop_button = QPushButton("⏹️ Stop")
        self.stop_button.clicked.connect(self.stop_problem)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        clear_button = QPushButton("🗑️ Clear Output")
        clear_button.clicked.connect(self.clear_output)
        button_layout.addWidget(clear_button)
        
        view_code_button = QPushButton("👁️ View Source Code")
        view_code_button.clicked.connect(self.view_source_code)
        button_layout.addWidget(view_code_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Results area
        results_group = QGroupBox("📊 Execution Results")
        results_layout = QVBoxLayout(results_group)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Consolas", 9))
        self.output_text.setMinimumHeight(200)
        results_layout.addWidget(self.output_text)
        
        layout.addWidget(results_group)
        
        self.problem_tabs.addTab(execution_widget, "⚡ Execute")
    
    def extract_problem_description(self):
        """Extract detailed problem description from the source file."""
        try:
            if os.path.exists(self.problem_data['file_path']):
                with open(self.problem_data['file_path'], 'r') as f:
                    content = f.read()
                
                # Extract module docstring
                if '"""' in content:
                    start = content.find('"""')
                    end = content.find('"""', start + 3)
                    if end > start:
                        docstring = content[start+3:end].strip()
                        
                        # Parse the docstring for structured content
                        return self.format_problem_description(docstring)
                        
            return f"<p>{self.problem_data.get('description', 'No description available.')}</p>"
            
        except Exception as e:
            return f"<p>Error reading problem description: {str(e)}</p>"
    
    def format_problem_description(self, docstring):
        """Format the docstring into HTML with proper sections."""
        lines = docstring.split('\n')
        html = "<div style='font-family: Arial; line-height: 1.6;'>"
        
        current_section = ""
        in_list = False
        
        for line in lines:
            line = line.strip()
            if not line:
                if in_list:
                    html += "</ul>"
                    in_list = False
                html += "<br>"
                continue
            
            # Check for section headers
            lower_line = line.lower()
            if any(keyword in lower_line for keyword in ['learning objectives:', 'objectives:', 'goal:', 'purpose:']):
                if in_list:
                    html += "</ul>"
                html += f"<h4>🎯 Learning Objectives</h4>"
                in_list = False
                current_section = "objectives"
            elif any(keyword in lower_line for keyword in ['example:', 'examples:', 'scenario:']):
                if in_list:
                    html += "</ul>"
                html += f"<h4>📝 Example</h4>"
                in_list = False
                current_section = "example"
            elif any(keyword in lower_line for keyword in ['task:', 'tasks:', 'implement:', 'requirements:']):
                if in_list:
                    html += "</ul>"
                html += f"<h4>✅ Tasks</h4>"
                in_list = False
                current_section = "tasks"
            elif line.startswith('-') or line.startswith('*'):
                # List item
                if not in_list:
                    html += "<ul>"
                    in_list = True
                html += f"<li>{line[1:].strip()}</li>"
            else:
                # Regular text
                if in_list:
                    html += "</ul>"
                    in_list = False
                if current_section == "":
                    html += f"<p><strong>{line}</strong></p>"
                    current_section = "main"
                else:
                    html += f"<p>{line}</p>"
        
        if in_list:
            html += "</ul>"
        
        html += "</div>"
        return html
    
    def extract_solution_approach(self):
        """Extract solution approach and methodology from the source code."""
        try:
            if not os.path.exists(self.problem_data['file_path']):
                return "<p>Source file not found.</p>"
            
            with open(self.problem_data['file_path'], 'r') as f:
                content = f.read()
            
            html = "<div style='font-family: Arial; line-height: 1.6;'>"
            
            # Extract function definitions and their docstrings
            import re

            # Find function definitions
            func_pattern = r'def\s+(\w+)\s*\([^)]*\):\s*"""([^"]+)"""'
            functions = re.findall(func_pattern, content, re.DOTALL)
            
            if functions:
                html += "<h4>🔧 Key Functions</h4>"
                for func_name, docstring in functions:
                    if not func_name.startswith('_'):  # Skip private functions
                        html += f"""
                        <div style='border-left: 3px solid #007bff; padding-left: 10px; margin: 10px 0;'>
                            <h5><code>{func_name}()</code></h5>
                            <p>{docstring.strip()}</p>
                        </div>
                        """
            
            # Extract class definitions
            class_pattern = r'class\s+(\w+).*?:\s*"""([^"]+)"""'
            classes = re.findall(class_pattern, content, re.DOTALL)
            
            if classes:
                html += "<h4>📦 Key Classes</h4>"
                for class_name, docstring in classes:
                    html += f"""
                    <div style='border-left: 3px solid #28a745; padding-left: 10px; margin: 10px 0;'>
                        <h5><code>{class_name}</code></h5>
                        <p>{docstring.strip()}</p>
                    </div>
                    """
            
            # Extract mathematical concepts (look for formulas and equations)
            if any(keyword in content for keyword in ['np.', 'scipy.', 'stats.', 'probability', 'bayes']):
                html += "<h4>📊 Mathematical Concepts</h4>"
                html += "<ul>"
                
                if 'bayes' in content.lower() or 'posterior' in content.lower():
                    html += "<li><strong>Bayesian Inference:</strong> Using prior knowledge to update beliefs with new evidence</li>"
                
                if 'np.random' in content or 'random' in content:
                    html += "<li><strong>Random Sampling:</strong> Generating random samples for simulation and analysis</li>"
                
                if 'plt.' in content or 'matplotlib' in content:
                    html += "<li><strong>Data Visualization:</strong> Creating plots to understand data and results</li>"
                
                if 'scipy.stats' in content:
                    html += "<li><strong>Statistical Distributions:</strong> Working with probability distributions</li>"
                
                html += "</ul>"
            
            html += "</div>"
            return html
            
        except Exception as e:
            return f"<p>Error analyzing solution: {str(e)}</p>"
    
    def extract_code_concepts(self):
        """Extract and explain key code concepts."""
        try:
            if not os.path.exists(self.problem_data['file_path']):
                return "<p>Source file not found.</p>"
            
            with open(self.problem_data['file_path'], 'r') as f:
                content = f.read()
            
            html = "<div style='font-family: Courier; font-size: 12px;'>"
            
            # Show key imports with explanations
            import_lines = [line.strip() for line in content.split('\n') if line.strip().startswith('import') or line.strip().startswith('from')]
            
            if import_lines:
                html += "<h4>📚 Key Libraries Used</h4>"
                html += "<div style='background-color: #f8f9fa; padding: 10px; border-radius: 4px;'>"
                
                for imp in import_lines[:10]:  # Show first 10 imports
                    html += f"<code>{imp}</code><br>"
                    
                    # Add explanations for common imports
                    if 'numpy' in imp:
                        html += "<small style='color: #666;'>→ Numerical computing and arrays</small><br>"
                    elif 'matplotlib' in imp:
                        html += "<small style='color: #666;'>→ Data visualization and plotting</small><br>"
                    elif 'scipy' in imp:
                        html += "<small style='color: #666;'>→ Scientific computing and statistics</small><br>"
                    elif 'pandas' in imp:
                        html += "<small style='color: #666;'>→ Data manipulation and analysis</small><br>"
                
                html += "</div><br>"
            
            # Show key variable assignments or calculations
            lines = content.split('\n')
            key_concepts = []
            
            for i, line in enumerate(lines):
                line = line.strip()
                if ('=' in line and not line.startswith('#') and not line.startswith('def') 
                    and not line.startswith('class') and len(line) < 80):
                    
                    # Skip simple assignments like x = 1
                    if any(keyword in line for keyword in ['np.', 'stats.', 'plt.', 'scipy.', 'random']):
                        key_concepts.append((i+1, line))
            
            if key_concepts:
                html += "<h4>🔑 Key Computational Steps</h4>"
                html += "<div style='background-color: #f8f9fa; padding: 10px; border-radius: 4px;'>"
                
                for line_num, code_line in key_concepts[:8]:  # Show first 8 key lines
                    html += f"<div style='margin: 5px 0;'>"
                    html += f"<small style='color: #999;'>Line {line_num}:</small><br>"
                    html += f"<code style='color: #d63384;'>{code_line}</code>"
                    html += "</div>"
                
                html += "</div>"
            
            html += "</div>"
            return html
            
        except Exception as e:
            return f"<p>Error extracting code concepts: {str(e)}</p>"
    
    def view_source_code(self):
        """Show the complete source code in a new dialog."""
        try:
            if os.path.exists(self.problem_data['file_path']):
                with open(self.problem_data['file_path'], 'r') as f:
                    source_code = f.read()
                
                # Create a dialog to show source code
                dialog = QMessageBox()
                dialog.setWindowTitle(f"Source Code: {self.problem_data['file_name']}")
                dialog.setText("Complete source code:")
                dialog.setDetailedText(source_code)
                dialog.setStandardButtons(QMessageBox.Ok)
                dialog.exec_()
            else:
                QMessageBox.warning(self, "File Not Found", 
                                  f"Source file not found: {self.problem_data['file_name']}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error reading source file: {str(e)}")
    
    def run_problem(self):
        """Run the problem file."""
        if not os.path.exists(self.problem_data['file_path']):
            QMessageBox.warning(self, "File Not Found", 
                              f"Problem file not found: {self.problem_data['file_name']}")
            return
        
        # Stop any existing runner
        if hasattr(self, 'problem_runner') and self.problem_runner:
            self.problem_runner.stop()
            self.problem_runner.wait(3000)  # Wait up to 3 seconds
            self.problem_runner.deleteLater()
        
        # Clear previous output
        self.clear_output()
        
        # Set up UI for running state
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        # Start problem runner
        working_dir = os.path.dirname(self.problem_data['file_path'])
        self.problem_runner = ProblemRunner(self.problem_data['file_name'], working_dir)
        self.problem_runner.output_received.connect(self.append_output)
        self.problem_runner.error_occurred.connect(self.show_error)
        self.problem_runner.finished.connect(self.on_problem_finished)
        self.problem_runner.start()
    
    def stop_problem(self):
        """Stop the running problem."""
        if hasattr(self, 'problem_runner') and self.problem_runner:
            self.problem_runner.stop()
    
    def on_problem_finished(self):
        """Handle problem completion."""
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        # Clean up the thread
        if hasattr(self, 'problem_runner') and self.problem_runner:
            self.problem_runner.wait(1000)  # Wait up to 1 second
            self.problem_runner.deleteLater()
            self.problem_runner = None
    
    def append_output(self, text: str):
        """Append text to the output area."""
        self.output_text.append(text)
        # Auto-scroll to bottom
        cursor = self.output_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.output_text.setTextCursor(cursor)
    
    def show_error(self, error_msg: str):
        """Show an error message."""
        self.append_output(f"\n❌ Error: {error_msg}")
    
    def clear_output(self):
        """Clear the output area."""
        self.output_text.clear()
    
    def closeEvent(self, event):
        """Handle widget close event."""
        # Stop any running problem
        if hasattr(self, 'problem_runner') and self.problem_runner:
            self.problem_runner.stop()
            self.problem_runner.wait(3000)  # Wait up to 3 seconds
            self.problem_runner.deleteLater()
        event.accept()


class AssignmentWidget(QWidget):
    """Main widget for displaying a homework assignment."""
    
    def __init__(self, assignment_data: Dict[str, Any], homework_manager, parent=None):
        super().__init__(parent)
        self.assignment_data = assignment_data
        self.homework_manager = homework_manager
        self.problem_widgets = {}
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Assignment header
        header_layout = QHBoxLayout()
        
        title_label = QLabel(f"Homework {self.assignment_data['number']}: {self.assignment_data['title']}")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Status label
        status_label = QLabel(f"Status: {self.assignment_data.get('status', 'Unknown')}")
        status_label.setFont(QFont("Arial", 10))
        header_layout.addWidget(status_label)
        
        layout.addLayout(header_layout)
        
        # Assignment description
        if self.assignment_data.get('description'):
            desc_group = QGroupBox("Description")
            desc_layout = QVBoxLayout(desc_group)
            
            desc_text = QTextEdit()
            desc_text.setPlainText(self.assignment_data['description'])
            desc_text.setReadOnly(True)
            desc_text.setMaximumHeight(100)
            desc_layout.addWidget(desc_text)
            
            layout.addWidget(desc_group)
        
        # Create tab widget for problems
        self.problem_tabs = QTabWidget()
        layout.addWidget(self.problem_tabs)
        
        # Add overview tab
        self.create_overview_tab()
        
        # Add problem tabs
        for problem in self.assignment_data.get('problems', []):
            self.create_problem_tab(problem)
        
        # If no problems found, show message
        if not self.assignment_data.get('problems'):
            self.create_no_problems_tab()
    
    def create_overview_tab(self):
        """Create the overview tab."""
        overview_widget = QWidget()
        layout = QVBoxLayout(overview_widget)
        
        # Assignment info
        info_group = QGroupBox("Assignment Information")
        info_layout = QVBoxLayout(info_group)
        
        info_text = f"""
        <b>Assignment:</b> Homework {self.assignment_data['number']}<br>
        <b>Title:</b> {self.assignment_data['title']}<br>
        <b>Status:</b> {self.assignment_data.get('status', 'Unknown')}<br>
        <b>Problems:</b> {len(self.assignment_data.get('problems', []))}<br>
        <b>Files:</b> {len(self.assignment_data.get('files', []))}<br>
        <b>Topics:</b> {', '.join(self.assignment_data.get('topics', ['Not specified']))}
        """
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)
        
        layout.addWidget(info_group)
        
        # Files list
        if self.assignment_data.get('files'):
            files_group = QGroupBox("Files")
            files_layout = QVBoxLayout(files_group)
            
            files_list = QListWidget()
            for file_name in self.assignment_data['files']:
                files_list.addItem(file_name)
            files_layout.addWidget(files_list)
            
            layout.addWidget(files_group)
        
        layout.addStretch()
        
        self.problem_tabs.addTab(overview_widget, "Overview")
    
    def create_problem_tab(self, problem_data: Dict[str, Any]):
        """Create a tab for an individual problem."""
        problem_widget = ProblemWidget(problem_data)
        tab_title = f"Problem {problem_data['number']}"
        self.problem_tabs.addTab(problem_widget, tab_title)
        
        problem_id = problem_data['number']
        self.problem_widgets[problem_id] = problem_widget
    
    def create_no_problems_tab(self):
        """Create a tab when no problems are found."""
        no_problems_widget = QWidget()
        layout = QVBoxLayout(no_problems_widget)
        
        message_label = QLabel("No problems found in this assignment.")
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setFont(QFont("Arial", 12))
        layout.addWidget(message_label)
        
        help_label = QLabel("Make sure problem files are named with 'problem' in the filename.")
        help_label.setAlignment(Qt.AlignCenter)
        help_label.setFont(QFont("Arial", 10))
        help_label.setStyleSheet("color: gray;")
        layout.addWidget(help_label)
        
        self.problem_tabs.addTab(no_problems_widget, "No Problems")
    
    def closeEvent(self, event):
        """Handle widget close event."""
        # Stop any running problems in all problem widgets
        for problem_widget in self.problem_widgets.values():
            if hasattr(problem_widget, 'problem_runner') and problem_widget.problem_runner:
                problem_widget.problem_runner.stop()
                problem_widget.problem_runner.wait(3000)
                problem_widget.problem_runner.deleteLater()
        event.accept()
