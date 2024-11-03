from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "common"
    label = 'common_app'  # Yana bir noyob nom bering

    def ready(self):
        import common.signals
