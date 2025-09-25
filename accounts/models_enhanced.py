"""
Enhanced User models with comprehensive data coverage
"""
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from utils.validators import validate_phone_number, validate_image_extension, validate_file_size
from utils.helpers import generate_unique_filename


class UserGroup(models.Model):
    """Custom user groups with enhanced functionality"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    group_type = models.CharField(max_length=50, choices=[
        ('department', 'Department'),
        ('team', 'Team'),
        ('project', 'Project'),
        ('role', 'Role'),
        ('custom', 'Custom'),
    ], default='custom')
    
    # Group settings
    is_active = models.BooleanField(default=True)
    max_members = models.IntegerField(null=True, blank=True)
    requires_approval = models.BooleanField(default=False)
    
    # Permissions and access
    permissions = models.ManyToManyField(Permission, blank=True)
    parent_group = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, related_name='created_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['group_type', 'is_active']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def member_count(self):
        return self.members.filter(is_active=True).count()


class CustomUser(AbstractUser):
    """Enhanced User model with comprehensive data coverage"""
    # Primary identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=20, unique=True, blank=True)  # Custom user ID
    
    # Basic information
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=17,
        blank=True,
        validators=[validate_phone_number]
    )
    
    # Personal details
    middle_name = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ], blank=True)
    
    # Address information
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state_province = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Professional information
    user_type = models.CharField(max_length=20, choices=[
        ('individual', 'Individual'),
        ('business', 'Business'),
        ('enterprise', 'Enterprise'),
        ('student', 'Student'),
        ('academic', 'Academic'),
        ('nonprofit', 'Non-profit'),
    ], default='individual')
    
    company_name = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    employee_id = models.CharField(max_length=50, blank=True)
    manager_email = models.EmailField(blank=True)
    
    # Profile and preferences
    bio = models.TextField(max_length=1000, blank=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_file_size]
    )
    cover_image = models.ImageField(
        upload_to='covers/',
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_file_size]
    )
    
    # Skills and experience
    skill_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ], default='beginner')
    
    experience_years = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    
    # Social links
    website = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    # Privacy and notification settings
    is_profile_public = models.BooleanField(default=True)
    show_email = models.BooleanField(default=False)
    show_phone = models.BooleanField(default=False)
    show_location = models.BooleanField(default=True)
    show_social_links = models.BooleanField(default=True)
    
    receive_notifications = models.BooleanField(default=True)
    receive_marketing_emails = models.BooleanField(default=False)
    receive_product_updates = models.BooleanField(default=True)
    receive_security_alerts = models.BooleanField(default=True)
    
    # Subscription and billing
    subscription_plan = models.CharField(max_length=20, choices=[
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('pro', 'Professional'),
        ('enterprise', 'Enterprise'),
        ('custom', 'Custom'),
    ], default='free')
    
    subscription_status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
        ('trial', 'Trial'),
    ], default='active')
    
    subscription_starts = models.DateTimeField(null=True, blank=True)
    subscription_expires = models.DateTimeField(null=True, blank=True)
    billing_cycle = models.CharField(max_length=20, choices=[
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('lifetime', 'Lifetime'),
    ], blank=True)
    
    # Usage and limits
    api_calls_limit = models.IntegerField(default=1000)
    api_calls_used = models.IntegerField(default=0)
    storage_limit_gb = models.IntegerField(default=5)
    storage_used_gb = models.FloatField(default=0.0)
    projects_limit = models.IntegerField(default=10)
    models_limit = models.IntegerField(default=5)
    
    # Security and authentication
    two_factor_enabled = models.BooleanField(default=False)
    backup_codes = models.JSONField(default=list, blank=True)
    security_questions = models.JSONField(default=dict, blank=True)
    password_changed_at = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    
    # Activity tracking
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    login_count = models.IntegerField(default=0)
    
    # Account status
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    verification_expires = models.DateTimeField(null=True, blank=True)
    
    # Group memberships
    user_groups = models.ManyToManyField(
        UserGroup,
        through='UserGroupMembership',
        related_name='members'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)  # Soft delete
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_id']),
            models.Index(fields=['user_type']),
            models.Index(fields=['subscription_plan']),
            models.Index(fields=['is_active', 'is_verified']),
            models.Index(fields=['created_at']),
            models.Index(fields=['last_activity']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.user_id:
            # Generate custom user ID
            last_user = CustomUser.objects.filter(user_id__startswith='USR').order_by('-user_id').first()
            if last_user and last_user.user_id:
                last_num = int(last_user.user_id[3:])
                self.user_id = f'USR{last_num + 1:06d}'
            else:
                self.user_id = 'USR000001'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name]
        return ' '.join(filter(None, parts)) or self.username
    
    @property
    def api_calls_remaining(self):
        return max(0, self.api_calls_limit - self.api_calls_used)
    
    @property
    def storage_remaining_gb(self):
        return max(0, self.storage_limit_gb - self.storage_used_gb)
    
    @property
    def subscription_active(self):
        if self.subscription_expires:
            return timezone.now() < self.subscription_expires
        return self.subscription_status == 'active'
    
    def can_make_api_call(self):
        return self.api_calls_used < self.api_calls_limit and self.subscription_active
    
    def increment_api_usage(self, count=1):
        self.api_calls_used += count
        self.last_activity = timezone.now()
        self.save(update_fields=['api_calls_used', 'last_activity'])


class UserGroupMembership(models.Model):
    """Through model for user-group relationships"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    
    role = models.CharField(max_length=50, choices=[
        ('member', 'Member'),
        ('admin', 'Admin'),
        ('owner', 'Owner'),
        ('moderator', 'Moderator'),
    ], default='member')
    
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('suspended', 'Suspended'),
        ('left', 'Left'),
    ], default='active')
    
    joined_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_memberships'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'group']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['group', 'role']),
        ]
    
    def __str__(self):
        return f"{self.user.username} in {self.group.name} ({self.role})"


