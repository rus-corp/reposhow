from rest_framework import serializers
from drf_spectacular.utils import OpenApiParameter

from .models import PaymentMethod, PaymentAgregator, TinkofPayment, Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = [
            "id",
            "name",
        ]


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            "id",
            "name",
            "comission",
        ]


class PaymentAgregatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentAgregator
        fields = [
            "id",
            "name",
        ]


class TransferMoneyToUserSerializer(serializers.Serializer):
    currency = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    to_account = serializers.CharField()


class TinkofDataRequestSerializer(serializers.Serializer):
    TerminalKey = serializers.CharField()
    OrderId = serializers.CharField()
    Success = serializers.BooleanField()
    Status = serializers.CharField()
    PaymentId = serializers.CharField()
    ErrorCode = serializers.CharField()
    Amount = serializers.IntegerField()
    CardId = serializers.CharField()
    Pan = serializers.CharField()
    ExpDate = serializers.CharField()
    Token = serializers.CharField()


class TinkofPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TinkofPayment
        fields = ["id", "created_at", "user_acc", "order_id", "order_status", "amount"]


class WithdrawFundsSerializer(serializers.Serializer):
    """
    (Serializer) для вывода средств на банковский счет
    """

    amount = serializers.FloatField(required=True)
    currency = serializers.CharField(required=True, allow_null=False)
    bank_card = serializers.CharField(required=True)
    expiry_month = serializers.IntegerField(required=True)
    expiry_year = serializers.IntegerField(required=True)
    note = serializers.CharField(required=False)
    save_payment_template = serializers.BooleanField(default=False)

    # Имя владельца карты (обязателен для валют USD, EUR, GBP)
    card_holder = serializers.CharField(required=False)

    # Страна владельца карты (ISO 3166-1 alpha-2: FR, RU, DE) (обязателен для валют USD, EUR, GBP)
    card_holder_country = serializers.CharField(required=False)

    # Населенный пункт владельца карты (обязателен для валют USD, EUR, GBP)
    card_holder_city = serializers.CharField(required=False)

    # Дата рождения владельца карты (Формат: ‘yyyy-MM-dd’) (обязателен для валют USD, EUR, GBP)
    card_holder_dob = serializers.CharField(required=False)

    # Номер мобильного телефона владельца карты (обязателен для валют USD, EUR, GBP, RUR)
    card_holder_mobile_phone_number = serializers.CharField(required=False)


class WithdrawalEcurrencySerializer(serializers.Serializer):
    amount = serializers.FloatField(required=False)
    # Сумма транзакции в криптовалюте (точность - до шести знаков после запятой). Передается в случае, если необходимо отправить точную сумму криптовалюты.
    cryptoCurrencyAmount = serializers.FloatField(required=False)
    currency = serializers.CharField(required=False, allow_null=False)
    ecurrency = serializers.CharField(required=False)
    # Метод пополнения счета, который будет использован для обмена на криптовалюту в SCI (ADVANCED_CASH, VISA, MASTERCARD, MIR)
    # depositMethod = serializers.CharField(required=True)
    receiver = serializers.CharField(required=True)
    # Тег Ripple
    destinationTag = serializers.CharField(required=False)
    # Идентификатор в системе учета пользователя
    orderId = serializers.CharField(required=True)
    note = serializers.CharField(required=False)

    
class AdvCashDepositFundsCallbackSerializer(serializers.Serializer):
    ac_account_email = serializers.EmailField()
    ac_sci_name = serializers.CharField(max_length=255)
    ac_amount = serializers.CharField()
    ac_currency = serializers.CharField(max_length=5)
    ac_sign = serializers.CharField(max_length=512)
    ac_transfer = serializers.CharField(max_length=255)
    ac_start_date = serializers.CharField()
    ac_src_wallet = serializers.CharField(max_length=255)
    ac_dest_wallet = serializers.CharField(max_length=255)
    ac_order_id = serializers.CharField(max_length=255)
    ac_hash = serializers.CharField(max_length=512)