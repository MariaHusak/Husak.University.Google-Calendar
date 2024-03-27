from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('privacy', views.privacy, name='privacy'),
    path('calendar', views.display_calendar, name='calendar'),
    path('calendar/<int:year>/<int:month>/', views.display_calendar, name='calendar_with_params'),
]