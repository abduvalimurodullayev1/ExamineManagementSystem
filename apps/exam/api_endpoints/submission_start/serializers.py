# apps/exam/api_endpoints/submission_start/serializers.py
from rest_framework import serializers
from apps.exam.models import Submission, QuestionScore
from django.utils import timezone

class SubmissionStartSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    remaining_time = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ['id', 'exam', 'student', 'started_at', 'attempt_number', 'questions', 'remaining_time']
        read_only_fields = ['id', 'student', 'started_at', 'attempt_number', 'questions', 'remaining_time']

    def get_questions(self, obj):
        questions = obj.get_questions(randomize=obj.exam.randomize_questions)
        return [{
            'id': qs.question.id,
            'body': qs.question.body,
            'type': qs.question.type,
            'options': [{'id': opt.id, 'text': opt.option_text} for opt in qs.question.options.all()] if qs.question.type == 'mcq' else None,
            'score': qs.score
        } for qs in questions]

    def get_remaining_time(self, obj):
        if obj.exam.is_timed:
            return (obj.exam.start_time + obj.exam.duration - timezone.now()).total_seconds()
        return None

    def validate_exam(self, value):
        if value.status != 'active':
            raise serializers.ValidationError("Exam must be active to start.")
        if value.start_time > timezone.now() or (value.is_timed and value.end_time < timezone.now()):
            raise serializers.ValidationError("Exam is not within its active time window.")
        return value

    def create(self, validated_data):
        student = self.context['request'].user
        exam = validated_data['exam']
        attempt_number = Submission.objects.filter(exam=exam, student=student).count() + 1
        if attempt_number > exam.attempt_limit:
            raise serializers.ValidationError("Attempt limit exceeded.")
        submission = Submission.objects.create(
            exam=exam,
            student=student,
            started_at=timezone.now(),
            attempt_number=attempt_number,
            status='started'
        )
        return submission