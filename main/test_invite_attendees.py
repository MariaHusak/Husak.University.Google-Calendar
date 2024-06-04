import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycalendar.settings')
django.setup()

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Event
from main.views import create_event
from unittest.mock import patch

class CreateEventTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password')

        self.invitee1 = User.objects.create_user(username='invitee1', email='invitee1@example.com', password='password')
        self.invitee2 = User.objects.create_user(username='invitee2', email='invitee2@example.com', password='password')

    @patch('main.views.send_mail')
    def test_create_event_with_invited_attendees(self, mock_send_mail):
        url = reverse('create_event')
        request = self.factory.post(url, {
            'event_title': 'Test Event',
            'event_date': '2024-04-25',
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'event_location': 'Test Location',
            'event_description': 'Test Description',
            'invited_emails': ['invitee1@example.com', 'invitee2@example.com'],
            'recurrence': '',
        })
        request.user = self.user

        response = create_event(request)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(title='Test Event').exists())
        self.assertEqual(mock_send_mail.call_count, 2)

    @patch('main.views.send_mail')
    def test_create_event_invalid_email(self, mock_send_mail):
        url = reverse('create_event')
        request = self.factory.post(url, {
            'event_title': 'Test Event',
            'event_date': '2024-04-25',
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'event_location': 'Test Location',
            'event_description': 'Test Description',
            'invited_emails': ['invalid_email@example'],
            'recurrence': '',
        })
        request.user = self.user

        response = create_event(request)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(title='Test Event').exists())
        self.assertEqual(mock_send_mail.call_count, 0)

