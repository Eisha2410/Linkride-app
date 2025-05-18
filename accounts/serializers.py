from rest_framework import serializers
from .models import User
from drivers.models import DriverProfile
from passengers.models import PassengerProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['cnic', 'phone_number', 'full_name', 'role', 'education', 'password']
    

    def validate_cnic(self, value):
        if User.objects.filter(cnic=value).exists():
            raise serializers.ValidationError("A user with this CNIC already exists.")
        return value

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        return value
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        if user.role == 'driver':
            from drivers.models import DriverProfile
            DriverProfile.objects.get_or_create(user=user) 
        elif user.role == 'passenger':
            from passengers.models import PassengerProfile
            PassengerProfile.objects.get_or_create(user=user)

        return user
