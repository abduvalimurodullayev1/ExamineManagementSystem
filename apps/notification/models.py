from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from ckeditor.fields import RichTextField
from django_resized import ResizedImageField
from django.conf import settings
from django.core.validators import FileExtensionValidator


class Notification(models.Model):
    class VisibilityChoices(models.TextChoices):
        PUBLIC = "public", _("Public")
        GROUP = "group", _("Group Only")
        PRIVATE = "private", _("Private")

    class NotificationTypeChoices(models.TextChoices):
        NEWS = "news", _("News")
        EXAM = "exam", _("Exam")
        ANNOUNCEMENT = "announcement", _("Announcement")
        SUBMISSION = "submission", _("Submission")
        OTHER = "other", _("Other")

    type = models.CharField(
        max_length=20,
        choices=NotificationTypeChoices.choices,
        default=NotificationTypeChoices.OTHER,
        verbose_name=_("Type")
    )
    visibility = models.CharField(max_length=20, choices=VisibilityChoices.choices, default=VisibilityChoices.PUBLIC)
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    content_text = RichTextField(blank=True, null=True, verbose_name=_("Content"))
    cover = ResizedImageField(
        size=[500, 350],
        crop=["middle", "center"],
        quality=95,
        blank=True,
        null=True,
        upload_to="notifications/%Y/%m",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        verbose_name=_("Cover")
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="notifications",
        verbose_name=_("Content Type")
    )
    content_id = models.BigIntegerField(blank=True, null=True, verbose_name=_("Content ID"))
    content = GenericForeignKey("content_type", "content_id")
    delivery_time = models.DateTimeField(default=timezone.now, verbose_name=_("Delivery Time"))
    is_sent = models.BooleanField(default=False, verbose_name=_("Is Sent"))
    data = models.JSONField(blank=True, null=True, verbose_name=_("Additional Data"))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Created By")
    )

    def __str__(self):
        return self.title

    def cover_url(self):
        return f"{settings.MEDIA_URL}{self.cover}" if self.cover else ""

    def push(self, group=None):
        from apps.notification.utils import send_push_notification
        send_push_notification(self, group)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        indexes = [
            models.Index(fields=['delivery_time', 'is_sent']),
            models.Index(fields=['type', 'created_by']),
        ]


class UserNotification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        related_name="user_notifications"
    )
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        verbose_name=_("Notification"),
        related_name="user_notifications"
    )
    is_read = models.BooleanField(default=False, verbose_name=_("Is Read"))
    read_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Read At"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])

    class Meta:
        verbose_name = _("User Notification")
        verbose_name_plural = _("User Notifications")
        indexes = [
            models.Index(fields=['user', 'is_read', 'created_at']),
        ]
        unique_together = ('user', 'notification')

    def __str__(self):
        return f"{self.user.email} - {self.notification.title}"
