# apps/exam/api_endpoints/submission_start/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.exam.api_endpoints.submission_start.serializers import SubmissionStartSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from telegram_bot import send_telegram_message

class SubmissionStartView(generics.CreateAPIView):
    serializer_class = SubmissionStartSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['exam'],
            properties={'exam': openapi.Schema(type=openapi.TYPE_INTEGER, description='Exam ID')}
        ),
        responses={201: SubmissionStartSerializer}
    )
    def perform_create(self, serializer):
        submission = serializer.save()
        message = f"{submission.student.username} imtihonni boshladi: {submission.exam.subject}"
        send_telegram_message(chat_id="group_chat_id", message=message)

__all__ = ['SubmissionStartView']