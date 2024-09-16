# events/admin.py
from django.contrib import admin
from .models import UserProfile, Event, EventRegistration

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(EventRegistration)
