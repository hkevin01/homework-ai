#!/usr/bin/env python3
"""
Scientific Machine Learning Homework GUI Application

A PyQt5 application for managing and running homework assignments.
"""

import os
import sys
from pathlib import Path

# Add src directory to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

try:
    from PyQt5.QtCore import Qt, QThread, QTimer, pyqtSignal
    from PyQt5.QtGui import QFont
    from PyQt5.QtWidgets import (
        QApplication,
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QListWidget,
        QMainWindow,
        QMessageBox,
        QProgressBar,
        QPushButton,
        QSplitter,
        QStatusBar,
        QTabWidget,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )
except ImportError:
    print("PyQt5 is required but not installed.")
    print("Please install it with: pip install PyQt5")
    sys.exit(1)

import subprocess
import threading
from typing import Dict, List, Optional


class HomeworkRunner(QThread):
    """Thread for running homework problems."""
    
    output_received = pyqtSignal(str)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self, script_path: str, working_dir: str):
        super().__init__()
        self.script_path = script_path
        self.working_dir = working_dir
        self.process = None
    
    def run(self):
        """Run the homework script."""
        try:
            os.chdir(self.working_dir)
            
            self.process = subprocess.Popen(
                [sys.executable, self.script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    self.output_received.emit(line.rstrip())
            
            self.process.wait()
            
            if self.process.returncode == 0:
                self.output_received.emit("\n✅ Completed successfully!")
            else:
                self.error_occurred.emit(f"Process exited with code {self.process.returncode}")
                
        except Exception as e:
            self.error_occurred.emit(f"Error: {str(e)}")
        finally:
            self.finished.emit()


class HomeworkGUI(QMainWindow):
    """Main homework GUI application."""
    
    def __init__(self):
        super().__init__()
        self.homework_runners = {}
        self.init_ui()
        self.discover_assignments()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("🎓 Scientific ML Homework Assistant")
        self.setMinimumSize(1000, 700)
        
        # Set stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 6px;
                margin-top: 1ex;
                padding-top: 12px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
                background-color: white;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title_label = QLabel("🎓 Scientific Machine Learning Homework Assistant")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("padding: 20px; color: #343a40;")
        main_layout.addWidget(title_label)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create overview tab
        self.create_overview_tab()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def create_overview_tab(self):
        """Create the main overview tab."""
        overview_widget = QWidget()
        layout = QVBoxLayout(overview_widget)
        
        # Create splitter
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Left panel - assignments list
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        assignments_group = QGroupBox("📚 Available Assignments")
        assignments_layout = QVBoxLayout(assignments_group)
        
        self.assignments_list = QListWidget()
        assignments_layout.addWidget(self.assignments_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.run_button = QPushButton("▶️ Run Selected")
        self.run_button.clicked.connect(self.run_selected_assignment)
        button_layout.addWidget(self.run_button)
        
        refresh_button = QPushButton("🔄 Refresh")
        refresh_button.clicked.connect(self.discover_assignments)
        button_layout.addWidget(refresh_button)
        
        assignments_layout.addLayout(button_layout)
        left_layout.addWidget(assignments_group)
        
        # Right panel - output
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        output_group = QGroupBox("📄 Output")
        output_layout = QVBoxLayout(output_group)
        
        self.output_text = QTextEdit()
        self.output_text.setFont(QFont("Consolas", 10))
        self.output_text.setReadOnly(True)
        output_layout.addWidget(self.output_text)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        output_layout.addWidget(self.progress_bar)
        
        # Clear button
        clear_button = QPushButton("🗑️ Clear Output")
        clear_button.clicked.connect(self.clear_output)
        output_layout.addWidget(clear_button)
        
        right_layout.addWidget(output_group)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])
        
        # Add tab
        self.tab_widget.addTab(overview_widget, "📋 Overview")
    
    def discover_assignments(self):
        """Discover available homework assignments."""
        self.assignments_list.clear()
        self.assignments = []
        
        # Look in src directory for homework folders
        src_path = Path(__file__).parent / "src"
        
        if src_path.exists():
            for homework_dir in sorted(src_path.glob("homework*")):
                if homework_dir.is_dir():
                    # Find Python files in the homework directory
                    problems = list(homework_dir.glob("problem*.py"))
                    
                    if problems:
                        hw_number = ''.join(filter(str.isdigit, homework_dir.name))
                        
                        # Try to read metadata
                        metadata_file = homework_dir / "metadata.json"
                        title = f"Homework {hw_number}"
                        
                        if metadata_file.exists():
                            try:
                                import json
                                with open(metadata_file, 'r') as f:
                                    metadata = json.load(f)
                                    title = f"HW {hw_number}: {metadata.get('title', f'Homework {hw_number}')}"
                            except:
                                pass
                        
                        # Add assignment
                        assignment = {
                            'title': title,
                            'directory': homework_dir,
                            'problems': problems
                        }
                        self.assignments.append(assignment)
                        self.assignments_list.addItem(title)
        
        if not self.assignments:
            self.assignments_list.addItem("No assignments found")
            self.output_text.append("No homework assignments found in src/ directory.")
        else:
            self.status_bar.showMessage(f"Found {len(self.assignments)} assignments")
            self.output_text.append(f"📚 Discovered {len(self.assignments)} homework assignments")
    
    def run_selected_assignment(self):
        """Run the selected assignment."""
        current_row = self.assignments_list.currentRow()
        
        if current_row < 0 or current_row >= len(self.assignments):
            QMessageBox.warning(self, "No Selection", "Please select an assignment to run.")
            return
        
        assignment = self.assignments[current_row]
        
        # Show available problems
        problems = assignment['problems']
        if not problems:
            QMessageBox.information(self, "No Problems", "No problem files found in this assignment.")
            return
        
        # For now, run the first problem
        problem_file = problems[0]
        self.run_problem(problem_file, assignment['directory'])
    
    def run_problem(self, problem_file: Path, working_dir: Path):
        """Run a specific problem file."""
        self.output_text.append(f"\n🚀 Running {problem_file.name}...")
        self.output_text.append("=" * 50)
        
        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.run_button.setEnabled(False)
        
        # Create and start runner
        runner = HomeworkRunner(problem_file.name, str(working_dir))
        runner.output_received.connect(self.append_output)
        runner.error_occurred.connect(self.show_error)
        runner.finished.connect(self.on_run_finished)
        runner.start()
        
        # Store runner reference
        self.homework_runners[runner] = True
    
    def append_output(self, text: str):
        """Append text to output area."""
        self.output_text.append(text)
        # Auto-scroll to bottom
        cursor = self.output_text.textCursor()
        cursor.movePosition(cursor.End)
        self.output_text.setTextCursor(cursor)
    
    def show_error(self, error_msg: str):
        """Show error message."""
        self.append_output(f"❌ Error: {error_msg}")
    
    def on_run_finished(self):
        """Handle completion of problem run."""
        self.progress_bar.setVisible(False)
        self.run_button.setEnabled(True)
        self.status_bar.showMessage("Ready")
        
        # Clean up runner reference
        sender = self.sender()
        if sender in self.homework_runners:
            del self.homework_runners[sender]
    
    def clear_output(self):
        """Clear the output text."""
        self.output_text.clear()
        self.status_bar.showMessage("Output cleared")


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application properties
    app.setApplicationName("Scientific ML Homework")
    app.setApplicationVersion("1.0")
    
    try:
        # Create and show main window
        window = HomeworkGUI()
        window.show()
        
        # Run the application
        return app.exec_()
    
    except Exception as e:
        print(f"Error starting application: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
