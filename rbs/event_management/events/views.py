# events/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, LoginForm
from .models import ApplyFormModel, UserProfile, Event , Application
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            profile = UserProfile(user=user, role=form.cleaned_data['role'])
            profile.save()

            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'events/register.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer

# Regular Django view
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)

                try:
                    profile = UserProfile.objects.get(user=user)
                except UserProfile.DoesNotExist:
                    return render(request, 'events/login.html', {'form': form, 'error': 'Profile not found'})

                # Redirect based on user's role
                if profile.role == 'admin':
                    return redirect('admin_dashboard')
                elif profile.role == 'user':
                    return redirect('dashboard')
                elif profile.role == 'attendee':
                    return redirect('attendee_dashboard')

            return render(request, 'events/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'events/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, EventRegistration, UserProfile

def dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    events = Event.objects.all()

    return render(request, 'events/dashboard.html', {
        'events': events,
        'profile': profile
    })

def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    profile = UserProfile.objects.get(user=request.user)

    if profile.role == 'attendee':
        # Check if the user has already registered
        if not EventRegistration.objects.filter(event=event, attendee=profile).exists():
            EventRegistration.objects.create(event=event, attendee=profile)
            return render(request, 'events/register_event.html', {'event': event})
        else:
            return render(request, 'events/register_event.html', {'event': event, 'already_registered': True})

    return redirect('dashboard')
@login_required
def admin_dashboard(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if the user is not authenticated

    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('login')  # Redirect to login if the user profile does not exist

    # Check if the user has an admin role
    if profile.role != 'admin':
        return redirect('attendee_dashboard')  # Redirect non-admin users to the regular dashboard

    # Fetch all events and registrations for the admin dashboard
    events = Event.objects.all()
    event_registrations = EventRegistration.objects.all()

    return render(request, 'events/admin_dashboard.html', {
        'events': events,
        'event_registrations': event_registrations,
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, EventRegistration
from .forms import EventForm, EventRegistrationForm

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            # Assign the logged-in admin as the organizer
            event.organizer = request.user.userprofile  # Assuming a UserProfile FK
            event.save()
            return redirect('admin_dashboard')  # Redirect after event creation
    else:
        form = EventForm()
    
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def update_event(request, event_id):
    if not request.user.userprofile.role == 'admin':
        return redirect('dashboard')
    
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/update_event.html', {'form': form, 'event': event})

@login_required
def delete_event(request, event_id):
    if not request.user.userprofile.role == 'admin':
        return redirect('dashboard')
    
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        event.delete()
        return redirect('admin_dashboard')
    
    return render(request, 'events/delete_event.html', {'event': event})

@login_required
def view_event_registrations(request, event_id):
    if not request.user.userprofile.role == 'admin':
        return redirect('dashboard')
    
    registrations = EventRegistration.objects.filter(event__id=event_id)
    
    return render(request, 'events/view_event_registrations.html', {'registrations': registrations})

from django.shortcuts import render, get_object_or_404
from .models import Event, EventRegistration

def view_event_registrations(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registrations = EventRegistration.objects.filter(event=event)
    return render(request, 'events/view_event_registrations.html', {
        'event': event,
        'registrations': registrations
    })

from django.shortcuts import render, get_object_or_404, redirect
from .models import Event

def apply_for_event(request, event_id):
    from .forms import ApplyForm  # Import inside the function to avoid circular import
    
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = ApplyForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.event = event
            application.user = request.user
            application.save()
            return redirect('success_page')  # Redirect to a success page after submission
    else:
        form = ApplyForm()

    return render(request, 'events/apply.html', {'form': form, 'event': event})




def success_page(request):
    return render(request, 'success.html')

from django.shortcuts import render
from .models import Event

def attendee_dashboard(request):
    events = Event.objects.all()  # Retrieve all events posted by the admin
    return render(request, 'events/attendee_dashboard.html', {'events': events})

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from .models import UserProfile
from .serializers import LoginSerializer


@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        print(username,password)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            # Determine redirect URL based on user role
            try:
                profile = UserProfile.objects.get(user=user)
               
                if profile.role == 'admin':
                    redirect_url = 'http://127.0.0.1:8000/admin-dashboard/'
                elif profile.role == 'organizer':
                    redirect_url = 'http://127.0.0.1:8000/organizer/dashboard/'
                else:
                    redirect_url = 'http://127.0.0.1:8000/home/'
            except UserProfile.DoesNotExist:
                redirect_url = 'http://127.0.0.1:8000/home/'  # Default redirect if profile not found
            return Response({'message': 'Login successful', 'redirect_url': redirect_url}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# myapp/views.py
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    return Response({'error': 'Account is inactive'}, status=status.HTTP_403_FORBIDDEN)
                
                login(request, user)

                # Redirect based on user role
                try:
                    profile = user.profile  # assuming a one-to-one profile relationship
                    if profile.role == 'organizer':
                        return Response({
                            'message': 'Login successful',
                            'redirect_url': '/organizer-dashboard/'
                        }, status=status.HTTP_200_OK)
                    elif profile.role == 'admin':
                        return Response({
                            'message': 'Login successful',
                            'redirect_url': '/admin-dashboard/'
                        }, status=status.HTTP_200_OK)
                    elif profile.role == 'attendee':
                        return Response({
                            'message': 'Login successful',
                            'redirect_url': '/attendee-dashboard/'
                        }, status=status.HTTP_200_OK)
                except AttributeError:
                    return Response({'error': 'User profile not found'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
