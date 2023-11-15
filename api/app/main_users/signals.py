import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from app.main_users.models import CustomUser
from app.raiting.models import Rating


log = logging.getLogger()


@receiver(post_save, sender=CustomUser)
def create_rating(sender, instance, created, **kwargs):
    try:
        Rating.objects.get_or_create(
            freelancer=instance
        )
    except Exception as e:
        log.error(e)
