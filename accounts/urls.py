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
from . import views

# URL patterns for user authentication and account management
urlpatterns = [
    # Django's built-in authentication URLs
    # Includes: login/, logout/, password_change/, password_reset/, etc.
    path('', include('django.contrib.auth.urls')),
    
    # Custom authentication views
    path('signup/', views.signup, name='signup'),               # User Registration
    path('profile/', views.profile, name='profile'),           # User Profile Management
]