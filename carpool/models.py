from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Ride(models.Model):
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driven_rides')
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    seats_available = models.PositiveIntegerField()
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    passengers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_rides', blank=True)
    is_checked_in = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(null=True, blank=True)
    is_checked_out = models.BooleanField(default=False)
    check_out_time = models.DateTimeField(null=True, blank=True)
    distance_km = models.FloatField(default=0)
    fare = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        
        if self.distance_km:
            self.fare = self.distance_km * settings.PER_KM_RATE
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.origin} to {self.destination} by {self.driver}"

class RideCheckIn(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='checkins')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('ride', 'user')  

    def __str__(self):
        return f"{self.user.username} - {self.ride} Check-in"