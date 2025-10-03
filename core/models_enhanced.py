"""
Enhanced models for NeuralFlow project management system
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

User = get_user_model()

class EnhancedProject(models.Model):
    """Project model with hierarchical task structure"""
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    collaborators = models.ManyToManyField(User, blank=True, related_name='collaborated_projects')
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    progress_percentage = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class HierarchicalTask(models.Model):
    """Enhanced task model with hierarchical structure"""
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('blocked', 'Blocked'),
        ('deferred', 'Deferred'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(EnhancedProject, on_delete=models.CASCADE, related_name='tasks')
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks')
    
    # Task identification
    task_number = models.CharField(max_length=20)  # e.g., "1", "1.1", "1.2.1"
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Status and progress
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    progress_percentage = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Dates
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    # Assignment and contact
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Time tracking
    estimated_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    actual_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['task_number']
        unique_together = ['project', 'task_number']
    
    def __str__(self):
        return f"{self.task_number}: {self.title}"
    
    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.end_date and self.end_date < timezone.now().date() and self.status != 'completed'
    
    @property
    def is_on_time(self):
        return self.completed_date and self.end_date and self.completed_date.date() <= self.end_date

class UserConnection(models.Model):
    """User networking and connections"""
    CONNECTION_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('blocked', 'Blocked'),
    ]
    
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_connections')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_connections')
    status = models.CharField(max_length=10, choices=CONNECTION_STATUS, default='pending')
    message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['from_user', 'to_user']
    
    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.status})"

class AIAutomation(models.Model):
    """AI automation configurations"""
    AUTOMATION_TYPES = [
        ('email', 'Email Automation'),
        ('whatsapp', 'WhatsApp Automation'),
        ('document', 'Document Generation'),
        ('task_creation', 'Task Creation'),
        ('reminder', 'Reminder System'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='automations')
    name = models.CharField(max_length=100)
    automation_type = models.CharField(max_length=20, choices=AUTOMATION_TYPES)
    
    # Configuration
    trigger_conditions = models.JSONField(default=dict)
    actions = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    
    # Integration settings
    email_config = models.JSONField(default=dict, blank=True)
    whatsapp_config = models.JSONField(default=dict, blank=True)
    document_config = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.automation_type})"

class TaskAnalytics(models.Model):
    """Task analytics and reporting"""
    project = models.OneToOneField(EnhancedProject, on_delete=models.CASCADE, related_name='analytics')
    
    # Completion metrics
    total_tasks = models.IntegerField(default=0)
    completed_tasks = models.IntegerField(default=0)
    overdue_tasks = models.IntegerField(default=0)
    on_time_completions = models.IntegerField(default=0)
    
    # Time metrics
    average_completion_time = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_estimated_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_actual_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Progress tracking
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    efficiency_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics for {self.project.name}"