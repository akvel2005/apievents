# events/models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('organizer', 'Organizer'),
        ('attendee', 'Attendee'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username

from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=100)
    # Add any other fields you may have, but no 'name' field

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=100)
    organizer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='organized_events')
    pass

    def __str__(self):
        return self.title

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='registrations')

    def __str__(self):
        return f'{self.attendee.user.username} - {self.event.title}'

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.event.title}'

    class Meta:
        unique_together = ('user', 'event')  
        
class ApplyFormModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # Adjust the relation as needed
    field1 = models.CharField(max_length=100)
    field2 = models.TextField()

    def __str__(self):
        return self.user.username
