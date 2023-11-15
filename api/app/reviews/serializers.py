from typing import Protocol

from rest_framework import serializers

from .models import Review
from .base.exception import (
    CustomerExecutorSameException,
    NotExecutorOrderException,
    NotCustomerOrderException,
    CustomerReviewAlreadyExistException
)
from app.main_users.serializers import CustomUserSerializer
from app.orders.serializers import OrderReviewSerializer
from app.orders.models import Order


class IReviewSerializer(Protocol):

    @staticmethod
    def _validate_review(customer_id: int, executor_id: int, order_id: int) -> bool:
        ...


class ReviewSerializer(serializers.ModelSerializer):
    customer = CustomUserSerializer()
    executor = CustomUserSerializer()
    order = OrderReviewSerializer()

    class Meta:
        model = Review
        fields = ['id', 'description', 'status', 'order', 'customer', 'executor']

    @staticmethod
    def _validate_review(customer_id: int, executor_id: int, order_id: int) -> bool:
        if not ReviewSerializer._check_customer(customer_id, executor_id):
            raise CustomerExecutorSameException
        if not ReviewSerializer._check_executor_order(order_id, executor_id):
            raise NotExecutorOrderException
        if not ReviewSerializer._check_customer_order(order_id, customer_id):
            raise NotCustomerOrderException
        if not ReviewSerializer._check_review(order_id, executor_id, customer_id):
            raise CustomerReviewAlreadyExistException

    @staticmethod
    def _check_customer(customer_id: int, executor_id: int) -> bool:
        return customer_id != executor_id

    @staticmethod
    def _check_executor_order(order_id: int, executor_id: int) -> bool:
        executor_order_ids = [order.id for order in Order.objects.filter(executor=executor_id)]
        return order_id in executor_order_ids

    @staticmethod
    def _check_review(order_id: int, executor_id: int, customer_id: int) -> bool:
        executor_order_by_customer_review = Review.objects.filter(
            order=order_id, executor=executor_id, customer=customer_id
            )
        return len(executor_order_by_customer_review) == 0

    @staticmethod
    def _check_customer_order(order_id: int, customer_id: int) -> bool:
        customer_order_ids = [order.id for order in Order.objects.filter(customer=customer_id)]
        return order_id in customer_order_ids


class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['description', 'status', 'order', 'customer', 'executor']

    def create(self, validated_data):
        ReviewSerializer._validate_review(self.data['customer'], self.data['executor'], self.data['order'])
        return super().create(validated_data)


class ReviewUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['description', 'status']




