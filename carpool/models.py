from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from drivers.models import Vehicle

User = get_user_model()

# FRONTEND:
# Main model representing a carpool ride
# Used in:
# - Ride creation form
# - Ride detail/list pages
# - Join, Check-in, Check-out buttons
class Ride(models.Model):
    # User who created the ride
    driver = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'driver'})

    # Locations for the ride
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    # Scheduled date and time
    date = models.DateField()
    time = models.TimeField()

    # How many seats are left
    seats_available = models.PositiveIntegerField()

    # Fare will be auto-calculated based on distance
    fare = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    # Timestamp of when the ride was created
    created_at = models.DateTimeField(auto_now_add=True)
    
    vehicle = models.ForeignKey('drivers.Vehicle', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Users who have joined this ride
    # Used when a user presses the "Join" button
    passengers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_rides', blank=True)

    # Check-in and check-out status and times
    # Used with "Check-In" and "Check-Out" buttons
    is_checked_in = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(null=True, blank=True)
    is_checked_out = models.BooleanField(default=False)
    check_out_time = models.DateTimeField(null=True, blank=True)

    # Estimated ride distance (in kilometers)
    # Used in fare calculation
    distance_km = models.FloatField(default=0)

    def __str__(self):
        return f"{self.origin} to {self.destination} by {self.driver}"

# FRONTEND:
# Optional model for tracking per-user check-in/out (not actively used)
# You can use this if you want to show logs/history in frontend later
class RideCheckIn(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='checkins')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('ride', 'user') # A user can only check in once per ride 

    def __str__(self):
        return f"{self.user.username} - {self.ride} Check-in"