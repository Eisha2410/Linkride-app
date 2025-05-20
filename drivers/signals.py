from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User 
from drivers.models import DriverProfile, Vehicle

@receiver(post_save, sender=User)
def create_driver_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'driver':
        vehicle = Vehicle.objects.create(
            driver=instance,
            number_plate="TEMP-000",       
            vehicle_model="TEMP_MODEL",
            vehicle_color="BLACK",
            model_year=2020,
            license_number= "0000"
        )
        DriverProfile.objects.create(
            user=instance,
            license_number="LICENSE-TEMP",  
            experience_years=0,  
            vehicle=vehicle
        )

@receiver(post_save, sender=User)
def sync_driver_profile(sender, instance, **kwargs):
    if instance.role == 'driver':
        profile = DriverProfile.objects.filter(user=instance).first()
        if profile:
            profile.cnic = instance.cnic
            profile.phone_number = instance.phone_number
            profile.full_name = instance.full_name
            profile.education = instance.education
            profile.save()