"""import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycalendar.settings')
django.setup()

from django.core.management import call_command
from django.core.management.base import CommandError
from django.core.mail import outbox
from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Event
from datetime import datetime, timedelta
from unittest.mock import patch

import logging
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ReminderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

    @patch('django.core.mail.send_mail')
    def test_send_reminder(self, mock_send_mail):
        event_date = datetime.now() + timedelta(days=1)
        event = Event.objects.create(title='Test Event', date=event_date.date(), start_time='10:00', end_time='11:00', creator=self.user)

        logger.info(f'Creator: {self.user}')
        call_command('create_reminders')

        logger.info(f'Outbox length: {len(outbox)}')
        logger.info(f'Outbox content: {outbox}')

        self.assertEqual(len(outbox), 1)
        self.assertEqual(outbox[0].subject, 'Upcoming Event Reminder')
        self.assertEqual(outbox[0].to, [self.user.email])

    @patch('django.core.mail.send_mail')
    def test_no_upcoming_events(self, mock_send_mail):
        with self.assertRaises(CommandError):
            call_command('create_reminders')"""

