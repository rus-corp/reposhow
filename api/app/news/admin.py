from django.contrib import admin

from .models import News, UserViews

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'for_all', 'for_freelancers', 'for_customers', 'for_founders']
    list_filter = ['created']
    search_fields = ['for_all', 'for_freelancers', 'for_customers', 'for_founders']
    date_hierarchy = 'created'
    prepopulated_fields = {'slug': ('title',), }
    
@admin.register(UserViews)
class UserViewsAdmin(admin.ModelAdmin):
    list_display = ("user", "news", "created")
    list_display_links = ("user", "news")
    readonly_fields = ("user", "news", "created")