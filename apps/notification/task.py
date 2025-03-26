from celery import shared_task
from django.utils import timezone
from .models import Notification
from celery import shared_task
from django.utils import timezone
from .models import Notification


@shared_task
def send_scheduled_notifications():
    now = timezone.now()
    notifications = Notification.objects.filter(is_sent=False, delivery_time__lte=now)
    if notifications.exists():
        for notification in notifications:
            notification.push()
        notifications.update(is_sent=True)





@shared_task
def send_group_notification(notification_id, group_id):
    from apps.exam.models import ExamGroup
    from apps.notification.models import Notification
    notification = Notification.objects.get(id=notification_id)
    group = ExamGroup.objects.get(id=group_id)
    notification.push(group=group)


@shared_task
def send_user_notification(notification_id, user_id):
    from apps.notification.models import Notification
    from django.contrib.auth import get_user_model
    User = get_user_model()
    notification = Notification.objects.get(id=notification_id)
    user = User.objects.get(id=user_id)
    notification.push()