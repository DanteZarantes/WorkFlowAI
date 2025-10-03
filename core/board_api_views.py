"""
Enhanced API views for board-based task and project management
"""
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from utils.board_storage import BoardStorage
import json

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def create_board(request):
    """Create a new board"""
    try:
        data = json.loads(request.body)
        board_storage = BoardStorage()
        
        # Ensure user_id is properly set
        user_id = request.user.id
        board_id = board_storage.create_board(user_id, data)
        
        return JsonResponse({
            'success': True,
            'board_id': board_id,
            'message': 'Board created successfully',
            'user_id': user_id  # Debug info
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
def get_boards(request):
    """Get all user boards"""
    try:
        board_storage = BoardStorage()
        user_id = request.user.id
        boards = board_storage.get_user_boards(user_id)
        
        # Filter boards to ensure they belong to current user
        user_boards = [board for board in boards if board.get('owner_id') == user_id]
        
        return JsonResponse({
            'success': True,
            'boards': user_boards,
            'user_id': user_id  # Debug info
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def create_board_task(request):
    """Create task in specific board"""
    try:
        data = json.loads(request.body)
        board_id = data.get('board_id')
        
        # Create default board if no board_id provided
        if not board_id:
            board_storage = BoardStorage()
            board_id = board_storage.create_board(request.user.id, {
                'name': 'Default Tasks',
                'description': 'Default board for tasks',
                'type': 'dashboard'
            })
            data['board_id'] = board_id
        
        board_storage = BoardStorage()
        success = board_storage.save_board_task(request.user.id, board_id, data)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'Task created successfully'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Failed to create task'
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
def get_board_tasks(request, board_id):
    """Get tasks for specific board"""
    try:
        board_storage = BoardStorage()
        tasks = board_storage.get_board_tasks(request.user.id, board_id)
        
        return JsonResponse({
            'success': True,
            'tasks': tasks
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def create_board_project(request):
    """Create project in specific board"""
    try:
        data = json.loads(request.body)
        board_id = data.get('board_id')
        
        # Create default board if no board_id provided
        if not board_id:
            board_storage = BoardStorage()
            board_id = board_storage.create_board(request.user.id, {
                'name': 'Default Projects',
                'description': 'Default board for projects',
                'type': 'dashboard'
            })
            data['board_id'] = board_id
        
        board_storage = BoardStorage()
        success = board_storage.save_board_project(request.user.id, board_id, data)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'Project created successfully'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Failed to create project'
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
def get_board_projects(request, board_id):
    """Get projects for specific board"""
    try:
        board_storage = BoardStorage()
        projects = board_storage.get_board_projects(request.user.id, board_id)
        
        return JsonResponse({
            'success': True,
            'projects': projects
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def update_board_task(request, board_id, task_id):
    """Update task in board"""
    try:
        data = json.loads(request.body)
        board_storage = BoardStorage()
        
        success = board_storage.update_board_task(request.user.id, board_id, task_id, data)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'Task updated successfully'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Failed to update task'
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_board_task(request, board_id, task_id):
    """Delete task from board"""
    try:
        board_storage = BoardStorage()
        success = board_storage.delete_board_task(request.user.id, board_id, task_id)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'Task deleted successfully'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Failed to delete task'
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)