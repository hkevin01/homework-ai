"""
Main Application for Scientific Machine Learning Homework GUI

This module provides a centralized PyQt application for managing and running
multiple homework assignments with a modern, tabbed interface.
"""

import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
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

from assignment_widget import AssignmentWidget
from homework_manager import HomeworkManager


class MainApplication(QMainWindow):
    """Main application window for the Scientific ML homework GUI."""
    
    def __init__(self):
        super().__init__()
        self.homework_manager = HomeworkManager()
        self.assignment_widgets = {}
        self.settings = QSettings("HomeworkAI", "SciMLHomework")
        
        self.init_ui()
        self.setup_menu_bar()
        self.setup_status_bar()
        self.load_settings()
        self.load_assignments()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Scientific Machine Learning - Homework Assistant")
        self.setMinimumSize(1200, 800)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e1e1e1;
                border: 1px solid #c0c0c0;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom-color: white;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create main tab widget
        self.main_tabs = QTabWidget()
        main_layout.addWidget(self.main_tabs)
        
        # Add overview tab
        self.create_overview_tab()
    
    def create_overview_tab(self):
        """Create the overview tab showing all assignments."""
        overview_widget = QWidget()
        layout = QVBoxLayout(overview_widget)
        
        # Title
        title_label = QLabel("Scientific Machine Learning Homework Assistant")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Create splitter for two-column layout
        splitter = QSplitter(QtCore.Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        # Left side: Assignment list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        assignments_group = QGroupBox("Available Assignments")
        assignments_layout = QVBoxLayout(assignments_group)
        
        self.assignment_list = QListWidget()
        self.assignment_list.itemClicked.connect(self.on_assignment_selected)
        assignments_layout.addWidget(self.assignment_list)
        
        # Buttons for assignment management
        button_layout = QHBoxLayout()
        
        open_button = QPushButton("Open Assignment")
        open_button.clicked.connect(self.open_selected_assignment)
        button_layout.addWidget(open_button)
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_assignments)
        button_layout.addWidget(refresh_button)
        
        assignments_layout.addLayout(button_layout)
        left_layout.addWidget(assignments_group)
        
        # Right side: Assignment details
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        details_group = QGroupBox("Assignment Details")
        details_layout = QVBoxLayout(details_group)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        details_layout.addWidget(self.details_text)
        
        right_layout.addWidget(details_group)
        
        # Add widgets to splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 600])
        
        # Add overview tab
        self.main_tabs.addTab(overview_widget, "Overview")
    
    def setup_menu_bar(self):
        """Set up the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        new_action = QAction('New Assignment', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_assignment)
        file_menu.addAction(new_action)
        
        open_action = QAction('Open Assignment Folder', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_assignment_folder)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        refresh_action = QAction('Refresh All', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.refresh_assignments)
        view_menu.addAction(refresh_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_status_bar(self):
        """Set up the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        self.status_bar.showMessage("Ready")
    
    def load_settings(self):
        """Load application settings."""
        # Restore window geometry
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        
        # Restore window state
        state = self.settings.value("windowState")
        if state:
            self.restoreState(state)
    
    def save_settings(self):
        """Save application settings."""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
    
    def load_assignments(self):
        """Load available assignments."""
        assignments = self.homework_manager.get_available_assignments()
        
        self.assignment_list.clear()
        for assignment in assignments:
            self.assignment_list.addItem(f"Homework {assignment['number']}: {assignment['title']}")
        
        if assignments:
            self.assignment_list.setCurrentRow(0)
            self.on_assignment_selected()
    
    def refresh_assignments(self):
        """Refresh the list of assignments."""
        self.homework_manager.refresh()
        self.load_assignments()
        self.status_bar.showMessage("Assignments refreshed", 2000)
    
    def on_assignment_selected(self):
        """Handle assignment selection."""
        current_row = self.assignment_list.currentRow()
        if current_row >= 0:
            assignments = self.homework_manager.get_available_assignments()
            if current_row < len(assignments):
                assignment = assignments[current_row]
                self.show_assignment_details(assignment)
    
    def show_assignment_details(self, assignment):
        """Show details for the selected assignment."""
        details = f"""
        <h2>📚 Homework {assignment['number']}: {assignment['title']}</h2>
        
        <h3>📝 Assignment Overview</h3>
        <p>{assignment.get('description', 'No description available.')}</p>
        
        <h3>🎯 Learning Objectives</h3>
        <ul>
        """
        
        # Add learning objectives from topics
        for topic in assignment.get('topics', ['General understanding']):
            details += f"<li>Master concepts in {topic}</li>"
        
        details += "</ul>"
        
        # Add problems section with detailed descriptions and actual questions
        if assignment.get('problems'):
            details += "<h3>🧩 Problems & Questions</h3>"
            for i, problem in enumerate(assignment['problems'], 1):
                # Get the actual question from the problem data
                question_text = problem.get('question', 'Question not available.')
                
                # Truncate long questions for overview
                if len(question_text) > 200:
                    question_preview = question_text[:200] + "..."
                else:
                    question_preview = question_text
                
                details += f"""
                <div style="border: 1px solid #ddd; margin: 10px 0; padding: 15px; background-color: #f9f9f9; border-radius: 8px;">
                    <h4 style="color: #2c3e50; margin-top: 0;">Problem {problem.get('number', i)}: {problem.get('title', 'Untitled')}</h4>
                    
                    <div style="background-color: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; margin: 10px 0;">
                        <strong>📋 Question:</strong><br>
                        <em>{question_preview}</em>
                    </div>
                    
                    <p><strong>📖 Description:</strong><br>
                    {problem.get('description', 'No description available.')}</p>
                    
                    <details style="margin: 10px 0;">
                        <summary style="cursor: pointer; font-weight: bold; color: #495057;">🎯 What you'll learn (click to expand)</summary>
                        <ul style="margin: 10px 0;">
                """
                
                for objective in problem.get('learning_objectives', ['Problem-solving skills']):
                    details += f"<li>{objective}</li>"
                
                solution_approach = problem.get('solution_approach', '')
                if solution_approach and solution_approach != "No solution approach described.":
                    details += f"""
                        </ul>
                        <p><strong>💡 Solution Approach:</strong><br>
                        <em>{solution_approach}</em></p>
                    </details>
                    """
                else:
                    details += "</ul></details>"
                
                details += f"""
                    <div style="margin-top: 10px; font-size: 0.9em; color: #6c757d;">
                        <strong>📄 File:</strong> <code>{problem.get('file_name', 'Unknown')}</code>
                    </div>
                </div>
                """
        
        # Add implementation details
        details += f"""
        <h3>📊 Assignment Statistics</h3>
        <div style="background-color: #e9ecef; padding: 15px; border-radius: 8px;">
            <table style="border-collapse: collapse; width: 100%;">
                <tr><td style="padding: 5px;"><strong>Status:</strong></td><td style="padding: 5px;">{assignment.get('status', 'Not started')}</td></tr>
                <tr><td style="padding: 5px;"><strong>Total Problems:</strong></td><td style="padding: 5px;">{len(assignment.get('problems', []))}</td></tr>
                <tr><td style="padding: 5px;"><strong>Source Files:</strong></td><td style="padding: 5px;">{len(assignment.get('files', []))}</td></tr>
                <tr><td style="padding: 5px;"><strong>Topics Covered:</strong></td><td style="padding: 5px;">{', '.join(assignment.get('topics', ['Not specified']))}</td></tr>
            </table>
        </div>
        
        <h3>📁 Assignment Files</h3>
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px;">
        """
        
        # Show first 10 files
        files = assignment.get('files', ['No files found'])
        for file_name in files[:10]:
            if file_name.endswith('.py'):
                icon = "🐍"
            elif file_name.endswith('.md'):
                icon = "📝"
            elif file_name.endswith('.json'):
                icon = "⚙️"
            else:
                icon = "📄"
            details += f"<div style='margin: 5px 0;'>{icon} <code>{file_name}</code></div>"
        
        if len(files) > 10:
            details += f"<div style='margin: 5px 0; font-style: italic; color: #6c757d;'>... and {len(files) - 10} more files</div>"
        
        details += """
        </div>
        
        <div style="background-color: #d1ecf1; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #17a2b8;">
            <p style="margin: 0;"><strong>💡 Quick Start:</strong> Click "Open Assignment" above to view detailed questions, solutions, and run the problems interactively!</p>
        </div>
        """
        
        self.details_text.setHtml(details)
    
    def open_selected_assignment(self):
        """Open the selected assignment in a new tab."""
        current_row = self.assignment_list.currentRow()
        if current_row >= 0:
            assignments = self.homework_manager.get_available_assignments()
            if current_row < len(assignments):
                assignment = assignments[current_row]
                self.open_assignment_tab(assignment)
    
    def open_assignment_tab(self, assignment):
        """Open an assignment in a new tab."""
        assignment_id = f"hw{assignment['number']}"
        
        # Check if tab already exists
        for i in range(self.main_tabs.count()):
            if self.main_tabs.widget(i).property("assignment_id") == assignment_id:
                self.main_tabs.setCurrentIndex(i)
                return
        
        # Create new assignment widget
        assignment_widget = AssignmentWidget(assignment, self.homework_manager)
        assignment_widget.setProperty("assignment_id", assignment_id)
        
        # Add tab
        tab_title = f"HW {assignment['number']}"
        tab_index = self.main_tabs.addTab(assignment_widget, tab_title)
        self.main_tabs.setCurrentIndex(tab_index)
        
        # Store reference
        self.assignment_widgets[assignment_id] = assignment_widget
    
    def new_assignment(self):
        """Create a new assignment."""
        # This could open a dialog to create a new assignment structure
        QMessageBox.information(self, "New Assignment", 
                              "This feature will be implemented to create new assignment templates.")
    
    def open_assignment_folder(self):
        """Open an assignment folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Assignment Folder")
        if folder:
            # Load assignment from folder
            self.homework_manager.load_assignment_from_folder(folder)
            self.refresh_assignments()
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(self, "About",
                         """
                         <h3>Scientific Machine Learning Homework Assistant</h3>
                         <p>A PyQt application for managing and running scientific machine learning homework assignments.</p>
                         <p>Version 1.0</p>
                         <p>Built with PyQt5 and Python</p>
                         """)
    
    def closeEvent(self, event):
        """Handle application close event."""
        self.save_settings()
        event.accept()


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better appearance
    
    # Set application metadata
    app.setApplicationName("Scientific Machine Learning Homework")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("HomeworkAI")
    
    # Create and show main window
    window = MainApplication()
    window.show()
    
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
