from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.exam.models import Exam, Submission
from apps.notification.models import Notification
from django.utils import timezone

@receiver(post_save, sender=Exam)
def notify_exam_status(sender, instance, created, **kwargs):
    if instance.status == "active" and instance.is_published and created:
        notification = Notification.objects.create(
            type="exam",
            title_uz=f"Imtihon boshlandi: {instance.subject.title}",
            title_ru=f"Экзамен начался: {instance.subject.title}",
            description_uz=f"{instance.subject.title} imtihoni boshlandi.",
            description_ru=f"Экзамен по {instance.subject.title} начался.",
            content=instance,
            delivery_time=instance.start_time
        )
        for group in instance.examgroup_set.all():
            notification.push(group=group)

@receiver(post_save, sender=Submission)
def notify_submission_evaluated(sender, instance, **kwargs):
    if instance.status == "evaluated":
        notification = Notification.objects.create(
            type="exam",
            title_uz=f"Natijangiz chiqdi: {instance.exam.subject.title}",
            title_ru=f"Результаты готовы: {instance.exam.subject.title}",
            description_uz=f"Ball: {instance.score}",
            description_ru=f"Балл: {instance.score}",
            content=instance,
            delivery_time=timezone.now()
        )
        UserNotification.objects.create(user=instance.student, notification=notification)
        notification.push()