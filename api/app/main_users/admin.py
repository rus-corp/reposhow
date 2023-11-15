from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, UserInfo, UserSpecialization, UserInfoCompany


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "email_confirm",
        "status",
        "date_joined",
        'paid_entrance_rub',
        'paid_entrance_usd',
    )
    exclude = ['first_name', 'last_name']
    list_display_links = ['id', 'email']
    list_filter = (
        "date_joined",
        "is_active",
        "email_confirm",
        "status",
    )
    search_fields = (
        "id",
        "email",
        "parent__last_name",
        "parent__email",
        "personal_number",
    )
    readonly_fields = [
        "date_joined",
        'get_account_rub_number',
        'get_account_usd_number',
        'get_account_eur_number',
        "get_referrals",
        "referal_link",
        "parent",
        'get_referals_emails',
        'slug'
    ]
    save_on_top = True
    actions = [
        "make_inactive",
        "paid_entrance_fee",
        "paid_entrance_fee_usd",
    ]


    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive.short_description = _("деактивировать")
    
    def get_account_rub_number(self, obj):
        if obj.rub_acc:
            return obj.rub_acc.balance
        else:
            return ""
        
    get_account_rub_number.short_description = _("Баланс счета RUB")

    def get_account_usd_number(self, obj):
        if obj.usd_acc:
            return obj.usd_acc.balance
        else:
            return ""
        
    get_account_usd_number.short_description = _("Баланс счета USD")
    
    def get_account_eur_number(self, obj):
        if obj.eur_acc:
            return obj.eur_acc.balance
        else:
            return ""
        
    get_account_eur_number.short_description = _("Баланс счета EUR")
    
    
    def get_referrals(self, obj):
        referrals = obj.referals
        return (
            f"1 level: {referrals.get('level1').count()}\n"
            f"2 level: {referrals.get('level2').count()}\n"
            f"3 level: {referrals.get('level3').count()}"
        )

    get_referrals.short_description = _("рефералы")
    
    def get_referals_emails(self, obj):
        level1 = CustomUser.objects.filter(parent=obj)
        level2 = CustomUser.objects.filter(parent__in=level1)
        level3 = CustomUser.objects.filter(parent__in=level2)
        
        level1_emails = [user.email for user in level1]
        level2_emails = [user.email for user in level2]
        level3_emails = [user.email for user in level3]
        
        return f"Level 1: {', '.join(level1_emails)}\nLevel 2: {', '.join(level2_emails)}\nLevel 3: {', '.join(level3_emails)}"

    get_referals_emails.short_description = 'Рефералы'


class UserinfoAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'father_name', 'on_vacation',]

class UserInfoCompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'short_company_name', 'ceo_name']
          

class UserSpecializationAdmin(admin.ModelAdmin):
    list_display = ['get_user', 'specialization']


# @admin.register(EmailToken)
# class EmailTokenAdmin(admin.ModelAdmin):
#     list_display = ['user', 'key']


admin.site.register(UserInfo, UserinfoAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserInfoCompany, UserInfoCompanyAdmin)
admin.site.register(UserSpecialization, UserSpecializationAdmin)
