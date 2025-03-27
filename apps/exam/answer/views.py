from rest_framework import views
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from apps.exam.models import Submission
from apps.exam.answer.serializers import AnswerSerializer


class AnswerSubmitView(views.APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('submission_id', openapi.IN_PATH, description="Submission ID", type=openapi.TYPE_INTEGER)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['answers'],
            properties={
                'answers': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'question': openapi.Schema(type=openapi.TYPE_INTEGER, description='Question ID'),
                            'answer_text': openapi.Schema(type=openapi.TYPE_STRING, description='Answer text (for MCQ or Essay)', nullable=True),
                            'answer_file': openapi.Schema(type=openapi.TYPE_FILE, description='Answer file (for Essay)', nullable=True),
                        },
                        required=['question']
                    )
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Answers submitted successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'submission_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    }
                )
            ),
            400: "Validation error (e.g., time expired, invalid answer format)"
        }
    )
    def post(self, request, submission_id):
        submission = Submission.objects.get(id=submission_id, student=request.user)
        now = timezone.now()

        if submission.exam.is_timed and now > submission.exam.end_time:
            raise serializers.ValidationError("Submission rejected: Exam time has ended.")

        answers_data = request.data.get('answers', [])
        for answer_data in answers_data:
            serializer = AnswerSerializer(data={
                'submission': submission.id,
                'question': answer_data['question'],
                'answer_text': answer_data.get('answer_text'),
                'answer_file': answer_data.get('answer_file')
            }, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(submission=submission)

        submission.submitted_at = now
        submission.save(update_fields=['submitted_at'])
        return Response({"message": "Answers submitted successfully", "submission_id": submission.id})


__all__ = ['AnswerSubmitView']