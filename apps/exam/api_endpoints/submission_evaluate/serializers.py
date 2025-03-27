# apps/exam/api_endpoints/submission_evaluate/serializers.py
from rest_framework import serializers
from apps.exam.models import Submission, Answer, QuestionScore

class AnswerEvaluateSerializer(serializers.ModelSerializer):
    score = serializers.FloatField(required=False)

    class Meta:
        model = Answer
        fields = ['id', 'question', 'answer_text', 'file', 'is_correct', 'score']

class SubmissionEvaluateSerializer(serializers.ModelSerializer):
    answers = AnswerEvaluateSerializer(many=True, required=False)

    class Meta:
        model = Submission
        fields = ['id', 'score', 'feedback', 'answers']
        read_only_fields = ['id']

    def validate(self, data):
        submission = self.instance
        if submission.status != 'submitted':
            raise serializers.ValidationError("Only submitted submissions can be evaluated.")
        if 'answers' in data:
            for answer_data in data['answers']:
                max_score = QuestionScore.objects.get(exam=submission.exam, question=answer_data['question']).score
                if answer_data.get('score', 0) > max_score:
                    raise serializers.ValidationError(f"Score for question {answer_data['question'].id} exceeds max score.")
        return data

    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers', None)
        if answers_data:
            for answer_data in answers_data:
                answer = Answer.objects.get(id=answer_data['id'])
                answer.is_correct = answer_data.get('is_correct', answer.is_correct)
                answer.score = answer_data.get('score', 0)
                answer.save()
        else:  # Avtomatik baholash
            for answer in instance.answers.all():
                if answer.question.type == 'mcq':
                    correct_option = answer.question.options.filter(is_correct=True).first()
                    answer.is_correct = answer.answer_text == str(correct_option.id)
                    answer.score = QuestionScore.objects.get(exam=instance.exam, question=answer.question).score if answer.is_correct else 0
                    answer.save()
        instance.score = sum(answer.score for answer in instance.answers.all())
        instance.feedback = validated_data.get('feedback', instance.feedback)
        instance.status = 'evaluated'
        instance.evaluated_by = self.context['request'].user
        instance.save()
        return instance