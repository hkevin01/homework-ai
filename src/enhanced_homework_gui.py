"""
Enhanced Scientific Machine Learning Homework GUI

A refined PyQt5 application for managing and running homework assignments
with improved user interface and better organization.
"""

import os
import sys
from pathlib import Path

try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
except ImportError:
    print("PyQt5 is required but not installed. Please install it with:")
    print("pip install PyQt5")
    sys.exit(1)

# Import our custom modules
try:
    from assignment_widget import AssignmentWidget
    from homework_manager import HomeworkManager
except ImportError:
    # Handle the case where we're running from different directory
    current_dir = Path(__file__).parent
    sys.path.append(str(current_dir))
    from assignment_widget import AssignmentWidget
    from homework_manager import HomeworkManager


class HomeworkMainWindow(QMainWindow):
    """Main window for the Scientific Machine Learning Homework Assistant."""
    
    def __init__(self):
        super().__init__()
        self.homework_manager = HomeworkManager()
        self.assignment_widgets = {}
        self.settings = QSettings("HomeworkAI", "SciMLHomework")
        
        self.init_ui()
        self.load_settings()
        self.load_assignments()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Scientific ML Homework Assistant")
        self.setMinimumSize(1000, 700)
        
        # Apply modern styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                background-color: white;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #e9ecef;
                border: 1px solid #dee2e6;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom-color: white;
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
                padding: 0 8px 0 8px;
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
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create main tab widget
        self.main_tabs = QTabWidget()
        main_layout.addWidget(self.main_tabs)
        
        # Create overview tab
        self.create_overview_tab()
        
        # Create menu bar and status bar
        self.create_menu_bar()
        self.create_status_bar()
    
    def create_overview_tab(self):
        """Create the main overview tab."""
        overview_widget = QWidget()
        layout = QVBoxLayout(overview_widget)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("🎓 Scientific Machine Learning Homework Assistant")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #343a40; padding: 20px;")
        header_layout.addWidget(title_label)
        layout.addLayout(header_layout)
        
        # Main content area
        content_splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(content_splitter)
        
        # Left panel: Assignment list
        left_panel = self.create_assignments_panel()
        content_splitter.addWidget(left_panel)
        
        # Right panel: Assignment details
        right_panel = self.create_details_panel()
        content_splitter.addWidget(right_panel)
        
        # Set splitter proportions
        content_splitter.setSizes([400, 600])
        
        # Add overview tab
        self.main_tabs.addTab(overview_widget, "📋 Overview")
    
    def create_assignments_panel(self):
        """Create the assignments list panel."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Assignments group
        assignments_group = QGroupBox("📚 Available Assignments")
        assignments_layout = QVBoxLayout(assignments_group)
        
        self.assignment_list = QListWidget()
        self.assignment_list.setMinimumHeight(300)
        self.assignment_list.itemClicked.connect(self.on_assignment_selected)
        self.assignment_list.itemDoubleClicked.connect(self.open_selected_assignment)
        assignments_layout.addWidget(self.assignment_list)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        open_btn = QPushButton("📖 Open")
        open_btn.clicked.connect(self.open_selected_assignment)
        button_layout.addWidget(open_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_assignments)
        button_layout.addWidget(refresh_btn)
        
        assignments_layout.addLayout(button_layout)
        layout.addWidget(assignments_group)
        
        return panel
    
    def create_details_panel(self):
        """Create the assignment details panel."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        details_group = QGroupBox("📄 Assignment Details")
        details_layout = QVBoxLayout(details_group)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMinimumHeight(300)
        details_layout.addWidget(self.details_text)
        
        layout.addWidget(details_group)
        
        # Quick actions
        actions_group = QGroupBox("⚡ Quick Actions")
        actions_layout = QHBoxLayout(actions_group)
        
        run_all_btn = QPushButton("▶️ Run All Problems")
        run_all_btn.clicked.connect(self.run_all_problems)
        actions_layout.addWidget(run_all_btn)
        
        view_files_btn = QPushButton("📁 View Files")
        view_files_btn.clicked.connect(self.view_assignment_files)
        actions_layout.addWidget(view_files_btn)
        
        layout.addWidget(actions_group)
        
        return panel
    
    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        new_action = QAction('&New Assignment...', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_assignment)
        file_menu.addAction(new_action)
        
        open_action = QAction('&Open Folder...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close_application)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('&View')
        
        refresh_action = QAction('&Refresh', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.refresh_assignments)
        view_menu.addAction(refresh_action)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_status_bar(self):
        """Create the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        self.status_bar.showMessage("Ready")
    
    def load_settings(self):
        """Load application settings."""
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        
        state = self.settings.value("windowState")
        if state:
            self.restoreState(state)
    
    def save_settings(self):
        """Save application settings."""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
    
    def load_assignments(self):
        """Load and display available assignments."""
        try:
            assignments = self.homework_manager.get_available_assignments()
            
            self.assignment_list.clear()
            for assignment in assignments:
                item_text = f"📓 Homework {assignment['number']}: {assignment['title']}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, assignment)
                self.assignment_list.addItem(item)
            
            if assignments:
                self.assignment_list.setCurrentRow(0)
                self.on_assignment_selected()
            else:
                self.details_text.setHtml("""
                <h3>No Assignments Found</h3>
                <p>No homework assignments were found in the project.</p>
                <p>Make sure you have homework folders in the <code>src/</code> directory.</p>
                """)
            
            self.status_bar.showMessage(f"Loaded {len(assignments)} assignments", 3000)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load assignments: {str(e)}")
    
    def refresh_assignments(self):
        """Refresh the assignments list."""
        self.homework_manager.refresh()
        self.load_assignments()
    
    def on_assignment_selected(self):
        """Handle assignment selection."""
        current_item = self.assignment_list.currentItem()
        if current_item:
            assignment = current_item.data(Qt.UserRole)
            self.show_assignment_details(assignment)
    
    def show_assignment_details(self, assignment):
        """Show details for the selected assignment."""
        problems_count = len(assignment.get('problems', []))
        files_count = len(assignment.get('files', []))
        
        details_html = f"""
        <h2>📓 Homework {assignment['number']}: {assignment['title']}</h2>
        
        <h3>📝 Description</h3>
        <p>{assignment.get('description', 'No description available.')}</p>
        
        <h3>📊 Statistics</h3>
        <ul>
            <li><strong>Problems:</strong> {problems_count}</li>
            <li><strong>Files:</strong> {files_count}</li>
            <li><strong>Status:</strong> {assignment.get('status', 'Unknown')}</li>
        </ul>
        
        <h3>🎯 Topics</h3>
        <p>{', '.join(assignment.get('topics', ['Not specified']))}</p>
        """
        
        if assignment.get('problems'):
            details_html += "<h3>🧩 Problems</h3><ul>"
            for problem in assignment['problems']:
                details_html += f"<li><strong>Problem {problem['number']}:</strong> {problem.get('title', 'Untitled')}</li>"
            details_html += "</ul>"
        
        if assignment.get('files'):
            details_html += "<h3>📁 Files</h3><ul>"
            for file_name in assignment['files'][:10]:  # Show first 10 files
                details_html += f"<li><code>{file_name}</code></li>"
            if len(assignment['files']) > 10:
                details_html += f"<li><em>... and {len(assignment['files']) - 10} more files</em></li>"
            details_html += "</ul>"
        
        self.details_text.setHtml(details_html)
    
    def open_selected_assignment(self):
        """Open the selected assignment in a new tab."""
        current_item = self.assignment_list.currentItem()
        if current_item:
            assignment = current_item.data(Qt.UserRole)
            self.open_assignment_tab(assignment)
    
    def open_assignment_tab(self, assignment):
        """Open an assignment in a new tab."""
        assignment_id = f"hw{assignment['number']}"
        
        # Check if tab already exists
        for i in range(self.main_tabs.count()):
            widget = self.main_tabs.widget(i)
            if hasattr(widget, 'assignment_id') and widget.assignment_id == assignment_id:
                self.main_tabs.setCurrentIndex(i)
                return
        
        # Create new assignment widget
        try:
            assignment_widget = AssignmentWidget(assignment, self.homework_manager)
            assignment_widget.assignment_id = assignment_id
            
            # Add tab
            tab_title = f"📓 HW {assignment['number']}"
            tab_index = self.main_tabs.addTab(assignment_widget, tab_title)
            self.main_tabs.setCurrentIndex(tab_index)
            
            # Store reference
            self.assignment_widgets[assignment_id] = assignment_widget
            
            self.status_bar.showMessage(f"Opened Homework {assignment['number']}", 2000)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open assignment: {str(e)}")
    
    def run_all_problems(self):
        """Run all problems in the selected assignment."""
        current_item = self.assignment_list.currentItem()
        if current_item:
            assignment = current_item.data(Qt.UserRole)
            reply = QMessageBox.question(
                self, 
                "Run All Problems",
                f"Run all problems in Homework {assignment['number']}?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.open_assignment_tab(assignment)
                # TODO: Implement running all problems
                self.status_bar.showMessage("Running all problems...", 3000)
    
    def view_assignment_files(self):
        """View files in the selected assignment."""
        current_item = self.assignment_list.currentItem()
        if current_item:
            assignment = current_item.data(Qt.UserRole)
            assignment_path = assignment.get('path')
            if assignment_path and os.path.exists(assignment_path):
                # Open file manager (platform-specific)
                import platform
                import subprocess
                
                system = platform.system()
                if system == "Windows":
                    subprocess.run(["explorer", assignment_path])
                elif system == "Darwin":  # macOS
                    subprocess.run(["open", assignment_path])
                else:  # Linux
                    subprocess.run(["xdg-open", assignment_path])
    
    def new_assignment(self):
        """Create a new assignment."""
        # Simple dialog for new assignment
        assignment_number, ok = QInputDialog.getInt(
            self, "New Assignment", "Assignment Number:", 1, 1, 100
        )
        if ok:
            assignment_title, ok = QInputDialog.getText(
                self, "New Assignment", "Assignment Title:"
            )
            if ok and assignment_title:
                try:
                    self.homework_manager.create_assignment_template(
                        assignment_number, assignment_title
                    )
                    self.refresh_assignments()
                    QMessageBox.information(
                        self, "Success", 
                        f"Created Homework {assignment_number}: {assignment_title}"
                    )
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to create assignment: {str(e)}")
    
    def open_folder(self):
        """Open an assignment folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Assignment Folder")
        if folder:
            try:
                self.homework_manager.load_assignment_from_folder(folder)
                self.refresh_assignments()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load folder: {str(e)}")
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(self, "About", """
        <h3>🎓 Scientific Machine Learning Homework Assistant</h3>
        <p>A modern PyQt5 application for managing and running scientific machine learning homework assignments.</p>
        <p><strong>Version:</strong> 2.0</p>
        <p><strong>Built with:</strong> PyQt5, Python, matplotlib</p>
        <p><strong>Features:</strong></p>
        <ul>
            <li>📚 Multi-assignment management</li>
            <li>🧩 Individual problem execution</li>
            <li>📊 Integrated plotting and visualization</li>
            <li>⚡ Modern, responsive interface</li>
        </ul>
        """)
    
    def close_application(self):
        """Close the application."""
        self.close()
    
    def closeEvent(self, event):
        """Handle application close event."""
        self.save_settings()
        event.accept()


def main():
    """Main entry point."""
    # Create QApplication
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application metadata
    app.setApplicationName("Scientific ML Homework")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("HomeworkAI")
    
    # Create and show main window
    try:
        window = HomeworkMainWindow()
        window.show()
        
        # Run the application
        return app.exec_()
    
    except Exception as e:
        print(f"Error starting application: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
