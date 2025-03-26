from apps.exam.models import Exam
from rest_framework import serializers

class ListExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'