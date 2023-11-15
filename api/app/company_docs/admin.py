from django.contrib import admin

from .models import Company_Doc, ReferalLink


class CompanyDocAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'desc', 'slug', "is_private"]
    prepopulated_fields = {'slug': ('name',)}



class ReferalLinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'specialization']



admin.site.register(Company_Doc, CompanyDocAdmin)
admin.site.register(ReferalLink, ReferalLinkAdmin)