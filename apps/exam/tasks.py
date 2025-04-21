from celery import shared_task

from apps.exam.models import Submission


@shared_task
def calculate_submission_score(submission_id):
    submission = Submission.objects.get(id=submission_id)
    submission.calculate_score()