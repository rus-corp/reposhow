from django_filters import rest_framework as filters
from django.utils.crypto import get_random_string

from .models import Order
from app.accounts.models import Account


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass



class OrderFilter(filters.FilterSet):
    price = filters.RangeFilter()
    specialization = CharFilterInFilter(field_name='specialization__name', lookup_expr='in')
    country = CharFilterInFilter(field_name='country__country_name', lookup_expr='in')
    executor_count = filters.NumberFilter(field_name='order_responses', lookup_expr='lt')
    executor = filters.CharFilter(method='filter_by_executor')    
    
    
    class Meta:
        model = Order
        fields = ['price', 'specialization', 'country', 'executor_count', 'executor']
        
        
    def filter_by_executor(self, queryset, name, value):
        current_user = self.request.user
        return queryset.filter(order_responses__executor=current_user)
        

def gen_unique_account_name(base_name, currency_code):
    acc_name = base_name
    while Account.objects.filter(account_name=f"{acc_name}-{currency_code}").exists():
        acc_name = f"{acc_name}-{get_random_string(length=4)}"
    return f"{acc_name}-{currency_code}"