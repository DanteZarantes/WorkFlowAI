"""
Custom User model and related models
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from utils.validators import validate_phone_number, validate_image_extension, validate_file_size
from utils.helpers import generate_unique_filename


class CustomUser(AbstractUser):
    """Extended User model with additional fields"""
    USER_TYPES = [
        ('individual', 'Individual'),
        ('business', 'Business'),
        ('enterprise', 'Enterprise'),
    ]
    
    SKILL_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=17,
        blank=True,
        validators=[validate_phone_number]
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='individual')
    company_name = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    # Profile settings
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_file_size]
    )
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVELS, default='beginner')
    is_profile_public = models.BooleanField(default=True)
    receive_notifications = models.BooleanField(default=True)
    receive_marketing_emails = models.BooleanField(default=False)
    
    # Subscription and usage
    subscription_plan = models.CharField(max_length=20, default='free')
    api_calls_limit = models.IntegerField(default=1000)
    api_calls_used = models.IntegerField(default=0)
    subscription_expires = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_type']),
            models.Index(fields=['subscription_plan']),
        ]
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    @property
    def api_calls_remaining(self):
        return max(0, self.api_calls_limit - self.api_calls_used)
    
    @property
    def api_usage_percentage(self):
        if self.api_calls_limit == 0:
            return 0
        return (self.api_calls_used / self.api_calls_limit) * 100
    
    def can_make_api_call(self):
        return self.api_calls_used < self.api_calls_limit
    
    def increment_api_usage(self, count=1):
        self.api_calls_used += count
        self.save(update_fields=['api_calls_used'])


class UserProfile(models.Model):
    """Extended profile information"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    
    # Professional info
    skills = models.JSONField(default=list, blank=True)  # List of skills
    interests = models.JSONField(default=list, blank=True)  # List of interests
    experience_years = models.IntegerField(null=True, blank=True)
    education = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    
    # Social links
    twitter_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    # Privacy settings
    show_email = models.BooleanField(default=False)
    show_phone = models.BooleanField(default=False)
    show_location = models.BooleanField(default=True)
    
    # Statistics
    profile_views = models.IntegerField(default=0)
    projects_count = models.IntegerField(default=0)
    connections_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class UserActivity(models.Model):
    """Track user activity for analytics"""
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('model_created', 'Model Created'),
        ('model_trained', 'Model Trained'),
        ('api_call', 'API Call'),
        ('profile_updated', 'Profile Updated'),
        ('connection_made', 'Connection Made'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['activity_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()}"