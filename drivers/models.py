from django.db import models
from django.conf import settings
from accounts.models import User

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cnic = models.CharField(max_length=15, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    vehicle_number = models.CharField(max_length=50, default='UNKNOWN123')
    license_number = models.CharField(max_length=50)
    experience_years = models.IntegerField(null=True, blank=True)
    vehicle = models.OneToOneField('Vehicle', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.full_name} - Driver Profile"

class Vehicle(models.Model):
    driver = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'driver'},
        related_name='vehicle'
    )
    
    registration_number = models.CharField(max_length=50)
    license_number = models.CharField(max_length=50)
    number_plate = models.CharField(max_length=15)
    model_year = models.IntegerField()
    vehicle_model = models.CharField(max_length=100)
    vehicle_color = models.CharField(max_length=50,  default="Black")

    def __str__(self):
        return f"{self.vehicle_model} - {self.number_plate}"
    
    def is_valid_model(self):
       
        import datetime
        current_year = datetime.datetime.now().year
        return self.model_year >= current_year - 10  # Example: only vehicles newer than 10 years
