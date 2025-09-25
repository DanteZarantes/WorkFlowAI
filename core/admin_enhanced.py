"""
Enhanced Django Admin configuration for comprehensive data management
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from accounts.models_enhanced import (
    CustomUser, UserGroup, UserGroupMembership, UserProfile, 
    UserActivity, UserSession
)
from core.models_enhanced import (
    Organization, Project, ProjectMembership, AIModel, Dataset,
    APIUsage, UserConnection, Notification, FileUpload, SystemLog
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Enhanced User Admin"""
    list_display = [
        'user_id', 'email', 'username', 'full_name', 'user_type',
        'subscription_plan', 'is_verified', 'is_active', 'created_at'
    ]
    list_filter = [
        'user_type', 'subscription_plan', 'subscription_status',
        'is_verified', 'is_active', 'two_factor_enabled', 'created_at'
    ]
    search_fields = ['user_id', 'email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Personal Information', {
            'fields': (
                'user_id', 'middle_name', 'date_of_birth', 'gender',
                'phone_number', 'bio', 'avatar', 'cover_image'
            )
        }),
        ('Address', {
            'fields': (
                'address_line1', 'address_line2', 'city', 'state_province',
                'postal_code', 'country', 'timezone'
            )
        }),
        ('Professional', {
            'fields': (
                'user_type', 'company_name', 'job_title', 'department',
                'employee_id', 'manager_email', 'skill_level', 'experience_years'
            )
        }),
        ('Social Links', {
            'fields': (
                'website', 'linkedin_url', 'github_url', 'twitter_url',
                'facebook_url', 'instagram_url'
            )
        }),
        ('Privacy Settings', {
            'fields': (
                'is_profile_public', 'show_email', 'show_phone',
                'show_location', 'show_social_links'
            )
        }),
        ('Notifications', {
            'fields': (
                'receive_notifications', 'receive_marketing_emails',
                'receive_product_updates', 'receive_security_alerts'
            )
        }),
        ('Subscription', {
            'fields': (
                'subscription_plan', 'subscription_status', 'subscription_starts',
                'subscription_expires', 'billing_cycle'
            )
        }),
        ('Usage & Limits', {
            'fields': (
                'api_calls_limit', 'api_calls_used', 'storage_limit_gb',
                'storage_used_gb', 'projects_limit', 'models_limit'
            )
        }),
        ('Security', {
            'fields': (
                'two_factor_enabled', 'password_changed_at',
                'failed_login_attempts', 'account_locked_until'
            )
        }),
        ('Activity', {
            'fields': (
                'last_login_ip', 'last_activity', 'login_count',
                'is_verified', 'verification_expires'
            )
        }),
    )
    
    readonly_fields = ['user_id', 'created_at', 'updated_at', 'last_activity']
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    """User Group Admin"""
    list_display = ['name', 'group_type', 'member_count', 'is_active', 'created_at']
    list_filter = ['group_type', 'is_active', 'requires_approval']
    search_fields = ['name', 'description']
    prepopulated_fields = {'name': ('name',)}
    
    def member_count(self, obj):
        return obj.member_count
    member_count.short_description = 'Members'


