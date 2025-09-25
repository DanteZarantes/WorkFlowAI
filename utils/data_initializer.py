"""
Professional data initialization utility for NeuralFlow
Ensures proper setup of JSON storage and data integrity
"""
import os
import json
from django.conf import settings
from django.contrib.auth import get_user_model
from .json_storage import json_storage

User = get_user_model()

class DataInitializer:
    """Initialize and validate data storage system"""
    
    def __init__(self):
        self.base_path = os.path.join(settings.BASE_DIR, 'data')
    
    def initialize_data_structure(self):
        """Create necessary directories and files"""
        directories = [
            os.path.join(self.base_path, 'users'),
            os.path.join(self.base_path, 'tasks'),
            os.path.join(self.base_path, 'projects'),
            os.path.join(self.base_path, 'models'),
            os.path.join(self.base_path, 'backups')
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            
        # Create index files for better organization
        self._create_index_files()
        
        print("Data structure initialized successfully")
    
    def _create_index_files(self):
        """Create index files for data organization"""
        index_data = {
            'created_at': '2024-01-01T00:00:00',
            'version': '1.0',
            'description': 'NeuralFlow JSON Data Storage'
        }
        
        index_files = [
            os.path.join(self.base_path, 'users', '_index.json'),
            os.path.join(self.base_path, 'tasks', '_index.json'),
            os.path.join(self.base_path, 'projects', '_index.json'),
            os.path.join(self.base_path, 'models', '_index.json')
        ]
        
        for index_file in index_files:
            if not os.path.exists(index_file):
                with open(index_file, 'w', encoding='utf-8') as f:
                    json.dump(index_data, f, indent=2)
    
    def sync_existing_users(self):
        """Sync existing database users to JSON storage"""
        users = User.objects.all()
        synced_count = 0
        
        for user in users:
            try:
                # Save user data to JSON
                success = json_storage.save_user_data(user)
                if success:
                    synced_count += 1
                    
                    # Initialize empty data files for user
                    self._initialize_user_data_files(user.id)
                    
            except Exception as e:
                print(f"Error syncing user {user.username}: {str(e)}")
        
        print(f"Synced {synced_count} users to JSON storage")
        return synced_count
    
    def _initialize_user_data_files(self, user_id):
        """Initialize empty data files for a user"""
        empty_data_structures = {
            'tasks': {'tasks': [], 'updated_at': None},
            'projects': {'projects': [], 'updated_at': None},
            'models': {'models': [], 'updated_at': None}
        }
        
        for data_type, structure in empty_data_structures.items():
            file_path = os.path.join(self.base_path, data_type, f'{data_type}_{user_id}.json')
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(structure, f, indent=2)
    
    def validate_data_integrity(self):
        """Validate data integrity across all JSON files"""
        issues = []
        
        # Check directory structure
        required_dirs = ['users', 'tasks', 'projects', 'models']
        for dir_name in required_dirs:
            dir_path = os.path.join(self.base_path, dir_name)
            if not os.path.exists(dir_path):
                issues.append(f"Missing directory: {dir_name}")
        
        # Check user data files
        users = User.objects.all()
        for user in users:
            user_file = os.path.join(self.base_path, 'users', f'user_{user.id}.json')
            if not os.path.exists(user_file):
                issues.append(f"Missing user data file for user {user.username}")
            else:
                # Validate JSON structure
                try:
                    with open(user_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'user_id' not in data or 'email' not in data:
                            issues.append(f"Invalid user data structure for user {user.username}")
                except json.JSONDecodeError:
                    issues.append(f"Corrupted JSON file for user {user.username}")
        
        if issues:
            print("Data integrity issues found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("Data integrity validation passed")
        
        return issues
    
    def create_backup(self):
        """Create backup of all JSON data"""
        import shutil
        from datetime import datetime
        
        backup_dir = os.path.join(self.base_path, 'backups', datetime.now().strftime('%Y%m%d_%H%M%S'))
        
        try:
            # Copy entire data directory
            shutil.copytree(self.base_path, backup_dir, ignore=shutil.ignore_patterns('backups'))
            print(f"Backup created: {backup_dir}")
            return backup_dir
        except Exception as e:
            print(f"Backup failed: {str(e)}")
            return None
    
    def get_storage_stats(self):
        """Get statistics about JSON storage usage"""
        stats = {
            'total_users': 0,
            'total_tasks': 0,
            'total_projects': 0,
            'total_models': 0,
            'storage_size_mb': 0
        }
        
        # Count files and calculate sizes
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith('.json') and not file.startswith('_'):
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    stats['storage_size_mb'] += file_size
                    
                    # Count by type
                    if 'user_' in file:
                        stats['total_users'] += 1
                    elif 'tasks_' in file:
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                stats['total_tasks'] += len(data.get('tasks', []))
                        except:
                            pass
                    elif 'projects_' in file:
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                stats['total_projects'] += len(data.get('projects', []))
                        except:
                            pass
                    elif 'models_' in file:
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                stats['total_models'] += len(data.get('models', []))
                        except:
                            pass
        
        stats['storage_size_mb'] = round(stats['storage_size_mb'] / (1024 * 1024), 2)
        
        return stats

# Global instance
data_initializer = DataInitializer()