from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.exam.api_endpoints.question_option.serializers import QuestionScoreSerializer
from apps.exam.permissions import IsTeacher


class QuestionScoreCreateView(generics.CreateAPIView):
    serializer_class = QuestionScoreSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        serializer.save()
        exam = serializer.instance.exam
        exam.update_calculated_total_score()


__all__ = ['QuestionScoreCreateView']
