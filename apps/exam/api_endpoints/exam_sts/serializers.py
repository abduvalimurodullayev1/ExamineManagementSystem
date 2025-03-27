from rest_framework import serializers
from apps.exam.models import Exam, Submission, Answer

class ExamStatsSerializer(serializers.ModelSerializer):
    average_score = serializers.SerializerMethodField()
    highest_score = serializers.SerializerMethodField()
    lowest_score = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()
    question_stats = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = ['id', 'subject', 'average_score', 'highest_score', 'lowest_score', 'participants', 'question_stats']

    def get_average_score(self, obj):
        submissions = Submission.objects.filter(exam=obj, status='evaluated')
        return submissions.aggregate(avg=Avg('score'))['avg'] or 0

    def get_highest_score(self, obj):
        return Submission.objects.filter(exam=obj, status='evaluated').aggregate(max=Max('score'))['max'] or 0

    def get_lowest_score(self, obj):
        return Submission.objects.filter(exam=obj, status='evaluated').aggregate(min=Min('score'))['min'] or 0

    def get_participants(self, obj):
        return Submission.objects.filter(exam=obj, status='evaluated').count()

    def get_question_stats(self, obj):
        return [{
            'question_id': qs.question.id,
            'body': qs.question.body,
            'correct_percentage': Answer.objects.filter(
                submission__exam=obj, question=qs.question, is_correct=True
            ).count() / max(1, Submission.objects.filter(exam=obj).count()) * 100
        } for qs in obj.questions.all()]