from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField


User = get_user_model()


class UserMailPermissions(models.Model):
    """Класс управления уведомлениями пользователя."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mails',
        verbose_name='Пользователь:',
        help_text='выберите подходящего пользователя'
    )
    account_refill = models.BooleanField(
        'Увед. о пополнении аккаунта:',
        default=False
    )
    customers_offers = models.BooleanField(
        'Увед. о предложениях заказчиков:',
        default=False
    )
    freelancers_responses = models.BooleanField(
        'Увед. об откликах заказчиков:',
        default=False
    )
    reviews = models.BooleanField(
        'Увед. об отзывах:',
        default=False
    )
    votes = models.BooleanField(
        'Увед. о голосованиях:',
        default=False
    )
    chat = models.BooleanField(
        'Увед. о пополнении аккаунта:',
        default=False
    )
    news = models.BooleanField(
        'Увед. о пополнении аккаунта:',
        default=False
    )


class Notification(models.Model):
    """Модель уведомлений, с разными типами (3.10)."""

    class Types(models.TextChoices):
        CHAT = 'chat', 'chat'
        NEWS = 'news', 'news'
        VOTES = 'votes', 'votes'
        REVIEWS = 'reviews', 'reviews'
        FR_RESPONSES = 'fr_responses', 'Responses from freelancers'
        CS_RESPONSES = 'cs_responses', 'Responses from customers'
        REFILL = 'refill', 'Account refill'

    class ExtraTypes(models.TextChoices):
        FOR_FREELANCERS = 'for_freelancers', 'News for freelancers'
        FOR_CUSTOMERS = 'for_customers', 'News for customers'
        FOR_FOUNDERS = 'for_founders', 'News for founders'
        FOR_ALL = 'for_all', 'News for all'

    email = models.EmailField(
        'Почта адресата:',
        blank=True, null=True
    )
    type_of_notifications = models.CharField(
        'Тип уведомлений:',
        choices=Types.choices
    )
    template_link = models.TextField(
        'Шаблон для отправки сообщения:',
        max_length=100
    )
    context = models.JSONField(
        'Контекст для темплейта:',
        blank=True, null=True
    )
    title = models.TextField(
        'Тема сообщения:',
        max_length=150
    )
    extra_classification = models.CharField(
        'Дополнительные параметры для уведомлений:',
        null=True, blank=True, choices=ExtraTypes.choices
    )
