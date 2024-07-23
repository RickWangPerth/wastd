from django.apps import AppConfig


class Wamtram2Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wamtram2"
    def ready(self):
        from wamtram2.utils import initialize_signals
        initialize_signals()
