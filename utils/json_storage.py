"""
Professional JSON storage utility for NeuralFlow
Handles user data, tasks, and model information in JSON format
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class JSONStorageManager:
    """Professional JSON storage manager for user data and tasks"""
    
    def __init__(self):
        self.base_path = os.path.join(settings.BASE_DIR, 'data')
        self.users_path = os.path.join(self.base_path, 'users')
        self.tasks_path = os.path.join(self.base_path, 'tasks')
        self.projects_path = os.path.join(self.base_path, 'projects')
        self.models_path = os.path.join(self.base_path, 'models')
        
        # Ensure directories exist
        for path in [self.users_path, self.tasks_path, self.projects_path, self.models_path]:
            os.makedirs(path, exist_ok=True)
    
    def _get_user_file_path(self, user_id: int) -> str:
        """Get the file path for a user's data"""
        return os.path.join(self.users_path, f'user_{user_id}.json')
    
    def _get_task_file_path(self, user_id: int) -> str:
        """Get the file path for a user's tasks"""
        return os.path.join(self.tasks_path, f'tasks_{user_id}.json')
    
    def _get_project_file_path(self, user_id: int) -> str:
        """Get the file path for a user's projects"""
        return os.path.join(self.projects_path, f'projects_{user_id}.json')
    
    def _get_model_file_path(self, user_id: int) -> str:
        """Get the file path for a user's AI models"""
        return os.path.join(self.models_path, f'models_{user_id}.json')
    
    def _read_json_file(self, file_path: str) -> Dict[str, Any]:
        """Safely read JSON file"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except (json.JSONDecodeError, IOError):
            return {}
    
    def _write_json_file(self, file_path: str, data: Dict[str, Any]) -> bool:
        """Safely write JSON file"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            return True
        except (IOError, TypeError):
            return False
    
    def save_user_data(self, user: User) -> bool:
        """Save user registration and profile data to JSON"""
        user_data = {
            'user_id': int(user.id),
            'group_id': user.groups.first().id if user.groups.exists() else None,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': user.user_type,
            'company_name': user.company_name,
            'job_title': user.job_title,
            'bio': user.bio,
            'location': user.location,
            'website': user.website,
            'linkedin_url': user.linkedin_url,
            'github_url': user.github_url,
            'skill_level': user.skill_level,
            'subscription_plan': user.subscription_plan,
            'api_calls_limit': user.api_calls_limit,
            'api_calls_used': user.api_calls_used,
            'is_profile_public': user.is_profile_public,
            'receive_notifications': user.receive_notifications,
            'date_joined': user.date_joined.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'updated_at': datetime.now().isoformat()
        }
        
        # Add profile data if exists
        if hasattr(user, 'profile'):
            profile = user.profile
            user_data['profile'] = {
                'skills': profile.skills,
                'interests': profile.interests,
                'experience_years': profile.experience_years,
                'education': profile.education,
                'certifications': profile.certifications,
                'profile_views': profile.profile_views,
                'projects_count': profile.projects_count,
                'connections_count': profile.connections_count
            }
        
        file_path = self._get_user_file_path(user.id)
        return self._write_json_file(file_path, user_data)
    
    def save_task_data(self, user_id: int, task_data: Dict[str, Any]) -> bool:
        """Save task data for a user"""
        file_path = self._get_task_file_path(user_id)
        existing_data = self._read_json_file(file_path)
        
        if not existing_data or 'tasks' not in existing_data:
            existing_data = {'tasks': [], 'updated_at': None}
        
        # Add timestamp and ID to task
        task_data['id'] = len(existing_data['tasks']) + 1
        task_data['created_at'] = datetime.now().isoformat()
        task_data['user_id'] = int(user_id)
        
        existing_data['tasks'].append(task_data)
        existing_data['updated_at'] = datetime.now().isoformat()
        
        return self._write_json_file(file_path, existing_data)
    
    def save_project_data(self, user_id: int, project_data: Dict[str, Any]) -> bool:
        """Save project data for a user"""
        file_path = self._get_project_file_path(user_id)
        existing_data = self._read_json_file(file_path)
        
        if not existing_data or 'projects' not in existing_data:
            existing_data = {'projects': [], 'updated_at': None}
        
        # Add timestamp and ID to project
        project_data['id'] = len(existing_data['projects']) + 1
        project_data['created_at'] = datetime.now().isoformat()
        project_data['user_id'] = int(user_id)
        
        existing_data['projects'].append(project_data)
        existing_data['updated_at'] = datetime.now().isoformat()
        
        return self._write_json_file(file_path, existing_data)
    
    def save_model_data(self, user_id: int, model_data: Dict[str, Any]) -> bool:
        """Save AI model data for a user"""
        file_path = self._get_model_file_path(user_id)
        existing_data = self._read_json_file(file_path)
        
        if not existing_data or 'models' not in existing_data:
            existing_data = {'models': [], 'updated_at': None}
        
        # Add timestamp and ID to model
        model_data['id'] = len(existing_data['models']) + 1
        model_data['created_at'] = datetime.now().isoformat()
        model_data['user_id'] = int(user_id)
        
        existing_data['models'].append(model_data)
        existing_data['updated_at'] = datetime.now().isoformat()
        
        return self._write_json_file(file_path, existing_data)
    
    def get_user_data(self, user_id: int) -> Dict[str, Any]:
        """Get user data from JSON"""
        file_path = self._get_user_file_path(user_id)
        return self._read_json_file(file_path)
    
    def get_user_tasks(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all tasks for a user"""
        file_path = self._get_task_file_path(user_id)
        data = self._read_json_file(file_path)
        if not data:
            # Initialize empty task file for new user
            data = {'tasks': [], 'updated_at': None}
            self._write_json_file(file_path, data)
        return data.get('tasks', [])
    
    def get_user_projects(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all projects for a user"""
        file_path = self._get_project_file_path(user_id)
        data = self._read_json_file(file_path)
        if not data:
            # Initialize empty project file for new user
            data = {'projects': [], 'updated_at': None}
            self._write_json_file(file_path, data)
        return data.get('projects', [])
    
    def get_user_models(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all AI models for a user"""
        file_path = self._get_model_file_path(user_id)
        data = self._read_json_file(file_path)
        if not data:
            # Initialize empty model file for new user
            data = {'models': [], 'updated_at': None}
            self._write_json_file(file_path, data)
        return data.get('models', [])
    
    def update_user_activity(self, user_id: int, activity_type: str, description: str, metadata: Dict = None) -> bool:
        """Log user activity"""
        file_path = self._get_user_file_path(user_id)
        user_data = self._read_json_file(file_path)
        
        if 'activities' not in user_data:
            user_data['activities'] = []
        
        activity = {
            'type': activity_type,
            'description': description,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        }
        
        user_data['activities'].append(activity)
        # Keep only last 100 activities
        user_data['activities'] = user_data['activities'][-100:]
        
        return self._write_json_file(file_path, user_data)

# Global instance
json_storage = JSONStorageManager()