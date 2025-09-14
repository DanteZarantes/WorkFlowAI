from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_signup(self):
        signup_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = self.client.post(reverse('signup'), data=signup_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        
        # Check if user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(reverse('login'), data=login_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_user_login_invalid_credentials(self):
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), data=login_data)
        self.assertEqual(response.status_code, 200)  # Stay on login page
        self.assertContains(response, 'Please enter a correct username and password')

    def test_user_logout(self):
        # First login
        self.client.login(username='testuser', password='testpass123')
        
        # Then logout
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout

    def test_profile_update(self):
        self.client.login(username='testuser', password='testpass123')
        
        profile_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'bio': 'Updated bio',
            'location': 'New City'
        }
        response = self.client.post(reverse('profile'), data=profile_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        # Check if profile was updated
        updated_user = User.objects.get(username='testuser')
        self.assertEqual(updated_user.first_name, 'John')
        self.assertEqual(updated_user.last_name, 'Doe')
        self.assertEqual(updated_user.bio, 'Updated bio')

    def test_protected_view_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('/accounts/login/', response.url)

    def test_authenticated_user_can_access_protected_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)