from rest_framework import serializers
from .models import Ride
from django.contrib.auth.models import User

# FRONTEND:
# Used for:
# - Displaying ride data in list/detail views
# - Sending form data to create/update rides
# Fields like 'driver', 'check-in/check-out' are read-only
class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields =  '__all__'
        read_only_fields = ['driver', 'vehicle']  
    
    
    def validate(self, data):
        request = self.context['request']
        user = request.user

        if user.role != 'driver':
            raise serializers.ValidationError("Only drivers can create rides.")
        if not user.driverprofile.vehicle_set.exists():
            raise serializers.ValidationError("Driver must have a registered vehicle.")
        
        return data

# FRONTEND:
# Used for:
# - User registration form (signup page)
# Password is write-only for security
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # Create user with hashed password using Django's built-in method
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user