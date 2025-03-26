from django.apps import AppConfig


class ExamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.exam'
    verbose_name = "Exam"


    def ready(self):
        import apps.exam.signals
