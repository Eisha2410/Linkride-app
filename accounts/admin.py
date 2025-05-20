from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from accounts.forms import CustomUserAdminForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('full_name', 'cnic', 'phone_number', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    fieldsets = (
        (None, {'fields': ('cnic', 'phone_number', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'education', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cnic', 'phone_number', 'full_name', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('cnic', 'phone_number', 'full_name')
    ordering = ('cnic',)

admin.site.register(User, UserAdmin)


admin.site.unregister(User)

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserAdminForm
    form = CustomUserAdminForm
    model = User

    list_display = ('full_name', 'cnic', 'phone_number', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('cnic', 'phone_number', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'education', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cnic', 'phone_number', 'full_name', 'education', 'role', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    search_fields = ('cnic', 'phone_number', 'full_name')
    ordering = ('cnic',)

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)