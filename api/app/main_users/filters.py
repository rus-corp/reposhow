from django.db.models import F
import django_filters.rest_framework as filters
from rest_framework.filters import OrderingFilter

from app.main_users.models import CustomUser


class NullsAlwaysLastOrderingFilter(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            f_ordering = []
            for o in ordering:
                if not o:
                    continue
                if o[0] == "-":
                    f_ordering.append(F(o[1:]).desc(nulls_last=True))
                else:
                    f_ordering.append(F(o).asc(nulls_last=True))
            return queryset.order_by(*f_ordering)

        return queryset


class CharFilterFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class FreelancerFilter(filters.FilterSet):
    specialization = CharFilterFilter(
        field_name="user_info__specialization__slug", lookup_expr="in"
    )
    activity = CharFilterFilter(
        field_name="user_info__specialization__category__activity__slug",
        lookup_expr="in",
    )
    category = CharFilterFilter(
        field_name="user_info__specialization__category__slug", lookup_expr="in"
    )

    class Meta:
        model = CustomUser
        fields = ['specialization', 'activity', 'category']
     
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.distinct()