from django.contrib import admin

from .models import (
    Currency,
    PaymentAgregator,
    PaymentMethod,
    TinkofPayment,
    Transaction,
    WithdrawalEcurrencyTransaction,
    BlackListTransactionsHash
)


@admin.register(TinkofPayment)
class TinkofPaymentAdmin(admin.ModelAdmin):
    list_display = ["user_acc", "amount"]
    list_display_links = ["user_acc", "amount"]


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "comission",
    ]
    filter_horizontal = ("currency",)


@admin.register(PaymentAgregator)
class PaymentAgregatorAdmin(admin.ModelAdmin):
    list_display = ["name", "account"]
    filter_horizontal = ("method",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["user", "user_acc", "currency", "amount"]
    search_fields = ["user", "bank_card", "note", "amount"]
    readonly_fields = [
        "created_at",
        "updated_at",
        "id",
    ]
    ordering = ["-created_at"]
    list_per_page = 25
    list_filter = ["user", "user_acc", "currency", "created_at", "updated_at"]
    fields = [
        "user",
        "user_acc",
        "currency",
        "amount",
        "bank_card",
        "expiry_month",
        "expiry_year",
        "note",
        "created_at",
        "updated_at",
    ]


@admin.register(WithdrawalEcurrencyTransaction)
class EcurrencyTransactionAdmin(admin.ModelAdmin):
    list_display = ["user", "amount", "currency", "cryptoCurrencyAmount", "ecurrency"]
    search_fields = [
        "user",
        "currency",
        "ecurrency",
        "receiver",
        "note",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
        "id",
    ]
    ordering = ["-created_at"]
    list_per_page = 25
    list_filter = ["user", "currency", "ecurrency", "created_at", "updated_at"]
    fields = [
        "user",
        "user_acc",
        "amount",
        "cryptoCurrencyAmount",
        "currency",
        "ecurrency",
        "receiver",
        "destinationTag",
        "orderId",
        "note",
        "created_at",
        "updated_at",
    ]


@admin.register(BlackListTransactionsHash)
class BlackListTransactionsHashAdmin(admin.ModelAdmin):
    list_display = ["ac_hash", "created_at", "updated_at"]
    search_fields = [
        "ac_hash",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
        "id",
    ]
    ordering = ["-created_at"]
    list_per_page = 25
    list_filter = ["created_at", "updated_at"]
    fields = [
        "ac_hash",
        "created_at",
        "updated_at",
    ]