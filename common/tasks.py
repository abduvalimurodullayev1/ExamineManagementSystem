# common/tasks.py
from pyfcm import FCMNotification
from celery import shared_task
from django.conf import settings
from .models import Notification


@shared_task
def send_push_notification(user_id, device_token, title, message):
    push_service = FCMNotification(api_key=settings.FCM_API_KEY)

    # Xabarni yuborish
    result = push_service.notify_single_device(
        registration_id=device_token,
        message_title=title,
        message_body=message
    )

    # Notification obyektini saqlash
    Notification.objects.create(user_id=user_id, title=title, message=message)

    return result
