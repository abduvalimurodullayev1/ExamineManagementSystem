from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.exam.api_endpoints.list_exam.serializers import *
from apps.exam.models import Exam


class ListExamView(generics.ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = ListExamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)