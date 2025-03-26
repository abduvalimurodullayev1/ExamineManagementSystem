from rest_framework import serializers, generics
from rest_framework.permissions import IsAuthenticated
from apps.exam.models import Question, QuestionOption
from apps.exam.permissions import IsTeacher

class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['option_text', 'is_correct']

class QuestionCreateSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ['subject', 'body', 'type', 'options', 'difficulty_level', 'attachment']

    def validate(self, data):
        question_type = data.get('type')
        options = data.get('options', [])

        if question_type == Question.QuestionTypes.MCQ:
            if len(options) < 2:
                raise serializers.ValidationError("MCQ must have at least 2 options.")
            correct_count = sum(1 for opt in options if opt.get('is_correct', False))
            if correct_count != 1:
                raise serializers.ValidationError("MCQ must have exactly one correct option.")
        elif question_type == Question.QuestionTypes.ESSAY and options:
            raise serializers.ValidationError("Essay questions cannot have options.")
        return data

    def create(self, validated_data):
        options_data = validated_data.pop('options', [])
        question = Question.objects.create(
            created_by=self.context['request'].user,
            **validated_data
        )
        if options_data:
            for option_data in options_data:
                QuestionOption.objects.create(question=question, **option_data)
        return question