@admin.register(UserGroupMembership)
class UserGroupMembershipAdmin(admin.ModelAdmin):
    """User Group Membership Admin"""
    list_display = ['user', 'group', 'role', 'status', 'joined_at']
    list_filter = ['role', 'status', 'joined_at']
    search_fields = ['user__username', 'user__email', 'group__name']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """User Profile Admin"""
    list_display = ['user', 'theme', 'language', 'profile_views', 'updated_at']
    list_filter = ['theme', 'language', 'updated_at']
    search_fields = ['user__username', 'user__email']


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """User Activity Admin"""
    list_display = ['user', 'activity_type', 'description', 'ip_address', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__username', 'description', 'ip_address']
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """User Session Admin"""
    list_display = ['user', 'ip_address', 'browser', 'os', 'country', 'is_active', 'last_activity']
    list_filter = ['is_active', 'browser', 'os', 'country', 'created_at']
    search_fields = ['user__username', 'ip_address', 'session_key']
    readonly_fields = ['session_key', 'created_at', 'last_activity']


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Organization Admin"""
    list_display = ['name', 'owner', 'industry', 'size', 'is_active', 'created_at']
    list_filter = ['industry', 'size', 'is_active', 'created_at']
    search_fields = ['name', 'slug', 'owner__username']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Enhanced Project Admin"""
    list_display = [
        'name', 'owner', 'organization', 'project_type', 'status',
        'priority', 'deadline', 'created_at'
    ]
    list_filter = [
        'project_type', 'status', 'priority', 'is_public',
        'is_template', 'created_at'
    ]
    search_fields = ['name', 'slug', 'owner__username', 'description']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'owner', 'organization')
        }),
        ('Project Details', {
            'fields': ('project_type', 'status', 'priority', 'tags')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'deadline')
        }),
        ('Settings', {
            'fields': ('is_public', 'is_template', 'budget')
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    """Project Membership Admin"""
    list_display = ['user', 'project', 'role', 'joined_at', 'invited_by']
    list_filter = ['role', 'joined_at']
    search_fields = ['user__username', 'project__name']


@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    """Enhanced AI Model Admin"""
    list_display = [
        'name', 'owner', 'project', 'model_type', 'framework',
        'version', 'status', 'accuracy', 'api_calls_count', 'created_at'
    ]
    list_filter = [
        'model_type', 'framework', 'status', 'is_public',
        'is_featured', 'created_at'
    ]
    search_fields = ['name', 'slug', 'owner__username', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'owner', 'project')
        }),
        ('Model Details', {
            'fields': ('model_type', 'framework', 'version', 'status', 'tags')
        }),
        ('Performance Metrics', {
            'fields': (
                'accuracy', 'precision', 'recall', 'f1_score',
                'training_loss', 'validation_loss'
            )
        }),
        ('Training Details', {
            'fields': (
                'training_data_size', 'validation_data_size', 'test_data_size',
                'training_duration_minutes', 'epochs', 'batch_size', 'learning_rate'
            )
        }),
        ('Deployment', {
            'fields': ('deployment_url', 'api_endpoint', 'deployment_config')
        }),
        ('Files', {
            'fields': ('model_file', 'config_file')
        }),
        ('Settings', {
            'fields': ('is_public', 'is_featured')
        }),
        ('Advanced', {
            'fields': ('hyperparameters', 'notes'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['api_calls_count', 'last_used']


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    """Dataset Admin"""
    list_display = [
        'name', 'owner', 'project', 'dataset_type', 'format',
        'row_count', 'file_size_mb', 'quality_score', 'created_at'
    ]
    list_filter = ['dataset_type', 'format', 'is_public', 'created_at']
    search_fields = ['name', 'slug', 'owner__username', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def file_size_mb(self, obj):
        return f"{obj.file_size_bytes / (1024*1024):.2f} MB"
    file_size_mb.short_description = 'File Size'


@admin.register(APIUsage)
class APIUsageAdmin(admin.ModelAdmin):
    """API Usage Admin"""
    list_display = [
        'user', 'ai_model', 'endpoint', 'method', 'status_code',
        'response_time_ms', 'cost', 'created_at'
    ]
    list_filter = [
        'method', 'status_code', 'billing_tier', 'created_at'
    ]
    search_fields = [
        'user__username', 'ai_model__name', 'endpoint',
        'request_id', 'ip_address'
    ]
    readonly_fields = ['request_id', 'created_at']
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(UserConnection)
class UserConnectionAdmin(admin.ModelAdmin):
    """User Connection Admin"""
    list_display = [
        'from_user', 'to_user', 'connection_type', 'status',
        'created_at', 'responded_at'
    ]
    list_filter = ['connection_type', 'status', 'created_at']
    search_fields = ['from_user__username', 'to_user__username']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Enhanced Notification Admin"""
    list_display = [
        'user', 'notification_type', 'title', 'priority',
        'is_read', 'sent_via_email', 'created_at'
    ]
    list_filter = [
        'notification_type', 'priority', 'is_read',
        'sent_via_email', 'sent_via_push', 'created_at'
    ]
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at', 'read_at']
    
    def mark_as_read(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_read=True, read_at=timezone.now())
    mark_as_read.short_description = "Mark selected notifications as read"
    
    actions = ['mark_as_read']


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    """Enhanced File Upload Admin"""
    list_display = [
        'original_name', 'user', 'project', 'file_type',
        'file_size_mb', 'processing_status', 'is_public', 'created_at'
    ]
    list_filter = [
        'file_type', 'processing_status', 'is_public', 'created_at'
    ]
    search_fields = ['original_name', 'user__username', 'description']
    readonly_fields = ['file_hash', 'file_size', 'created_at']
    
    def file_size_mb(self, obj):
        return f"{obj.file_size / (1024*1024):.2f} MB"
    file_size_mb.short_description = 'File Size'


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    """System Log Admin"""
    list_display = [
        'level', 'logger_name', 'message_preview', 'user',
        'ip_address', 'created_at'
    ]
    list_filter = ['level', 'logger_name', 'created_at']
    search_fields = ['message', 'user__username', 'ip_address']
    readonly_fields = ['created_at']
    
    def message_preview(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    message_preview.short_description = 'Message'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


# Custom admin site configuration
admin.site.site_header = "NeuralFlow Administration"
admin.site.site_title = "NeuralFlow Admin"
admin.site.index_title = "Welcome to NeuralFlow Administration"