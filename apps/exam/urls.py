from apps.exam.api_endpoints.exam_create.views import ExamCreateView
# from apps.exam.api_endpoints.list_exam.views import



from django.urls import path

app_name = "exam"

urlpatterns = [
    path("create/", ExamCreateView.as_view(), name="exam_create"),
]