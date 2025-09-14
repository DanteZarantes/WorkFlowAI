from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from accounts.models import CustomUser

User = get_user_model()

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_str_method(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_user_profile_fields(self):
        self.user.bio = 'Test bio'
        self.user.location = 'Test City'
        self.user.website = 'https://example.com'
        self.user.phone = '+1234567890'
        self.user.save()

        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.bio, 'Test bio')
        self.assertEqual(updated_user.location, 'Test City')
        self.assertEqual(updated_user.website, 'https://example.com')
        self.assertEqual(updated_user.phone, '+1234567890')

    def test_user_optional_fields(self):
        # Test that optional fields can be empty
        user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        self.assertEqual(user.bio, '')
        self.assertEqual(user.location, '')
        self.assertEqual(user.website, '')
        self.assertEqual(user.phone, '')
        self.assertIsNone(user.birth_date)
        self.assertFalse(user.avatar)

    def test_email_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username='testuser3',
                email='',
                password='testpass123'
            )