# apps/exam/api_endpoints/submission_submit/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.exam.api_endpoints.submission_submit.serializers import SubmissionSubmitSerializer
from apps.exam.models import Submission
from telegram_bot import send_telegram_message

class SubmissionSubmitView(generics.UpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSubmitSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def perform_update(self, serializer):
        submission = serializer.save()
        message = f"{submission.student.username} imtihonni topshirdi: {submission.exam.subject}"
        send_telegram_message(chat_id="group_chat_id", message=message)

__all__ = ['SubmissionSubmitView']