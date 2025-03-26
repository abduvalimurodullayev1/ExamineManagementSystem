from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.exam.api_endpoints.exam_update.serializers import *
from apps.exam.permissions import IsTeacher


class ExamUpdateView(generics.UpdateAPIView):
    queryset = Exam.objects.all()
    serializer_class = UpdateExamSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def perform_update(self, serializer):
        serializer.save()


__all__ = ['ExamUpdateView']
