from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from utils.secure_json_storage import SecureJSONStorage
from core.models_enhanced import HierarchicalTask, UserConnection, AIAutomation, EnhancedProject
import json

User = get_user_model()

class Command(BaseCommand):
    help = 'Sync enhanced models and initialize secure storage for all users'

    def add_arguments(self, parser):
        parser.add_argument('--create-sample-data', action='store_true', help='Create sample data for testing')

    def handle(self, *args, **options):
        storage = SecureJSONStorage()
        
        self.stdout.write(self.style.SUCCESS('Starting enhanced models sync...'))
        
        # Initialize storage for all users
        users = User.objects.all()
        for user in users:
            self.stdout.write(f'Syncing user: {user.username} (ID: {user.id})')
            
            # Initialize user data if not exists
            user_data = storage.get_user_data(user.id)
            if not user_data:
                storage.save_user_data(user.id, {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'profile': {
                        'skills': [],
                        'preferences': {},
                        'account_type': 'personal'
                    },
                    'activities': [],
                    'created_at': user.date_joined.isoformat() if user.date_joined else None
                })
            
            # Create sample data if requested
            if options['create_sample_data']:
                self.create_sample_data(storage, user.id)
        
        self.stdout.write(self.style.SUCCESS('Enhanced models sync completed!'))
        
        # Display statistics
        self.display_statistics(storage)

    def create_sample_data(self, storage, user_id):
        """Create sample hierarchical tasks, connections, and automations"""
        
        # Sample hierarchical tasks
        sample_tasks = [
            {
                'id': f'task_{user_id}_1',
                'title': 'Project Setup',
                'description': 'Initialize new project workspace',
                'status': 'Completed',
                'priority': 'High',
                'progress': 100,
                'task_number': '1',
                'parent_id': None,
                'created_at': '2024-01-15T10:00:00Z'
            },
            {
                'id': f'task_{user_id}_1_1',
                'title': 'Environment Configuration',
                'description': 'Set up development environment',
                'status': 'Completed',
                'priority': 'High',
                'progress': 100,
                'task_number': '1.1',
                'parent_id': f'task_{user_id}_1',
                'created_at': '2024-01-15T10:30:00Z'
            },
            {
                'id': f'task_{user_id}_1_2',
                'title': 'Database Design',
                'description': 'Design database schema',
                'status': 'In Progress',
                'priority': 'Medium',
                'progress': 75,
                'task_number': '1.2',
                'parent_id': f'task_{user_id}_1',
                'created_at': '2024-01-15T11:00:00Z'
            },
            {
                'id': f'task_{user_id}_2',
                'title': 'Feature Development',
                'description': 'Implement core features',
                'status': 'In Progress',
                'priority': 'High',
                'progress': 45,
                'task_number': '2',
                'parent_id': None,
                'created_at': '2024-01-16T09:00:00Z'
            }
        ]
        
        # Sample user connections
        sample_connections = [
            {
                'id': f'conn_{user_id}_1',
                'connected_user_id': user_id + 1 if user_id > 1 else user_id + 2,
                'connection_type': 'colleague',
                'status': 'accepted',
                'created_at': '2024-01-10T14:00:00Z'
            }
        ]
        
        # Sample AI automations
        sample_automations = [
            {
                'id': f'auto_{user_id}_1',
                'name': 'Daily Status Report',
                'automation_type': 'email',
                'trigger_conditions': {'time': '09:00', 'frequency': 'daily'},
                'actions': {
                    'send_email': {
                        'to': 'team@company.com',
                        'subject': 'Daily Progress Update',
                        'template': 'daily_report'
                    }
                },
                'is_active': True,
                'created_at': '2024-01-12T16:00:00Z'
            }
        ]
        
        # Sample projects
        sample_projects = [
            {
                'id': f'proj_{user_id}_1',
                'title': 'AI Dashboard Enhancement',
                'description': 'Enhance dashboard with analytics and user management',
                'status': 'active',
                'progress': 65,
                'team_members': [user_id],
                'created_at': '2024-01-10T08:00:00Z'
            }
        ]
        
        # Save sample data
        storage.save_user_tasks(user_id, sample_tasks)
        storage.save_user_connections(user_id, sample_connections)
        storage.save_user_automations(user_id, sample_automations)
        storage.save_user_projects(user_id, sample_projects)
        
        self.stdout.write(f'  Created sample data for user {user_id}')

    def display_statistics(self, storage):
        """Display storage statistics"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('STORAGE STATISTICS'))
        self.stdout.write('='*50)
        
        users = User.objects.all()
        total_tasks = 0
        total_projects = 0
        total_connections = 0
        total_automations = 0
        
        for user in users:
            tasks = storage.get_user_tasks(user.id)
            projects = storage.get_user_projects(user.id)
            connections = storage.get_user_connections(user.id)
            automations = storage.get_user_automations(user.id)
            
            total_tasks += len(tasks)
            total_projects += len(projects)
            total_connections += len(connections)
            total_automations += len(automations)
            
            self.stdout.write(f'User {user.username}: {len(tasks)} tasks, {len(projects)} projects, {len(connections)} connections, {len(automations)} automations')
        
        self.stdout.write(f'\nTOTAL: {total_tasks} tasks, {total_projects} projects, {total_connections} connections, {total_automations} automations')
        self.stdout.write('='*50)