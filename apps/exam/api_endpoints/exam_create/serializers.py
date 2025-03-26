from apps.exam.models import Exam
from rest_framework import serializers


class CreateExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = [
            'subject',
            'start_time',
            'duration',
            'status',
            'is_published',
            'is_timed',
            'randomize_questions',
            'attempt_limit',
            'max_score'
        ]

        extra_kwargs = {
            'start_time': {'required': False},
            'duration': {'required': False},
            'status': {'required': False},
            'is_published': {'required': False},
            'is_timed': {'required': False},
            'randomize_questions': {'required': False},
            'attempt_limit': {'required': False},
            'max_score': {'required': False},
        }

    def create(self, validated_data):
        return Exam.objects.create(**validated_data)
