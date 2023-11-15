from django.apps import AppConfig


class UserDocsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.user_docs'
    verbose_name = 'Документы пользователя'