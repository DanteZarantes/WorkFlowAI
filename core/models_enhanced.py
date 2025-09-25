"""
Enhanced Core models with comprehensive data coverage
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from utils.helpers import generate_unique_filename
from utils.validators import validate_file_size, validate_image_extension

User = get_user_model()


class TimeStampedModel(models.Model):
    """Abstract base model with comprehensive timestamps"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)  # Soft delete
    
    class Meta:
        abstract = True


class Organization(TimeStampedModel):
    """Organization/Company model"""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    
    # Contact information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Address
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Organization details
    industry = models.CharField(max_length=100, blank=True)
    size = models.CharField(max_length=20, choices=[
        ('startup', '1-10 employees'),
        ('small', '11-50 employees'),
        ('medium', '51-200 employees'),
        ('large', '201-1000 employees'),
        ('enterprise', '1000+ employees'),
    ], blank=True)
    
    # Settings
    is_active = models.BooleanField(default=True)
    logo = models.ImageField(
        upload_to='organizations/logos/',
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_file_size]
    )
    
    # Subscription
    subscription_plan = models.CharField(max_length=20, default='free')
    subscription_expires = models.DateTimeField(null=True, blank=True)
    
    # Owner
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_organizations')
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name


class Project(TimeStampedModel):
    """Enhanced project model"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    
    # Ownership
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='projects',
        null=True,
        blank=True
    )
    
    # Project details
    project_type = models.CharField(max_length=50, choices=[
        ('research', 'Research'),
        ('development', 'Development'),
        ('production', 'Production'),
        ('experiment', 'Experiment'),
        ('prototype', 'Prototype'),
    ], default='development')
    
    status = models.CharField(max_length=20, choices=[
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('archived', 'Archived'),
    ], default='planning')
    
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], default='medium')
    
    # Timeline
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    
    # Settings
    is_public = models.BooleanField(default=False)
    is_template = models.BooleanField(default=False)
    
    # Collaboration
    collaborators = models.ManyToManyField(
        User,
        through='ProjectMembership',
        related_name='collaborated_projects'
    )
    
    # Resources
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        unique_together = ['owner', 'slug']
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['owner', 'status']),
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['project_type']),
        ]
    
    def __str__(self):
        return self.name


class ProjectMembership(models.Model):
    """Project membership with roles"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    role = models.CharField(max_length=20, choices=[
        ('viewer', 'Viewer'),
        ('contributor', 'Contributor'),
        ('editor', 'Editor'),
        ('admin', 'Admin'),
        ('owner', 'Owner'),
    ], default='contributor')
    
    permissions = models.JSONField(default=list, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    invited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_project_invitations'
    )
    
    class Meta:
        unique_together = ['user', 'project']
    
    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.role})"


