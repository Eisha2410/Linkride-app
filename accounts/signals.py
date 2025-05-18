from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from drivers.models import Vehicle  
from passengers.models import PassengerProfile

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'passenger':
            PassengerProfile.objects.create(user=instance)
