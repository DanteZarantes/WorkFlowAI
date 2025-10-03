"""
Enhanced URL patterns for NeuralFlow API
"""
from django.urls import path
from . import api_views_enhanced

app_name = 'core_enhanced'

urlpatterns = [
    # Project Management
    path('api/projects/', api_views_enhanced.create_project, name='create_project'),
    path('api/projects/list/', api_views_enhanced.get_user_projects, name='get_user_projects'),
    
    # Task Management with Hierarchical Structure
    path('api/tasks/', api_views_enhanced.create_task, name='create_task'),
    path('api/tasks/list/', api_views_enhanced.get_user_tasks, name='get_user_tasks'),
    path('api/tasks/<int:task_id>/progress/', api_views_enhanced.update_task_progress, name='update_task_progress'),
    
    # Dashboard and Analytics
    path('api/dashboard/', api_views_enhanced.get_dashboard_data, name='get_dashboard_data'),
    path('api/analytics/charts/', api_views_enhanced.get_analytics_charts, name='get_analytics_charts'),
    
    # User Networking
    path('api/users/directory/', api_views_enhanced.get_user_directory, name='get_user_directory'),
    path('api/connections/send/', api_views_enhanced.send_connection_request, name='send_connection_request'),
    
    # AI Automation
    path('api/automations/', api_views_enhanced.create_automation, name='create_automation'),
]