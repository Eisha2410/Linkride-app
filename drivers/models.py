from django.db import models
from django.conf import settings
from accounts.models import User

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={"role": "driver"})
    license_number = models.CharField(max_length=50)
    experience_years = models.PositiveIntegerField()

    def __str__(self):
        return self.user.full_name

class Vehicle(models.Model):
    driver = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'driver'},
        related_name='vehicle'
    )
    
    registration_number = models.CharField(max_length=50)
    license_number = models.CharField(max_length=50)
    number_plate = models.CharField(max_length=15)
    model_year = models.IntegerField()
    vehicle_model = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.vehicle_model} - {self.number_plate}"
    
    def is_valid_model(self):
       
        import datetime
        current_year = datetime.datetime.now().year
        return self.model_year >= current_year - 10  # Example: only vehicles newer than 10 years
