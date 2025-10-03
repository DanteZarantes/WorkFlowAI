"""
Board-specific URL patterns
"""
from django.urls import path
from . import board_api_views

urlpatterns = [
    path('api/boards/', board_api_views.create_board, name='create_board'),
    path('api/boards/list/', board_api_views.get_boards, name='get_boards'),
    path('api/boards/tasks/', board_api_views.create_board_task, name='create_board_task'),
    path('api/boards/<str:board_id>/tasks/', board_api_views.get_board_tasks, name='get_board_tasks'),
    path('api/boards/projects/', board_api_views.create_board_project, name='create_board_project'),
    path('api/boards/<str:board_id>/projects/', board_api_views.get_board_projects, name='get_board_projects'),
    path('api/boards/<str:board_id>/tasks/<str:task_id>/', board_api_views.update_board_task, name='update_board_task'),
    path('api/boards/<str:board_id>/tasks/<str:task_id>/delete/', board_api_views.delete_board_task, name='delete_board_task'),
]