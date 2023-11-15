from rest_framework import serializers
from django.utils import timezone
from drf_spectacular.utils import extend_schema_field
from rest_framework.response import Response

from .models import Order, OrderResponse
from app.main_users.models import CustomUser, UserInfo
from app.user_docs.models import Country
from app.categories.models import Specialization
from app.categories.serializers import SpecializationSerializer
from app.accounts.models import Account
from app.accounts.operations import check_customer_balance, create_order_transfer_money
from app.orders_comment.serializers import OrderResponseCommentSerializer
from .services import gen_unique_account_name

class CountryOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]
        extra_kwargs = {
            "name": {"validators": []},
        }


class SpecializationOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ["id", "name"]


class UserInfoOrderSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()

    class Meta:
        model = UserInfo
        fields = ["id", "first_name", "last_name", "avatar", 'company_name']

    def get_company_name(self, obj):
        if obj.user.legal_status == 'LG':
            return ''.join(obj.company.company_name)
        return None


class OrderCustomUserSerializer(serializers.ModelSerializer):
    user_info = UserInfoOrderSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'user_info']
        read_only_fields = ['id', 'email', 'username']


class OrderExecutorSerializer(serializers.ModelSerializer):
    executor = OrderCustomUserSerializer()
    order_response_comments = OrderResponseCommentSerializer(many=True)

    class Meta:
        model = OrderResponse
        fields = [
            "id",
            "executor",
            "executor_status",
            "text",
            "price",
            "term",
            "created_at",
            "file1",
            "file2",
            "file3",
            "order_response_comments",
        ]
        read_only_fields = [
            "id",
            "executor",
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    executor = OrderExecutorSerializer(many=True, source="order_responses")
    specialization = SpecializationSerializer(read_only=True)
    customer = OrderCustomUserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "specialization",
            "price",
            "currency",
            "customer",
            "executor",
            "slug",
            "created_at",
            "target_audience",
            "atention",
            "file1",
            "file2",
            "file3",
            "period",
        ]
        read_only_fields = [
            "customer",
        ]


class OrderListSerializer(serializers.ModelSerializer):
    time_since_created = serializers.SerializerMethodField(
        method_name="get_time_since_created"
    )
    executor_count = serializers.SerializerMethodField(
        method_name="get_executors_count"
    )
    period_execution = serializers.SerializerMethodField(
        method_name="get_period_execution"
    )
    specialization = SpecializationSerializer(read_only=True)
    customer = OrderCustomUserSerializer(read_only=True)
    annotated_comments = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "specialization",
            "price",
            "currency",
            "customer",
            "time_since_created",
            "executor_count",
            "period_execution",
            "views",
            "annotated_comments",
        ]
        read_only_fields = [
            "customer",
            "views",
            "time_since_created",
            "period_execution",
            "executor_count",
            "annotated_comments",
        ]

    @extend_schema_field(serializers.DateTimeField())
    def get_time_since_created(self, obj):
        now = timezone.now()
        time_since_created = now - obj.created_at
        return time_since_created

    @extend_schema_field(serializers.IntegerField())
    def get_executors_count(self, order):
        return order.order_responses.count()

    @extend_schema_field(serializers.DateField())
    def get_period_execution(self, order):
        if order.period:
            now = timezone.now().date()
            period_of_execution = order.period - now
            return period_of_execution.days
        else:
            return "Срок не определен"


class OrderCreateSerializer(serializers.ModelSerializer):
    specialization_id = serializers.IntegerField()
    period = serializers.DateField(required=False)
    country = CountryOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "name",
            "description",
            "price",
            "currency",
            "created_at",
            "specialization_id",
            "period",
            "slug",
            "target_audience",
            "atention",
            "status",
            "customer",
            "file1",
            "file2",
            "file3",
            "country",
        ]
        read_only_fields = ["customer", "slug"]

    def create(self, validated_data):
        user = self.context["request"].user
        price = validated_data.get("price", 0)
        currency = validated_data["currency"]
        country_data = validated_data.pop("country", [])
        if check_customer_balance(customer=user, currency=currency, price=price):
            name = validated_data.get("name")
            specialization_id = validated_data.pop("specialization_id")
            validated_data["specialization"] = Specialization.objects.get(
                id=specialization_id
            )
            validated_data["rub_acc"] = Account.objects.create(
                account_name=gen_unique_account_name(name[:12], "rub")
            )
            validated_data["usd_acc"] = Account.objects.create(
                account_name=gen_unique_account_name(name[:12], "usd"), 
                currency="USD"
            )
            validated_data["eur_acc"] = Account.objects.create(
                account_name=gen_unique_account_name(name[:12], "eur"), 
                currency="EUR"
            )
            order = super().create(validated_data)
            create_order_transfer_money(user, currency, price, order)
        else:
            return Response({"error": "Not enough funds"})
        for country_info in country_data:
            try:
                country = Country.objects.get(**country_info)
                order.country.add(country)
            except Country.DoesNotExist:
                return Response({"error": "Country does not exist"})
        return order

    def update(self, instance, validated_data):
        order = super().update(validated_data)
        return super().update(instance, validated_data)


class OrderStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['status']


class OrderExecutorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['executor']


class OrderIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id']


class OrderReviewSerializer(serializers.ModelSerializer):
    specialization = SpecializationSerializer()

    class Meta:
        model = Order
        fields = ['id', 'name', 'slug', 'description', 'specialization', 'price', 'currency',
                  'slug', 'created_at', 'target_audience', 'atention', 'file1', 'file2', 'file3', 'period']