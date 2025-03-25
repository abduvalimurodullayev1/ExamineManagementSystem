from modeltranslation.translator import TranslationOptions, register
from apps.notification import models


@register(models.Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'text')

