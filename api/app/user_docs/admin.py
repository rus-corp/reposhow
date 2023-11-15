from django.contrib import admin

from .models import UserDoc, BankAccount, Country, Region, Contract


class UserDocsAdmin(admin.ModelAdmin):
    list_display = ['get_user', 'personal_number', 'document_name', 'document_number','document_issued']
    


class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['get_user', 'bank_name', 'bank_address', 'bank_bic', 'bank_correspondent_account', 'payment_account', 'recipients_name']
    

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone_code', 'region']



@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['user',]

admin.site.register(UserDoc, UserDocsAdmin)
admin.site.register(BankAccount, BankAccountAdmin)
