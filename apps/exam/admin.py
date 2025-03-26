
from django.contrib import admin

from apps.exam.models import *


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('subject', 'start_time', 'duration', 'status')
    list_filter = ('subject', 'status')
    search_fields = ('subject__title',)



@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('body', 'subject', 'type')
    list_filter = ('subject', 'type')
    search_fields = ('body', 'subject__title')

    def save_model(self, request, obj, form, change):
        obj.clean()
        super().save_model(request, obj, form, change)


@admin.register(QuestionScore)
class QuestionScoreAdmin(admin.ModelAdmin):
    list_display = ('question', 'score')
    list_filter = ('question', 'score', 'order')
    search_fields = ('question__body', 'question__subject__title')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'score', 'status')
    list_filter = ('student', 'exam', 'status')
    search_fields = ('student__username', 'exam__subject__title')


@admin.register(ExamGroup)
class ExamGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name', )
    search_fields = ('name', )


@admin.register(ExamStatistics)
class ExamStatisticsAdmin(admin.ModelAdmin):
    list_display = ( 'highest_score', 'lowest_score', 'average_score', 'participants')
    list_filter = ('participants', 'average_score', 'highest_score', 'lowest_score')
    search_fields = ('exam__subject__title', )



