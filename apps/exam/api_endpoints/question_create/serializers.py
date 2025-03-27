from rest_framework import serializers
from apps.exam.models import Question, QuestionOption

class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['option_text', 'is_correct']

class QuestionCreateSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ['subject', 'body', 'type', 'options', 'difficulty_level', 'attachment', 'tags']

    def validate(self, data):
        question_type = data.get('type')
        options = data.get('options', [])
        if question_type == 'mcq' and len(options) < 2:
            raise serializers.ValidationError("MCQ must have at least 2 options.")
        if question_type == 'mcq' and sum(1 for opt in options if opt.get('is_correct')) != 1:
            raise serializers.ValidationError("MCQ must have exactly one correct option.")
        if question_type in ['essay', 'short_answer'] and options:
            raise serializers.ValidationError(f"{question_type} questions cannot have options.")
        return data

    def create(self, validated_data):
        options_data = validated_data.pop('options', [])
        question = Question.objects.create(created_by=self.context['request'].user, **validated_data)
        for option_data in options_data:
            QuestionOption.objects.create(question=question, **option_data)
        return question