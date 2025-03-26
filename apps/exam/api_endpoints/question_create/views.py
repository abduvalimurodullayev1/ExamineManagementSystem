from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.exam.api_endpoints.question_create.serializers import QuestionCreateSerializer
from apps.exam.permissions import IsTeacher


class QuestionCreateView(generics.CreateAPIView):
    serializer_class = QuestionCreateSerializer
    permission_classes = [IsAuthenticated, IsTeacher]


__all__ = ['QuestionCreateView']
