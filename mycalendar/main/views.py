from django.shortcuts import render
import calendar
from datetime import datetime, timedelta

def index(request):
    return render(request, 'main/index.html')

def privacy(request):
    return render(request, 'main/privacy.html')


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

    return render(request, 'main/calendar.html', {'calendar': cal_data, 'month_name': month_name, 'year_name': year_name, 'next_month': next_month, 'prev_month': prev_month})