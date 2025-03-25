from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationTypeChoices(models.TextChoices):
    news = "news",  _("News")
    exam = "exam", _("Exam")
    announcement = "announcement", _("E'lon")
    other = "other", _("Other")


class NotificationType(models.Model):
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

