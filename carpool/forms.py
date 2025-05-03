from django import forms
from .models import Ride

# FRONTEND:
# This form is used in the Django template (create_ride.html)
# for creating a ride through the backend UI.

class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['origin', 'destination', 'date', 'time', 'seats_available', 'fare']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }