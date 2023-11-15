from .models import Operation
from app.main_users.models import CustomUser
from .serializers import OperQueryParamSerializer


class OperationServices:
    model = Operation

    @classmethod
    def get_operations(cls, params: dict, user: CustomUser):
        """Filter operations by currency, date"""
        
        params = OperQueryParamSerializer(data=params)
        params.is_valid(raise_exception=True)
        validated_param = params.validated_data
        
        currency = validated_param.get('currency', None)
        min_date = validated_param.get('min_date', None)
        max_date = validated_param.get('max_date', None)
        curr_acc = {
            "EUR": user.eur_acc,
            "USD": user.usd_acc,
            "RUB": user.rub_acc
        }

        filters  = {}
        if currency:
            filters["to_account"] = curr_acc[currency] 
        if min_date and max_date:
            filters["time_operation__date__range"] = [min_date, max_date]
        return cls.model.objects.filter(**filters)