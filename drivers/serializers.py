from rest_framework import serializers
from .models import DriverProfile, Vehicle
from accounts.models import User

class DriverProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  

    class Meta:
        model = DriverProfile
        fields = ['user'] 

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