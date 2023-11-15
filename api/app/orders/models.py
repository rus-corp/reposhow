from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from transliterate import translit
from django.utils.text import slugify


from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


from app.portfolio.validators import file_size_validate
from app.user_docs.models import Country


User = get_user_model()


class OrderManager(models.Manager):
    """Фильтр опубликованных заказов"""

    def get_queryset(self):
        return super().get_queryset().filter(status=Order.OrderStatus.PUBLISHED)


class Order(models.Model):
    """Модель заказа, его статус и валюта"""

    class OrderStatus(models.TextChoices):
        MODERATION = "MD", "Moderation"  # на модерации
        PUBLISHED = (
            "PB",
            "Published",
        )  # опубликованный
        ACCEPTED = (
            "AC",
            "Accepted",
        )  # подтвержденный исполнитель
        ON_EXECUTION = "OE", "On_Execution"  # на исполнении
        ON_ACCEPTED = "OA", "On_Accepted"  # на приемке
        COMPLETED = "CP", "Comleted"  # исполненный

    class CURRENCY_CHOICES(models.TextChoices):
        RUB = "RUB", "RUB"
        USD = "USD", "USD"

    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.PositiveIntegerField(
        default=0, blank=True, null=True
    )
    currency = models.CharField(
        _("валюта цены заказа"),
        max_length=3,
        choices=CURRENCY_CHOICES.choices,
        default=CURRENCY_CHOICES.RUB,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    period = models.DateField(_("Срок выполнения"), blank=True, null=True)

    specialization = models.ForeignKey(
        to="categories.Specialization",
        on_delete=models.PROTECT,
        related_name="order_specializations",
    )
    country = models.ManyToManyField(Country, related_name="countries", blank=True)

    slug = models.SlugField(max_length=255)
    views = models.IntegerField(default=0)
    target_audience = models.TextField(
        _("Целевая аудитория"), blank=True, max_length=300
    )
    atention = models.TextField(_("Обратить внимание"), max_length=300, blank=True)

    # активность заказа
    status = models.CharField(
        max_length=2, choices=OrderStatus.choices, default=OrderStatus.MODERATION
    )
    # заказчик
    customer = models.ForeignKey(
        User,
        verbose_name=_("Заказчик"),
        on_delete=models.CASCADE,
        related_name="order_customers",
    )
    # исполнитель
    executor = models.ManyToManyField(User, through="OrderResponse", blank=True)

    rub_acc = models.OneToOneField(
        to="accounts.Account", on_delete=models.CASCADE, related_name="order_rub_acc"
    )
    usd_acc = models.OneToOneField(
        to="accounts.Account", on_delete=models.CASCADE, related_name="order_usd_acc"
    )
    eur_acc = models.OneToOneField(
        to="accounts.Account", on_delete=models.CASCADE, related_name="order_eur_acc"
    )

    file1 = models.FileField(
        upload_to="order_files/%Y/%m/%d",
        blank=True,
        null=True,
        validators=[file_size_validate],
    )
    file2 = models.FileField(
        upload_to="order_files/%Y/%m/%d",
        blank=True,
        null=True,
        validators=[file_size_validate],
    )
    file3 = models.FileField(
        upload_to="order_files/%Y/%m/%d",
        blank=True,
        null=True,
        validators=[file_size_validate],
    )

    objects = models.Manager()
    published = OrderManager()

    class Meta:
        verbose_name = _("заказ")
        verbose_name_plural = _("заказы")
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name

    def change_executor_status(self, executor, new_status):
        try:
            executor_entry = self.order_responses.get(executor=executor)
            executor_entry.executor_status = new_status
            executor_entry.save()
        except:
            OrderResponse.objects.create(order=self, executor=executor)


class OrderResponse(models.Model):
    """Кандидат и в дальнейшем исполнитель заказа"""

    class ExecutorStatus(models.TextChoices):
        NO_STATUS = "NS", "No_Status"
        CANDIDATE = "CN", "Candidate"
        EXECUTOR = "EX", "Executor"

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_responses"
    )
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="order_responses"
    )
    executor_status = models.CharField(
        max_length=2, choices=ExecutorStatus.choices, default=ExecutorStatus.NO_STATUS
    )
    text = models.TextField(
        max_length=500, verbose_name=_("Текст отклика"), blank=True, null=True
    )
    price = models.DecimalField(
        _("Стоимость выполнения"),
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
    )
    term = models.DateField(_("Срок выполнения"), blank=True, null=True)
    created_at = models.DateTimeField(_("Дата отклика"), auto_now_add=True)

    file1 = models.FileField(
        upload_to="order_responses/%Y/%m/%d",
        blank=True,
        null=True,
        verbose_name=_("Файл1"),
    )
    file2 = models.FileField(
        upload_to="order_responses/%Y/%m/%d",
        blank=True,
        null=True,
        verbose_name=_("Файл2"),
    )
    file3 = models.FileField(
        upload_to="order_responses/%Y/%m/%d",
        blank=True,
        null=True,
        verbose_name=_("Файл3"),
    )

    class Meta:
        verbose_name = "Отклик на заказ"
        verbose_name_plural = "Отклики на заказ"

    def __str__(self):
        return f"Задача {self.order},  откликнулся {self.executor}" 


class OrderResponseComment(MPTTModel):
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    order_response = models.ForeignKey(
        OrderResponse,
        on_delete=models.CASCADE,
        related_name="order_response_comments",
        verbose_name=_("Отклик"),
    )
    user = models.ForeignKey(
        to="main_users.CustomUser",
        on_delete=models.PROTECT,
        related_name="order_response_comments",
        verbose_name=_("Оставил комметарий"),
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="replies",
        blank=True,
        null=True,
        verbose_name=_("родитель комментария"),
    )
    file1 = models.FileField(
        upload_to="order_response_comments/%Y/%m/%d",
        blank=True,
        null=True,
        verbose_name=_("Файл1"),
    )
    file2 = models.FileField(
        upload_to="order_response_comments/%Y/%m/%d",
        blank=True,
        null=True,
        verbose_name=_("Файл2"),
    )
    file3 = models.FileField(
        upload_to="order_response_comments/%Y/%m/%d",
        blank=True,
        null=True,
        verbose_name=_("Файл3"),
    )

    class Meta:
        verbose_name = 'Комментарий к отклику'
        verbose_name_plural = 'Комментарии к откликам'

    def __str__(self) -> str:
        return f"{self.order_response}, комментарий {self.user}"
