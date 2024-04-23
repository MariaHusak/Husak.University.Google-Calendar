from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('privacy', views.privacy, name='privacy'),
    path('login', views.login, name='login'),
    path('calendar', views.display_calendar, name='calendar'),
    path('calendar/<int:year>/<int:month>/', views.display_calendar, name='calendar_with_params'),
    path('create_event/', views.create_event, name='create_event'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('invitations/', views.invitations_page, name='invitations_page'),
    path('respond_invitation/<int:event_id>/', views.respond_invitation, name='respond_invitation'),


]


