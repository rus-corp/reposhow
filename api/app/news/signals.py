from django.db.models.signals import post_save
from django.dispatch import receiver

from app.news.models import News
from app.mails.models import Notification


@receiver(post_save, sender=News)
def create_notification(sender, instance, created, **kwargs):
    Notification.objects.create(
        title='Click-News!',
        type_of_notifications='news',
        template_link='mails/News.html',
        context={'link': 'http://127.0.0.1:8000/'},
    )
    return
