"""
Enhanced API views for NeuralFlow project management
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q
from utils.secure_json_storage import secure_storage
from datetime import datetime, timedelta
import json

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_project(request):
    """Create a new project for the authenticated user"""
    try:
        project_data = {
            'name': request.data.get('name'),
            'description': request.data.get('description', ''),
            'status': request.data.get('status', 'not_started'),
            'priority': request.data.get('priority', 'medium'),
            'start_date': request.data.get('start_date'),
            'end_date': request.data.get('end_date'),
            'progress_percentage': 0,
            'collaborators': request.data.get('collaborators', [])
        }
        
        if not project_data['name']:
            return Response({'error': 'Project name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        success = secure_storage.save_project_data(request.user.id, project_data)
        
        if success:
            return Response({'message': 'Project created successfully', 'project': project_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to create project'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_projects(request):
    """Get all projects for the authenticated user"""
    try:
        projects = secure_storage.get_user_projects(request.user.id)
        return Response({'projects': projects}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    """Create a new task with hierarchical structure"""
    try:
        task_data = {
            'project_id': request.data.get('project_id'),
            'parent_task_id': request.data.get('parent_task_id'),
            'task_number': request.data.get('task_number'),
            'title': request.data.get('title'),
            'description': request.data.get('description', ''),
            'status': request.data.get('status', 'not_started'),
            'priority': request.data.get('priority', 'medium'),
            'progress_percentage': request.data.get('progress_percentage', 0),
            'start_date': request.data.get('start_date'),
            'end_date': request.data.get('end_date'),
            'assigned_to': request.data.get('assigned_to'),
            'email': request.data.get('email', ''),
            'phone': request.data.get('phone', ''),
            'estimated_hours': request.data.get('estimated_hours'),
            'actual_hours': request.data.get('actual_hours', 0)
        }
        
        if not task_data['title']:
            return Response({'error': 'Task title is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate hierarchical task number if not provided
        if not task_data['task_number']:
            tasks = secure_storage.get_user_tasks(request.user.id)
            if task_data['parent_task_id']:
                # Find parent task and generate subtask number
                parent_task = next((t for t in tasks if t.get('id') == task_data['parent_task_id']), None)
                if parent_task:
                    parent_number = parent_task.get('task_number', '1')
                    subtask_count = len([t for t in tasks if t.get('parent_task_id') == task_data['parent_task_id']])
                    task_data['task_number'] = f"{parent_number}.{subtask_count + 1}"
                else:
                    task_data['task_number'] = str(len(tasks) + 1)
            else:
                # Main task
                main_tasks = [t for t in tasks if not t.get('parent_task_id')]
                task_data['task_number'] = str(len(main_tasks) + 1)
        
        success = secure_storage.save_task_data(request.user.id, task_data)
        
        if success:
            return Response({'message': 'Task created successfully', 'task': task_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to create task'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_tasks(request):
    """Get all tasks for the authenticated user"""
    try:
        tasks = secure_storage.get_user_tasks(request.user.id)
        
        # Organize tasks hierarchically
        main_tasks = []
        task_dict = {task['id']: task for task in tasks}
        
        for task in tasks:
            if not task.get('parent_task_id'):
                # Main task
                task['subtasks'] = [t for t in tasks if t.get('parent_task_id') == task['id']]
                main_tasks.append(task)
        
        return Response({'tasks': main_tasks}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task_progress(request, task_id):
    """Update task progress and status"""
    try:
        progress = request.data.get('progress_percentage')
        status_value = request.data.get('status')
        
        if progress is None:
            return Response({'error': 'Progress percentage is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not (0 <= progress <= 100):
            return Response({'error': 'Progress must be between 0 and 100'}, status=status.HTTP_400_BAD_REQUEST)
        
        success = secure_storage.update_task_progress(request.user.id, int(task_id), progress, status_value)
        
        if success:
            return Response({'message': 'Task progress updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to update task progress'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_data(request):
    """Get comprehensive dashboard data with analytics"""
    try:
        dashboard_data = secure_storage.generate_dashboard_data(request.user.id)
        return Response(dashboard_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_directory(request):
    """Get public user directory for networking"""
    try:
        # Get users with public profiles
        public_users = User.objects.filter(is_profile_public=True).exclude(id=request.user.id)
        
        users_data = []
        for user in public_users:
            user_data = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'company_name': user.company_name,
                'job_title': user.job_title,
                'bio': user.bio,
                'location': user.location,
                'skill_level': user.skill_level,
                'date_joined': user.date_joined.isoformat()
            }
            users_data.append(user_data)
        
        return Response({'users': users_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_connection_request(request):
    """Send connection request to another user"""
    try:
        to_user_id = request.data.get('to_user_id')
        message = request.data.get('message', '')
        
        if not to_user_id:
            return Response({'error': 'Target user ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Save connection request in both users' data
        connection_data = {
            'from_user_id': request.user.id,
            'to_user_id': to_user_id,
            'message': message,
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        
        # Add to sender's data
        sender_data = secure_storage.get_user_data(request.user.id)
        if 'connections' not in sender_data:
            sender_data['connections'] = []
        sender_data['connections'].append(connection_data)
        secure_storage._write_secure_file(secure_storage._get_file_path('users', request.user.id), sender_data)
        
        # Add to receiver's data
        receiver_data = secure_storage.get_user_data(to_user_id)
        if 'connections' not in receiver_data:
            receiver_data['connections'] = []
        receiver_data['connections'].append(connection_data)
        secure_storage._write_secure_file(secure_storage._get_file_path('users', to_user_id), receiver_data)
        
        return Response({'message': 'Connection request sent successfully'}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_analytics_charts(request):
    """Get data for analytics charts"""
    try:
        tasks = secure_storage.get_user_tasks(request.user.id)
        projects = secure_storage.get_user_projects(request.user.id)
        
        # Chart 1: Task Status Distribution (Pie Chart)
        status_distribution = {}
        for task in tasks:
            status = task.get('status', 'not_started')
            status_distribution[status] = status_distribution.get(status, 0) + 1
        
        # Chart 2: Project Progress (Bar Chart)
        project_progress = []
        for project in projects:
            project_progress.append({
                'name': project.get('name', 'Unnamed'),
                'progress': project.get('progress_percentage', 0)
            })
        
        # Chart 3: Task Completion Timeline (Line Chart)
        completion_timeline = {}
        for task in tasks:
            if task.get('status') == 'completed' and task.get('completed_date'):
                date = task['completed_date'][:10]  # Get date part
                completion_timeline[date] = completion_timeline.get(date, 0) + 1
        
        charts_data = {
            'task_status_distribution': status_distribution,
            'project_progress': project_progress,
            'completion_timeline': completion_timeline
        }
        
        return Response({'charts': charts_data}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_automation(request):
    """Create AI automation configuration"""
    try:
        automation_data = {
            'name': request.data.get('name'),
            'automation_type': request.data.get('automation_type'),
            'trigger_conditions': request.data.get('trigger_conditions', {}),
            'actions': request.data.get('actions', {}),
            'is_active': request.data.get('is_active', True),
            'email_config': request.data.get('email_config', {}),
            'whatsapp_config': request.data.get('whatsapp_config', {}),
            'document_config': request.data.get('document_config', {}),
            'created_at': datetime.now().isoformat()
        }
        
        if not automation_data['name'] or not automation_data['automation_type']:
            return Response({'error': 'Name and automation type are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save automation data
        file_path = secure_storage._get_file_path('automations', request.user.id)
        existing_data = secure_storage._read_secure_file(file_path)
        
        if 'automations' not in existing_data:
            existing_data = {'automations': [], 'updated_at': None}
        
        automation_data['id'] = len(existing_data['automations']) + 1
        existing_data['automations'].append(automation_data)
        existing_data['updated_at'] = datetime.now().isoformat()
        
        success = secure_storage._write_secure_file(file_path, existing_data)
        
        if success:
            return Response({'message': 'Automation created successfully', 'automation': automation_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to create automation'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)