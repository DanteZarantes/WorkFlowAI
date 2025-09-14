"""
Core models for NeuralFlow application
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from utils.helpers import generate_unique_filename
from utils.validators import validate_file_size, validate_image_extension

User = get_user_model()


class TimeStampedModel(models.Model):
    """Abstract base model with created and updated timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class AIModel(TimeStampedModel):
    """AI Model configuration"""
    MODEL_TYPES = [
        ('classification', 'Classification'),
        ('regression', 'Regression'),
        ('nlp', 'Natural Language Processing'),
        ('computer_vision', 'Computer Vision'),
        ('recommendation', 'Recommendation'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('training', 'Training'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('error', 'Error'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_models')
    accuracy = models.FloatField(null=True, blank=True)
    training_data_size = models.IntegerField(default=0)
    api_calls_count = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['model_type']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_model_type_display()})"


class Project(TimeStampedModel):
    """User projects"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    ai_models = models.ManyToManyField(AIModel, blank=True, related_name='projects')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'name']
    
    def __str__(self):
        return self.name


class APIUsage(TimeStampedModel):
    """Track API usage for billing and analytics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_usage')
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='usage_logs')
    endpoint = models.CharField(max_length=100)
    request_count = models.IntegerField(default=1)
    response_time_ms = models.IntegerField(null=True, blank=True)
    status_code = models.IntegerField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['ai_model', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.endpoint} ({self.created_at})"


class UserConnection(TimeStampedModel):
    """User connections/following system"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_connections')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_connections')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['from_user', 'to_user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"


class Notification(TimeStampedModel):
    """User notifications"""
    NOTIFICATION_TYPES = [
        ('connection_request', 'Connection Request'),
        ('connection_accepted', 'Connection Accepted'),
        ('model_trained', 'Model Training Complete'),
        ('api_limit_reached', 'API Limit Reached'),
        ('system_update', 'System Update'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    action_url = models.URLField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class FileUpload(TimeStampedModel):
    """File uploads for training data, etc."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(
        upload_to=generate_unique_filename,
        validators=[validate_file_size]
    )
    original_name = models.CharField(max_length=255)
    file_size = models.IntegerField()
    content_type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_processed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.original_name} - {self.user.username}"