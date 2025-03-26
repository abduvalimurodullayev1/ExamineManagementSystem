from celery import shared_task
from apps.exam.models import Exam


@shared_task
def update_exam_statuses():
    exams = Exam.objects.filter(is_published=True).exclude(status=Exam.ExamStatus.FINISHED)
    for exam in exams:
        exam.update_status()
