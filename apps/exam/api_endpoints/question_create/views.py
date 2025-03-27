# apps/exam/api_endpoints/question_create/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.exam.permissions import IsTeacher
from apps.exam.api_endpoints.question_create.serializers import QuestionCreateSerializer
from telegram_bot import send_telegram_message

class QuestionCreateView(generics.CreateAPIView):
    serializer_class = QuestionCreateSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        question = serializer.save()
        message = f"Yangi savol qo'shildi: {question.body[:50]}..."
        send_telegram_message(chat_id="teacher_chat_id", message=message)

__all__ = ['QuestionCreateView']