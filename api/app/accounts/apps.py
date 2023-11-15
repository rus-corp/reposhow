from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.accounts'
    verbose_name = 'Счета'

    def ready(self):
        import app.accounts.signals