"""
Professional middleware for JSON storage operations
Handles automatic data synchronization and activity logging
"""
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .json_storage import json_storage
from accounts.models import UserProfile, UserActivity

User = get_user_model()

class JSONStorageMiddleware(MiddlewareMixin):
    """Middleware to handle JSON storage operations"""
    
    def process_request(self, request):
        """Process incoming requests"""
        # Add JSON storage manager to request
        request.json_storage = json_storage
        return None
    
    def process_response(self, request, response):
        """Process outgoing responses"""
        # Log API usage if it's an API endpoint
        if hasattr(request, 'user') and request.user.is_authenticated:
            if request.path.startswith('/accounts/api/'):
                json_storage.update_user_activity(
                    request.user.id,
                    'api_call',
                    f'API call to {request.path}',
                    {
                        'method': request.method,
                        'status_code': response.status_code,
                        'ip_address': request.META.get('REMOTE_ADDR')
                    }
                )
        
        return response

# Signal handlers for automatic JSON storage sync
@receiver(post_save, sender=User)
def sync_user_to_json(sender, instance, created, **kwargs):
    """Automatically sync user data to JSON when user is saved"""
    try:
        json_storage.save_user_data(instance)
        
        if created:
            # Create user profile if it doesn't exist
            UserProfile.objects.get_or_create(user=instance)
            
            # Log user creation
            json_storage.update_user_activity(
                instance.id,
                'account_created',
                'User account created'
            )
    except Exception as e:
        # Log error but don't break the application
        print(f"Error syncing user {instance.username} to JSON: {str(e)}")

@receiver(post_save, sender=UserProfile)
def sync_profile_to_json(sender, instance, **kwargs):
    """Automatically sync user profile data to JSON when profile is saved"""
    try:
        json_storage.save_user_data(instance.user)
    except Exception as e:
        print(f"Error syncing profile for {instance.user.username} to JSON: {str(e)}")

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Log user login activity"""
    try:
        json_storage.update_user_activity(
            user.id,
            'login',
            'User logged in',
            {
                'ip_address': request.META.get('REMOTE_ADDR'),
                'user_agent': request.META.get('HTTP_USER_AGENT', '')[:200]
            }
        )
    except Exception as e:
        print(f"Error logging login for {user.username}: {str(e)}")

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Log user logout activity"""
    try:
        if user:
            json_storage.update_user_activity(
                user.id,
                'logout',
                'User logged out',
                {
                    'ip_address': request.META.get('REMOTE_ADDR')
                }
            )
    except Exception as e:
        print(f"Error logging logout: {str(e)}")