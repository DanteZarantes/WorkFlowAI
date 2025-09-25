"""
Enhanced DRF Serializers for comprehensive API coverage
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models_enhanced import (
    CustomUser, UserGroup, UserGroupMembership, UserProfile,
    UserActivity, UserSession
)
from core.models_enhanced import (
    Organization, Project, ProjectMembership, AIModel, Dataset,
    APIUsage, UserConnection, Notification, FileUpload, SystemLog
)

User = get_user_model()


class UserGroupSerializer(serializers.ModelSerializer):
    """User Group serializer"""
    member_count = serializers.ReadOnlyField()
    
    class Meta:
        model = UserGroup
        fields = [
            'id', 'name', 'description', 'group_type', 'is_active',
            'max_members', 'requires_approval', 'member_count',
            'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'member_count']


class UserProfileSerializer(serializers.ModelSerializer):
    """User Profile serializer"""
    class Meta:
        model = UserProfile
        fields = [
            'skills', 'interests', 'languages', 'certifications',
            'education', 'work_experience', 'theme', 'language',
            'date_format', 'time_format', 'profile_views',
            'projects_count', 'connections_count', 'achievements',
            'custom_fields', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'profile_views', 'projects_count', 'connections_count',
            'created_at', 'updated_at'
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    """Enhanced User serializer"""
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    api_calls_remaining = serializers.ReadOnlyField()
    storage_remaining_gb = serializers.ReadOnlyField()
    subscription_active = serializers.ReadOnlyField()
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'user_id', 'username', 'email', 'first_name',
            'middle_name', 'last_name', 'full_name', 'phone_number',
            'date_of_birth', 'gender', 'address_line1', 'address_line2',
            'city', 'state_province', 'postal_code', 'country', 'timezone',
            'user_type', 'company_name', 'job_title', 'department',
            'employee_id', 'bio', 'avatar', 'cover_image', 'skill_level',
            'experience_years', 'website', 'linkedin_url', 'github_url',
            'twitter_url', 'facebook_url', 'instagram_url',
            'is_profile_public', 'show_email', 'show_phone', 'show_location',
            'show_social_links', 'subscription_plan', 'subscription_status',
            'api_calls_limit', 'api_calls_used', 'api_calls_remaining',
            'storage_limit_gb', 'storage_used_gb', 'storage_remaining_gb',
            'subscription_active', 'is_verified', 'last_activity',
            'profile', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user_id', 'full_name', 'api_calls_remaining',
            'storage_remaining_gb', 'subscription_active', 'is_verified',
            'last_activity', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }


class UserGroupMembershipSerializer(serializers.ModelSerializer):
    """User Group Membership serializer"""
    user = CustomUserSerializer(read_only=True)
    group = UserGroupSerializer(read_only=True)
    
    class Meta:
        model = UserGroupMembership
        fields = [
            'id', 'user', 'group', 'role', 'status',
            'joined_at', 'approved_by', 'approved_at'
        ]
        read_only_fields = ['id', 'joined_at', 'approved_at']


class UserActivitySerializer(serializers.ModelSerializer):
    """User Activity serializer"""
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = UserActivity
        fields = [
            'id', 'user', 'activity_type', 'description',
            'ip_address', 'user_agent', 'session_id', 'metadata',
            'related_object_type', 'related_object_id', 'country',
            'city', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserSessionSerializer(serializers.ModelSerializer):
    """User Session serializer"""
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = UserSession
        fields = [
            'id', 'user', 'session_key', 'ip_address', 'user_agent',
            'device_type', 'browser', 'os', 'country', 'city',
            'created_at', 'last_activity', 'expires_at', 'is_active'
        ]
        read_only_fields = [
            'id', 'session_key', 'created_at', 'last_activity'
        ]


class OrganizationSerializer(serializers.ModelSerializer):
    """Organization serializer"""
    owner = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'slug', 'description', 'email', 'phone',
            'website', 'address_line1', 'address_line2', 'city',
            'state', 'postal_code', 'country', 'industry', 'size',
            'is_active', 'logo', 'subscription_plan', 'subscription_expires',
            'owner', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class ProjectMembershipSerializer(serializers.ModelSerializer):
    """Project Membership serializer"""
    user = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = ProjectMembership
        fields = [
            'id', 'user', 'role', 'permissions', 'joined_at', 'invited_by'
        ]
        read_only_fields = ['id', 'joined_at']


class ProjectSerializer(serializers.ModelSerializer):
    """Enhanced Project serializer"""
    owner = CustomUserSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    collaborators = ProjectMembershipSerializer(
        source='projectmembership_set',
        many=True,
        read_only=True
    )
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'slug', 'description', 'owner', 'organization',
            'project_type', 'status', 'priority', 'start_date', 'end_date',
            'deadline', 'is_public', 'is_template', 'budget', 'tags',
            'metadata', 'collaborators', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class AIModelSerializer(serializers.ModelSerializer):
    """Enhanced AI Model serializer"""
    owner = CustomUserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    
    class Meta:
        model = AIModel
        fields = [
            'id', 'name', 'slug', 'description', 'owner', 'project',
            'model_type', 'framework', 'version', 'status', 'accuracy',
            'precision', 'recall', 'f1_score', 'training_loss',
            'validation_loss', 'training_data_size', 'validation_data_size',
            'test_data_size', 'training_duration_minutes', 'epochs',
            'batch_size', 'learning_rate', 'deployment_url', 'api_endpoint',
            'deployment_config', 'api_calls_count', 'last_used',
            'model_file', 'config_file', 'is_public', 'is_featured',
            'hyperparameters', 'tags', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'slug', 'api_calls_count', 'last_used',
            'created_at', 'updated_at'
        ]


class DatasetSerializer(serializers.ModelSerializer):
    """Dataset serializer"""
    owner = CustomUserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'name', 'slug', 'description', 'owner', 'project',
            'dataset_type', 'format', 'file_size_bytes', 'row_count',
            'column_count', 'completeness_score', 'quality_score',
            'data_file', 'schema_file', 'is_public', 'schema',
            'statistics', 'tags', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'slug', 'file_size_bytes', 'created_at', 'updated_at'
        ]


class APIUsageSerializer(serializers.ModelSerializer):
    """API Usage serializer"""
    user = CustomUserSerializer(read_only=True)
    ai_model = AIModelSerializer(read_only=True)
    
    class Meta:
        model = APIUsage
        fields = [
            'id', 'user', 'ai_model', 'endpoint', 'method',
            'request_size_bytes', 'response_size_bytes', 'response_time_ms',
            'status_code', 'ip_address', 'user_agent', 'api_key',
            'cost', 'billing_tier', 'request_id', 'error_message',
            'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'request_id', 'created_at']


class UserConnectionSerializer(serializers.ModelSerializer):
    """User Connection serializer"""
    from_user = CustomUserSerializer(read_only=True)
    to_user = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = UserConnection
        fields = [
            'id', 'from_user', 'to_user', 'status', 'connection_type',
            'message', 'responded_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'responded_at', 'created_at', 'updated_at']


class NotificationSerializer(serializers.ModelSerializer):
    """Enhanced Notification serializer"""
    user = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'notification_type', 'title', 'message',
            'priority', 'action_url', 'action_text', 'is_read',
            'read_at', 'sent_via_email', 'sent_via_push',
            'related_object_type', 'related_object_id', 'metadata',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'read_at', 'sent_via_email', 'sent_via_push',
            'created_at', 'updated_at'
        ]


class FileUploadSerializer(serializers.ModelSerializer):
    """Enhanced File Upload serializer"""
    user = CustomUserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    
    class Meta:
        model = FileUpload
        fields = [
            'id', 'user', 'project', 'file', 'original_name',
            'file_size', 'content_type', 'file_hash', 'file_type',
            'is_processed', 'processing_status', 'processing_error',
            'is_public', 'access_count', 'description', 'tags',
            'metadata', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'file_size', 'content_type', 'file_hash',
            'is_processed', 'processing_status', 'processing_error',
            'access_count', 'created_at', 'updated_at'
        ]


class SystemLogSerializer(serializers.ModelSerializer):
    """System Log serializer"""
    user = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = SystemLog
        fields = [
            'id', 'level', 'logger_name', 'message', 'user',
            'ip_address', 'user_agent', 'exception_type',
            'exception_message', 'stack_trace', 'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


# Nested serializers for detailed views
class ProjectDetailSerializer(ProjectSerializer):
    """Detailed Project serializer with related objects"""
    ai_models = AIModelSerializer(many=True, read_only=True)
    datasets = DatasetSerializer(many=True, read_only=True)
    files = FileUploadSerializer(many=True, read_only=True)


class UserDetailSerializer(CustomUserSerializer):
    """Detailed User serializer with related objects"""
    owned_projects = ProjectSerializer(many=True, read_only=True)
    owned_models = AIModelSerializer(many=True, read_only=True)
    recent_activities = UserActivitySerializer(
        source='activities',
        many=True,
        read_only=True
    )
    active_sessions = UserSessionSerializer(
        source='sessions',
        many=True,
        read_only=True
    )


class AIModelDetailSerializer(AIModelSerializer):
    """Detailed AI Model serializer with usage stats"""
    usage_logs = APIUsageSerializer(many=True, read_only=True)
    
    class Meta(AIModelSerializer.Meta):
        fields = AIModelSerializer.Meta.fields + ['usage_logs']


# Summary serializers for list views
class UserSummarySerializer(serializers.ModelSerializer):
    """Minimal User serializer for lists"""
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'user_id', 'username', 'email', 'full_name',
            'avatar', 'user_type', 'is_verified'
        ]


class ProjectSummarySerializer(serializers.ModelSerializer):
    """Minimal Project serializer for lists"""
    owner = UserSummarySerializer(read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'slug', 'description', 'owner',
            'status', 'priority', 'created_at'
        ]


class AIModelSummarySerializer(serializers.ModelSerializer):
    """Minimal AI Model serializer for lists"""
    owner = UserSummarySerializer(read_only=True)
    
    class Meta:
        model = AIModel
        fields = [
            'id', 'name', 'slug', 'model_type', 'status',
            'accuracy', 'owner', 'created_at'
        ]