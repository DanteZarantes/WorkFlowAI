"""
Django Settings Package

This package contains environment-specific Django settings:
- base.py: Shared settings for all environments
- development.py: Local development settings
- production.py: Production deployment settings

Usage:
Set DJANGO_SETTINGS_MODULE environment variable to:
- config.settings.development (for development)
- config.settings.production (for production)
"""