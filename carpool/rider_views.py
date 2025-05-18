from django.shortcuts import render, redirect, get_object_or_404
from .models import Ride
from .forms import RideForm
from rest_framework import viewsets, generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from .serializers import RideSerializer
from .utils import get_distance_km
from drivers.models import Vehicle
from rest_framework.decorators import action

def ride_list(request):
    rides = Ride.objects.all().order_by('-date', '-time')
    return render(request, 'carpool/ride_list.html', {'rides': rides})

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

class RideListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        origin = self.request.data.get('origin')
        destination = self.request.data.get('destination')
        distance_km = get_distance_km(origin, destination)
        fare = distance_km * settings.PER_KM_RATE
        serializer.save(driver=self.request.user, distance_km=distance_km, fare=fare)

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

class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    queryset = Ride.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        if user.role != 'driver':
            raise PermissionDenied("Only drivers can create rides.")

        try:
            vehicle = Vehicle.objects.get(driver=user)
        except Vehicle.DoesNotExist:
            raise ValidationError("You must have a registered vehicle to create a ride.")

        serializer.save(driver=user, vehicle=vehicle)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'driver':
            return Ride.objects.filter(driver=user)
        return Ride.objects.all()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def checkin(self, request, pk=None):
        ride = self.get_object()

        if ride.driver != request.user:
            return Response({'error': 'Only the driver can check in.'}, status=status.HTTP_403_FORBIDDEN)
        if ride.is_checked_in:
            return Response({'error': 'Already checked in.'}, status=status.HTTP_400_BAD_REQUEST)

        ride.is_checked_in = True
        ride.check_in_time = timezone.now()
        ride.save()
        return Response({'success': 'Checked in successfully', 'check_in_time': ride.check_in_time})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def checkout(self, request, pk=None):
        ride = self.get_object()

        if ride.driver != request.user:
            return Response({'error': 'Only the driver can check out.'}, status=status.HTTP_403_FORBIDDEN)
        if not ride.is_checked_in:
            return Response({'error': 'Check-in required before check-out.'}, status=status.HTTP_400_BAD_REQUEST)
        if ride.is_checked_out:
            return Response({'error': 'Already checked out.'}, status=status.HTTP_400_BAD_REQUEST)

        ride.is_checked_out = True
        ride.check_out_time = timezone.now()
        ride.save()
        return Response({'success': 'Checked out successfully', 'check_out_time': ride.check_out_time})
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
