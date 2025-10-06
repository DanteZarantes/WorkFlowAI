#!/usr/bin/env python
"""
Test script to verify board isolation between users
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from utils.board_storage import BoardStorage

User = get_user_model()

def test_board_isolation():
    """Test that boards are properly isolated between users"""
    print("Testing board isolation...")
    
    # Get or create test users
    user1, created1 = User.objects.get_or_create(
        username='testuser1',
        defaults={'email': 'test1@example.com'}
    )
    user2, created2 = User.objects.get_or_create(
        username='testuser2', 
        defaults={'email': 'test2@example.com'}
    )
    
    print(f"User 1: {user1.username} (ID: {user1.id})")
    print(f"User 2: {user2.username} (ID: {user2.id})")
    
    board_storage = BoardStorage()
    
    # Create boards for each user
    board1_data = {
        'name': 'User 1 Board',
        'description': 'This board belongs to user 1',
        'type': 'mindmap'
    }
    
    board2_data = {
        'name': 'User 2 Board', 
        'description': 'This board belongs to user 2',
        'type': 'kanban'
    }
    
    # Create boards
    board1_id = board_storage.create_board(user1.id, board1_data)
    board2_id = board_storage.create_board(user2.id, board2_data)
    
    print(f"Created board for user 1: {board1_id}")
    print(f"Created board for user 2: {board2_id}")
    
    # Test isolation - each user should only see their own boards
    user1_boards = board_storage.get_user_boards(user1.id)
    user2_boards = board_storage.get_user_boards(user2.id)
    
    print(f"\nUser 1 boards: {len(user1_boards)}")
    for board in user1_boards:
        print(f"  - {board['name']} (Owner: {board.get('owner_id')})")
        if board.get('owner_id') != user1.id:
            print(f"    ERROR: Board owner mismatch! Expected {user1.id}, got {board.get('owner_id')}")
    
    print(f"\nUser 2 boards: {len(user2_boards)}")
    for board in user2_boards:
        print(f"  - {board['name']} (Owner: {board.get('owner_id')})")
        if board.get('owner_id') != user2.id:
            print(f"    ERROR: Board owner mismatch! Expected {user2.id}, got {board.get('owner_id')}")
    
    # Test cross-contamination
    user1_board_names = [b['name'] for b in user1_boards]
    user2_board_names = [b['name'] for b in user2_boards]
    
    if 'User 2 Board' in user1_board_names:
        print("ERROR: User 1 can see User 2's board!")
        return False
    
    if 'User 1 Board' in user2_board_names:
        print("ERROR: User 2 can see User 1's board!")
        return False
    
    print("\nBoard isolation test PASSED!")
    return True

def test_task_isolation():
    """Test that tasks are properly isolated between users"""
    print("\nTesting task isolation...")
    
    user1 = User.objects.get(username='testuser1')
    user2 = User.objects.get(username='testuser2')
    
    board_storage = BoardStorage()
    
    # Get user boards
    user1_boards = board_storage.get_user_boards(user1.id)
    user2_boards = board_storage.get_user_boards(user2.id)
    
    if not user1_boards or not user2_boards:
        print("ERROR: No boards found for testing")
        return False
    
    board1_id = user1_boards[0]['id']
    board2_id = user2_boards[0]['id']
    
    # Create tasks for each user
    task1_data = {
        'title': 'User 1 Task',
        'description': 'This task belongs to user 1'
    }
    
    task2_data = {
        'title': 'User 2 Task',
        'description': 'This task belongs to user 2'
    }
    
    # Create tasks
    success1 = board_storage.save_board_task(user1.id, board1_id, task1_data)
    success2 = board_storage.save_board_task(user2.id, board2_id, task2_data)
    
    print(f"Task creation - User 1: {success1}, User 2: {success2}")
    
    # Test isolation
    user1_tasks = board_storage.get_board_tasks(user1.id, board1_id)
    user2_tasks = board_storage.get_board_tasks(user2.id, board2_id)
    
    print(f"User 1 tasks: {len(user1_tasks)}")
    for task in user1_tasks:
        print(f"  - {task['title']} (Owner: {task.get('owner_id')})")
        if task.get('owner_id') != user1.id:
            print(f"    ERROR: Task owner mismatch! Expected {user1.id}, got {task.get('owner_id')}")
    
    print(f"User 2 tasks: {len(user2_tasks)}")
    for task in user2_tasks:
        print(f"  - {task['title']} (Owner: {task.get('owner_id')})")
        if task.get('owner_id') != user2.id:
            print(f"    ERROR: Task owner mismatch! Expected {user2.id}, got {task.get('owner_id')}")
    
    # Test cross-access (user 1 trying to access user 2's board)
    cross_tasks = board_storage.get_board_tasks(user1.id, board2_id)
    if cross_tasks:
        print(f"ERROR: User 1 can access User 2's board tasks! Found {len(cross_tasks)} tasks")
        return False
    
    print("Task isolation test PASSED!")
    return True

if __name__ == '__main__':
    try:
        board_test = test_board_isolation()
        task_test = test_task_isolation()
        
        if board_test and task_test:
            print("\n✅ All isolation tests PASSED!")
        else:
            print("\n❌ Some isolation tests FAILED!")
            sys.exit(1)
            
    except Exception as e:
        print(f"Test error: {e}")
        sys.exit(1)