from django.urls import path

from common.views import *

app_name = "common"
urlpatterns = [
    # path('assign-exam/<int:exam_id>/', AssignStudentExam.as_view(), name='assign_exam'),
    # path('exams/<int:exam_id>/assign-students/', AssignStudentsView.as_view(), name='assign-students'),
    path('exams/<int:exam_id>/students/', AssignCreate.as_view(), name='assigned-students'),
    path("listsubject", ListSubjectView.as_view(), name="list-subject"),
    path("create_subjects/", CreateSubjects.as_view(), name="subkect-create"),
    path("Update-subject/<int:pk>", UpdateSubjects.as_view(), name="subject"),
    path("DeleteSubject/<int:pk>", DeleteSubject.as_view(), name="delete-subject"),
    path("ExamineCreate/<int:pk>/", ExamineCreate.as_view(), name="examine-create"),
    path("ExamineDelete/<int:pk>", ExamineDelete.as_view(), name="examine_delete"),
    path("ExamineUpdate/<int:pk>", ExamineUpdate.as_view(), name="ExamineUpdate"),
    path("ListExamine", ListExamine.as_view(), name="list-examine"),
    # talabalarni tayinlash imtihonga
    path("AssignCreate/<int:exam_id>", AssignCreate.as_view(), name="assign_create"),
    path("AssignMentStudent", AssignMentStudent.as_view(), name="list"),
    # test options
    # path("SubmitTest/<int:id>/", SubmitTestView.as_view(), name="submit"),
    path("SubmitAnswer/<int:exam_id>/", SubmitTestView.as_view(), name="submit_answer"),
    # path("QuestionDetail/<int:pk>/", QuestionDetail.as_view(), name="question"),
    path('api/reports/exams', ExamReportsView.as_view(), name='exam-reports'),
    # path('api/reports/eksam/', ExamineResultViewSet.as_view({'get': 'list'}), name='exam-results-list'),
    path('results/pdf/', GeneratePdf.as_view(), name='generate_pdf'),

]
