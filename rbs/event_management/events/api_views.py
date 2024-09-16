from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .serializers import EventSerializer
from django.shortcuts import get_object_or_404
from .serializers import LoginSerializer


# Event List and Create API
class EventListCreateAPI(APIView):
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)  # Set the user as the event creator
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Event Detail (Retrieve, Update, Delete)
class EventDetailAPI(APIView):
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from .models import UserProfile

class UserRegistrationAPIView(APIView):
    def post(self, request):
        user_serializer = UserRegistrationSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            # Get role and assign profile
            role = request.data.get('role', 'attendee')
            UserProfile.objects.create(user=user, role=role)
            return Response({
                'message': 'User registered successfully',
                'user': user_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            print(username,password)
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return Response({
                    'message': 'Login successful',
                    'redirect_url': '/dashboard/'  # Example redirect URL
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import generics
from .models import Application
from .serializers import ApplicationSerializer

class ApplicationListAPI(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

# api_views.py
from rest_framework.generics import ListCreateAPIView
from .models import Event
from .serializers import EventSerializer

class EventListCreateAPI(ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# api_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .serializers import EventSerializer

class EventListAPI(APIView):
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

class RegisterEventAPI(APIView):
    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        user = request.user
        # Assuming you have a model for event registrations
        if not event.registrations.filter(user=user).exists():
            event.registrations.create(user=user)
            return Response({'message': 'Registered successfully'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Already registered'}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Event
from django.shortcuts import get_object_or_404

class EventDeleteAPI(APIView):
    def delete(self, request, event_id, format=None):
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
