from django.contrib import admin
from .models import DriverProfile, Vehicle

@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'experience_years')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('driver', 'vehicle_model', 'number_plate', 'license_number')
