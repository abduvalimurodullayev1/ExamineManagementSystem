from rest_framework import serializers
from apps.exam.models import Submission
from django.utils import timezone



class SubmissionStartSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ['id', 'exam', 'student', 'started_at', 'attempt_number', 'questions']
        read_only_fields = ['id', 'student', 'started_at', 'attempt_number', 'questions']

    def get_questions(self, obj):
        questions = obj.get_questions()
        return [{
            'id': qs.question.id,
            'body': qs.question.body,
            'type': qs.question.type,
            'options': [{'id': opt.id, 'text': opt.option_text} for opt in qs.question.options.all()] if qs.question.type == 'mcq' else None,
            'score': qs.score
        } for qs in questions]

    def create(self, validated_data):
        student = self.context['request'].user
        exam = validated_data['exam']
        attempt_number = Submission.objects.filter(exam=exam, student=student).count() + 1
        submission = Submission.objects.create(
            exam=exam,
            student=student,
            started_at=timezone.now(),
            attempt_number=attempt_number
        )
        return submission
