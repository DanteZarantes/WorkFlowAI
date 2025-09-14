from django.test import TestCase
from accounts.forms import SignUpForm, ProfileForm
from accounts.models import CustomUser

class FormsTestCase(TestCase):
    def test_signup_form_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_password_mismatch(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'differentpass123'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_signup_form_missing_email(self):
        form_data = {
            'username': 'newuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_profile_form_valid(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'bio': 'Test bio',
            'location': 'Test City',
            'website': 'https://example.com',
            'phone': '+1234567890'
        }
        form = ProfileForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())

    def test_profile_form_invalid_website(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'website': 'invalid-url'
        }
        form = ProfileForm(data=form_data, instance=user)
        self.assertFalse(form.is_valid())
        self.assertIn('website', form.errors)