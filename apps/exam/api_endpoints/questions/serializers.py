from apps.exam.models import Question
from rest_framework import serializers

class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['body', 'subject', 'type', 'correct_answer', 'options']

    def create(self, validated_data):
        return Question.objects.create(**validated_data)