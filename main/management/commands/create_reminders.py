from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime
from main.models import Event

class Command(BaseCommand):
    help = 'Send reminders for upcoming events'

    def handle(self, *args, **kwargs):
        today = timezone.now()
        today = datetime.combine(today.date(), datetime.min.time())

        upcoming_events = Event.objects.filter(date__gte=today.date())

        for event in upcoming_events:
            event_datetime = datetime.combine(event.date, datetime.min.time())

            time_until_event = event_datetime - today

            if time_until_event.days == 0:
                creator_email = event.creator.email
                try:
                    send_mail(
                        'Upcoming Event Reminder',
                        f'Don\'t forget! You have an event "{event.title}" scheduled for {event.date} at {event.start_time}.',
                        'husakmaria74@email.com',
                        [creator_email],
                        fail_silently=False,
                    )
                    self.stdout.write(self.style.SUCCESS(f'Reminder sent for event "{event.title}"'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to send reminder for event "{event.title}": {e}'))
        if not upcoming_events:
            raise CommandError('No upcoming events found')

