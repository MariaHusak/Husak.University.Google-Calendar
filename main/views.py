from django.shortcuts import render
import calendar
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse
from .models import Event
import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.core.exceptions import ValidationError
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def index(request):
    return render(request, 'main/index.html')

def privacy(request):
    return render(request, 'main/privacy.html')

def login(request):
    return render(request, 'account/login.html')


@login_required
def display_calendar(request, year=None, month=None):
    today = datetime.today()
    if year is None:
        year = today.year
    if month is None:
        month = today.month

    cal = calendar.Calendar()
    cal_data = cal.monthdayscalendar(year, month)

    month_name = calendar.month_name[month]
    year_name = str(year)

    next_month = (today.replace(year=year, month=month) + timedelta(days=31)).strftime('%Y/%m')
    prev_month = (today.replace(year=year, month=month) - timedelta(days=1)).strftime('%Y/%m')

    if month == 1:
        prev_month = f"{year - 1}/12"
    else:
        prev_month = f"{year}/{month - 1:02d}"

    events = Event.objects.filter(date__year=year, date__month=month)
    event_data = []
    for event in events:
        event_info = {
            'title': event.title,
            'date': event.date,
            'start_time': event.start_time,
            'end_time': event.end_time,
            'location': event.location,
            'description': event.description,
            'creator_nickname': event.creator.username,
            'invited_users_nicknames': [user.username for user in event.invited_users.all()]
        }
        event_data.append(event_info)

    return render(request, 'main/calendar.html', {'calendar': cal_data, 'month_name': month_name,
                                                  'year_name': year_name, 'next_month': next_month,
                                                  'prev_month': prev_month, 'events': event_data})


@login_required
def create_event(request):
    if request.method == 'POST':
        event_title = request.POST.get('event_title')
        event_date = request.POST.get('event_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        event_location = request.POST.get('event_location')
        event_description = request.POST.get('event_description')
        invited_emails = request.POST.getlist('invited_emails')

        creator = request.user

        event = Event.objects.create(title=event_title, date=event_date, start_time=start_time,
                                     end_time=end_time, location=event_location, description=event_description,
                                     creator=creator)

        for email in invited_emails:
            try:
                invited_user = User.objects.get(email=email)
                event.invited_users.add(invited_user)

                send_mail(
                    'You have been invited to an event',
                    f'You have been invited to the event "{event.title}" scheduled on {event.date} {event.start_time} - {event.end_time} by {event.creator}.',
                    'husakmaria74@gmail.com',
                    [email],
                    fail_silently=False,
                )
                logger.info(f'Invitation email sent to {email} for event "{event.title}"')
            except User.DoesNotExist:
                logger.warning(f'User with email {email} does not exist. Invitation email not sent.')
            except BadHeaderError:
                logger.error(f'Invalid header found while sending email to {email}.')
            except ValidationError as e:
                logger.error(f'Validation error occurred while sending email to {email}: {str(e)}')

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

@login_required
def delete_event(request, event_id):
    if request.method == 'POST':
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            logger.info(f"Event with ID {event_id} deleted successfully.")
            return JsonResponse({'success': True})
        except Event.DoesNotExist:
            logger.warning(f"Attempted to delete non-existing event with ID {event_id}.")
            return JsonResponse({'success': False, 'error': 'Event does not exist'}, status=404)
    else:
        logger.error("DELETE request received with incorrect method.")
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

