#!/usr/bin/env python
"""
Initialize Enhanced Features for NeuralFlow
This script sets up secure storage and sample data for all users
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from utils.secure_json_storage import SecureJSONStorage
import json
from datetime import datetime, timedelta

User = get_user_model()

def initialize_enhanced_features():
    """Initialize enhanced features for all users"""
    storage = SecureJSONStorage()
    
    print("Initializing Enhanced Features...")
    print("="*50)
    
    # Get all users
    users = User.objects.all()
    if not users.exists():
        print("No users found. Please create a user first.")
        return
    
    for user in users:
        print(f"Setting up user: {user.username} (ID: {user.id})")
        
        # Initialize user data
        user_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'profile': {
                'skills': ['Python', 'Django', 'AI/ML', 'Project Management'],
                'preferences': {
                    'theme': 'dark',
                    'notifications': True,
                    'auto_sync': True
                },
                'account_type': 'personal'
            },
            'activities': [
                {
                    'id': f'activity_{user.id}_1',
                    'type': 'login',
                    'description': 'User logged in',
                    'timestamp': datetime.now().isoformat()
                },
                {
                    'id': f'activity_{user.id}_2',
                    'type': 'project_created',
                    'description': 'Created new project workspace',
                    'timestamp': (datetime.now() - timedelta(hours=2)).isoformat()
                }
            ],
            'created_at': user.date_joined.isoformat() if user.date_joined else datetime.now().isoformat()
        }
        # Create user data file manually since save_user_data expects User object
        file_path = storage._get_file_path('users', user.id)
        storage._write_secure_file(file_path, user_data)
        
        # Create sample hierarchical tasks
        sample_tasks = [
            {
                'id': f'task_{user.id}_1',
                'title': 'Project Setup & Planning',
                'description': 'Initialize project workspace and define requirements',
                'status': 'Completed',
                'priority': 'High',
                'progress': 100,
                'task_number': '1',
                'parent_id': None,
                'start_date': '2024-01-15',
                'end_date': '2024-01-17',
                'estimated_hours': 8,
                'actual_hours': 6.5,
                'created_at': '2024-01-15T10:00:00Z'
            },
            {
                'id': f'task_{user.id}_1_1',
                'title': 'Environment Configuration',
                'description': 'Set up development environment and dependencies',
                'status': 'Completed',
                'priority': 'High',
                'progress': 100,
                'task_number': '1.1',
                'parent_id': f'task_{user.id}_1',
                'start_date': '2024-01-15',
                'end_date': '2024-01-16',
                'estimated_hours': 4,
                'actual_hours': 3.5,
                'created_at': '2024-01-15T10:30:00Z'
            },
            {
                'id': f'task_{user.id}_1_2',
                'title': 'Database Schema Design',
                'description': 'Design and implement database schema',
                'status': 'In Progress',
                'priority': 'Medium',
                'progress': 75,
                'task_number': '1.2',
                'parent_id': f'task_{user.id}_1',
                'start_date': '2024-01-16',
                'end_date': '2024-01-18',
                'estimated_hours': 6,
                'actual_hours': 4.5,
                'created_at': '2024-01-15T11:00:00Z'
            },
            {
                'id': f'task_{user.id}_2',
                'title': 'Feature Development',
                'description': 'Implement core application features',
                'status': 'In Progress',
                'priority': 'High',
                'progress': 45,
                'task_number': '2',
                'parent_id': None,
                'start_date': '2024-01-18',
                'end_date': '2024-01-25',
                'estimated_hours': 20,
                'actual_hours': 9,
                'created_at': '2024-01-16T09:00:00Z'
            },
            {
                'id': f'task_{user.id}_2_1',
                'title': 'User Authentication System',
                'description': 'Implement secure user authentication',
                'status': 'Completed',
                'priority': 'High',
                'progress': 100,
                'task_number': '2.1',
                'parent_id': f'task_{user.id}_2',
                'start_date': '2024-01-18',
                'end_date': '2024-01-20',
                'estimated_hours': 8,
                'actual_hours': 7,
                'created_at': '2024-01-16T09:30:00Z'
            },
            {
                'id': f'task_{user.id}_2_2',
                'title': 'Dashboard Analytics',
                'description': 'Create analytics dashboard with charts',
                'status': 'In Progress',
                'priority': 'Medium',
                'progress': 60,
                'task_number': '2.2',
                'parent_id': f'task_{user.id}_2',
                'start_date': '2024-01-20',
                'end_date': '2024-01-23',
                'estimated_hours': 12,
                'actual_hours': 7.5,
                'created_at': '2024-01-16T10:00:00Z'
            }
        ]
        # Save tasks manually
        file_path = storage._get_file_path('tasks', user.id)
        tasks_data = {'tasks': sample_tasks, 'updated_at': datetime.now().isoformat()}
        storage._write_secure_file(file_path, tasks_data)
        
        # Create sample projects
        sample_projects = [
            {
                'id': f'proj_{user.id}_1',
                'title': 'AI Dashboard Enhancement',
                'description': 'Enhance dashboard with advanced analytics, user management, and AI automation features',
                'status': 'active',
                'priority': 'high',
                'progress': 65,
                'start_date': '2024-01-10',
                'end_date': '2024-02-15',
                'team_members': [user.id],
                'created_at': '2024-01-10T08:00:00Z'
            },
            {
                'id': f'proj_{user.id}_2',
                'title': 'User Connection System',
                'description': 'Build networking system for user connections and collaboration',
                'status': 'active',
                'priority': 'medium',
                'progress': 30,
                'start_date': '2024-01-20',
                'end_date': '2024-02-28',
                'team_members': [user.id],
                'created_at': '2024-01-20T14:00:00Z'
            }
        ]
        # Save projects manually
        file_path = storage._get_file_path('projects', user.id)
        projects_data = {'projects': sample_projects, 'updated_at': datetime.now().isoformat()}
        storage._write_secure_file(file_path, projects_data)
        
        # Create sample user connections (if multiple users exist)
        if users.count() > 1:
            other_users = users.exclude(id=user.id)[:2]
            sample_connections = []
            for i, other_user in enumerate(other_users):
                sample_connections.append({
                    'id': f'conn_{user.id}_{other_user.id}',
                    'connected_user_id': other_user.id,
                    'connected_username': other_user.username,
                    'connection_type': 'colleague',
                    'status': 'accepted',
                    'message': 'Great to connect with you on NeuralFlow!',
                    'created_at': (datetime.now() - timedelta(days=i+1)).isoformat()
                })
            # Save connections manually
            file_path = storage._get_file_path('users', user.id)
            user_data = storage._read_secure_file(file_path)
            user_data['connections'] = sample_connections
            storage._write_secure_file(file_path, user_data)
        
        # Create sample AI automations
        sample_automations = [
            {
                'id': f'auto_{user.id}_1',
                'name': 'Daily Progress Report',
                'automation_type': 'email',
                'trigger_conditions': {
                    'time': '09:00',
                    'frequency': 'daily',
                    'days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
                },
                'actions': {
                    'send_email': {
                        'to': 'team@company.com',
                        'subject': 'Daily Progress Update - {{date}}',
                        'template': 'daily_report',
                        'include_tasks': True,
                        'include_analytics': True
                    }
                },
                'is_active': True,
                'created_at': '2024-01-12T16:00:00Z'
            },
            {
                'id': f'auto_{user.id}_2',
                'name': 'Task Deadline Reminder',
                'automation_type': 'whatsapp',
                'trigger_conditions': {
                    'task_due_in_hours': 24,
                    'task_status': ['in_progress', 'not_started']
                },
                'actions': {
                    'send_whatsapp': {
                        'message': 'Task "{{task_title}}" is due in 24 hours!',
                        'include_task_details': True
                    }
                },
                'is_active': False,
                'created_at': '2024-01-14T11:30:00Z'
            }
        ]
        # Save automations manually
        file_path = storage._get_file_path('automations', user.id)
        automations_data = {'automations': sample_automations, 'updated_at': datetime.now().isoformat()}
        storage._write_secure_file(file_path, automations_data)
        
        print(f"  Created {len(sample_tasks)} hierarchical tasks")
        print(f"  Created {len(sample_projects)} projects")
        print(f"  Created {len(sample_automations)} AI automations")
        if users.count() > 1:
            print(f"  Created user connections")
    
    print("\nEnhanced Features Initialization Complete!")
    print("="*50)
    print("Features Available:")
    print("  - Secure encrypted JSON storage")
    print("  - Hierarchical task management (1, 1.1, 1.2, etc.)")
    print("  - User connections and networking")
    print("  - AI automation framework")
    print("  - Advanced analytics dashboard")
    print("  - Custom UI with scrollbars and animations")
    print("  - Progress tracking with 6 status types")
    print("\nAccess your enhanced dashboard at: http://localhost:8000/dashboard/")

if __name__ == '__main__':
    initialize_enhanced_features()