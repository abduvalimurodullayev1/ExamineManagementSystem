# apps/exam/api_endpoints/exam_create/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.exam.permissions import IsTeacher
from apps.exam.api_endpoints.exam_create.serializers import CreateExamSerializer
from telegram_bot import send_telegram_message

class ExamCreateView(generics.CreateAPIView):
    serializer_class = CreateExamSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        exam = serializer.save(created_by=self.request.user)
        message = f"Yangi imtihon yaratildi: {exam.subject} - {exam.start_time}"
        send_telegram_message(chat_id="group_chat_id", message=message)

__all__ = ['ExamCreateView']