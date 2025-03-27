from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.exam.permissions import IsTeacher
from apps.exam.api_endpoints.submission_evaluate.serializers import SubmissionEvaluateSerializer
from apps.exam.models import Submission
from telegram_bot import send_telegram_message

class SubmissionEvaluateView(generics.UpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionEvaluateSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    lookup_field = 'id'

    def perform_update(self, serializer):
        submission = serializer.save()
        message = f"{submission.student.username} uchun natija: {submission.score}/{submission.exam.max_score}"
        send_telegram_message(chat_id=submission.student.telegram_id, message=message)

__all__ = ['SubmissionEvaluateView']