from typing import Protocol, Type

from django.conf import settings
from django.db.models import F
from django.db import transaction

from rest_framework import serializers

from .models import Work, CurrentWork
from .base.exception import (
    BestWorkLimitExceedException,
    WorkStatusNotCompletedException,
    OrderAlreadyInCurrentWorkException,
    NotOwnerOfOrderException,
    TablePlaceOutOfRangeException,
)
from app.categories.serializers import SpecializationSerializer
from app.orders.serializers import (
    OrderStatusSerializer,
    OrderDetailSerializer,
    OrderExecutorSerializer,
    OrderIdSerializer,
)
from app.main_users.models import CustomUser
from app.orders.models import Order


# Work Serializers
class IWorkSerializer(Protocol):
    @staticmethod
    def _validate_work(user_id: int) -> bool:
        ...


class WorkSerializer(serializers.ModelSerializer):
    category = SpecializationSerializer()

    class Meta:
        model = Work
        fields = [
            "id",
            "title",
            "description",
            "image",
            "created_at",
            "price",
            "price_currency",
            "link",
            "video",
            "file1",
            "file2",
            "file3",
            "file4",
            "category",
            "time_spend",
            "table_place",
        ]
        read_only_fields = [
            "user",
        ]

    @staticmethod
    def _validate_work(user_id: int, table_place: int) -> bool:
        if not WorkSerializer._check_works_count(user_id):
            raise BestWorkLimitExceedException()
        elif WorkSerializer._check_table_place(user_id, table_place):
            WorkSerializer._take_place(user=user_id, table_place=table_place)

    @staticmethod
    def _check_works_count(user_id: int) -> bool:
        return len(Work.objects.filter(user=user_id)) < settings.ACCEPT_BEST_WORKS

    @staticmethod
    def _check_table_place(user_id: int, table_place: int) -> bool:
        return Work.objects.filter(user=user_id, table_place=table_place).exists()
    
    @staticmethod
    def _take_place(user: Type[CustomUser], table_place: int) -> None:
        try:
            with transaction.atomic():
                Work.objects.filter(user=user, table_place__gte=table_place).update(table_place=F('table_place') + 1)

                Work.objects.filter(user=user, table_place=table_place).update(table_place=table_place)
        except Exception as e:
            pass

    @staticmethod
    def _insert_table_place(user_id: int, table_place: int):
        user_works = Work.objects.filter(user=user_id)
        if user_works.filter(table_place=table_place).first():
            updated_works = user_works.filter(table_place__gte=table_place).all()

            new_index = table_place + 1
            for updated_work in updated_works:
                updated_work.table_place = new_index
                updated_work.save()
                new_index += 1


class WorkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = [
            "title",
            "description",
            "image",
            "created_at",
            "price",
            "price_currency",
            "link",
            "video",
            "file1",
            "file2",
            "file3",
            "file4",
            "category",
            "time_spend",
            "table_place",
        ]

    def create(self, validated_data):
        WorkSerializer._validate_work(
            self.context["user_id"], self.validated_data["table_place"]
        )
        WorkSerializer._insert_table_place(
            self.context["user_id"], self.validated_data["table_place"]
        )
        return super().create(validated_data)


class WorkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = [
            "title",
            "description",
            "image",
            "created_at",
            "price",
            "price_currency",
            "table_place",
            "link",
            "video",
            "file1",
            "file2",
            "file3",
            "file4",
            "category",
            "time_spend",
        ]


# CurrentWork Serializers
class ICurrentWorkSerializer(Protocol):
    @staticmethod
    def _validate_order(user_id: int) -> bool:
        ...


class CurrentWorkSerializer(serializers.ModelSerializer):
    order = OrderDetailSerializer()

    class Meta:
        model = CurrentWork
        fields = [
            "id",
            "order",
            "title",
            "description",
            "image",
            "created_at",
            "price",
            "price_currency",
            "link",
            "video",
            "file1",
            "file2",
            "file3",
            "file4",
            "category",
            "time_spend",
            "table_place",
        ]

    @staticmethod
    def _validate_order(order_id: int, user_id: int, table_place: int):
        if not CurrentWorkSerializer._check_order_status(order_id):
            raise WorkStatusNotCompletedException()
        if not CurrentWorkSerializer._check_order_in_current_works(order_id):
            raise OrderAlreadyInCurrentWorkException()
        if not CurrentWorkSerializer._check_order_owner(order_id, user_id):
            raise NotOwnerOfOrderException()
        if not CurrentWorkSerializer._check_table_place(user_id, table_place):
            raise TablePlaceOutOfRangeException

    @staticmethod
    def _check_table_place(user_id: int, table_place: int) -> bool:
        return table_place in range(
            0, len(CurrentWork.objects.filter(user=user_id)) + 1
        )

    @staticmethod
    def _check_order_owner(order_id: int, user_id: int) -> bool:
        return (
            user_id
            in OrderExecutorSerializer(Order.objects.get(pk=order_id)).data["executor"]
        )

    @staticmethod
    def _check_order_status(order_id: int) -> bool:
        status = OrderStatusSerializer(Order.objects.get(pk=order_id)).data["status"]
        return status == Order.OrderStatus.COMPLETED

    @staticmethod
    def _check_order_in_current_works(order_id: int) -> bool:
        return len(CurrentWork.objects.filter(order=order_id)) == 0

    @staticmethod
    def _insert_table_place(user_id: int, table_place: int):
        user_works = CurrentWork.objects.filter(user=user_id)
        if user_works.filter(table_place=table_place).first():
            updated_works = user_works.filter(table_place__gte=table_place).all()

            new_index = table_place + 1
            for updated_work in updated_works:
                updated_work.table_place = new_index
                updated_work.save()
                new_index += 1


class CurrentWorkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentWork
        fields = [
            "order",
            "title",
            "description",
            "image",
            "created_at",
            "price",
            "price_currency",
            "link",
            "video",
            "file1",
            "file2",
            "file3",
            "file4",
            "category",
            "time_spend",
            "table_place",
        ]

    def create(self, validated_data):
        CurrentWorkSerializer._validate_order(
            self.data["order"],
            self.context["user_id"],
            self.validated_data["table_place"],
        )
        CurrentWorkSerializer._insert_table_place(
            self.context["user_id"], self.validated_data["table_place"]
        )
        return super().create(validated_data)


class CurrentWorkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentWork
        fields = [
            "order",
            "title",
            "description",
            "image",
            "created_at",
            "price",
            "price_currency",
            "link",
            "video",
            "file1",
            "file2",
            "file3",
            "file4",
            "category",
            "time_spend",
            "table_place",
        ]

    def update(self, instance, validated_data):
        CurrentWorkSerializer._validate_order(
            OrderIdSerializer(self.validated_data["order"]).data["id"],
            self.context["user_id"],
            self.validated_data["table_place"],
        )
        return super().update(instance, validated_data)
