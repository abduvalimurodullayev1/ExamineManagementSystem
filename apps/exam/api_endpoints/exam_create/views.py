from apps.exam.api_endpoints.exam_create.serializers import *

from rest_framework import generics


class ExamCreateView(generics.CreateAPIView):
    serializer_class = CreateExamSerializer

    def perform_create(self, serializer):
        serializer.save()



__all__ = ['ExamCreateView']
