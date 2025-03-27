# apps/exam/api_endpoints/submission_submit/serializers.py
from rest_framework import serializers
from apps.exam.models import Submission, Answer, QuestionOption
from django.utils import timezone

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'answer_text', 'file']
        extra_kwargs = {'file': {'required': False}}

class SubmissionSubmitSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Submission
        fields = ['id', 'answers']
        read_only_fields = ['id']

    def validate(self, data):
        submission = self.instance
        if submission.status != 'started':
            raise serializers.ValidationError("Submission must be in 'started' status.")
        if submission.exam.is_timed and timezone.now() > submission.exam.end_time:
            raise serializers.ValidationError("Submission time has expired.")
        questions = set(qs.question.id for qs in submission.exam.questions.all())
        answered_questions = set(ans['question'].id for ans in data['answers'])
        if questions != answered_questions:
            raise serializers.ValidationError("All questions must be answered.")
        return data

    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers')
        for answer_data in answers_data:
            Answer.objects.create(submission=instance, **answer_data)
        instance.status = 'submitted'
        instance.submitted_at = timezone.now()
        instance.save()
        return instance