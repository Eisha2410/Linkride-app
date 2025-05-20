from django import forms
from accounts.models import User

class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')

        if role == 'driver':
            required_fields = ['cnic', 'phone_number', 'education']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required for drivers.')
