# apps/exam/api_endpoints/exam_update/serializers.py
from rest_framework import serializers
from apps.exam.models import Exam
from django.utils import timezone

class UpdateExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = [
            'exam_type', 'subject', 'start_time', 'duration', 'status',
            'is_published', 'is_timed', 'randomize_questions', 'attempt_limit',
            'max_score', 'passing_score', 'tags', 'instructions', 'is_proctored'
        ]
        extra_kwargs = {field: {'required': False} for field in fields}

    def validate(self, data):
        instance = self.instance
        is_timed = data.get('is_timed', instance.is_timed)
        duration = data.get('duration', instance.duration)
        status = data.get('status', instance.status)
        start_time = data.get('start_time', instance.start_time)
        max_score = data.get('max_score', instance.max_score)
        passing_score = data.get('passing_score', instance.passing_score)

        if instance.status != 'draft' and status != instance.status:
            raise serializers.ValidationError("Only draft exams can change status.")
        if is_timed and (duration is None or duration <= 0):
            raise serializers.ValidationError("Duration must be positive when exam is timed.")
        if status == 'draft' and start_time < timezone.now():
            raise serializers.ValidationError("Start time cannot be in the past for a draft exam.")
        if passing_score is not None and max_score is not None and passing_score > max_score:
            raise serializers.ValidationError("Passing score cannot exceed max score.")
        if status == 'active' and not data.get('is_published', instance.is_published):
            raise serializers.ValidationError("Cannot set an unpublished exam to active status.")
        return data