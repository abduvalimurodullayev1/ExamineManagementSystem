from django.db.models import Avg, Max, Min, Count
from django.dispatch import receiver
# from django.db import signals
from django.db.models.signals import post_save
from apps.exam.models import ExamStatistics, Submission


@receiver(post_save, sender=Submission)
def update_exam_statistics(sender, instance, **kwargs):
    if instance.status == Submission.SubmissionStatus.EVALUATED:
        stats, _ = ExamStatistics.objects.get_or_create(exam=instance.exam)

        submissions = Submission.objects.filter(exam=instance.exam, status=Submission.SubmissionStatus.EVALUATED)
        scores = submissions.aggregate(
            avg_score=Avg('score'),
            max_score=Max('score'),
            min_score=Min('score'),
            participants=Count('id')
        )

        stats.average_score = scores['avg_score'] or 0
        stats.highest_score = scores['max_score'] or 0
        stats.lowest_score = scores['min_score'] or 0
        stats.participants = scores['participants'] or 0

        stats.save(update_fields=['average_score', 'highest_score', 'lowest_score', 'participants'])