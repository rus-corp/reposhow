from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import Fund, Account, Operation



class FundAdmin(admin.ModelAdmin):
    list_display = ['id',"name", "rub_account", "usd_account", 'eur_account', 'get_rub_balance', 'get_usd_balance', 'get_eur_balance']
    readonly_fields = ['rub_balance', 'usd_balance', 'eur_balance']
    list_display_links = ['name']
    
    def rub_balance(self, obj):
        return obj.rub_account.balance
    
    rub_balance.short_description = _("Баланс счета RUB")
    
    def usd_balance(self, obj):
        return obj.usd_account.balance
    
    usd_balance.short_description = _("Баланс счета USD")
    
    def eur_balance(self, obj):
        return obj.eur_account.balance
    
    eur_balance.short_description = _("Баланс счета EUR")
    
    
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_name', 'currency', 'balance',]
    search_fields = ['account_name']
    list_display_links = ['account_name']

    # def has_add_permission(self, request: HttpRequest) -> bool:
    #     return False
    # def has_change_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
    #     return False


class OperationAdmin(admin.ModelAdmin):
    list_display = (
        "purpose_of_payment",
        "value",
        "from_account",
        "to_account",
        "time_operation",
    )


admin.site.register(Fund, FundAdmin)
admin.site.register(Operation, OperationAdmin)