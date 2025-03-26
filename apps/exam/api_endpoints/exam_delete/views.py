from apps.exam.models import Exam
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.exam.api_endpoints.exam_delete.serializers import ExamDeleteSerializer
from apps.exam.permissions import IsTeacher
from rest_framework import serializers


class ExamDeleteApiView(generics.DestroyAPIView):
    queryset = Exam.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    serializer_class = ExamDeleteSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def perform_destroy(self, instance):
        if not instance.is_published:
            raise serializers.ValidationError("Exam is already unpublished.")
        instance.is_published = False
        instance.save()


__all__ = ['ExamDeleteApiView']
