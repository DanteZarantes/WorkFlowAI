"""
Management command to fix user ID issues and migrate to secure storage
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from utils.secure_json_storage import secure_storage
from utils.json_storage import json_storage
import os
import json

User = get_user_model()

class Command(BaseCommand):
    help = 'Fix user ID issues and migrate to secure storage'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--migrate-all',
            action='store_true',
            help='Migrate all existing data to secure storage',
        )
        parser.add_argument(
            '--fix-user-ids',
            action='store_true',
            help='Fix user ID numbering starting from 1',
        )
        parser.add_argument(
            '--create-missing',
            action='store_true',
            help='Create missing user data files',
        )
    
    def handle(self, *args, **options):
        if options['fix_user_ids']:
            self.fix_user_ids()
        
        if options['migrate_all']:
            self.migrate_to_secure_storage()
        
        if options['create_missing']:
            self.create_missing_user_files()
        
        self.stdout.write(self.style.SUCCESS('User data migration completed successfully'))
    
    def fix_user_ids(self):
        """Fix user ID numbering to start from actual user IDs"""
        self.stdout.write('Fixing user ID numbering...')
        
        users = User.objects.all().order_by('id')
        for user in users:
            self.stdout.write(f'Processing user {user.id}: {user.email}')
            
            # Create secure user data with correct ID
            success = secure_storage.save_user_data(user)
            if success:
                self.stdout.write(f'  ✓ Created secure data for user {user.id}')
            else:
                self.stdout.write(f'  ✗ Failed to create secure data for user {user.id}')
    
    def migrate_to_secure_storage(self):
        """Migrate existing JSON data to secure storage"""
        self.stdout.write('Migrating existing data to secure storage...')
        
        old_data_path = os.path.join('data')
        if not os.path.exists(old_data_path):
            self.stdout.write('No old data directory found')
            return
        
        # Migrate user data
        users_path = os.path.join(old_data_path, 'users')
        if os.path.exists(users_path):
            for filename in os.listdir(users_path):
                if filename.startswith('user_') and filename.endswith('.json'):
                    old_user_id = filename.replace('user_', '').replace('.json', '')
                    try:
                        old_user_id = int(old_user_id)
                        user = User.objects.get(id=old_user_id)
                        
                        # Read old data
                        with open(os.path.join(users_path, filename), 'r') as f:
                            old_data = json.load(f)
                        
                        # Save to secure storage
                        secure_storage.save_user_data(user)
                        self.stdout.write(f'  ✓ Migrated user {old_user_id}')
                        
                    except (ValueError, User.DoesNotExist):
                        self.stdout.write(f'  ✗ Skipped invalid user file: {filename}')
        
        # Migrate task data
        tasks_path = os.path.join(old_data_path, 'tasks')
        if os.path.exists(tasks_path):
            for filename in os.listdir(tasks_path):
                if filename.startswith('tasks_') and filename.endswith('.json'):
                    old_user_id = filename.replace('tasks_', '').replace('.json', '')
                    try:
                        old_user_id = int(old_user_id)
                        
                        # Read old task data
                        with open(os.path.join(tasks_path, filename), 'r') as f:
                            old_data = json.load(f)
                        
                        if 'tasks' in old_data:
                            for task in old_data['tasks']:
                                secure_storage.save_task_data(old_user_id, task)
                        
                        self.stdout.write(f'  ✓ Migrated tasks for user {old_user_id}')
                        
                    except (ValueError, json.JSONDecodeError):
                        self.stdout.write(f'  ✗ Skipped invalid task file: {filename}')
        
        # Migrate project data
        projects_path = os.path.join(old_data_path, 'projects')
        if os.path.exists(projects_path):
            for filename in os.listdir(projects_path):
                if filename.startswith('projects_') and filename.endswith('.json'):
                    old_user_id = filename.replace('projects_', '').replace('.json', '')
                    try:
                        old_user_id = int(old_user_id)
                        
                        # Read old project data
                        with open(os.path.join(projects_path, filename), 'r') as f:
                            old_data = json.load(f)
                        
                        if 'projects' in old_data:
                            for project in old_data['projects']:
                                secure_storage.save_project_data(old_user_id, project)
                        
                        self.stdout.write(f'  ✓ Migrated projects for user {old_user_id}')
                        
                    except (ValueError, json.JSONDecodeError):
                        self.stdout.write(f'  ✗ Skipped invalid project file: {filename}')
    
    def create_missing_user_files(self):
        """Create missing user data files for all users"""
        self.stdout.write('Creating missing user data files...')
        
        users = User.objects.all()
        for user in users:
            # Check if user data exists
            user_data = secure_storage.get_user_data(user.id)
            if not user_data:
                success = secure_storage.save_user_data(user)
                if success:
                    self.stdout.write(f'  ✓ Created data file for user {user.id}: {user.email}')
                else:
                    self.stdout.write(f'  ✗ Failed to create data file for user {user.id}')
            else:
                self.stdout.write(f'  - User {user.id} already has data file')
        
        self.stdout.write(f'Processed {users.count()} users')