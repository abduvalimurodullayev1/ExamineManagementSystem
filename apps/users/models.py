from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from apps.users.managers import UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from time import timezone


# User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True


class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("student", "Student"),
        ("teacher", "Teacher"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")
    username = models.CharField(max_length=150, unique=False, null=True, blank=True, verbose_name=_("username"))
    verification_code = models.CharField(max_length=6)
    activation_key_expires = models.DateTimeField(blank=True, null=True)
    device_token = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=150, unique=True, verbose_name=_("email"))
    is_verified = models.BooleanField(default=False, verbose_name=_("is verified"))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    def token(self):
        pass
