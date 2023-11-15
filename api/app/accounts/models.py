from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils import timezone


class Account(models.Model):
    """Модель счетов юзеров, фондов"""

    CURRENCY_CHOICES = (
        ("RUB", _("Рубли")),
        ("USD", _("Доллары США")),
        ("EUR", _("Евро")),
    )
    currency = models.CharField(
        _("валюта счета"), max_length=3, choices=CURRENCY_CHOICES, default="RUB"
    )
    account_name = models.CharField(_("Cчёт"), max_length=18, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.account_name

    class Meta:
        verbose_name = _("счёт")
        verbose_name_plural = _("счета")


class Fund(models.Model):
    """Фонды компании"""

    name = models.CharField(
        _("наименование фонда"), max_length=255,
        unique=True
    )
    rub_account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="rub_fund",
        blank=True,
        verbose_name=_("Счет RUB"),
    )
    usd_account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="usd_fund",
        blank=True,
        verbose_name=_("Счет USD"),
    )
    eur_account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="eur_fund",
        blank=True,
        verbose_name=_("Счет EUR"),
    )

    def get_rub_balance(self):
        return self.rub_account.balance

    get_rub_balance.short_description = "Баланс RUB"

    def get_usd_balance(self):
        return self.usd_account.balance

    get_usd_balance.short_description = "Баланс USD"

    def get_eur_balance(self):
        return self.eur_account.balance

    get_eur_balance.short_description = "Баланс EUR"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("фонд")
        verbose_name_plural = _("фонды")


class Operation(models.Model):
    """Операции по счетам с назначенями платежей"""

    class Currency_Choises(models.TextChoices):
        RUB = "RUB", "RUB"
        USD = "USD", "USD"

    currency = models.CharField(
        _("валюта операции"),
        max_length=3,
        choices=Currency_Choises.choices,
        default="RUB",
    )
    purpose_of_payment = models.CharField(
        _("назначение платежа"), max_length=100
    )
    value = models.DecimalField(_("сумма"), max_digits=10, decimal_places=2)
    from_account = models.ForeignKey(
        Account,
        related_name="from_acc",
        on_delete=models.PROTECT,
        verbose_name=_("счёт списания"),
    )
    to_account = models.ForeignKey(
        Account,
        related_name="to_acc",
        on_delete=models.PROTECT,
        verbose_name=_("счёт зачисления"),
    )
    time_operation = models.DateTimeField(_("время операции"), auto_now_add=True)

    class Meta:
        ordering = ("-time_operation",)
        verbose_name = _("транзакция")
        verbose_name_plural = _("транзакции")

    def __str__(self) -> str:
        return f"{self.purpose_of_payment}: from - {self.from_account} to - {self.to_account}"
