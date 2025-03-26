from rest_framework import serializers
from apps.exam.models import Exam



class ExamDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'is_published']
        read_only_fields = ['id', 'is_published']
