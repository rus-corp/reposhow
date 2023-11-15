from django.apps import AppConfig


class VoitingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.voiting'
    verbose_name = 'Голосование'

    def ready(self) -> None:
        import app.voiting.signals
