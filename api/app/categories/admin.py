from django.contrib import admin

from .models import Activity, Category, Specialization


class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'activity']
    prepopulated_fields = {"slug": ("name",)}

class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']
    prepopulated_fields = {"slug": ("name",)}



admin.site.register(Activity, ActivityAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Specialization, SpecializationAdmin)
