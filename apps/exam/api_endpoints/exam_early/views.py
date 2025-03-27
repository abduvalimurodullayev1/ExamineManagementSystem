# apps/exam/api_endpoints/exam_finish/views.py
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.exam.permissions import IsTeacher
from apps.exam.models import Exam, Submission
from apps.exam.api_endpoints.exam_finish.serializers import ExamFinishEarlySerializer
from django.utils import timezone
from telegram_bot import send_telegram_message
from drf_yasg.utils import swagger_auto_schema

class ExamFinishEarlyView(views.APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    @swagger_auto_schema(
        request_body=ExamFinishEarlySerializer,
        responses={200: ExamFinishEarlySerializer, 404: "Exam not found"}
    )
    def post(self, request, id):
        try:
            exam = Exam.objects.get(id=id, created_by=request.user)
            if exam.status != 'active':
                return Response({"error": "Only active exams can be finished early"}, status=400)
            exam.status = 'finished'
            exam.end_time = timezone.now()
            exam.save()
            submissions = Submission.objects.filter(exam=exam, status='started')
            submissions.update(status='submitted', submitted_at=timezone.now())
            serializer = ExamFinishEarlySerializer(exam)
            message = f"Imtihon muddatidan oldin tugadi: {exam.subject}"
            send_telegram_message(chat_id="group_chat_id", message=message)
            return Response(serializer.data)
        except Exam.DoesNotExist:
            return Response({"error": "Exam not found"}, status=404)

__all__ = ['ExamFinishEarlyView']