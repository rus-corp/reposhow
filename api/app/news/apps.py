from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.news'
    verbose_name = 'Новости'

    def ready(self):
        import app.news.signals
