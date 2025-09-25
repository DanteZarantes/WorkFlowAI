"""
Django management command to setup JSON data storage system
Usage: python manage.py setup_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from utils.data_initializer import data_initializer

User = get_user_model()

class Command(BaseCommand):
    help = 'Initialize JSON data storage system for NeuralFlow'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--sync-users',
            action='store_true',
            help='Sync existing users to JSON storage'
        )
        parser.add_argument(
            '--validate',
            action='store_true',
            help='Validate data integrity'
        )
        parser.add_argument(
            '--backup',
            action='store_true',
            help='Create backup of existing data'
        )
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Show storage statistics'
        )
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Setting up NeuralFlow JSON Data Storage System')
        )
        
        # Initialize data structure
        self.stdout.write('Initializing data structure...')
        data_initializer.initialize_data_structure()
        
        # Sync existing users if requested
        if options['sync_users']:
            self.stdout.write('Syncing existing users...')
            synced_count = data_initializer.sync_existing_users()
            self.stdout.write(
                self.style.SUCCESS(f'Synced {synced_count} users')
            )
        
        # Validate data integrity if requested
        if options['validate']:
            self.stdout.write('Validating data integrity...')
            issues = data_initializer.validate_data_integrity()
            if not issues:
                self.stdout.write(
                    self.style.SUCCESS('Data integrity validation passed')
                )
        
        # Create backup if requested
        if options['backup']:
            self.stdout.write('Creating backup...')
            backup_path = data_initializer.create_backup()
            if backup_path:
                self.stdout.write(
                    self.style.SUCCESS(f'Backup created: {backup_path}')
                )
        
        # Show statistics if requested
        if options['stats']:
            self.stdout.write('Storage statistics:')
            stats = data_initializer.get_storage_stats()
            for key, value in stats.items():
                self.stdout.write(f'  {key}: {value}')
        
        self.stdout.write(
            self.style.SUCCESS('\nJSON Data Storage System setup complete!')
        )
        self.stdout.write(
            'Next steps:'
        )
        self.stdout.write(
            '1. Run: python manage.py setup_data --sync-users (to sync existing users)'
        )
        self.stdout.write(
            '2. Run: python manage.py setup_data --validate (to validate data)'
        )
        self.stdout.write(
            '3. Test registration and login functionality'
        )