from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    event_type = models.CharField(max_length=10, choices=[('online', 'Online'), ('offline', 'Offline')],
                                  default='offline')
    location = models.CharField(max_length=100, blank=True, null=True, default='')
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    invited_users = models.ManyToManyField(User, related_name='invited_events')

    def __str__(self):
        return self.title

