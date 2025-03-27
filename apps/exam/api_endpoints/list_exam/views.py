# apps/exam/api_endpoints/list_exam/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.exam.api_endpoints.list_exam.serializers import ListExamSerializer
from apps.exam.models import Exam
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class ListExamView(generics.ListAPIView):
    serializer_class = ListExamSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status', 'subject', 'start_time']
    search_fields = ['tags', 'instructions']
    pagination_class = generics.ListAPIView.pagination_class  # Default 10 per page

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            return Exam.objects.filter(created_by=user)
        elif user.is_student:
            return Exam.objects.filter(exam_group__students=user)
        return Exam.objects.all()

__all__ = ['ListExamView']