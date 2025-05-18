from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, cnic, phone_number, password=None, **extra_fields):
        if not cnic:
            raise ValueError("Users must have a CNIC")
        if not phone_number:
            raise ValueError("Users must have a phone number")
        
        user = self.model(cnic=cnic, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cnic, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(cnic, phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('driver', 'Driver'),
        ('passenger', 'Passenger'),
    )

    cnic = models.CharField(max_length=15, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    education = models.CharField(max_length=100, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'cnic'
    REQUIRED_FIELDS = ['phone_number', 'full_name']

    def __str__(self):
        return f"{self.full_name} ({self.role})"



