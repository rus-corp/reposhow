from django.core.management import BaseCommand
from django.template.loader import render_to_string

from app.mails.models import Notification
from app.mails.utils import _send_email


class Command(BaseCommand):
    """Команда уведомлений откликов на заказы."""

    help = 'Sends orders notifications'

    def handle(self, *args, **kwargs):
        instances = Notification.objects.filter(
            type_of_notifications='fr_responses'
        )
        for row in instances:
            _send_email(
                subject=row.title,
                recipients=[row.email],
                html_content=render_to_string(
                    f'{row.template_link}',
                    context=row.context,
                )
            )
        instances.delete()
