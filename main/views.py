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
from dateutil.relativedelta import relativedelta
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@login_required
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

    # Filter events based on the logged-in user
    events = Event.objects.filter(date__year=year, date__month=month, creator=request.user)

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
        recurrence = request.POST.get('recurrence')

        creator = request.user

        if not all([event_title, event_date, start_time, end_time]):
            return JsonResponse({'success': False, 'error': 'Incomplete event data'}, status=400)

        event = Event.objects.create(title=event_title, date=event_date, start_time=start_time,
                                     end_time=end_time, location=event_location, description=event_description,
                                     creator=creator, recurrence=recurrence)
        if recurrence:
            if recurrence == 'daily':
                delta = relativedelta(days=1)
            elif recurrence == 'weekly':
                delta = relativedelta(weeks=1)
            elif recurrence == 'monthly':
                delta = relativedelta(months=1)
            elif recurrence == 'yearly':
                delta = relativedelta(years=1)
            else:
                delta = None

            if delta:
                event_date = datetime.strptime(event_date, '%Y-%m-%d').date()
                end_date = datetime.today().date() + relativedelta(years=1)
                while event_date < end_date:
                    new_event = Event.objects.create(title=event_title, date=event_date, start_time=start_time,
                                                     end_time=end_time, location=event_location,
                                                     description=event_description,
                                                     creator=creator, recurrence=recurrence)

                    for email in invited_emails:
                        try:
                            invited_user = User.objects.get(email=email)
                            new_event.invited_users.add(invited_user)

                            send_mail(
                                'You have been invited to an event',
                                f'You have been invited to the event "{event.title}" scheduled on {event_date} {start_time} - {end_time} by {creator}.',
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

                    event_date += delta

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


from django.http import JsonResponse

@login_required
@require_POST
def delete_event(request, event_title):
    try:
        event = Event.objects.get(title=event_title)
        # Check if the requesting user is the creator of the event
        if event.creator == request.user:
            event.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'You are not authorized to delete this event.'}, status=403)
    except Event.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Event does not exist.'}, status=404)
