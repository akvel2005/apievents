# events/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from .models import ApplyFormModel  

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
from django import forms
from .models import Event, EventRegistration

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']
        
class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['attendee', 'event']


class ApplyForm(forms.ModelForm):
    class Meta:
        model = ApplyFormModel
        fields = ['field1', 'field2'] 

