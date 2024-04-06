import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycalendar.settings')
django.setup()

from django.core import mail
from .models import Event
from .views import create_event
from django.test import TestCase, RequestFactory, override_settings
from django.contrib.auth.models import User




class InviteOtherTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_create_event_success(self):
        request = self.factory.post('/create_event/', {
            'event_title': 'Test Event',
            'event_date': '2024-04-05',
            'start_time': '10:00',
            'end_time': '12:00',
            'event_location': 'Test Location',
            'event_description': 'Test Description',
            'invited_emails': ['invitee1@example.com', 'invitee2@example.com']
        })
        request.user = self.user

        response = create_event(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 0)

    def test_create_event_invalid_email(self):

        request = self.factory.post('/create_event/', {
            'event_title': 'Test Event',
            'event_date': '2024-04-05',
            'start_time': '10:00',
            'end_time': '12:00',
            'event_location': 'Test Location',
            'event_description': 'Test Description',
            'invited_emails': ['invalid_email']
        })
        request.user = self.user

        response = create_event(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 0)

    def test_create_event_no_emails(self):
        request = self.factory.post('/create_event/', {
            'event_title': 'Test Event',
            'event_date': '2024-04-05',
            'start_time': '10:00',
            'end_time': '12:00',
            'event_location': 'Test Location',
            'event_description': 'Test Description',
            'invited_emails': []
        })
        request.user = self.user

        response = create_event(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 0)


