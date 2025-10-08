#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This is the main entry point for Django management commands.
Use this file to run Django commands like:
- python manage.py runserver (start development server)
- python manage.py makemigrations (create database migrations)
- python manage.py migrate (apply database migrations)
- python manage.py createsuperuser (create admin user)
- python manage.py collectstatic (collect static files)
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

def main():
    """
    Run administrative tasks.
    
    Sets up Django environment and executes command-line arguments.
    Uses development settings by default from config.settings.development
    """
    # Set default Django settings module
    # Points to config/settings/development.py for local development
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    
    try:
        # Import Django's command-line execution function
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Provide helpful error message if Django is not installed
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the command-line arguments
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()