class AIModel(TimeStampedModel):
    """Enhanced AI Model with comprehensive tracking"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    
    # Ownership
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_models')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ai_models')
    
    # Model details
    model_type = models.CharField(max_length=50, choices=[
        ('classification', 'Classification'),
        ('regression', 'Regression'),
        ('clustering', 'Clustering'),
        ('nlp', 'Natural Language Processing'),
        ('computer_vision', 'Computer Vision'),
        ('recommendation', 'Recommendation'),
        ('time_series', 'Time Series'),
        ('reinforcement_learning', 'Reinforcement Learning'),
        ('generative', 'Generative'),
        ('custom', 'Custom'),
    ])
    
    framework = models.CharField(max_length=50, choices=[
        ('tensorflow', 'TensorFlow'),
        ('pytorch', 'PyTorch'),
        ('scikit_learn', 'Scikit-learn'),
        ('keras', 'Keras'),
        ('xgboost', 'XGBoost'),
        ('lightgbm', 'LightGBM'),
        ('huggingface', 'Hugging Face'),
        ('custom', 'Custom'),
    ], blank=True)
    
    version = models.CharField(max_length=20, default='1.0.0')
    
    # Status and lifecycle
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('training', 'Training'),
        ('validating', 'Validating'),
        ('testing', 'Testing'),
        ('deployed', 'Deployed'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deprecated', 'Deprecated'),
        ('error', 'Error'),
    ], default='draft')
    
    # Performance metrics
    accuracy = models.FloatField(null=True, blank=True)
    precision = models.FloatField(null=True, blank=True)
    recall = models.FloatField(null=True, blank=True)
    f1_score = models.FloatField(null=True, blank=True)
    training_loss = models.FloatField(null=True, blank=True)
    validation_loss = models.FloatField(null=True, blank=True)
    
    # Training details
    training_data_size = models.IntegerField(default=0)
    validation_data_size = models.IntegerField(default=0)
    test_data_size = models.IntegerField(default=0)
    training_duration_minutes = models.IntegerField(null=True, blank=True)
    epochs = models.IntegerField(null=True, blank=True)
    batch_size = models.IntegerField(null=True, blank=True)
    learning_rate = models.FloatField(null=True, blank=True)
    
    # Deployment
    deployment_url = models.URLField(blank=True)
    api_endpoint = models.URLField(blank=True)
    deployment_config = models.JSONField(default=dict, blank=True)
    
    # Usage tracking
    api_calls_count = models.IntegerField(default=0)
    last_used = models.DateTimeField(null=True, blank=True)
    
    # Files and artifacts
    model_file = models.FileField(
        upload_to='models/',
        blank=True,
        null=True,
        validators=[validate_file_size]
    )
    config_file = models.FileField(
        upload_to='models/configs/',
        blank=True,
        null=True
    )
    
    # Settings
    is_public = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Metadata
    hyperparameters = models.JSONField(default=dict, blank=True)
    tags = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['owner', 'slug']
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['owner', 'status']),
            models.Index(fields=['project', 'status']),
            models.Index(fields=['model_type']),
            models.Index(fields=['is_public', 'is_featured']),
        ]
    
    def __str__(self):
        return f"{self.name} v{self.version}"


class Dataset(TimeStampedModel):
    """Dataset management"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    
    # Ownership
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='datasets')
    
    # Dataset details
    dataset_type = models.CharField(max_length=50, choices=[
        ('tabular', 'Tabular'),
        ('image', 'Image'),
        ('text', 'Text'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('time_series', 'Time Series'),
        ('graph', 'Graph'),
        ('mixed', 'Mixed'),
    ])
    
    format = models.CharField(max_length=20, choices=[
        ('csv', 'CSV'),
        ('json', 'JSON'),
        ('parquet', 'Parquet'),
        ('hdf5', 'HDF5'),
        ('tfrecord', 'TFRecord'),
        ('images', 'Images'),
        ('other', 'Other'),
    ])
    
    # Size and statistics
    file_size_bytes = models.BigIntegerField(default=0)
    row_count = models.IntegerField(default=0)
    column_count = models.IntegerField(default=0)
    
    # Quality metrics
    completeness_score = models.FloatField(null=True, blank=True)
    quality_score = models.FloatField(null=True, blank=True)
    
    # Files
    data_file = models.FileField(
        upload_to='datasets/',
        validators=[validate_file_size]
    )
    schema_file = models.FileField(
        upload_to='datasets/schemas/',
        blank=True,
        null=True
    )
    
    # Settings
    is_public = models.BooleanField(default=False)
    
    # Metadata
    schema = models.JSONField(default=dict, blank=True)
    statistics = models.JSONField(default=dict, blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    class Meta:
        unique_together = ['owner', 'slug']
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.name


class APIUsage(TimeStampedModel):
    """Comprehensive API usage tracking"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_usage')
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='usage_logs')
    
    # Request details
    endpoint = models.CharField(max_length=200)
    method = models.CharField(max_length=10, choices=[
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        ('PATCH', 'PATCH'),
    ])
    
    # Request/Response
    request_size_bytes = models.IntegerField(default=0)
    response_size_bytes = models.IntegerField(default=0)
    response_time_ms = models.IntegerField()
    status_code = models.IntegerField()
    
    # Client information
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    api_key = models.CharField(max_length=100, blank=True)
    
    # Billing
    cost = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    billing_tier = models.CharField(max_length=20, blank=True)
    
    # Metadata
    request_id = models.CharField(max_length=100, unique=True)
    error_message = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['ai_model', 'created_at']),
            models.Index(fields=['status_code']),
            models.Index(fields=['request_id']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.endpoint} ({self.status_code})"


class UserConnection(TimeStampedModel):
    """Enhanced user connections"""
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_connections')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_connections')
    
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('blocked', 'Blocked'),
    ], default='pending')
    
    connection_type = models.CharField(max_length=20, choices=[
        ('follow', 'Follow'),
        ('friend', 'Friend'),
        ('colleague', 'Colleague'),
        ('mentor', 'Mentor'),
        ('student', 'Student'),
    ], default='follow')
    
    message = models.TextField(blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['from_user', 'to_user']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['from_user', 'status']),
            models.Index(fields=['to_user', 'status']),
        ]
    
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"


class Notification(TimeStampedModel):
    """Enhanced notification system"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    notification_type = models.CharField(max_length=50, choices=[
        ('connection_request', 'Connection Request'),
        ('connection_accepted', 'Connection Accepted'),
        ('project_invitation', 'Project Invitation'),
        ('model_trained', 'Model Training Complete'),
        ('model_deployed', 'Model Deployed'),
        ('api_limit_warning', 'API Limit Warning'),
        ('api_limit_reached', 'API Limit Reached'),
        ('subscription_expiring', 'Subscription Expiring'),
        ('subscription_expired', 'Subscription Expired'),
        ('security_alert', 'Security Alert'),
        ('system_update', 'System Update'),
        ('maintenance', 'Maintenance'),
        ('custom', 'Custom'),
    ])
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Notification settings
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], default='medium')
    
    # Actions
    action_url = models.URLField(blank=True)
    action_text = models.CharField(max_length=50, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Delivery
    sent_via_email = models.BooleanField(default=False)
    sent_via_push = models.BooleanField(default=False)
    
    # Related objects
    related_object_type = models.CharField(max_length=50, blank=True)
    related_object_id = models.CharField(max_length=100, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['priority']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class FileUpload(TimeStampedModel):
    """Enhanced file upload tracking"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files', null=True, blank=True)
    
    # File details
    file = models.FileField(
        upload_to=generate_unique_filename,
        validators=[validate_file_size]
    )
    original_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    content_type = models.CharField(max_length=100)
    file_hash = models.CharField(max_length=64, blank=True)  # SHA-256
    
    # Classification
    file_type = models.CharField(max_length=50, choices=[
        ('dataset', 'Dataset'),
        ('model', 'Model'),
        ('config', 'Configuration'),
        ('image', 'Image'),
        ('document', 'Document'),
        ('code', 'Code'),
        ('other', 'Other'),
    ])
    
    # Processing
    is_processed = models.BooleanField(default=False)
    processing_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    
    processing_error = models.TextField(blank=True)
    
    # Access control
    is_public = models.BooleanField(default=False)
    access_count = models.IntegerField(default=0)
    
    # Metadata
    description = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'file_type']),
            models.Index(fields=['project']),
            models.Index(fields=['is_processed']),
        ]
    
    def __str__(self):
        return f"{self.original_name} - {self.user.username}"


class SystemLog(models.Model):
    """System-wide logging"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    level = models.CharField(max_length=20, choices=[
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ])
    
    logger_name = models.CharField(max_length=100)
    message = models.TextField()
    
    # Context
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Additional data
    exception_type = models.CharField(max_length=100, blank=True)
    exception_message = models.TextField(blank=True)
    stack_trace = models.TextField(blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['level', 'created_at']),
            models.Index(fields=['logger_name']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.level} - {self.logger_name} - {self.created_at}"