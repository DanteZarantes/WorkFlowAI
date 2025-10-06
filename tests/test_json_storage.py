#!/usr/bin/env python
"""
Test script for JSON storage system
Run this to verify that the JSON storage is working correctly
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from utils.json_storage import json_storage
from utils.data_initializer import data_initializer

User = get_user_model()

def test_json_storage():
    """Test JSON storage functionality"""
    print("Testing NeuralFlow JSON Storage System")
    print("=" * 50)
    
    # Test 1: Initialize data structure
    print("1. Testing data structure initialization...")
    data_initializer.initialize_data_structure()
    print("Data structure initialized")
    
    # Test 2: Create test user if not exists
    print("\n2. Testing user data storage...")
    test_user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        test_user.set_password('testpass123')
        test_user.save()
        print("Test user created")
    else:
        print("Test user already exists")
    
    # Test 3: Save user data to JSON
    success = json_storage.save_user_data(test_user)
    if success:
        print("User data saved to JSON")
    else:
        print("Failed to save user data")
    
    # Test 4: Test task creation
    print("\n3. Testing task data storage...")
    task_data = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': 'high',
        'status': 'pending'
    }
    
    success = json_storage.save_task_data(test_user.id, task_data)
    if success:
        print("Task data saved to JSON")
    else:
        print("Failed to save task data")
    
    # Test 5: Test project creation
    print("\n4. Testing project data storage...")
    project_data = {
        'name': 'Test Project',
        'description': 'This is a test project',
        'status': 'active',
        'priority': 'medium'
    }
    
    success = json_storage.save_project_data(test_user.id, project_data)
    if success:
        print("Project data saved to JSON")
    else:
        print("Failed to save project data")
    
    # Test 6: Test model creation
    print("\n5. Testing AI model data storage...")
    model_data = {
        'name': 'Test Model',
        'description': 'This is a test AI model',
        'model_type': 'classification',
        'status': 'draft'
    }
    
    success = json_storage.save_model_data(test_user.id, model_data)
    if success:
        print("AI model data saved to JSON")
    else:
        print("Failed to save AI model data")
    
    # Test 7: Test data retrieval
    print("\n6. Testing data retrieval...")
    user_data = json_storage.get_user_data(test_user.id)
    tasks = json_storage.get_user_tasks(test_user.id)
    projects = json_storage.get_user_projects(test_user.id)
    models = json_storage.get_user_models(test_user.id)
    
    print(f"Retrieved user data: {bool(user_data)}")
    print(f"Retrieved {len(tasks)} tasks")
    print(f"Retrieved {len(projects)} projects")
    print(f"Retrieved {len(models)} AI models")
    
    # Test 8: Test activity logging
    print("\n7. Testing activity logging...")
    success = json_storage.update_user_activity(
        test_user.id,
        'test_activity',
        'This is a test activity'
    )
    if success:
        print("Activity logged successfully")
    else:
        print("Failed to log activity")
    
    # Test 9: Show storage statistics
    print("\n8. Storage statistics:")
    stats = data_initializer.get_storage_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 50)
    print("JSON Storage System test completed!")
    print("\nNext steps:")
    print("1. Run: python manage.py setup_data --sync-users")
    print("2. Test registration at: http://localhost:8000/accounts/signup/")
    print("3. Test login at: http://localhost:8000/accounts/login/")

if __name__ == '__main__':
    test_json_storage()