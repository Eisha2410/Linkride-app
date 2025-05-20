from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from passengers.models import PassengerProfile

@receiver(post_save, sender=User)
def create_passenger_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'passenger':
        if not hasattr(instance, 'passengerprofile'):
            PassengerProfile.objects.create(user=instance, emergency_contact="0000000000")

@receiver(post_save, sender=User)
def sync_passenger_profile(sender, instance, **kwargs):
    if instance.role == 'passenger':
        profile = PassengerProfile.objects.filter(user=instance).first()
        if profile:
            profile.cnic = instance.cnic
            profile.phone_number = instance.phone_number
            profile.full_name = instance.full_name
            profile.education = instance.education
            profile.save()