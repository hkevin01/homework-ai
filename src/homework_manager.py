"""
Homework Manager for Scientific Machine Learning Assignments

This module manages homework assignments, their metadata, and provides
utilities for discovering and loading assignment data.
"""

import glob
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


class HomeworkManager:
    """Manager class for handling homework assignments."""
    
    def __init__(self, base_path: Optional[str] = None):
        """Initialize the homework manager."""
        if base_path is None:
            # Get the project root directory
            current_file = Path(__file__).resolve()
            self.base_path = current_file.parent.parent
        else:
            self.base_path = Path(base_path)
        
        self.assignments_cache = {}
        self.refresh()
    
    def refresh(self):
        """Refresh the cache of available assignments."""
        self.assignments_cache.clear()
        self._discover_assignments()
    
    def _discover_assignments(self):
        """Discover assignments in the project structure."""
        # Look for assignments in src/ directory
        src_path = self.base_path / "src"
        if src_path.exists():
            for homework_dir in src_path.glob("homework*"):
                if homework_dir.is_dir():
                    assignment_data = self._load_assignment_data(homework_dir)
                    if assignment_data:
                        self.assignments_cache[assignment_data['number']] = assignment_data
        
        # Also check assignments/ directory if it exists
        assignments_path = self.base_path / "assignments"
        if assignments_path.exists():
            for homework_dir in assignments_path.glob("homework*"):
                if homework_dir.is_dir():
                    assignment_data = self._load_assignment_data(homework_dir)
                    if assignment_data:
                        self.assignments_cache[assignment_data['number']] = assignment_data
    
    def _load_assignment_data(self, homework_dir: Path) -> Optional[Dict[str, Any]]:
        """Load assignment data from a homework directory."""
        try:
            # Extract homework number from directory name
            dir_name = homework_dir.name
            hw_number = ''.join(filter(str.isdigit, dir_name))
            if not hw_number:
                return None
            
            # Look for metadata file
            metadata_file = homework_dir / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
            else:
                # Create default metadata
                metadata = self._create_default_metadata(homework_dir)
            
            # Add computed fields
            metadata['number'] = int(hw_number)
            metadata['path'] = str(homework_dir)
            metadata['files'] = self._get_assignment_files(homework_dir)
            metadata['problems'] = self._discover_problems(homework_dir)
            
            return metadata
            
        except Exception as e:
            print(f"Error loading assignment from {homework_dir}: {e}")
            return None
    
    def _create_default_metadata(self, homework_dir: Path) -> Dict[str, Any]:
        """Create default metadata for an assignment."""
        hw_number = ''.join(filter(str.isdigit, homework_dir.name))
        
        # Try to read README for description
        description = "No description available."
        readme_file = homework_dir / "README.md"
        if readme_file.exists():
            try:
                with open(readme_file, 'r') as f:
                    content = f.read()
                    # Extract first paragraph as description
                    lines = content.split('\n')
                    for line in lines:
                        if line.strip() and not line.startswith('#'):
                            description = line.strip()
                            break
            except Exception:
                pass
        
        return {
            'title': f"Homework {hw_number}",
            'description': description,
            'topics': ['Scientific Machine Learning'],
            'status': 'Available',
        }
    
    def _get_assignment_files(self, homework_dir: Path) -> List[str]:
        """Get list of Python files in the assignment directory."""
        files = []
        for py_file in homework_dir.glob("*.py"):
            if not py_file.name.startswith('__'):
                files.append(py_file.name)
        return sorted(files)
    
    def _discover_problems(self, homework_dir: Path) -> List[Dict[str, Any]]:
        """Discover individual problems in the assignment."""
        problems = []
        
        # Look for problem files (problem*.py or *_problem*.py)
        problem_patterns = ["problem*.py", "*problem*.py"]
        
        for pattern in problem_patterns:
            for problem_file in homework_dir.glob(pattern):
                if not problem_file.name.startswith('__'):
                    problem_data = self._load_problem_data(problem_file)
                    if problem_data:
                        problems.append(problem_data)
        
        return sorted(problems, key=lambda x: x.get('number', 0))
    
    def _load_problem_data(self, problem_file: Path) -> Optional[Dict[str, Any]]:
        """Load data for an individual problem."""
        try:
            # Extract problem number from filename
            filename = problem_file.stem
            problem_number = ''.join(filter(str.isdigit, filename))
            if not problem_number:
                problem_number = "1"
            
            # Read file to extract detailed problem information
            description = "No description available."
            question = "No question available."
            learning_objectives = []
            solution_approach = "No solution approach described."
            
            try:
                with open(problem_file, 'r') as f:
                    content = f.read()
                    
                    # Extract module docstring
                    if '"""' in content:
                        start = content.find('"""')
                        end = content.find('"""', start + 3)
                        if end > start:
                            docstring = content[start+3:end].strip()
                            lines = docstring.split('\n')
                            
                            # Parse the docstring structure
                            current_section = "description"
                            for line in lines:
                                line = line.strip()
                                if not line:
                                    continue
                                
                                # Check for section headers
                                if any(keyword in line.lower() for keyword in ['problem:', 'question:', 'task:']):
                                    current_section = "question"
                                    # Extract question text after the colon
                                    if ':' in line:
                                        question = line.split(':', 1)[1].strip()
                                    continue
                                elif any(keyword in line.lower() for keyword in ['objective', 'learn', 'goal']):
                                    current_section = "objectives"
                                    continue
                                elif any(keyword in line.lower() for keyword in ['solution', 'approach', 'method']):
                                    current_section = "solution"
                                    continue
                                elif any(keyword in line.lower() for keyword in ['example', 'scenario', 'given']):
                                    current_section = "question"
                                    if current_section == "question" and question == "No question available.":
                                        question = line
                                    continue
                                
                                # Add content to appropriate section
                                if current_section == "description" and description == "No description available.":
                                    description = line
                                elif current_section == "question":
                                    if question == "No question available.":
                                        question = line
                                    else:
                                        question += " " + line
                                elif current_section == "objectives" and (line.startswith('-') or line.startswith('*')):
                                    learning_objectives.append(line[1:].strip())
                                elif current_section == "solution":
                                    if solution_approach == "No solution approach described.":
                                        solution_approach = line
                                    else:
                                        solution_approach += " " + line
                    
                    # If we didn't find a specific question, look for comments with "Problem" or "Question"
                    if question == "No question available.":
                        question = self._extract_question_from_comments(content)
                    
                    # If still no question, use the description
                    if question == "No question available." and description != "No description available.":
                        question = description
                        
            except Exception as e:
                print(f"Error parsing problem file {problem_file}: {e}")
            
            return {
                'number': int(problem_number),
                'title': self._extract_title_from_filename(problem_file.name),
                'description': description,
                'question': question,
                'solution_approach': solution_approach,
                'file_path': str(problem_file),
                'file_name': problem_file.name,
                'learning_objectives': learning_objectives or [
                    "Practice scientific computing concepts",
                    "Apply machine learning techniques",
                    "Develop problem-solving skills"
                ]
            }
            
        except Exception as e:
            print(f"Error loading problem from {problem_file}: {e}")
            return None
    
    def _extract_question_from_comments(self, content: str) -> str:
        """Extract question text from comments in the code."""
        lines = content.split('\n')
        question_lines = []
        in_question = False
        
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                comment = line[1:].strip()
                if any(keyword in comment.lower() for keyword in ['problem:', 'question:', 'task:', 'given:', 'find:']):
                    in_question = True
                    if ':' in comment:
                        question_lines.append(comment.split(':', 1)[1].strip())
                    else:
                        question_lines.append(comment)
                elif in_question and comment:
                    question_lines.append(comment)
                elif in_question and not comment:
                    break
        
        return ' '.join(question_lines) if question_lines else "No question available."
    
    def _extract_title_from_filename(self, filename: str) -> str:
        """Extract a readable title from the filename."""
        # Remove extension and problem number prefix
        name = filename.replace('.py', '')
        parts = name.split('_')
        
        # Capitalize each part and join with spaces
        title_parts = []
        for part in parts:
            if part.lower() not in ['problem', 'hw', 'homework'] and not part.isdigit():
                title_parts.append(part.replace('_', ' ').title())
        
        return ' '.join(title_parts) if title_parts else f"Problem {parts[0] if parts else '1'}"
    
    def get_available_assignments(self) -> List[Dict[str, Any]]:
        """Get list of all available assignments."""
        return sorted(self.assignments_cache.values(), key=lambda x: x['number'])
    
    def get_assignment(self, number: int) -> Optional[Dict[str, Any]]:
        """Get a specific assignment by number."""
        return self.assignments_cache.get(number)
    
    def load_assignment_from_folder(self, folder_path: str):
        """Load an assignment from a specific folder."""
        folder = Path(folder_path)
        if folder.exists() and folder.is_dir():
            assignment_data = self._load_assignment_data(folder)
            if assignment_data:
                self.assignments_cache[assignment_data['number']] = assignment_data
                return assignment_data
        return None
    
    def create_assignment_template(self, number: int, title: str, target_dir: Optional[str] = None):
        """Create a template for a new assignment."""
        if target_dir is None:
            target_dir = self.base_path / "src" / f"homework{number}"
        else:
            target_dir = Path(target_dir)
        
        # Create directory structure
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Create metadata file
        metadata = {
            'title': title,
            'description': f'Homework assignment {number} for Scientific Machine Learning',
            'topics': ['Scientific Machine Learning'],
            'status': 'In Progress',
        }
        
        metadata_file = target_dir / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Create README
        readme_content = f"""# Homework {number}: {title}

## Description
{metadata['description']}

## Problems
- Problem 1: [Description needed]

## Instructions
1. Implement the solutions in the corresponding problem files
2. Run the GUI to test your solutions
3. Verify all tests pass

## Files
- `problem1_*.py` - Solution for Problem 1
- `README.md` - This file
- `metadata.json` - Assignment metadata
"""
        
        readme_file = target_dir / "README.md"
        with open(readme_file, 'w') as f:
            f.write(readme_content)
        
        # Create __init__.py
        init_file = target_dir / "__init__.py"
        with open(init_file, 'w') as f:
            f.write(f'"""Homework {number}: {title}"""\n')
        
        return str(target_dir)
