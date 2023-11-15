from django.db.models.signals import post_save
from django.dispatch import receiver

from app.reviews.models import Review
from app.mails.models import Notification


@receiver(post_save, sender=Review)
def create_notification(sender, instance, created, **kwargs):
    Notification.objects.create(
        title="You've got a new Review!",
        type_of_notifications='reviews',
        template_link='mails/reviews.html',
        context={'link': None},
        email=instance.executor.email
    )
    return
