import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycalendar.settings')
django.setup()

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from main.models import Event
from datetime import datetime
from main.views import display_calendar
from unittest.mock import patch

class CalendarViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password')

    @patch('main.views.get_object_or_404')
    def test_display_calendar(self, mock_get_object_or_404):
        event1 = Event.objects.create(title='Event 1', date=datetime.today().date(), start_time='10:00:00',
                                      end_time='12:00:00', category='work', creator=self.user)
        event2 = Event.objects.create(title='Event 2', date=datetime.today().date(), start_time='14:00:00',
                                      end_time='16:00:00', category='personal', creator=self.user)
        event3 = Event.objects.create(title='Event 3', date=datetime.today().date(), start_time='18:00:00',
                                      end_time='20:00:00', category='social', creator=self.user)

        request = self.factory.get(reverse('calendar'))
        request.user = self.user

        mock_get_object_or_404.side_effect = Event.DoesNotExist

        response = display_calendar(request)

        self.assertContains(response, event1.title)
        self.assertContains(response, event2.title)
        self.assertContains(response, event3.title)

        self.assertContains(response, 'background-color: #F0E68C;', count=1)
        self.assertContains(response, 'background-color: violet;', count=1)
        self.assertContains(response, 'background-color: #A31F34;', count=1)
