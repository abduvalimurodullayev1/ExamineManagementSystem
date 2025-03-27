# apps/exam/api_endpoints/exam_stats/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.exam.permissions import IsTeacher
from apps.exam.api_endpoints.exam_stats.serializers import ExamStatsSerializer
from apps.exam.models import Exam
from django_filters.rest_framework import DjangoFilterBackend
from telegram_bot import send_telegram_message

class ExamStatsView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamStatsSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['exam_group']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        message = f"Statistika: {instance.subject}\nO'rtacha: {data['average_score']}\nIshtirokchilar: {data['participants']}"
        send_telegram_message(chat_id="teacher_chat_id", message=message)
        return Response(data)

__all__ = ['ExamStatsView']