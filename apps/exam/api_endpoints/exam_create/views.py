from rest_framework.permissions import IsAuthenticated

from apps.exam.api_endpoints.exam_create.serializers import *

from rest_framework import generics

from apps.exam.permissions import IsTeacher



class ExamCreateView(generics.CreateAPIView):
    serializer_class = CreateExamSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)  # Set created_by from request user

__all__ = ['ExamCreateView']