class UserProfile(models.Model):
    """Extended profile information"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    
    # Professional details
    skills = models.JSONField(default=list, blank=True)
    interests = models.JSONField(default=list, blank=True)
    languages = models.JSONField(default=list, blank=True)
    certifications = models.JSONField(default=list, blank=True)
    education = models.JSONField(default=list, blank=True)
    work_experience = models.JSONField(default=list, blank=True)
    
    # Preferences
    theme = models.CharField(max_length=20, choices=[
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto'),
    ], default='auto')
    
    language = models.CharField(max_length=10, default='en')
    date_format = models.CharField(max_length=20, default='YYYY-MM-DD')
    time_format = models.CharField(max_length=10, choices=[
        ('12', '12 Hour'),
        ('24', '24 Hour'),
    ], default='24')
    
    # Statistics
    profile_views = models.IntegerField(default=0)
    projects_count = models.IntegerField(default=0)
    connections_count = models.IntegerField(default=0)
    achievements = models.JSONField(default=list, blank=True)
    
    # Custom fields
    custom_fields = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class UserActivity(models.Model):
    """Comprehensive user activity tracking"""
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('password_change', 'Password Change'),
        ('profile_update', 'Profile Update'),
        ('model_created', 'Model Created'),
        ('model_trained', 'Model Trained'),
        ('model_deleted', 'Model Deleted'),
        ('project_created', 'Project Created'),
        ('project_updated', 'Project Updated'),
        ('project_deleted', 'Project Deleted'),
        ('api_call', 'API Call'),
        ('file_upload', 'File Upload'),
        ('connection_request', 'Connection Request'),
        ('connection_accepted', 'Connection Accepted'),
        ('group_joined', 'Group Joined'),
        ('group_left', 'Group Left'),
        ('subscription_changed', 'Subscription Changed'),
        ('security_event', 'Security Event'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPES)
    description = models.CharField(max_length=255)
    
    # Request details
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    
    # Additional data
    metadata = models.JSONField(default=dict, blank=True)
    related_object_type = models.CharField(max_length=50, blank=True)
    related_object_id = models.CharField(max_length=100, blank=True)
    
    # Geolocation (optional)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['activity_type', 'created_at']),
            models.Index(fields=['ip_address']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()}"


class UserSession(models.Model):
    """Track user sessions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=100, unique=True)
    
    # Session details
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device_type = models.CharField(max_length=50, blank=True)
    browser = models.CharField(max_length=100, blank=True)
    os = models.CharField(max_length=100, blank=True)
    
    # Location
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['session_key']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.ip_address}"