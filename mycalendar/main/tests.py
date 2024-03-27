import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycalendar.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationTest(TestCase):
    def setUp(self):
        # Create a test user
        self.username = 'mariia'
        self.email = 'husakmaria74@gmail.com'
        self.password = '12345678'
        self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_login(self):
        # Test login with correct credentials
        response = self.client.post(reverse('login'), {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)

    def test_invalid_login(self):
        # Test login with incorrect credentials
        response = self.client.post(reverse('login'), {'username': self.username, 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        # Log in the user first
        self.client.login(username=self.username, password=self.password)

        # Test logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_access(self):
        # Log in the user first
        self.client.login(username=self.username, password=self.password)

        # Test accessing a protected page
        response = self.client.get(reverse('protected_page'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_access(self):
        # Test accessing a protected page without logging in
        response = self.client.get(reverse('protected_page'))
        self.assertEqual(response.status_code, 302)



