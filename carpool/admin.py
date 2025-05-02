from django.contrib import admin
from .models import Ride, RideCheckIn
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

User = get_user_model()
admin.site.unregister(User)
admin.site.site_header = "Carpool Admin"
admin.site.site_title = "Carpool Admin Portal"
admin.site.index_title = "Welcome to Carpool Management"

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('driver', 'origin', 'destination', 'date', 'time', 'seats_available', 'fare')
    list_filter = ('date', 'origin', 'destination')
    search_fields = ('origin', 'destination', 'driver__username')
    ordering = ('-date',)

@admin.register(User)
class CustomUserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

@admin.register(RideCheckIn)
class RideCheckInAdmin(admin.ModelAdmin):
    list_display = ['ride', 'user', 'check_in_time', 'check_out_time']