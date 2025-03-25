from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from ckeditor.fields import RichTextField
from django_resized import ResizedImageField
from django.conf import settings

class Notification(models.Model):
    class NotificationTypeChoices(models.TextChoices):
        NEWS = "news", _("News")
        EXAM = "exam", _("Exam")
        ANNOUNCEMENT = "announcement", _("E'lon")
        OTHER = "other", _("Other")

    type = models.CharField(
        max_length=20,
        choices=NotificationTypeChoices.choices,
        default=NotificationTypeChoices.OTHER,
        verbose_name=_("Type")
    )
    title = models.CharField(_("Title"))
    description = models.TextField(_("Description"), blank=True, null=True)
    text = RichTextField(_("Content"), blank=True, null=True)
    cover = ResizedImageField(
        _("Cover"),
        size=[500, 350],
        crop=["middle", "center"],
        quality=95,
        blank=True,
        null=True,
        upload_to="notification/%Y/%m",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="notifications",
    )
    content_id = models.BigIntegerField(blank=True, null=True)
    content = GenericForeignKey("content_type", "content_id")
    delivery_time = models.DateTimeField(_("Delivery Time"), default=timezone.now)
    data = models.JSONField(_("Data"), blank=True, null=True)

    def __str__(self):
        return self.title_uz

    def cover_url(self):
        return f"{settings.HOST}{self.cover.url}" if self.cover else ""

    def push(self, group=None):
        from utils.notifications import send_push_notification
        send_push_notification(self, group)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        indexes = [models.Index(fields=['delivery_time'])]


class UserNotification(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name=_("User"), related_name="notification_users")
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, verbose_name=_("Notification"))
    is_read = models.BooleanField(default=False, verbose_name=_("Is Read"))

    class Meta:
        verbose_name = _("User Notification")
        verbose_name_plural = _("User Notifications")
        indexes = [models.Index(fields=['user', 'is_read'])]