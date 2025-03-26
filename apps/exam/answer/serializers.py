from rest_framework import serializers, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.exam.models import Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'answer_text', 'answer_file']

    def validate(self, data):
        question = data['question']
        if question.type == 'mcq' and not data.get('answer_text'):
            raise serializers.ValidationError("MCQ requires an answer_text from options.")
        if question.type == 'essay' and not (data.get('answer_text') or data.get('answer_file')):
            raise serializers.ValidationError("Essay requires either answer_text or answer_file.")
        return data
