"""
Custom validators for the application
"""
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re


def validate_username(value):
    """Validate username format"""
    if len(value) < 3:
        raise ValidationError('Username must be at least 3 characters long.')
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValidationError('Username can only contain letters, numbers, and underscores.')


def validate_phone_number(value):
    """Validate phone number format"""
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_regex(value)


def validate_file_size(value):
    """Validate file size (max 5MB)"""
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("Maximum file size is 5MB")


def validate_image_extension(value):
    """Validate image file extensions"""
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    ext = value.name.lower().split('.')[-1]
    if f'.{ext}' not in allowed_extensions:
        raise ValidationError('Only image files are allowed (jpg, jpeg, png, gif, webp)')