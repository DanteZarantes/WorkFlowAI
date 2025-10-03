"""
Initialize default boards for users
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from utils.board_storage import BoardStorage

User = get_user_model()

class Command(BaseCommand):
    help = 'Initialize default boards for all users'
    
    def handle(self, *args, **options):
        board_storage = BoardStorage()
        
        for user in User.objects.all():
            # Check if user already has boards
            existing_boards = board_storage.get_user_boards(user.id)
            
            if not existing_boards:
                # Create default dashboard board
                default_board = {
                    'name': 'My Dashboard',
                    'description': 'Default dashboard for task and project management',
                    'type': 'dashboard'
                }
                
                board_id = board_storage.create_board(user.id, default_board)
                self.stdout.write(
                    self.style.SUCCESS(f'Created default board for user {user.username}: {board_id}')
                )
            else:
                self.stdout.write(f'User {user.username} already has {len(existing_boards)} boards')
        
        self.stdout.write(self.style.SUCCESS('Board initialization complete'))