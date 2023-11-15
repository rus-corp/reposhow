from django.core.management import BaseCommand
from django.template.loader import render_to_string

from app.mails.models import Notification
from app.mails.utils import _send_email


class Command(BaseCommand):
    """Команда для расслки уведомлений о отзывах. """

    help = 'Sends notifications about new review to user'

    def handle(self, *args, **kwargs):
        notifications = Notification.objects.filter(type_of_notifications='reviews')
        if len(notifications) > 0:
            for row in notifications:
                _send_email(
                    subject=row.title,
                    html_content=render_to_string(
                        f'{row.template_link}',
                        context=row.context
                    ),
                    recipients=[row.email]
                )
        notifications.delete()
