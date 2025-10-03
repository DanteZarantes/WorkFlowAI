"""
Management command to fix board data isolation issues
"""
import os
import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from utils.board_storage import BoardStorage
from utils.secure_json_storage import SecureJSONStorage

User = get_user_model()

class Command(BaseCommand):
    help = 'Fix board data isolation issues and ensure proper user ownership'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be fixed without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        board_storage = BoardStorage()
        secure_storage = SecureJSONStorage()
        
        # Get all users
        users = User.objects.all()
        
        for user in users:
            self.stdout.write(f'Checking user: {user.username} (ID: {user.id})')
            
            # Check boards
            boards = board_storage.get_user_boards(user.id)
            invalid_boards = [b for b in boards if b.get('owner_id') != user.id]
            
            if invalid_boards:
                self.stdout.write(
                    self.style.ERROR(
                        f'Found {len(invalid_boards)} boards with incorrect ownership for user {user.username}'
                    )
                )
                
                if not dry_run:
                    # Fix board ownership
                    file_path = board_storage._get_file_path('boards', user.id)
                    data = board_storage._read_secure_file(file_path)
                    
                    if 'boards' in data:
                        # Remove boards that don't belong to this user
                        data['boards'] = [b for b in data['boards'] if b.get('owner_id') == user.id]
                        board_storage._write_secure_file(file_path, data)
                        self.stdout.write(self.style.SUCCESS(f'Fixed board ownership for user {user.username}'))
            
            # Check tasks
            tasks_file = board_storage._get_file_path('board_tasks', user.id)
            tasks_data = board_storage._read_secure_file(tasks_file)
            
            fixed_tasks = False
            for board_id, board_data in tasks_data.items():
                if isinstance(board_data, dict) and 'tasks' in board_data:
                    invalid_tasks = [t for t in board_data['tasks'] if t.get('owner_id') != user.id]
                    
                    if invalid_tasks:
                        self.stdout.write(
                            self.style.ERROR(
                                f'Found {len(invalid_tasks)} tasks with incorrect ownership in board {board_id} for user {user.username}'
                            )
                        )
                        
                        if not dry_run:
                            # Remove tasks that don't belong to this user
                            board_data['tasks'] = [t for t in board_data['tasks'] if t.get('owner_id') == user.id]
                            fixed_tasks = True
            
            if fixed_tasks and not dry_run:
                board_storage._write_secure_file(tasks_file, tasks_data)
                self.stdout.write(self.style.SUCCESS(f'Fixed task ownership for user {user.username}'))
            
            # Check projects
            projects_file = board_storage._get_file_path('board_projects', user.id)
            projects_data = board_storage._read_secure_file(projects_file)
            
            fixed_projects = False
            for board_id, board_data in projects_data.items():
                if isinstance(board_data, dict) and 'projects' in board_data:
                    invalid_projects = [p for p in board_data['projects'] if p.get('owner_id') != user.id]
                    
                    if invalid_projects:
                        self.stdout.write(
                            self.style.ERROR(
                                f'Found {len(invalid_projects)} projects with incorrect ownership in board {board_id} for user {user.username}'
                            )
                        )
                        
                        if not dry_run:
                            # Remove projects that don't belong to this user
                            board_data['projects'] = [p for p in board_data['projects'] if p.get('owner_id') == user.id]
                            fixed_projects = True
            
            if fixed_projects and not dry_run:
                board_storage._write_secure_file(projects_file, projects_data)
                self.stdout.write(self.style.SUCCESS(f'Fixed project ownership for user {user.username}'))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN COMPLETE - Run without --dry-run to apply fixes'))
        else:
            self.stdout.write(self.style.SUCCESS('Board isolation fix complete!'))