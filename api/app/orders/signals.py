from django.db.models.signals import post_save
from django.dispatch import receiver

from app.mails.models import Notification
from app.orders.models import OrderResponse


@receiver(post_save, sender=OrderResponse)
def create_notification(sender, instance, created, **kwargs):
    Notification.objects.create(
        title="You've got a new response on your order",
        template_link='mails/Performer_response_to_the_order.html',
        context={},
        email=instance.order.customer.email,
        type_of_notifications='fr_responses'
    )
    return
