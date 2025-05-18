from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from passengers.models import PassengerProfile

@receiver(post_save, sender=User)
def create_passenger_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'passenger':
        if not hasattr(instance, 'passengerprofile'):
            PassengerProfile.objects.create(user=instance)