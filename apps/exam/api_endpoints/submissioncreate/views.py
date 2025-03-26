from rest_framework import serializers, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.exam.models import Submission, QuestionScore
# from apps.exam.permissions import IsStudent
from apps.exam.api_endpoints.submissioncreate.serializers import SubmissionStartSerializer
from django.utils import timezone

class SubmissionStartView(generics.CreateAPIView):
    serializer_class = SubmissionStartSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['exam'],
            properties={
                'exam': openapi.Schema(type=openapi.TYPE_INTEGER, description='Exam ID'),
            }
        ),
        responses={
            201: openapi.Response(
                description="Submission started successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'exam': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'student': openapi.Schema(type=openapi.TYPE_STRING),
                        'started_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                        'attempt_number': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'questions': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'body': openapi.Schema(type=openapi.TYPE_STRING),
                                    'type': openapi.Schema(type=openapi.TYPE_STRING, enum=['mcq', 'essay', 'true_false', 'short_answer', 'matching']),
                                    'options': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                'text': openapi.Schema(type=openapi.TYPE_STRING),
                                            }
                                        ),
                                        nullable=True
                                    ),
                                    'score': openapi.Schema(type=openapi.TYPE_INTEGER),
                                }
                            )
                        )
                    }
                )
            ),
            400: "Validation error (e.g., exam not active, attempt limit exceeded)"
        }
    )
    def perform_create(self, serializer):
        serializer.save()

__all__ = ['SubmissionStartView']