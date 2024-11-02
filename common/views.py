import redis
from django.db.models import Sum, Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from common.models import *
from common.send_notification import send_exam_notification
from common.serializers import SubjectSerializer, ExamineSerializer, AssignStudentsSerializer, SubmissionSerializer, \
    ExamResultSerializer, TestSubmissionSerializer
import logging
from weasyprint import HTML
from common.tasks import send_push_notification

logger = logging.getLogger(__name__)

redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


# Redis serverining sog‘ligini tekshiruvchi API
@api_view(["GET"])
def health_check_redis(request):
    try:
        redis_client.ping()
        return Response({"status": "success"}, status=status.HTTP_200_OK)
    except redis.ConnectionError:
        return Response(
            {"status": "error", "message": "Redis server ishlamayapti."},
            status=status.HTTP_400_BAD_REQUEST,
        )


# Subject modeliga oid API'lar
class ListSubjectView(ListAPIView):
    serializer_class = SubjectSerializer
    queryset = Subjects.objects.all()
    permission_classes = [IsAuthenticated]


class CreateSubjects(CreateAPIView):
    serializer_class = SubjectSerializer
    queryset = Subjects.objects.all()
    permission_classes = [IsAdminUser]


class UpdateSubjects(UpdateAPIView):
    serializer_class = SubjectSerializer
    queryset = Subjects.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = "pk"


class DeleteSubject(DestroyAPIView):
    serializer_class = SubjectSerializer
    queryset = Subjects.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = "pk"


class ExamineCreate(CreateAPIView):
    serializer_class = ExamineSerializer
    queryset = Examine.objects.all()
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        exam = serializer.save()

        users = User.objects.filter(is_active=True)
        for user in users:
            if hasattr(user, 'device_token') and user.device_token:
                send_push_notification.delay(
                    user_id=user.id,
                    device_token=user.device_token,
                    title="Yangi imtihon tayinlandi!",
                    message=f"Siz {exam.title} imtihoniga tayinlandingiz."
                )


class ExamineDelete(DestroyAPIView):
    serializer_class = ExamineSerializer
    queryset = Examine.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = "pk"


class ExamineUpdate(UpdateAPIView):
    serializer_class = ExamineSerializer
    queryset = Examine.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = "pk"


class ListExamine(ListAPIView):
    serializer_class = ExamineSerializer
    queryset = Examine.objects.all()
    permission_classes = [IsAuthenticated]


class AssignCreate(APIView):
    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: "Yaratildi",
            status.HTTP_400_BAD_REQUEST: "Xatolik mavjud"
        },
        request_body=AssignStudentsSerializer
    )
    def post(self, request, exam_id):
        exam = get_object_or_404(Examine, id=exam_id)
        serializer = AssignStudentsSerializer(data=request.data, context={"exam": exam})

        if serializer.is_valid():
            serializer.save()
            for student in exam.assigned_users.all():
                send_exam_notification(student, exam)  # O'zgartirish kiritildi
            return Response({"message": "Talabalar muvaffaqiyatli tayinlandi"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignMentStudent(ListAPIView):
    serializer_class = AssignStudentsSerializer
    queryset = Assignment.objects.all()
    permission_classes = [IsAdminUser]


class SubmitTestView(APIView):
    @swagger_auto_schema(
        request_body=TestSubmissionSerializer,
        responses={201: "Test muvaffaqiyatli topshirildi."}
    )
    def post(self, request, exam_id):
        exam = get_object_or_404(Examine, id=exam_id)

        if not exam.assigned_users.filter(id=request.user.id).exists():
            return Response(
                {"error": "Siz tayinlanmagansiz."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            serializer = TestSubmissionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = request.user
            total_questions = exam.question_count
            correct_answers_count = 0

            for answer in serializer.validated_data['answers']:
                question_id = answer['question_id']
                selected_answer = answer['answer']

                if Submission.objects.filter(student=user, exam=exam, question__id=question_id).exists():
                    return Response({"error": f"Savol {question_id} ga allaqachon javob berilgan."},
                                    status=status.HTTP_400_BAD_REQUEST)

                question = get_object_or_404(Question, id=question_id, subject=exam.subjects)
                is_correct = question.correct_answer == selected_answer

                Submission.objects.create(
                    student=user,
                    exam=exam,
                    question=question,
                    answer=selected_answer,
                    is_correct=is_correct
                )

                if is_correct:
                    correct_answers_count += 1

            correct_percentage = (correct_answers_count / total_questions) * 100 if total_questions > 0 else 0

            ExamResult.objects.create(
                student=user,
                exam=exam,
                score=correct_percentage,
                passed=correct_percentage >= exam.passing_percentage
            )

            return Response({
                "message": "Keyingi savolga o'ting",
                "correct_percentage": correct_percentage
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error in SubmitTestView: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ExamReportsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        exam_results = ExamResult.objects.all()
        serializer = ExamResultSerializer(exam_results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        student = get_object_or_404(User, id=student_id)

        if request.user != student and not request.user.is_staff:
            return Response(
                {"error": "Siz faqat o'z natijalaringizni ko'rishingiz mumkin."},
                status=status.HTTP_403_FORBIDDEN
            )

        exam_results = ExamResult.objects.filter(student=student)
        serializer = ExamResultSerializer(exam_results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from django.db.models import Sum, Count


@method_decorator(csrf_exempt, name='dispatch')
class GeneratePdf(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = ExamResult.objects.filter(student=request.user) \
            .values('exam__exam_name') \
            .annotate(total_score=Sum('score')) \
            .annotate(passed_count=Count('passed', filter=Q(passed=True)))

        if not results:
            return Response("Topilmadi", status=status.HTTP_404_NOT_FOUND)

        html_content = render_to_string('result.html', {'results': results})

        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="exam_results.pdf"'
        return response