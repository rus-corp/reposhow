from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest


from .models import Order, OrderResponse, OrderResponseComment

class OrderExecutorInline(admin.TabularInline):
    model = OrderResponse


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "description",
        "price",
        "currency",
        "created_at",
        "status",
        "customer",
        'period',
    ]
    list_display_links = ['id', 'name',]
    inlines = [OrderExecutorInline,]
    save_on_top = True




class OrderResponseCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_response', 'user', 'created_at']
    list_display_links = ['order_response']
    
    
    
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderResponse)
admin.site.register(OrderResponseComment, OrderResponseCommentAdmin)



