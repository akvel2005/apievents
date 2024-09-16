from django.urls import path
from .api_views import EventListCreateAPI, EventDetailAPI, ApplicationListAPI,  UserRegistrationAPIView
from .views import login_view
from . import api_views
from .api_views import EventListCreateAPI, EventDetailAPI, ApplicationListAPI, UserRegistrationAPIView
# event_management/urls.py
from django.contrib import admin
from django.urls import path, include
# event_management/urls.py
from django.contrib import admin
from django.urls import path
from events import views
from .views import LoginAPIView

urlpatterns = [
 path('api/login/', LoginAPIView.as_view(), name='api_login'),  # New API-based login view

    path('api/register/', api_views.UserRegistrationAPIView.as_view(), name='register_api'),
    path('api/events/', api_views.EventListCreateAPI.as_view(), name='event_list_create_api'),
    path('api/events/<int:event_id>/', api_views.EventDetailAPI.as_view(), name='event_detail_api'),
    path('api/events/delete/<int:event_id>/', api_views.EventDeleteAPI.as_view(), name='event_delete_api'),
    path('', views.user_login, name='login'),
     path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('register_event/<int:event_id>/', views.register_event, name='register_event'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Custom admin page
    path('admin/create-event/', views.create_event, name='create_event'),
    path('admin/update-event/<int:event_id>/', views.update_event, name='update_event'),
    path('admin/delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('admin/view-registrations/<int:event_id>/', views.view_event_registrations, name='view_event_registrations'),
    path('register_event/<int:event_id>/', views.register_event, name='register_event'),
    path('dashboard/', views.attendee_dashboard, name='attendee_dashboard'),

]

