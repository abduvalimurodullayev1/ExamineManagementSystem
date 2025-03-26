import uuid
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, FileExtensionValidator
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.users.managers import UserManager


def activation_key_expiry():
    return timezone.now() + timezone.timedelta(hours=24)


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        ADMIN = "admin", _("Admin")
        TEACHER = "teacher", _("Teacher")
        STUDENT = "student", _("Student")
        MODERATOR = "moderator", _("Moderator")

    role = models.CharField(
        max_length=10,
        choices=RoleChoices.choices,
        default=RoleChoices.STUDENT,
        verbose_name=_("Role")
    )
    email = models.EmailField(
        max_length=150,
        unique=True,
        verbose_name=_("Email"),
        error_messages={"unique": _("A user with that email already exists.")}
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_("Username"),
        help_text=_("Optional unique username")
    )
    verification_token = models.CharField(
        max_length=120,
        blank=True,
        verbose_name=_("Verification Code"),
        help_text=_("6-digit code for email verification")
    )
    activation_key_expires = models.DateTimeField(
        default=activation_key_expiry,  # Correct: pass the function itself
        verbose_name=_("Activation Key Expires")
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_("Is Verified"),
        help_text=_("Indicates if the email is verified")
    )
    device_token = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("Device Token"),
        help_text=_("For push notifications")
    )
    last_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("Last Login IP")
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def generate_verification_token(self):
        self.verification_token = uuid.uuid4()
        self.activation_key_expires = timezone.now() + timezone.timedelta(hours=24)

    def save(self, *args, **kwargs):
        if not self.verification_token or self.activation_key_expires < timezone.now():
            self.generate_verification_token()
        if not self.username:
            self.username = None
        super().save(*args, **kwargs)

    def is_activation_key_valid(self):
        return self.activation_key_expires >= timezone.now() and not self.is_verified

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        indexes = [
            models.Index(fields=['email', 'role']),
            models.Index(fields=['is_verified', 'last_login']),
        ]

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        related_name='profile'
    )
    first_name = models.CharField(max_length=255, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last Name"))
    phone_number = models.CharField(
        max_length=20,
        verbose_name=_("Phone Number"),
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_(
            "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))]
    )
    address = models.CharField(max_length=255, blank=True, verbose_name=_("Address"))
    city = models.CharField(max_length=100, blank=True, verbose_name=_("City"))
    country = models.CharField(max_length=100, blank=True, verbose_name=_("Country"))
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/%d/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        verbose_name=_("Avatar")
    )
    bio = models.TextField(blank=True, verbose_name=_("Bio"))

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        indexes = [models.Index(fields=['user', 'phone_number'])]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.avatar and self.avatar.size > 5 * 1024 * 1024:
            raise ValidationError(_("Avatar file size cannot exceed 5MB."))
        super().save(*args, **kwargs)


class UserStatistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_exams = models.PositiveIntegerField(default=0)
    average_score = models.FloatField(default=0)
    highest_score = models.FloatField(default=0)

    def __str__(self):
        return f"Statistics for {self.user.email}"
