from rest_framework import serializers
from apps.exam.models import QuestionScore, Exam

class QuestionScoreSerializer(serializers.ModelSerializer):
    question_details = serializers.CharField(source='question.body', read_only=True)

    class Meta:
        model = QuestionScore
        fields = ['exam', 'question', 'score', 'order', 'question_details']

    def validate(self, data):
        exam = data['exam']
        if exam.created_by != self.context['request'].user:
            raise serializers.ValidationError("You can only add questions to your own exams.")
        if exam.status != 'draft':
            raise serializers.ValidationError("Questions can only be added to draft exams.")
        if QuestionScore.objects.filter(exam=exam, question=data['question']).exists():
            raise serializers.ValidationError("This question is already added to the exam.")
        return data