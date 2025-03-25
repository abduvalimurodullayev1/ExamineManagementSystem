from celery import shared_task
from django.utils import timezone
from .models import Notification

@shared_task
def send_scheduled_notifications():
    now = timezone.now()
    notifications = Notification.objects.filter(is_sent=False, delivery_time__lte=now)
    for notification in notifications:
        notification.push()
        notification.is_sent = True
        notification.save()