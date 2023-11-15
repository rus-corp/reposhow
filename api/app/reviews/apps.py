from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.reviews'
    verbose_name = "Отызвы о пользователе"

    def ready(self):
        import app.reviews.signals