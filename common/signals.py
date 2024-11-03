from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Assignment, Submission, Notification, ExamResult


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


def calculate_exam_result(sender, instance, **kwargs):
    exam = instance.exam
    student = instance.student
    total_questions = exam.questions.count()
    answered_questions = Submission.objects.filter(exam=exam, student=student).count()

    if answered_questions == total_questions:
        correct_answers = Submission.objects.filter(
            exam=exam,
            student=student,
            is_correct=True
        ).count()

        score_percentage = (correct_answers / total_questions) * 100

        exam_result, created = ExamResult.objects.get_or_create(student=student, exam=exam)
        exam_result.score = score_percentage
        exam_result.passed = score_percentage >= exam.passing_percentage
        exam_result.save()
