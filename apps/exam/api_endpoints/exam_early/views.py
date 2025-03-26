from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.exam.models import Exam
from apps.exam.api_endpoints.exam_early.serializers import ExamFinishEarlySerializer
from apps.exam.permissions import IsTeacher


class ExamFinishEarlyView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request, id):
        exam = Exam.objects.get(id=id)
        exam.finish_early(request.user)
        serializer = ExamFinishEarlySerializer(exam)
        return Response(serializer.data)


__all__ = ['ExamFinishEarlyView']
