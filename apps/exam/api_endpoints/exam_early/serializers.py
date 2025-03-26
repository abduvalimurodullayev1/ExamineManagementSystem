from rest_framework import serializers
from apps.exam.models import Exam



class ExamFinishEarlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'status']
        read_only_fields = ['id', 'status']
