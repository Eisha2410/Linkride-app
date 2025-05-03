from django.shortcuts import render, redirect
from .models import Ride
from .forms import RideForm
from rest_framework import viewsets, generics, permissions, status
from .serializers import RideSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

# FRONTEND: Used only for Django template testing
# NOT used in React frontend
def ride_list(request):
    rides = Ride.objects.all().order_by('-date', '-time')
    return render(request, 'carpool/ride_list.html', {'rides': rides})

# FRONTEND: Used only for Django template testing
# NOT used in React frontend
def create_ride(request):
    if request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.driver = request.user
            ride.save()
            return redirect('ride_list')
    else:
        form = RideForm()
    return render(request, 'carpool/create_ride.html', {'form': form})

# FRONTEND: 
# - "Available Rides" page (GET)
# - "Create Ride" form/button (POST)
# React will call this for listing and creating rides
class RideListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(driver=self.request.user)

# FRONTEND:
# - View/Edit/Delete specific ride
# Used when user opens ride detail page, updates or deletes it
class RideRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if self.get_object().driver != self.request.user:
            raise PermissionDenied("You are not allowed to update this ride.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.driver != self.request.user:
            raise PermissionDenied("You are not allowed to delete this ride.")
        instance.delete()

# FRONTEND:
# - Can be used for future filtering rides by driver
# You can expose this ViewSet for admin or profile pages
class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    queryset = Ride.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(driver=self.request.user)

    def get_queryset(self):
        return Ride.objects.filter(driver=self.request.user)

# FRONTEND:
# - "Register" screen/form
# Sends user registration data and receives auth token
class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.id,
                "username": user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# FRONTEND:
# - "Join Ride" button
# Called when a user joins a ride from ride detail or list
class JoinRideView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id):
        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if user == ride.driver:
            return Response({"error": "Driver cannot join their own ride."}, status=status.HTTP_400_BAD_REQUEST)

        if user in ride.passengers.all():
            return Response({"error": "User already joined this ride."}, status=status.HTTP_400_BAD_REQUEST)

        if ride.seats_available <= 0:
            return Response({"error": "No seats available."}, status=status.HTTP_400_BAD_REQUEST)

        ride.passengers.add(user)
        ride.seats_available -= 1
        ride.save()
        return Response({"message": "Successfully joined the ride."}, status=status.HTTP_200_OK)

# FRONTEND:
# - "Check-In" button
# Called when ride starts, to mark user as checked in
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ride_check_in(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return Response({'error': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)

    if ride.is_checked_in:
        return Response({'error': 'Already checked in'}, status=status.HTTP_400_BAD_REQUEST)

    ride.is_checked_in = True
    ride.check_in_time = timezone.now()
    ride.save()
    return Response({'success': 'Checked in successfully'}, status=status.HTTP_200_OK)

# FRONTEND:
# - "Check-Out" button
# Called when ride ends, to mark user as checked out
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ride_check_out(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return Response({'error': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)

    if not ride.is_checked_in:
        return Response({'error': 'Check-in required before check-out'}, status=status.HTTP_400_BAD_REQUEST)

    if ride.is_checked_out:
        return Response({'error': 'Already checked out'}, status=status.HTTP_400_BAD_REQUEST)

    ride.is_checked_out = True
    ride.check_out_time = timezone.now()
    ride.save()
    return Response({'success': 'Checked out successfully'}, status=status.HTTP_200_OK)
