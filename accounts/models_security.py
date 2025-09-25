"""
Enterprise Security Models - SQL Server inspired security system for Django
"""
import uuid
import hashlib
import secrets
import ipaddress
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError


class WeakPassword(models.Model):
    """Common weak passwords blacklist"""
    password = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'security_weak_passwords'
        indexes = [models.Index(fields=['password'])]
    
    def __str__(self):
        return self.password


class SecurityEvent(models.Model):
    """Security event logging"""
    SEVERITY_CHOICES = [
        (0, 'Info'),
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Critical'),
    ]
    
    EVENT_TYPES = [
        ('LOGIN_SUCCESS', 'Login Success'),
        ('LOGIN_INVALID_USERNAME', 'Invalid Username'),
        ('LOGIN_INVALID_PASSWORD', 'Invalid Password'),
        ('LOGIN_EXPIRED_ACCOUNT', 'Expired Account'),
        ('LOGIN_LOCKED_ACCOUNT', 'Locked Account'),
        ('LOGIN_PRIVILEGE_DENY', 'Privilege Denied'),
        ('LOGIN_IPRANGE_DENY', 'IP Range Denied'),
        ('PASSWORD_CHANGE', 'Password Change'),
        ('ACCOUNT_LOCKED', 'Account Locked'),
        ('PRIVILEGE_GRANTED', 'Privilege Granted'),
        ('PRIVILEGE_REVOKED', 'Privilege Revoked'),
        ('SUSPICIOUS_ACTIVITY', 'Suspicious Activity'),
        ('BRUTE_FORCE_ATTEMPT', 'Brute Force Attempt'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application_name = models.CharField(max_length=50)
    event_datetime = models.DateTimeField(auto_now_add=True)
    remote_host = models.GenericIPAddressField()
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    severity = models.IntegerField(choices=SEVERITY_CHOICES)
    event_details = models.TextField()
    user = models.ForeignKey('SecurityUser', on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        db_table = 'security_events'
        ordering = ['-event_datetime']
        indexes = [
            models.Index(fields=['event_type', 'event_datetime']),
            models.Index(fields=['remote_host', 'event_datetime']),
            models.Index(fields=['severity', 'event_datetime']),
        ]
    
    def __str__(self):
        return f"{self.event_type} - {self.remote_host} - {self.event_datetime}"


class PasswordPolicy(models.Model):
    """Password policy configuration"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    policy_name = models.CharField(max_length=50, unique=True)
    min_password_length = models.IntegerField(validators=[MinValueValidator(4), MaxValueValidator(128)])
    min_lower_chars = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    min_upper_chars = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    min_numeric_chars = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    min_special_chars = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    allow_weak_passwords = models.BooleanField(default=False)
    password_expire_days = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(365)])
    min_password_reuse_days = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(365)])
    max_failed_attempts = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(20)])
    lockout_duration_minutes = models.IntegerField(default=30, validators=[MinValueValidator(1), MaxValueValidator(1440)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'security_password_policies'
    
    def __str__(self):
        return self.policy_name


class SecurityAccount(models.Model):
    """Security account with IP restrictions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_name = models.CharField(max_length=200, unique=True)
    password_policy = models.ForeignKey(PasswordPolicy, on_delete=models.PROTECT)
    ip_range_start = models.GenericIPAddressField(null=True, blank=True)
    ip_range_end = models.GenericIPAddressField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Account limits
    max_users = models.IntegerField(default=100, validators=[MinValueValidator(1)])
    max_concurrent_sessions = models.IntegerField(default=10, validators=[MinValueValidator(1)])
    
    # Subscription info
    subscription_expires = models.DateTimeField(null=True, blank=True)
    features_enabled = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'security_accounts'
        indexes = [models.Index(fields=['is_active'])]
    
    def __str__(self):
        return self.account_name
    
    def check_ip_range(self, ip_address):
        """Check if IP address is within allowed range"""
        if not self.ip_range_start or not self.ip_range_end:
            return True
        
        try:
            ip = ipaddress.ip_address(ip_address)
            start = ipaddress.ip_address(self.ip_range_start)
            end = ipaddress.ip_address(self.ip_range_end)
            return start <= ip <= end
        except ValueError:
            return False


class SecurityUser(AbstractUser):
    """Enhanced security user model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=20, unique=True, blank=True)  # Custom user ID
    account = models.ForeignKey(SecurityAccount, on_delete=models.CASCADE, related_name='users')
    
    # Enhanced user info
    display_name = models.CharField(max_length=200)
    employee_id = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    
    # Security fields
    password_hash = models.CharField(max_length=128)  # SHA-256 hash
    password_salt = models.CharField(max_length=32)   # Random salt
    must_reset_password = models.BooleanField(default=False)
    failed_login_attempts = models.IntegerField(default=0)
    locked_until_datetime = models.DateTimeField(null=True, blank=True)
    password_last_changed = models.DateTimeField(auto_now_add=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    login_count = models.IntegerField(default=0)
    
    # Two-factor authentication
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=32, blank=True)
    backup_codes = ArrayField(models.CharField(max_length=10), size=10, default=list, blank=True)
    
    # Account status
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    verification_expires = models.DateTimeField(null=True, blank=True)
    
    # Session management
    max_concurrent_sessions = models.IntegerField(default=3)
    session_timeout_minutes = models.IntegerField(default=60)
    
    # Audit fields
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'display_name']
    
    class Meta:
        db_table = 'security_users'
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['account', 'is_active']),
            models.Index(fields=['email']),
            models.Index(fields=['locked_until_datetime']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.user_id:
            # Generate custom user ID
            last_user = SecurityUser.objects.filter(user_id__startswith='USR').order_by('-user_id').first()
            if last_user and last_user.user_id:
                last_num = int(last_user.user_id[3:])
                self.user_id = f'USR{last_num + 1:06d}'
            else:
                self.user_id = 'USR000001'
        super().save(*args, **kwargs)
    
    def set_secure_password(self, raw_password):
        """Set password with salt and hash"""
        self.password_salt = secrets.token_hex(16)
        password_with_salt = f"{raw_password}{self.password_salt}"
        self.password_hash = hashlib.sha256(password_with_salt.encode()).hexdigest()
        self.password_last_changed = timezone.now()
        self.failed_login_attempts = 0
        self.locked_until_datetime = None
    
    def check_password(self, raw_password):
        """Check password against hash"""
        password_with_salt = f"{raw_password}{self.password_salt}"
        return hashlib.sha256(password_with_salt.encode()).hexdigest() == self.password_hash
    
    def is_account_locked(self):
        """Check if account is currently locked"""
        if self.locked_until_datetime:
            return timezone.now() < self.locked_until_datetime
        return False
    
    def lock_account(self):
        """Lock account based on policy"""
        policy = self.account.password_policy
        self.locked_until_datetime = timezone.now() + timedelta(minutes=policy.lockout_duration_minutes)
        self.save(update_fields=['locked_until_datetime'])
    
    def unlock_account(self):
        """Unlock account"""
        self.locked_until_datetime = None
        self.failed_login_attempts = 0
        self.save(update_fields=['locked_until_datetime', 'failed_login_attempts'])
    
    def increment_failed_attempts(self):
        """Increment failed login attempts"""
        self.failed_login_attempts += 1
        policy = self.account.password_policy
        if self.failed_login_attempts >= policy.max_failed_attempts:
            self.lock_account()
        else:
            self.save(update_fields=['failed_login_attempts'])
    
    def password_needs_reset(self):
        """Check if password needs to be reset"""
        if self.must_reset_password:
            return True
        
        policy = self.account.password_policy
        if policy.password_expire_days > 0:
            expire_date = self.password_last_changed + timedelta(days=policy.password_expire_days)
            return timezone.now() > expire_date
        
        return False
    
    def __str__(self):
        return f"{self.display_name} ({self.user_id})"


class UserPasswordHistory(models.Model):
    """Password history for reuse prevention"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(SecurityUser, on_delete=models.CASCADE, related_name='password_history')
    password_hash = models.CharField(max_length=128)
    date_changed = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'security_user_password_history'
        ordering = ['-date_changed']
        indexes = [
            models.Index(fields=['user', 'date_changed']),
        ]


class StoredLogin(models.Model):
    """Remember me / stored login tokens"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(SecurityUser, on_delete=models.CASCADE, related_name='stored_logins')
    application_name = models.CharField(max_length=50)
    login_code_hash = models.CharField(max_length=128)
    created_datetime = models.DateTimeField(auto_now_add=True)
    expires_datetime = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'security_stored_logins'
        indexes = [
            models.Index(fields=['user', 'application_name']),
            models.Index(fields=['expires_datetime']),
        ]
    
    def is_valid(self):
        """Check if stored login is still valid"""
        return self.is_active and timezone.now() <= self.expires_datetime


class Privilege(models.Model):
    """System privileges"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    privilege_code = models.CharField(max_length=50)
    application_name = models.CharField(max_length=50)
    privilege_description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'security_privileges'
        unique_together = ['privilege_code', 'application_name']
        indexes = [
            models.Index(fields=['application_name', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.privilege_code} - {self.application_name}"


class AccountPrivilege(models.Model):
    """Account-level privileges"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(SecurityAccount, on_delete=models.CASCADE, related_name='privileges')
    privilege = models.ForeignKey(Privilege, on_delete=models.CASCADE)
    assigned_by = models.CharField(max_length=100)
    assigned_datetime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'security_account_privileges'
        unique_together = ['account', 'privilege']


class UserPrivilege(models.Model):
    """User-level privileges"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(SecurityUser, on_delete=models.CASCADE, related_name='privileges')
    privilege = models.ForeignKey(Privilege, on_delete=models.CASCADE)
    assigned_by = models.CharField(max_length=100)
    assigned_datetime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'security_user_privileges'
        unique_together = ['user', 'privilege']


class UserConfiguration(models.Model):
    """User configuration options"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(SecurityUser, on_delete=models.CASCADE, related_name='configurations')
    application_name = models.CharField(max_length=50)
    config_key = models.CharField(max_length=100)
    config_value = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'security_user_configurations'
        unique_together = ['user', 'application_name', 'config_key']


class UserSession(models.Model):
    """Active user sessions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(SecurityUser, on_delete=models.CASCADE, related_name='active_sessions')
    session_key = models.CharField(max_length=100, unique=True)
    application_name = models.CharField(max_length=50)
    
    # Session details
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device_fingerprint = models.CharField(max_length=128, blank=True)
    
    # Location (optional)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'security_user_sessions'
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['session_key']),
            models.Index(fields=['expires_at']),
        ]
    
    def is_expired(self):
        """Check if session is expired"""
        return timezone.now() > self.expires_at
    
    def extend_session(self, minutes=60):
        """Extend session expiry"""
        self.expires_at = timezone.now() + timedelta(minutes=minutes)
        self.save(update_fields=['expires_at', 'last_activity'])


class LoginAttempt(models.Model):
    """Track login attempts for security analysis"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    success = models.BooleanField()
    failure_reason = models.CharField(max_length=100, blank=True)
    application_name = models.CharField(max_length=50)
    
    # Geolocation
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'security_login_attempts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ip_address', 'created_at']),
            models.Index(fields=['username', 'created_at']),
            models.Index(fields=['success', 'created_at']),
        ]


class SecurityAuditLog(models.Model):
    """Comprehensive audit logging"""
    AUDIT_ACTIONS = [
        ('USER_CREATED', 'User Created'),
        ('USER_UPDATED', 'User Updated'),
        ('USER_DELETED', 'User Deleted'),
        ('PASSWORD_CHANGED', 'Password Changed'),
        ('PRIVILEGE_GRANTED', 'Privilege Granted'),
        ('PRIVILEGE_REVOKED', 'Privilege Revoked'),
        ('ACCOUNT_LOCKED', 'Account Locked'),
        ('ACCOUNT_UNLOCKED', 'Account Unlocked'),
        ('SESSION_CREATED', 'Session Created'),
        ('SESSION_TERMINATED', 'Session Terminated'),
        ('CONFIG_CHANGED', 'Configuration Changed'),
        ('POLICY_UPDATED', 'Policy Updated'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action = models.CharField(max_length=50, choices=AUDIT_ACTIONS)
    user = models.ForeignKey(SecurityUser, on_delete=models.SET_NULL, null=True, blank=True)
    performed_by = models.ForeignKey(SecurityUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_actions')
    target_user = models.ForeignKey(SecurityUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_targets')
    
    # Details
    description = models.TextField()
    old_values = models.JSONField(default=dict, blank=True)
    new_values = models.JSONField(default=dict, blank=True)
    
    # Context
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    application_name = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'security_audit_log'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['action', 'created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['performed_by', 'created_at']),
        ]