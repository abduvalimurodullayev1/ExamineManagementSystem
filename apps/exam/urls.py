from apps.exam.api_endpoints.exam_create.views import ExamCreateView
# from apps.exam.api_endpoints.list_exam.views import


from django.urls import path

from apps.exam.api_endpoints.exam_delete.views import ExamDeleteApiView
from apps.exam.api_endpoints.exam_early.views import ExamFinishEarlyView
from apps.exam.api_endpoints.exam_sts.views import ExamStatsView
from apps.exam.api_endpoints.exam_update.views import ExamUpdateView
from apps.exam.api_endpoints.list_exam.views import ListExamView

app_name = "exam"

urlpatterns = [
    path("create/", ExamCreateView.as_view(), name="exam_create"),
    path("list/", ListExamView.as_view(), name="exam_list"),
    path("ExamDelete/<int:pk>/", ExamDeleteApiView.as_view(), name="exam_delete"),
    path("ExamFinishEarlyView/", ExamFinishEarlyView.as_view(), name="exam_finish_early"),
    path("ExamStatsView/<int:id>/", ExamStatsView.as_view(), name="exam_stats"),
    path("ExamUpdateView/<int:id>/", ExamUpdateView.as_view(), name="exam_update"),

]
