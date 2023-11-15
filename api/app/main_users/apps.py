from django.apps import AppConfig


class MainUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.main_users'
    verbose_name = 'Пользователи'

    def ready(self) -> None:
        import app.main_users.signals
