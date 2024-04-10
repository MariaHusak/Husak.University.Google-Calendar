import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycalendar.settings')
django.setup()

from django.core import mail
from .views import create_event
from django.test import TestCase, RequestFactory, override_settings, Client
from django.core.management import call_command
from django.utils import timezone
from unittest.mock import patch
from .models import Event, User
from django.urls import reverse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User


class ReminderNotificationTests(TestCase):
    def test_handle_sends_reminder_for_upcoming_event(self):
        user = User.objects.create(username='test_user', email='test@example.com')

        today = timezone.now()
        event_date = today.date()
        event_time = today.time()

        creator = User.objects.create(username='creator_user', email='creator@example.com')

        event = Event.objects.create(
            title='Test Event',
            date=event_date,
            start_time=event_time,
            end_time=event_time,
            creator=creator
        )
        event.invited_users.add(user)

        with patch('main.models.Event.objects.filter') as mock_filter:
            mock_filter.return_value = [event]

            with patch('django.core.mail.send_mail') as mock_send_mail:
                call_command('create_reminders')

                mock_send_mail.assert_called_once_with(
                    'Upcoming Event Reminder',
                    f'Don\'t forget! You have an event "{event.title}" scheduled for {event.date} at {event.start_time}.',
                    'husakmaria74@email.com',
                    [creator.email],
                    fail_silently=False,
                )

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




class EventTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com', password='testpassword')
        self.event_data = {
            'title': 'Test Event',
            'date': '2024-04-10',
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'location': 'Test Location',
            'description': 'Test Description',
            'recurrence': 'monthly',
            'invited_emails': 'test1@example.com, test2@example.com'
        }

    def test_create_event(self):
        # one-time event
        response = self.client.post(reverse('create_event'), self.event_data)
        print("Response status code:", response.status_code)
        print("Event count:", Event.objects.count())
        self.assertEqual(response.status_code, 302)


    def test_monthly_event_recurrence(self):
        # monthly event
        event = Event.objects.create(
            title='Test Monthly Event',
            date=datetime.today().strftime('%Y-%m-%d'),
            start_time='10:00:00',
            end_time='11:00:00',
            location='Test Location',
            description='Test Description',
            recurrence='monthly',
            creator=self.user
        )

        next_month_date = datetime.strptime(event.date, '%Y-%m-%d') + relativedelta(months=1)
        self.client.post(reverse('create_event'), self.event_data)
        self.assertEqual(Event.objects.count(), 1)

        while next_month_date < datetime.today():
            self.assertTrue(Event.objects.filter(date=next_month_date.strftime('%Y-%m-%d')).exists())
            next_month_date += relativedelta(months=1)


class EventCreationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.invited_user = User.objects.create_user(username='inviteduser', email='inviteduser@example.com', password='password')
        self.client.login(username='testuser', password='password')

    @patch('main.views.send_mail')
    def test_create_event(self, mock_send_mail):
        data = {
            'event_title': 'Test Event',
            'event_date': '2024-04-10',
            'start_time': '12:00',
            'end_time': '13:00',
            'event_location': 'Test Location',
            'event_description': 'Test Description',
            'invited_emails': ['inviteduser@example.com'],
            'recurrence': 'daily'
        }

        response = self.client.post(reverse('create_event'), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

        self.assertTrue(Event.objects.filter(title='Test Event').exists())

        mock_send_mail.assert_called()
        self.assertTrue(mock_send_mail.call_count >= 1)

    def test_create_event_missing_data(self):
        incomplete_event_data = {
            'event_date': '2024-04-10',
            'start_time': '12:00',
            'end_time': '13:00',
            'event_location': 'Test Location',
            'event_description': 'Test Description',
            'invited_emails': ['inviteduser@example.com'],
            'recurrence': 'daily'
        }

        response = self.client.post(reverse('create_event'), data=incomplete_event_data)

        self.assertEqual(response.status_code, 400)

        event = Event.objects.filter(title='Test Event').first()
        self.assertIsNone(event)

    def test_create_event_invalid_date(self):
        invalid_date_event_data = {
            'event_date': 'invalid-date',
            'start_time': '12:00',
            'end_time': '13:00',
            'event_location': 'Test Location',
            'event_description': 'Test Description',
            'invited_emails': ['inviteduser@example.com'],
            'recurrence': 'daily'
        }
        response = self.client.post(reverse('create_event'), data=invalid_date_event_data)

        self.assertEqual(response.status_code, 400)

        event = Event.objects.filter(title='Test Event').first()
        self.assertIsNone(event)


