from rest_framework import serializers
from .models import PassengerProfile
from accounts.models import User

class PassengerProfileSerializer(serializers.ModelSerializer):
    cnic = serializers.CharField(source='user.cnic', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    education = serializers.CharField(source='user.education', read_only=True)

    class Meta:
        model = PassengerProfile
        fields = fields = ['user', 'emergency_contact', 'cnic', 'phone_number', 'full_name', 'education']
