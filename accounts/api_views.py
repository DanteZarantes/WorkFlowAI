"""
Professional API views for task, project, and model management with JSON storage
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from utils.json_storage import json_storage
import json


@method_decorator(csrf_exempt, name='dispatch')
class TaskAPIView(View):
    """API endpoint for task management with JSON storage"""
    
    def post(self, request):
        """Create a new task"""
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        try:
            data = json.loads(request.body)
            task_data = {
                'title': data.get('title', ''),
                'description': data.get('description', ''),
                'priority': data.get('priority', 'medium'),
                'status': data.get('status', 'pending'),
                'category': data.get('category', 'general'),
                'due_date': data.get('due_date'),
                'tags': data.get('tags', []),
                'metadata': data.get('metadata', {})
            }
            
            # Save task to JSON
            success = json_storage.save_task_data(request.user.id, task_data)
            
            if success:
                # Log task creation activity
                json_storage.update_user_activity(
                    request.user.id,
                    'task_created',
                    f'Task created: {task_data["title"]}'
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Task created successfully',
                    'task': task_data
                })
            else:
                return JsonResponse({'error': 'Failed to save task'}, status=500)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def get(self, request):
        """Get user tasks"""
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        tasks = json_storage.get_user_tasks(request.user.id)
        return JsonResponse({'tasks': tasks})


@method_decorator(csrf_exempt, name='dispatch')
class ProjectAPIView(View):
    """API endpoint for project management with JSON storage"""
    
    def post(self, request):
        """Create a new project"""
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        try:
            data = json.loads(request.body)
            project_data = {
                'name': data.get('name', ''),
                'description': data.get('description', ''),
                'status': data.get('status', 'active'),
                'priority': data.get('priority', 'medium'),
                'start_date': data.get('start_date'),
                'end_date': data.get('end_date'),
                'team_members': data.get('team_members', []),
                'technologies': data.get('technologies', []),
                'budget': data.get('budget'),
                'metadata': data.get('metadata', {})
            }
            
            # Save project to JSON
            success = json_storage.save_project_data(request.user.id, project_data)
            
            if success:
                # Log project creation activity
                json_storage.update_user_activity(
                    request.user.id,
                    'project_created',
                    f'Project created: {project_data["name"]}'
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Project created successfully',
                    'project': project_data
                })
            else:
                return JsonResponse({'error': 'Failed to save project'}, status=500)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def get(self, request):
        """Get user projects"""
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        projects = json_storage.get_user_projects(request.user.id)
        return JsonResponse({'projects': projects})


@method_decorator(csrf_exempt, name='dispatch')
class ModelAPIView(View):
    """API endpoint for AI model management with JSON storage"""
    
    def post(self, request):
        """Create a new AI model"""
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        try:
            data = json.loads(request.body)
            model_data = {
                'name': data.get('name', ''),
                'description': data.get('description', ''),
                'model_type': data.get('model_type', 'classification'),
                'status': data.get('status', 'draft'),
                'accuracy': data.get('accuracy'),
                'training_data_size': data.get('training_data_size', 0),
                'parameters': data.get('parameters', {}),
                'hyperparameters': data.get('hyperparameters', {}),
                'performance_metrics': data.get('performance_metrics', {}),
                'is_public': data.get('is_public', False),
                'metadata': data.get('metadata', {})
            }
            
            # Save model to JSON
            success = json_storage.save_model_data(request.user.id, model_data)
            
            if success:
                # Log model creation activity
                json_storage.update_user_activity(
                    request.user.id,
                    'model_created',
                    f'AI Model created: {model_data["name"]}'
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'AI Model created successfully',
                    'model': model_data
                })
            else:
                return JsonResponse({'error': 'Failed to save model'}, status=500)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def get(self, request):
        """Get user AI models"""
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        models = json_storage.get_user_models(request.user.id)
        return JsonResponse({'models': models})


@login_required
def dashboard_data(request):
    """Get dashboard data from JSON storage"""
    user_data = json_storage.get_user_data(request.user.id)
    tasks = json_storage.get_user_tasks(request.user.id)
    projects = json_storage.get_user_projects(request.user.id)
    models = json_storage.get_user_models(request.user.id)
    
    dashboard_info = {
        'user': user_data,
        'stats': {
            'total_tasks': len(tasks),
            'completed_tasks': len([t for t in tasks if t.get('status') == 'completed']),
            'total_projects': len(projects),
            'active_projects': len([p for p in projects if p.get('status') == 'active']),
            'total_models': len(models),
            'active_models': len([m for m in models if m.get('status') == 'active'])
        },
        'recent_activities': user_data.get('activities', [])[-10:]
    }
    
    return JsonResponse(dashboard_info)