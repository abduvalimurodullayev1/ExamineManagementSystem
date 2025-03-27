# apps/exam/api_endpoints/exam_finish/serializers.py
from rest_framework import serializers
from apps.exam.models import Exam

class ExamFinishEarlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'status', 'end_time']
        read_only_fields = ['id', 'status', 'end_time']