from rest_framework import serializers
from .models import PassengerProfile
from accounts.models import User

class PassengerProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = PassengerProfile
        fields = ['user', 'emergency_contact']
