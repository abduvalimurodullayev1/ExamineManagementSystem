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
    class ReleCHOICES(models.TextChoices):
        ADMIN = "admin", _("Admin")
        STUDENT = "student", _("Student")
        TEACHER = "teacher", _("Teacher")
    role = models.CharField(max_length=10, choices=ReleCHOICES.choices, default=ReleCHOICES.STUDENT, verbose_name=_("Role"))
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



class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"))
    first_name = models.CharField(max_length=255, verbose_name=_("First name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last name"))
    phone_number = models.CharField(max_length=20, verbose_name=_("Phone number"))
    address = models.CharField(max_length=255, verbose_name=_("Address"))
    city = models.CharField(max_length=255, verbose_name=_("City"))
    avatar = models.ImageField(upload_to='avatars/', verbose_name=_("Avatar"))
    device_token = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"