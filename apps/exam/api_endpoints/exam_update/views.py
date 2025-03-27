# apps/exam/api_endpoints/exam_update/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.exam.permissions import IsTeacher
from apps.exam.models import Exam
from apps.exam.api_endpoints.exam_update.serializers import UpdateExamSerializer
# from telegram_bot import send_telegram_message

class ExamUpdateView(generics.UpdateAPIView):
    queryset = Exam.objects.all()
    serializer_class = UpdateExamSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def perform_update(self, serializer):
        exam = serializer.save()
        if 'status' in serializer.validated_data:
            message = f"Imtihon holati yangilandi: {exam.subject} - {exam.status}"
            # send_telegram_message(chat_id="group_chat_id", message=message)

__all__ = ['ExamUpdateView']