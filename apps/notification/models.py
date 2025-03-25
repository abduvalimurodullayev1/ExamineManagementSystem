import json

import requests
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from onesignal_sdk.client import Client
from onesignal_sdk.error import OneSignalHTTPError


from ckeditor.fields import RichTextField

from apps.users.models import BaseModel, User


class NotificationTypeChoices(models.TextChoices):
    news = "news", _("News")
    exam = "exam", _("Exam")
    announcement = "announcement", _("E'lon")
    other = "other", _("Other")


class NotificationType(BaseModel):
    type = models.CharField(
        max_length=20,
        choices=NotificationTypeChoices.choices,
        default=NotificationTypeChoices.other
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"))

    class Meta:
        db_table = "notification_type"
        verbose_name = _("Notification Type")
        verbose_name_plural = _("Notification Types")


class Notification(BaseModel):
    type = models.ForeignKey(
        NotificationType,
        on_delete=models.CASCADE,
        verbose_name=_("type"),
        related_name="notifications",
    )
    title = models.CharField(_("title"), max_length=256)
    description = models.CharField(
        _("description"), max_length=256, blank=True, null=True
    )
    text = RichTextField(_("content"), blank=True, null=True)
    cover = ResizedImageField(
        _("cover"),
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

    delivery_time = models.DateTimeField(_("delivery time"), default=timezone.now)
    data = models.JSONField(_("data"), blank=True, null=True)

    client = Client(
        app_id=settings.ONESIGNAL_APP_ID,
        rest_api_key=settings.ONESIGNAL_REST_KEY,
        user_auth_key=settings.ONESIGNAL_AUTH_KEY,
    )

    def __str__(self):
        return f"{self.title}"

    def cover_url(self):
        return f"{settings.HOST}{self.cover.url}" if self.cover else ""

    def push(self):
        try:
            data = {
                "id": self.content_id,
                "object_type": self.type.type,
                "cover_url": f"{settings.HOST}{self.cover.url}",
                "description": self.description,
                "description_ru": self.description_ru,
                "text": self.text,
                "text_ru": self.text_ru,
            }

            order_notification_body = {
                "contents": {"ru": self.title_ru, "uz": self.title},
                "included_segments": ["Active Users"],
                "data": data,
            }
            self.client.send_notification(order_notification_body)

        except Exception as e:
            print(e)

    class Meta:
        db_table = "notification"
        verbose_name = _("Notification")
        verbose_name_plural = _("1. Notificationlar")


class UserNotification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"), related_name="notification_users")
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, verbose_name=_("Notification"))
    is_read = models.BooleanField(default=False, verbose_name=_("Is Read"))

    class Meta:
        db_table = "user_notification"
        verbose_name = _("User Notification")
        verbose_name_plural = _("User Notifications")
