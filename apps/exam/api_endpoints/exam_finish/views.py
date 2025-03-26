from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.exam.models import Exam
from apps.exam.api_endpoints.exam_finish.serializers import ExamFinishEarlySerializer
from apps.exam.permissions import IsTeacher


class ExamFinishEarlyView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    @swagger_auto_schema(
        request_body=ExamFinishEarlySerializer,
        responses={200: ExamFinishEarlySerializer}
    )
    def post(self, request, id):
        try:
            exam = Exam.objects.get(id=id)
            exam.finish_early(request.user)
            serializer = ExamFinishEarlySerializer(exam)
            return Response(serializer.data)
        except Exam.DoesNotExist:
            return Response({"error": "Exam not found"}, status=404)
