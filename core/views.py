from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from utils.secure_json_storage import SecureJSONStorage
from utils.board_storage import BoardStorage
import json

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')



def contact(request):
    return render(request, 'core/contact.html')

@login_required
def dashboard(request):
    # Initialize board storage
    board_storage = BoardStorage()
    
    # Get user data from boards
    user_data = board_storage.get_user_data(request.user.id)
    boards = board_storage.get_user_boards(request.user.id)
    tasks = board_storage.get_all_user_tasks(request.user.id)
    projects = board_storage.get_all_user_projects(request.user.id)
    
    # Calculate board-based statistics
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.get('status') == 'Completed'])
    task_stats = {
        'total': total_tasks,
        'completed': completed_tasks,
        'in_progress': len([t for t in tasks if t.get('status') == 'In Progress']),
        'blocked': len([t for t in tasks if t.get('status') == 'Blocked']),
        'not_started': len([t for t in tasks if t.get('status') == 'Not Started']),
        'completion_percentage': int((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0)
    }
    
    project_stats = {
        'total': len(projects),
        'active': len([p for p in projects if p.get('status') == 'active']),
        'completed': len([p for p in projects if p.get('status') == 'completed']),
        'on_hold': len([p for p in projects if p.get('status') == 'on_hold'])
    }
    
    context = {
        'user_data': user_data,
        'boards': boards,
        'task_stats': task_stats,
        'project_stats': project_stats,
        'recent_tasks': tasks[-5:] if tasks else [],
        'recent_projects': projects[-3:] if projects else [],
        'automations_count': 0,  # Will be implemented later
        'connections_count': 0,  # Will be implemented later
        'recent_activities': user_data.get('activities', [])[-10:] if user_data else []
    }
    
    return render(request, 'core/enhanced_dashboard.html', context)

def pricing(request):
    return render(request, 'core/pricing.html')

def blog(request):
    return render(request, 'core/blog.html')

def case_studies(request):
    return render(request, 'core/case_studies.html')

def resources(request):
    return render(request, 'core/resources.html')



def privacy(request):
    return render(request, 'core/privacy.html')

def terms(request):
    return render(request, 'core/terms.html')

def api_docs(request):
    return render(request, 'core/api_docs.html')

def tutorials(request):
    return render(request, 'core/tutorials.html')

def community(request):
    return render(request, 'core/community.html')

@login_required
def analytics(request):
    return render(request, 'core/analytics.html')

@login_required
def models(request):
    # Get user models from secure storage
    storage = SecureJSONStorage()
    user_models = storage.get_user_models(request.user.id) if hasattr(storage, 'get_user_models') else []
    
    context = {
        'models': user_models,
        'total_models': len(user_models),
        'active_models': len([m for m in user_models if m.get('status') == 'active']),
        'draft_models': len([m for m in user_models if m.get('status') == 'draft'])
    }
    
    return render(request, 'core/models.html', context)

@login_required
def settings(request):
    return render(request, 'core/settings.html')

def team(request):
    return render(request, 'core/team.html')

def press(request):
    return render(request, 'core/press.html')

def machine_learning(request):
    return render(request, 'core/machine_learning.html')







def ai_visualization(request):
    return render(request, 'core/ai_visualization.html')







def user_directory(request):
    return render(request, 'core/user_directory.html')

def theme_settings(request):
    return render(request, 'core/theme_settings.html')

# Project Management Views
def project_boards(request):
    return render(request, 'core/project_boards.html')





def kanban(request):
    return render(request, 'core/kanban.html')

def ai_dashboard(request):
    return render(request, 'core/ai_dashboard.html')

def mindmap(request):
    return render(request, 'core/mindmap.html')

def task_tree(request):
    return render(request, 'core/task_tree.html')