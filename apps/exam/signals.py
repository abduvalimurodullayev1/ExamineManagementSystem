from django.db.models import Avg, Max, Min, Count
from django.dispatch import receiver
# from django.db import signals
from django.db import models
from django.db.models.signals import post_save
from apps.exam.models import ExamStatistics, Submission, QuestionScore, QuestionStatistics
from django.db.models.signals import post_delete


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
        pass_count = submissions.filter(score__gte=models.F('exam__passing_score')).count()
        stats.average_score = scores['avg_score'] or 0
        stats.highest_score = scores['max_score'] or 0
        stats.lowest_score = scores['min_score'] or 0
        stats.participants = scores['participants'] or 0
        stats.pass_rate = (pass_count / stats.participants * 100) if stats.participants > 0 else 0
        stats.save(update_fields=['average_score', 'highest_score', 'lowest_score', 'participants', 'pass_rate'])

        for qs in QuestionScore.objects.filter(exam=instance.exam):
            q_stats, _ = QuestionStatistics.objects.get_or_create(exam=instance.exam, question=qs.question)
            q_stats.update_stats()


@receiver(post_delete, sender=Submission)
def update_exam_statistics_on_delete(sender, instance, **kwargs):
    if instance.status == Submission.SubmissionStatus.EVALUATED:
        update_exam_statistics(sender, instance)
