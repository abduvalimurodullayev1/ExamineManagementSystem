from modeltranslation.translator import TranslationOptions, register
from apps.exam import models

@register(models.Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('body', 'correct_answer', 'options')
