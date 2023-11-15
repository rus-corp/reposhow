from django.core.management import BaseCommand
from django.template.loader import render_to_string

from app.mails.models import Notification
from app.mails.utils import _send_email
from app.main_users.models import CustomUser


class Command(BaseCommand):
    """Команда делающая рассылку новостей."""

    help = "Send all news to its auditory"

    def handle(self, *args, **kwargs):
        all_news = Notification.objects.filter(type_of_notifications="news")
        users = CustomUser.objects.filter(mails__news=True)
        emails = list(user.email for user in users)
        if len(all_news) > 0:
            for row in all_news:
                _send_email(
                    subject=row.title,
                    html_content=render_to_string(
                        f"{row.template_link}", context=row.context
                    ),
                    recipients=emails,
                )
        all_news.delete()
