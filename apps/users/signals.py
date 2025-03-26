# apps/users/signals.py
import jwt
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.exam.models import Submission
from apps.notification.models import Notification
from apps.users.models import Profile, User
from apps.users.task import send_mail_to_user


@receiver(post_save, sender=Submission)
def create_submission_notification(sender, instance, created, **kwargs):
    if created:
        message = f"Your submission for {instance.exam.exam_name} has been received."
        Notification.objects.create(user=instance.student, message=message)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print("Profile created")
        Profile.objects.create(user=instance)

    instance.profile.save()


@receiver(post_save, sender=User)
def send_verification_token_email(sender, instance, created, **kwargs):
    if created:
        send_mail_to_user.delay(instance.id, instance.email)
