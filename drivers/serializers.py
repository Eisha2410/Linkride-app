from rest_framework import serializers
from .models import DriverProfile, Vehicle
from accounts.models import User
from drivers.models import DriverProfile

class DriverProfileSerializer(serializers.ModelSerializer):  
    cnic = serializers.CharField(source='user.cnic', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    education = serializers.CharField(source='user.education', read_only=True)

    class Meta:
        model = DriverProfile
        fields = ['user', 'vehicle_number', 'license_number', 'experience_years', 'cnic', 'phone_number', 'full_name', 'education']

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

    def validate_model_year(self, value):
        import datetime
        current_year = datetime.datetime.now().year
        if value < current_year - 10:
            raise serializers.ValidationError("Vehicle model is too old.")
        return value

    def create(self, validated_data):
        request = self.context['request']
        validated_data['driver'] = request.user
        return super().create(validated_data)