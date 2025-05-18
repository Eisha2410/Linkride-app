from django.contrib import admin
from .models import PassengerProfile

@admin.register(PassengerProfile)
class PassengerProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

