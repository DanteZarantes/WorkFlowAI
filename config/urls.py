"""
Main URL Configuration for NeuralFlow Project

This file defines the main URL routing for the entire Django application.
It includes:
- Admin interface URLs
- API endpoints
- User authentication URLs
- Core application URLs
- Static/Media file serving (development only)

URL Structure:
- /admin/ - Django admin interface
- /api/ - REST API endpoints
- /accounts/ - User authentication (login, signup, profile)
- / - Main application pages (home, services, tools, etc.)
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.api_views import user_profile

# Main URL patterns for the application
urlpatterns = [
    # Django Admin Interface
    # Access at: http://localhost:8000/admin/
    path('admin/', admin.site.urls),
    
    # Core Application URLs
    # Includes: home, services, tools, dashboard, etc.
    # Access at: http://localhost:8000/
    path('', include('core.urls')),
    
    # User Authentication URLs
    # Includes: login, logout, signup, profile, password reset
    # Access at: http://localhost:8000/accounts/
    path('accounts/', include('accounts.urls')),
    
    # API Endpoint for User Profile
    # Access at: http://localhost:8000/api/auth/user/
    path('api/auth/user/', user_profile, name='api_user'),
]

# Serve static and media files during development
# In production, use a web server (nginx/apache) to serve these files
if settings.DEBUG:
    # Media files (user uploads like avatars, documents)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Static files (CSS, JavaScript, images)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)