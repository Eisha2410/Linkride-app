from django.contrib import admin
from .models import Ride, RideCheckIn
from django.contrib.auth import get_user_model


User = get_user_model()
admin.site.site_header = "Carpool Admin"
admin.site.site_title = "Carpool Admin Portal"
admin.site.index_title = "Welcome to Carpool Management"

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('driver', 'origin', 'destination', 'date', 'time', 'seats_available', 'fare')
    list_filter = ('date', 'origin', 'destination')
    search_fields = ('origin', 'destination', 'driver__username')
    ordering = ('-date',)


@admin.register(RideCheckIn)
class RideCheckInAdmin(admin.ModelAdmin):
    list_display = ['ride', 'user', 'check_in_time', 'check_out_time']