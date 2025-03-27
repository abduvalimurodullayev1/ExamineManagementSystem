# apps/exam/api_endpoints/question_score/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.exam.permissions import IsTeacher
from apps.exam.api_endpoints.question_score.serializers import QuestionScoreSerializer
from telegram_bot import send_telegram_message

class QuestionScoreCreateView(generics.CreateAPIView):
    serializer_class = QuestionScoreSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        question_score = serializer.save()
        exam = question_score.exam
        exam.max_score = sum(qs.score for qs in exam.questions.all())
        exam.save()
        message = f"Imtihonga savol qo'shildi: {exam.subject}"
        send_telegram_message(chat_id="group_chat_id", message=message)

__all__ = ['QuestionScoreCreateView']