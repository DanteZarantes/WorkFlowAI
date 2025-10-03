"""
Secure JSON storage system with proper user isolation and encryption
"""
import json
import os
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from django.conf import settings
from django.contrib.auth import get_user_model
from cryptography.fernet import Fernet
import base64

User = get_user_model()

class SecureJSONStorage:
    """Secure JSON storage with encryption and user isolation"""
    
    def __init__(self):
        self.base_path = os.path.join(settings.BASE_DIR, 'secure_data')
        self._ensure_directories()
        self._setup_encryption()
    
    def _ensure_directories(self):
        """Create necessary directories"""
        directories = ['users', 'projects', 'tasks', 'analytics', 'automations']
        for directory in directories:
            path = os.path.join(self.base_path, directory)
            os.makedirs(path, exist_ok=True)
    
    def _setup_encryption(self):
        """Setup encryption key"""
        key_file = os.path.join(self.base_path, '.encryption_key')
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                self.encryption_key = f.read()
        else:
            self.encryption_key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(self.encryption_key)
        self.cipher = Fernet(self.encryption_key)
    
    def _get_user_hash(self, user_id: int) -> str:
        """Generate secure hash for user ID"""
        return hashlib.sha256(f"user_{user_id}_{settings.SECRET_KEY}".encode()).hexdigest()[:16]
    
    def _get_file_path(self, data_type: str, user_id: int) -> str:
        """Get secure file path for user data"""
        user_hash = self._get_user_hash(user_id)
        return os.path.join(self.base_path, data_type, f"{data_type}_{user_hash}.json")
    
    def _encrypt_data(self, data: Dict[str, Any]) -> bytes:
        """Encrypt data"""
        json_data = json.dumps(data, default=str, ensure_ascii=False)
        return self.cipher.encrypt(json_data.encode())
    
    def _decrypt_data(self, encrypted_data: bytes) -> Dict[str, Any]:
        """Decrypt data"""
        try:
            decrypted = self.cipher.decrypt(encrypted_data)
            return json.loads(decrypted.decode())
        except Exception:
            return {}
    
    def _read_secure_file(self, file_path: str) -> Dict[str, Any]:
        """Read and decrypt file"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    encrypted_data = f.read()
                return self._decrypt_data(encrypted_data)
            return {}
        except Exception:
            return {}
    
    def _write_secure_file(self, file_path: str, data: Dict[str, Any]) -> bool:
        """Encrypt and write file"""
        try:
            encrypted_data = self._encrypt_data(data)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
            return True
        except Exception:
            return False
    
    def save_user_data(self, user: User) -> bool:
        """Save user data securely"""
        user_data = {
            'user_id': user.id,  # Use actual user ID, not starting from 6
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
            'is_profile_public': user.is_profile_public,
            'receive_notifications': user.receive_notifications,
            'date_joined': user.date_joined.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'updated_at': datetime.now().isoformat(),
            'activities': [],
            'connections': []
        }
        
        file_path = self._get_file_path('users', user.id)
        return self._write_secure_file(file_path, user_data)
    
    def save_project_data(self, user_id: int, project_data: Dict[str, Any]) -> bool:
        """Save project data for specific user"""
        file_path = self._get_file_path('projects', user_id)
        existing_data = self._read_secure_file(file_path)
        
        if 'projects' not in existing_data:
            existing_data = {'projects': [], 'updated_at': None}
        
        project_data['id'] = len(existing_data['projects']) + 1
        project_data['created_at'] = datetime.now().isoformat()
        project_data['owner_id'] = user_id
        
        existing_data['projects'].append(project_data)
        existing_data['updated_at'] = datetime.now().isoformat()
        
        return self._write_secure_file(file_path, existing_data)
    
    def save_task_data(self, user_id: int, task_data: Dict[str, Any]) -> bool:
        """Save task data with hierarchical structure"""
        file_path = self._get_file_path('tasks', user_id)
        existing_data = self._read_secure_file(file_path)
        
        if 'tasks' not in existing_data:
            existing_data = {'tasks': [], 'updated_at': None}
        
        # Generate task number if not provided
        if 'task_number' not in task_data:
            task_data['task_number'] = str(len(existing_data['tasks']) + 1)
        
        task_data['id'] = len(existing_data['tasks']) + 1
        task_data['created_at'] = datetime.now().isoformat()
        task_data['owner_id'] = user_id
        task_data['progress_percentage'] = task_data.get('progress_percentage', 0)
        task_data['status'] = task_data.get('status', 'not_started')
        
        existing_data['tasks'].append(task_data)
        existing_data['updated_at'] = datetime.now().isoformat()
        
        return self._write_secure_file(file_path, existing_data)
    
    def save_analytics_data(self, user_id: int, analytics_data: Dict[str, Any]) -> bool:
        """Save analytics data"""
        file_path = self._get_file_path('analytics', user_id)
        analytics_data['updated_at'] = datetime.now().isoformat()
        analytics_data['user_id'] = user_id
        
        return self._write_secure_file(file_path, analytics_data)
    
    def get_user_data(self, user_id: int) -> Dict[str, Any]:
        """Get user data"""
        file_path = self._get_file_path('users', user_id)
        return self._read_secure_file(file_path)
    
    def get_user_projects(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user projects"""
        file_path = self._get_file_path('projects', user_id)
        data = self._read_secure_file(file_path)
        return data.get('projects', [])
    
    def get_user_tasks(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user tasks"""
        file_path = self._get_file_path('tasks', user_id)
        data = self._read_secure_file(file_path)
        return data.get('tasks', [])
    
    def get_analytics_data(self, user_id: int) -> Dict[str, Any]:
        """Get analytics data"""
        file_path = self._get_file_path('analytics', user_id)
        return self._read_secure_file(file_path)
    
    def update_task_progress(self, user_id: int, task_id: int, progress: int, status: str = None) -> bool:
        """Update task progress"""
        file_path = self._get_file_path('tasks', user_id)
        data = self._read_secure_file(file_path)
        
        if 'tasks' not in data:
            return False
        
        for task in data['tasks']:
            if task.get('id') == task_id:
                task['progress_percentage'] = progress
                if status:
                    task['status'] = status
                task['updated_at'] = datetime.now().isoformat()
                break
        
        data['updated_at'] = datetime.now().isoformat()
        return self._write_secure_file(file_path, data)
    
    def get_user_connections(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user connections"""
        user_data = self.get_user_data(user_id)
        return user_data.get('connections', [])
    
    def get_user_automations(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user automations"""
        file_path = self._get_file_path('automations', user_id)
        data = self._read_secure_file(file_path)
        return data.get('automations', [])
    
    def get_user_models(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user AI models"""
        # For now, return empty list since we don't have models in secure storage yet
        # This can be extended later to store AI model configurations
        return []
    
    def generate_analytics(self, user_id: int) -> Dict[str, Any]:
        """Generate analytics data for dashboard"""
        return self.generate_dashboard_data(user_id)
    
    def generate_dashboard_data(self, user_id: int) -> Dict[str, Any]:
        """Generate dashboard analytics"""
        tasks = self.get_user_tasks(user_id)
        projects = self.get_user_projects(user_id)
        
        # Task analytics
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.get('status') == 'completed'])
        in_progress_tasks = len([t for t in tasks if t.get('status') == 'in_progress'])
        overdue_tasks = len([t for t in tasks if self._is_task_overdue(t)])
        on_time_completions = len([t for t in tasks if self._is_task_on_time(t)])
        
        # Project analytics
        total_projects = len(projects)
        completed_projects = len([p for p in projects if p.get('status') == 'completed'])
        
        dashboard_data = {
            'user_id': user_id,
            'task_summary': {
                'total': total_tasks,
                'completed': completed_tasks,
                'in_progress': in_progress_tasks,
                'overdue': overdue_tasks,
                'on_time_completions': on_time_completions,
                'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            },
            'project_summary': {
                'total': total_projects,
                'completed': completed_projects,
                'completion_rate': (completed_projects / total_projects * 100) if total_projects > 0 else 0
            },
            'charts_data': {
                'task_status_distribution': self._get_task_status_distribution(tasks),
                'project_progress': self._get_project_progress_data(projects),
                'completion_trends': self._get_completion_trends(tasks)
            },
            'generated_at': datetime.now().isoformat()
        }
        
        # Save analytics
        self.save_analytics_data(user_id, dashboard_data)
        return dashboard_data
    
    def _is_task_overdue(self, task: Dict[str, Any]) -> bool:
        """Check if task is overdue"""
        if not task.get('end_date') or task.get('status') == 'completed':
            return False
        
        try:
            from datetime import datetime
            end_date = datetime.fromisoformat(task['end_date'].replace('Z', '+00:00'))
            return end_date < datetime.now()
        except:
            return False
    
    def _is_task_on_time(self, task: Dict[str, Any]) -> bool:
        """Check if task was completed on time"""
        if task.get('status') != 'completed' or not task.get('end_date') or not task.get('completed_date'):
            return False
        
        try:
            from datetime import datetime
            end_date = datetime.fromisoformat(task['end_date'].replace('Z', '+00:00'))
            completed_date = datetime.fromisoformat(task['completed_date'].replace('Z', '+00:00'))
            return completed_date <= end_date
        except:
            return False
    
    def _get_task_status_distribution(self, tasks: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get task status distribution for charts"""
        distribution = {}
        for task in tasks:
            status = task.get('status', 'not_started')
            distribution[status] = distribution.get(status, 0) + 1
        return distribution
    
    def _get_project_progress_data(self, projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get project progress data for charts"""
        return [
            {
                'name': project.get('name', 'Unnamed Project'),
                'progress': project.get('progress_percentage', 0),
                'status': project.get('status', 'not_started')
            }
            for project in projects
        ]
    
    def _get_completion_trends(self, tasks: List[Dict[str, Any]]) -> Dict[str, List]:
        """Get completion trends for charts"""
        # This would be more complex in real implementation
        # For now, return basic structure
        return {
            'dates': [],
            'completed': [],
            'created': []
        }

# Global instance
secure_storage = SecureJSONStorage()