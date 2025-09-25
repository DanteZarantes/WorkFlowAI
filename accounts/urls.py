"""
User Authentication URL Configuration

This file defines URL patterns for user authentication and account management.
Includes routes for:
- Django's built-in authentication views (login, logout, password reset)
- User registration (signup)
- User profile management

All URLs are prefixed with /accounts/ (e.g., http://localhost:8000/accounts/login/)
"""

from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .api_views import TaskAPIView, ProjectAPIView, ModelAPIView, dashboard_data

# URL patterns for user authentication and account management
urlpatterns = [
    # Django built-in authentication views
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('test-login/', LoginView.as_view(template_name='registration/test_login.html'), name='test_login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    
    # API endpoints for JSON data management
    path('api/tasks/', TaskAPIView.as_view(), name='api_tasks'),
    path('api/projects/', ProjectAPIView.as_view(), name='api_projects'),
    path('api/models/', ModelAPIView.as_view(), name='api_models'),
    path('api/dashboard/', dashboard_data, name='api_dashboard'),
]