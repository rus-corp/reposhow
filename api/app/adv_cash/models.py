import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Валюта")

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"

    def __str__(self) -> str:
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Метод оплаты")
    comission = models.DecimalField(
        max_digits=7, decimal_places=6, verbose_name="Комиссия"
    )
    currency = models.ManyToManyField(Currency, related_name="currencies")

    class Meta:
        verbose_name = "Способ платежа"
        verbose_name_plural = "Способы платежей"

    def __str__(self) -> str:
        return self.name


class PaymentAgregator(models.Model):
    name = models.CharField(
        max_length=150, unique=True, verbose_name="Агрегатор платежа"
    )
    method = models.ManyToManyField(PaymentMethod, related_name="methods")
    account = models.OneToOneField(
        to="accounts.Account",
        on_delete=models.CASCADE,
        related_name="agregator_accounts",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Агрегатор Платежа"
        verbose_name_plural = "Агрегаторы платежей"

    def __str__(self) -> str:
        return self.name


class TinkofPayment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user_acc = models.CharField(max_length=20)
    order_id = models.CharField(max_length=50)
    order_status = models.CharField(max_length=20)
    amount = models.IntegerField()
    description = models.CharField(max_length=150, default="")
    confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Оплата Тинькоф"
        verbose_name_plural = "Оплаты через Тинькоф"

    def __str__(self) -> str:
        return self.order_id


# class Invoice(models.Model):
#     user = models.ForeignKey(to='main_users.CustomUser', on_delete=models.CASCADE, related_name='invoices')
#     text = models.TextField(blank=True)

#     class Meta:
#         verbose_name = 'Счет на оплату'
#         verbose_name_plural = 'Счета на оплату'

#     def __str__(self) -> str:
#         return self.user.user_info.email


class Transaction(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name=_("ID"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("дата создания")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("дата изменения"))
    user = models.ForeignKey(
        "main_users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_transactions",
        verbose_name=_("Пользователь"),
    )
    user_acc = models.ForeignKey(
        "accounts.Account",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="acc_transactions",
        verbose_name=_("Счет"),
    )
    currency = models.CharField(
        max_length=3, null=False, blank=False, verbose_name=_("Валюта")
    )
    amount = models.FloatField(null=False, blank=False, verbose_name=_("Сумма"))
    bank_card = models.CharField(
        max_length=155, null=False, blank=False, verbose_name=_("Номер карты")
    )
    expiry_month = models.IntegerField(
        null=False, blank=False, verbose_name=_("Месяц истечения")
    )
    expiry_year = models.IntegerField(
        null=False, blank=False, verbose_name=_("Год истечения")
    )
    note = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Описание для транзакции")
    )

    def __str__(self):
        return f"{self.user} : {self.user_acc}"

    class Meta:
        db_table = "adv_cash__transactions"
        verbose_name = _("Транзакция вывода на банк счет")
        verbose_name_plural = _("Транзакции вывода на банк счет")
        ordering = ("-created_at",)


class WithdrawalEcurrencyTransaction(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name=_("ID"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("дата создания")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("дата изменения"))
    user = models.ForeignKey(
        "main_users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_ecurrency_transactions",
        verbose_name=_("Пользователь"),
    )
    user_acc = models.ForeignKey(
        "accounts.Account",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="acc_ecurrency_transactions",
        verbose_name=_("Счет"),
    )
    amount = models.FloatField(null=True, blank=True, verbose_name=_("Сумма"))
    cryptoCurrencyAmount = models.FloatField(
        null=True, blank=False, verbose_name=_("Сумма транзакции в криптовалюте")
    )
    currency = models.CharField(
        max_length=5, null=False, blank=False, verbose_name=_("Валюта")
    )
    ecurrency = models.CharField(
        max_length=15, null=False, blank=False, verbose_name=_("Электронная валюта")
    )
    receiver = models.CharField(
        max_length=1024, null=False, blank=False, verbose_name=_("Получатель")
    )
    destinationTag = models.CharField(
        max_length=1024, null=True, blank=True, verbose_name=_("Тег Ripple")
    )
    orderId = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        verbose_name=_("Идентификатор в системе учета пользователя"),
    )
    note = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Описание для транзакции")
    )

    def __str__(self):
        return f"{self.user} : {self.ecurrency}"

    class Meta:
        db_table = "adv_cash__to_crypto_transactions"
        verbose_name = _("Вывод средств в стороннюю платежную систему")
        verbose_name_plural = _("Выводы средств в стороннюю платежную систему")
        ordering = ("-created_at",)


class BlackListTransactionsHash(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name=_("ID"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("дата создания")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("дата изменения"))
    ac_hash = models.CharField(null=False, blank=False, verbose_name=_("Хеш"))

    def __str__(self):
        return f"{self.ac_hash}"

    class Meta:
        db_table = "black_list_transaction_hash"
        verbose_name = _("Черный список хэшей транзакций")
        verbose_name_plural = _("Черный список хэшей транзакций")
        ordering = ("-created_at",)
