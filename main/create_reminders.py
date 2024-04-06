from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from .models import Event
#D:\Нова папка\Husak.University.Google-Calendar\mycalendar\main
from datetime import datetime

class Command(BaseCommand):
    help = 'Send reminders for upcoming events'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        upcoming_events = Event.objects.filter(date__gte=today)

        for event in upcoming_events:
            event_datetime = datetime.combine(event.date, datetime.min.time())  # Convert event.date to datetime

            time_until_event = event_datetime - today

            if time_until_event.days == 0:
                try:
                    send_mail(
                        'Upcoming Event Reminder',
                        'Don\'t forget! You have an event "{event.title}" scheduled for {event.date} at {event.start_time}.',
                        'husakmaria74@email.com',
                        [user.email for user in event.invited_users.all()],
                        fail_silently=False,
                    )
                    self.stdout.write(self.style.SUCCESS('Reminder sent for event "{event.title}"'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR('Failed to send reminder for event "{event.title}": {e}'))

