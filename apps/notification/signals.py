from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.exam.models import Exam, Submission
from apps.notification.models import Notification, UserNotification
from django.utils import timezone

@receiver(post_save, sender=Exam)
def notify_exam_status(sender, instance, created, **kwargs):
    if instance.status == Exam.ExamStatus.ACTIVE and instance.is_published and not created:
        notification = Notification.objects.create(
            type=Notification.NotificationTypeChoices.EXAM,
            title=f"Exam Started: {instance.subject.title}",
            description=f"The {instance.subject.title} exam has started.",
            content_text=f"Start Time: {instance.start_time}",
            content=instance,
            delivery_time=instance.start_time,
            created_by=instance.created_by
        )
        for group in instance.examgroup_set.all():
            from apps.notification.task import send_group_notification
            send_group_notification.delay(notification.id, group.id)


@receiver(post_save, sender=Submission)
def notify_submission_evaluated(sender, instance, **kwargs):
    if instance.status == Submission.SubmissionStatus.EVALUATED:
        notification = Notification.objects.create(
            type=Notification.NotificationTypeChoices.SUBMISSION,
            title=f"Results Ready: {instance.exam.subject.title}",
            description=f"Your score: {instance.score}",
            content_text=f"Feedback: {instance.feedback or 'No feedback provided'}",
            content=instance,
            delivery_time=timezone.now(),
            created_by=instance.evaluated_by
        )
        UserNotification.objects.create(
            user=instance.student,
            notification=notification
        )
        from apps.notification.task import send_user_notification
        send_user_notification.delay(notification.id, instance.student.id)

