from django import forms
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):
    cnic = forms.CharField(max_length=15, required=True)
    phone = forms.CharField(max_length=15, required=True)
    education = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('full_name','cnic', 'phone_number', 'education', 'role', 'password1', 'password2')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number already exists")
        return phone_number

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
