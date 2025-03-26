from rest_framework import serializers, generics
from apps.exam.models import QuestionScore, Exam, Question

class QuestionScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionScore
        fields = ['exam', 'question', 'score', 'order']

    def validate(self, data):
        exam = data['exam']
        question = data['question']
        if exam.created_by != self.context['request'].user:
            raise serializers.ValidationError("You can only add questions to your own exams.")
        if QuestionScore.objects.filter(exam=exam, question=question).exists():
            raise serializers.ValidationError("This question is already added to the exam.")
        return data
