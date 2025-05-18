from django.db import models
from django.conf import settings
from accounts.models import User

class PassengerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cnic = models.CharField(max_length=15, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.user.full_name
