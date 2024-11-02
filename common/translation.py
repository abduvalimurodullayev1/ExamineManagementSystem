from modeltranslation.translator import register, TranslationOptions
from common.models import Subjects, Examine, Question, Assignment, Submission, Notification, ExamResult


@register(Subjects)
class SubjectTranslation(TranslationOptions):
    fields = ('title', 'description', 'active')


@register(Examine)
class ExamineTranslation(TranslationOptions):
    fields = ('exam_name', 'active')


@register(Question)
class QuestionTranslation(TranslationOptions):
    fields = ('body', 'correct_answer', 'options', 'type')


@register(Assignment)
class AssignmentTranslation(TranslationOptions):
    fields = ('completed',)


@register(Submission)
class SubmissionTranslation(TranslationOptions):
    fields = ('answer',)


@register(Notification)
class NotificationTranslation(TranslationOptions):
    fields = ('message', 'is_read')


@register(ExamResult)
class ExamResultTranslation(TranslationOptions):
    fields = ('score', 'passed')
