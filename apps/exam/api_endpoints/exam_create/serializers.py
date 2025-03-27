from rest_framework import serializers
from apps.exam.models import Exam, Question, QuestionOption, QuestionScore
from django.utils import timezone
from rest_framework.exceptions import ValidationError


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['option_text', 'is_correct']
        extra_kwargs = {'is_correct': {'default': False}}


class QuestionCreateSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ['subject', 'body', 'type', 'options', 'difficulty_level', 'attachment']
        extra_kwargs = {
            'difficulty_level': {'default': 'medium'},
            'attachment': {'required': False}
        }

    def validate(self, data):
        question_type = data.get('type')
        options = data.get('options', [])
        if question_type == 'mcq' and len(options) < 2:
            raise serializers.ValidationError("MCQ must have at least 2 options.")
        if question_type == 'mcq' and sum(1 for opt in options if opt.get('is_correct')) != 1:
            raise serializers.ValidationError("MCQ must have exactly one correct option.")
        if question_type == 'essay' and options:
            raise serializers.ValidationError("Essay questions cannot have options.")
        return data


class CreateExamSerializer(serializers.ModelSerializer):
    questions = QuestionCreateSerializer(many=True, required=True)

    class Meta:
        model = Exam
        fields = [
            'exam_type', 'subject', 'start_time', 'duration', 'status',
            'is_published', 'is_timed', 'randomize_questions', 'attempt_limit',
            'max_score', 'tags', 'instructions', 'questions', 'is_proctored'
        ]
        extra_kwargs = {
            'status': {'default': 'draft'},
            'is_published': {'default': False},
            'is_timed': {'default': False},
            'randomize_questions': {'default': False},
            'attempt_limit': {'default': 1},
            'is_proctored': {'default': False}
        }

    def validate(self, data):
        if data.get('is_timed') and (data.get('duration') is None or data.get('duration') <= 0):
            raise serializers.ValidationError("Duration must be positive when exam is timed.")
        if data.get('start_time') < timezone.now():
            raise serializers.ValidationError("Start time cannot be in the past.")
        if not data.get('questions'):
            raise serializers.ValidationError("At least one question is required.")
        return data

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        exam = Exam.objects.create(created_by=self.context['request'].user, **validated_data)
        total_score = 0
        for idx, question_data in enumerate(questions_data):
            options_data = question_data.pop('options', [])
            question = Question.objects.create(created_by=self.context['request'].user, **question_data)
            for option_data in options_data:
                QuestionOption.objects.create(question=question, **option_data)
            QuestionScore.objects.create(exam=exam, question=question, score=5, order=idx + 1)
            total_score += 5
        exam.max_score = total_score
        exam.save()
        return exam
