from rest_framework import serializers
from apps.exam.models import Exam

class ListExamSerializer(serializers.ModelSerializer):
    total_questions = serializers.SerializerMethodField()
    group_name = serializers.CharField(source='exam_group.name', read_only=True)

    class Meta:
        model = Exam
        fields = '__all__'

    def get_total_questions(self, obj):
        return obj.questions.count()