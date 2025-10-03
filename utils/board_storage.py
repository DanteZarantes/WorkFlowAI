"""
Board-based storage system with hierarchical task management
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from utils.secure_json_storage import SecureJSONStorage

class BoardStorage(SecureJSONStorage):
    """Board-based storage extending secure JSON storage"""
    
    def __init__(self):
        super().__init__()
        self._ensure_board_directories()
    
    def _ensure_board_directories(self):
        """Create board-specific directories"""
        directories = ['boards', 'board_tasks', 'board_projects']
        for directory in directories:
            path = os.path.join(self.base_path, directory)
            os.makedirs(path, exist_ok=True)
    
    def create_board(self, user_id: int, board_data: Dict[str, Any]) -> str:
        """Create a new board"""
        board_id = f"board_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}"
        
        board = {
            'id': board_id,
            'name': board_data.get('name', 'Untitled Board'),
            'description': board_data.get('description', ''),
            'type': board_data.get('type', 'mindmap'),
            'owner_id': user_id,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'settings': board_data.get('settings', {}),
            'task_counter': 0,
            'project_counter': 0
        }
        
        file_path = self._get_file_path('boards', user_id)
        existing_data = self._read_secure_file(file_path)
        
        if 'boards' not in existing_data:
            existing_data = {'boards': []}
        
        existing_data['boards'].append(board)
        existing_data['updated_at'] = datetime.now().isoformat()
        
        self._write_secure_file(file_path, existing_data)
        return board_id
    
    def get_user_boards(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all boards for a user"""
        file_path = self._get_file_path('boards', user_id)
        data = self._read_secure_file(file_path)
        return data.get('boards', [])
    
    def get_board(self, user_id: int, board_id: str) -> Optional[Dict[str, Any]]:
        """Get specific board"""
        boards = self.get_user_boards(user_id)
        return next((b for b in boards if b['id'] == board_id), None)
    
    def save_board_task(self, user_id: int, board_id: str, task_data: Dict[str, Any]) -> bool:
        """Save task to specific board with hierarchical numbering"""
        file_path = self._get_file_path('board_tasks', user_id)
        existing_data = self._read_secure_file(file_path)
        
        if board_id not in existing_data:
            existing_data[board_id] = {'tasks': [], 'updated_at': None}
        
        # Generate hierarchical task number
        parent_id = task_data.get('parent_id')
        if parent_id:
            # Find parent task and generate child number
            parent_task = self._find_task_by_id(existing_data[board_id]['tasks'], parent_id)
            if parent_task:
                parent_number = parent_task['task_number']
                child_count = len([t for t in existing_data[board_id]['tasks'] 
                                 if t.get('parent_id') == parent_id])
                task_data['task_number'] = f"{parent_number}.{child_count + 1}"
            else:
                task_data['task_number'] = str(len(existing_data[board_id]['tasks']) + 1)
        else:
            # Root task
            root_count = len([t for t in existing_data[board_id]['tasks'] 
                            if not t.get('parent_id')])
            task_data['task_number'] = str(root_count + 1)
        
        task_data['id'] = f"task_{len(existing_data[board_id]['tasks']) + 1}_{datetime.now().strftime('%H%M%S')}"
        task_data['board_id'] = board_id
        task_data['created_at'] = datetime.now().isoformat()
        task_data['owner_id'] = user_id
        task_data['status'] = task_data.get('status', 'Not Started')
        task_data['progress'] = task_data.get('progress', 0)
        
        existing_data[board_id]['tasks'].append(task_data)
        existing_data[board_id]['updated_at'] = datetime.now().isoformat()
        
        return self._write_secure_file(file_path, existing_data)
    
    def get_board_tasks(self, user_id: int, board_id: str) -> List[Dict[str, Any]]:
        """Get tasks for specific board"""
        file_path = self._get_file_path('board_tasks', user_id)
        data = self._read_secure_file(file_path)
        return data.get(board_id, {}).get('tasks', [])
    
    def save_board_project(self, user_id: int, board_id: str, project_data: Dict[str, Any]) -> bool:
        """Save project to specific board"""
        file_path = self._get_file_path('board_projects', user_id)
        existing_data = self._read_secure_file(file_path)
        
        if board_id not in existing_data:
            existing_data[board_id] = {'projects': [], 'updated_at': None}
        
        project_data['id'] = f"proj_{len(existing_data[board_id]['projects']) + 1}_{datetime.now().strftime('%H%M%S')}"
        project_data['board_id'] = board_id
        project_data['created_at'] = datetime.now().isoformat()
        project_data['owner_id'] = user_id
        project_data['status'] = project_data.get('status', 'active')
        project_data['progress'] = project_data.get('progress', 0)
        
        existing_data[board_id]['projects'].append(project_data)
        existing_data[board_id]['updated_at'] = datetime.now().isoformat()
        
        return self._write_secure_file(file_path, existing_data)
    
    def get_board_projects(self, user_id: int, board_id: str) -> List[Dict[str, Any]]:
        """Get projects for specific board"""
        file_path = self._get_file_path('board_projects', user_id)
        data = self._read_secure_file(file_path)
        return data.get(board_id, {}).get('projects', [])
    
    def get_all_user_tasks(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all tasks from all user boards"""
        file_path = self._get_file_path('board_tasks', user_id)
        data = self._read_secure_file(file_path)
        
        all_tasks = []
        for board_id, board_data in data.items():
            if isinstance(board_data, dict) and 'tasks' in board_data:
                all_tasks.extend(board_data['tasks'])
        
        return all_tasks
    
    def get_all_user_projects(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all projects from all user boards"""
        file_path = self._get_file_path('board_projects', user_id)
        data = self._read_secure_file(file_path)
        
        all_projects = []
        for board_id, board_data in data.items():
            if isinstance(board_data, dict) and 'projects' in board_data:
                all_projects.extend(board_data['projects'])
        
        return all_projects
    
    def _find_task_by_id(self, tasks: List[Dict[str, Any]], task_id: str) -> Optional[Dict[str, Any]]:
        """Find task by ID"""
        return next((t for t in tasks if t.get('id') == task_id), None)
    
    def update_board_task(self, user_id: int, board_id: str, task_id: str, updates: Dict[str, Any]) -> bool:
        """Update specific task in board"""
        file_path = self._get_file_path('board_tasks', user_id)
        data = self._read_secure_file(file_path)
        
        if board_id not in data:
            return False
        
        for task in data[board_id]['tasks']:
            if task.get('id') == task_id:
                task.update(updates)
                task['updated_at'] = datetime.now().isoformat()
                break
        else:
            return False
        
        data[board_id]['updated_at'] = datetime.now().isoformat()
        return self._write_secure_file(file_path, data)
    
    def delete_board_task(self, user_id: int, board_id: str, task_id: str) -> bool:
        """Delete task from board"""
        file_path = self._get_file_path('board_tasks', user_id)
        data = self._read_secure_file(file_path)
        
        if board_id not in data:
            return False
        
        original_count = len(data[board_id]['tasks'])
        data[board_id]['tasks'] = [t for t in data[board_id]['tasks'] if t.get('id') != task_id]
        
        if len(data[board_id]['tasks']) < original_count:
            data[board_id]['updated_at'] = datetime.now().isoformat()
            return self._write_secure_file(file_path, data)
        
        return False

# Global instance
board_storage = BoardStorage()