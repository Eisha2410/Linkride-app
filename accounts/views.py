from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from drivers.models import DriverProfile
from passengers.models import PassengerProfile
from drivers.serializers import DriverProfileSerializer
from passengers.serializers import PassengerProfileSerializer
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import SignUpForm  

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  
            return redirect('http://localhost:3000/') 
        else:
            print(form.errors) 
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')  

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == 'driver':
            try:
                profile = DriverProfile.objects.get(user=user)
                serializer = DriverProfileSerializer(profile)
            except DriverProfile.DoesNotExist:
                return Response({'error': 'Driver profile not found'}, status=status.HTTP_404_NOT_FOUND)

        elif user.role == 'passenger':
            try:
                profile = PassengerProfile.objects.get(user=user)
                serializer = PassengerProfileSerializer(profile)
            except PassengerProfile.DoesNotExist:
                return Response({'error': 'Passenger profile not found'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)