from rest_framework import serializers
from .models import Operation, Account




class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_name', 'balance', 'currency',]
        # read_only_fields = ['', '',]
        
        

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['id', 'from_account', 'to_account', 'value', 'purpose_of_payment', 'currency', 'time_operation']
        # read_only_fields = ['', '',]

class OperQueryParamSerializer(serializers.Serializer):
    currency = serializers.ChoiceField(
        choices=["EUR", "USD", "RUB"],
        required=True,
    )
    min_date = serializers.DateField(
        format='%Y-%m-%d',
        required=False,
        allow_null=True,
    )
    max_date = serializers.DateField(
        format='%Y-%m-%d',
        required=False,
        allow_null=True,
    )
