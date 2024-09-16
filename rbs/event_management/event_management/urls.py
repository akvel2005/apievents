# event_management/urls.py
from django.contrib import admin
from django.urls import path, include
# event_management/urls.py
from django.contrib import admin
from django.urls import path
from events import views

urlpatterns = [
   
    path('', include('events.urls')),  # Include the events app URLs
    

]


# event_management/urls.py
from django.contrib import admin
from django.urls import path
from events import views


    