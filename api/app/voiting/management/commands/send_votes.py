from django.core.management import BaseCommand
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from app.mails.models import Notification
from app.mails.utils import _send_email


User = get_user_model()


class Command(BaseCommand):
    """Команда для расслыки уведомлений об голосованиях."""

    help = 'Send notifications about new votes to users.'

    def handle(self, *args, **kwargs):
        news = Notification.objects.filter(type_of_notifications='votes')
        users = User.objects.filter(mails__news=True)
        emails = list(user.email for user in users)
        if len(news) > 0:
            for row in news:
                _send_email(
                    subject=row.title,
                    html_content=render_to_string(
                        f"{row.template_link}", context=row.context
                    ),
                    recipients=emails
                )
        news.delete()
