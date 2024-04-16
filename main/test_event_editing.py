import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycalendar.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Event


# Unit Tests for Event Editing
class EditEventTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

        self.event = Event.objects.create(
            title='Test Event',
            date='2024-04-13',
            start_time='12:00',
            end_time='13:00',
            location='Test Location',
            description='Test Description',
            creator=self.user
        )

        self.client = Client()

    def test_edit_event(self):
        self.client.login(username='testuser', password='password')

        updated_data = {
            'title': 'Updated Event',
            'date': '2024-04-14',
            'start_time': '14:00',
            'end_time': '15:00',
            'location': 'Updated Location',
            'description': 'Updated Description',
        }
        response = self.client.post(reverse('edit_event', args=[self.event.pk]), updated_data)

        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, 'Updated Event')
        self.assertEqual(str(self.event.date), '2024-04-14')
        self.assertEqual(str(self.event.start_time), '14:00:00')
        self.assertEqual(str(self.event.end_time), '15:00:00')
        self.assertEqual(self.event.location, 'Updated Location')
        self.assertEqual(self.event.description, 'Updated Description')

    def test_edit_event_not_logged_in(self):
        response = self.client.get(reverse('edit_event', args=[self.event.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

        response = self.client.post(reverse('edit_event', args=[self.event.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
