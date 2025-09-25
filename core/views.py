from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from utils.json_storage import json_storage

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def services(request):
    return render(request, 'core/services.html')

def contact(request):
    return render(request, 'core/contact.html')

@login_required
def dashboard(request):
    # Get user data from JSON storage for dashboard
    user_data = json_storage.get_user_data(request.user.id)
    tasks = json_storage.get_user_tasks(request.user.id)
    projects = json_storage.get_user_projects(request.user.id)
    models = json_storage.get_user_models(request.user.id)
    
    context = {
        'user_data': user_data,
        'stats': {
            'total_tasks': len(tasks),
            'completed_tasks': len([t for t in tasks if t.get('status') == 'completed']),
            'total_projects': len(projects),
            'active_projects': len([p for p in projects if p.get('status') == 'active']),
            'total_models': len(models),
            'active_models': len([m for m in models if m.get('status') == 'active'])
        },
        'recent_tasks': tasks[-5:] if tasks else [],
        'recent_projects': projects[-3:] if projects else [],
        'recent_activities': user_data.get('activities', [])[-10:] if user_data else []
    }
    
    return render(request, 'core/dashboard.html', context)

def pricing(request):
    return render(request, 'core/pricing.html')

def blog(request):
    return render(request, 'core/blog.html')

def case_studies(request):
    return render(request, 'core/case_studies.html')

def resources(request):
    return render(request, 'core/resources.html')

def careers(request):
    return render(request, 'core/careers.html')

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
    # Get user models from JSON storage
    user_models = json_storage.get_user_models(request.user.id)
    
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

def chatbots(request):
    return render(request, 'core/chatbots.html')

def computer_vision(request):
    return render(request, 'core/computer_vision.html')

def help_center(request):
    return render(request, 'core/help_center.html')

def ai_visualization(request):
    return render(request, 'core/ai_visualization.html')

def calculator(request):
    return render(request, 'core/calculator.html')

def text_analyzer(request):
    return render(request, 'core/text_analyzer.html')

def color_generator(request):
    return render(request, 'core/color_generator.html')

def user_directory(request):
    return render(request, 'core/user_directory.html')

def theme_settings(request):
    return render(request, 'core/theme_settings.html')

# Project Management Views
def project_boards(request):
    return render(request, 'core/project_boards.html')

def mindmap(request):
    return render(request, 'core/mindmap.html')

def task_tree(request):
    return render(request, 'core/task_tree.html')

def kanban(request):
    return render(request, 'core/kanban.html')

def ai_dashboard(request):
    return render(request, 'core/ai_dashboard.html')