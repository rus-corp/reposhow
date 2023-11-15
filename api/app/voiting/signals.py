from django.db.models.signals import post_save
from django.dispatch import receiver

from app.mails.models import Notification
from app.voiting.models import Question


@receiver(post_save, sender=Question)
def create_notification(sender, instance, created, **kwargs):
    Notification.objects.create(
        type_of_notifications='votes',
        template_link='mails/Voting.html',
        context={},
        title='New voting started!',
    )
