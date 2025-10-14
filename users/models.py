from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50, unique=True)
    user_type = models.CharField(max_length=50, choices=(
        ('organizer', 'Organizer'),
        ('member', 'Member'),
        
    ))
    email = models.EmailField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'  # Use phone_number as username
    REQUIRED_FIELDS = ['full_name', 'user_type']

    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"
