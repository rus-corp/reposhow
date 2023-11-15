from django.db import models
from django.utils.translation import gettext_lazy as _


class Review(models.Model):

    class Status(models.TextChoices):
        POSITIVE = 'PT', 'Positive'
        NEGATIVE = 'NT', 'Negative'

    description = models.TextField(max_length=500)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.POSITIVE)

    order = models.ForeignKey(to='orders.Order', on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(to='main_users.CustomUser', verbose_name= _('Заказчик'), on_delete=models.CASCADE, related_name='review_customer')
    executor = models.ForeignKey(to='main_users.CustomUser', verbose_name= _('Исполнитель'), on_delete=models.CASCADE, related_name='review_executor')

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')
