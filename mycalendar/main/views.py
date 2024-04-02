from django.shortcuts import render
import calendar
from datetime import datetime, timedelta
from django.http import JsonResponse
from .models import Event
import logging
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .forms import EventForm



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
            'creator_nickname': event.creator.username,  # Display creator's nickname
            'invited_users_nicknames': [user.username for user in event.invited_users.all()]  # Display invited users' nicknames
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
            except User.DoesNotExist:
                pass

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
