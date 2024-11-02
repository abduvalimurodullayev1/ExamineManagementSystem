# apps/users/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Assignment, Submission, Notification


@receiver(post_save, sender=Assignment)
def create_assignment_notification(sender, instance, created, **kwargs):
    if created:
        message = f"New assignment assigned: {instance.exam.exam_name}"
        Notification.objects.create(user=instance.student, message=message)


@receiver(post_save, sender=Submission)
def create_submission_notification(sender, instance, created, **kwargs):
    if created:
        message = f"Your submission for {instance.exam.exam_name} has been received."
        Notification.objects.create(user=instance.student, message=message)
