from apps.exam.models import Exam
from rest_framework import serializers


class CreateExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = [
            'exam_type', 'subject', 'start_time', 'duration', 'status',
            'is_published', 'is_timed', 'randomize_questions', 'attempt_limit',
            'max_score', 'tags', 'instructions'
        ]
        extra_kwargs = {
            'exam_type': {'required': True},
            'subject': {'required': True},    # Required in model
            'start_time': {'required': True}, # Required in model
            'duration': {'required': False},
            'status': {'required': False},
            'is_published': {'required': False},
            'is_timed': {'required': False},
            'randomize_questions': {'required': False},
            'attempt_limit': {'required': False},
            'max_score': {'required': False},
            'tags': {'required': False},
            'instructions': {'required': False},
        }

    def validate(self, data):
        if data.get('is_timed', False) and (data.get('duration') is None or data.get('duration') <= 0):
            raise serializers.ValidationError("Duration must be positive when exam is timed.")
        if data.get('status', Exam.ExamStatus.DRAFT) == Exam.ExamStatus.DRAFT and data['start_time'] < timezone.now():
            raise serializers.ValidationError("Start time cannot be in the past for a draft exam.")
        return data
