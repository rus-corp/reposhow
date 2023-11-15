from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import permissions, generics, viewsets, status
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from django.utils.text import slugify
from transliterate import translit
from django.db.models import Count
from rest_framework.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _


from ..main_users.permissions import IsOwner
from .models import Order, OrderResponse, OrderResponseComment
from .serializers import (
    OrderDetailSerializer,
    OrderListSerializer,
    OrderCreateSerializer,
    OrderResponseCommentSerializer,
)
from .services import OrderFilter
from app.reviews.models import Review
from app.accounts.operations import create_order_transfer_money, check_customer_balance


User = get_user_model()


class OrderListPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 30


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.published.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    pagination_class = OrderListPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderFilter
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        elif self.action == "create":
            return OrderCreateSerializer
        elif self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return OrderDetailSerializer
        else:
            return OrderListSerializer

    def perform_create(self, serializer):
        user = self.request.user
        text = self.request.data.get("name")

        try:
            name = translit(text, reversed=True)
            slug = slugify(name)
        except:
            slug = slugify(text)
        serializer.save(customer=user, slug=slug)

    """Откликнуться на заказ, путь: orders/pk заказа/enroll/"""

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def enroll(self, *args, **kwargs):
        order = self.get_object()
        price = self.request.data.get("price")
        text = self.request.data.get("text")
        term = self.request.data.get("term")
        user = self.request.user
        if user.status == "CS" or user.status == "FR":
            OrderResponse.objects.create(
                order=order,
                executor=self.request.user,
                text=text,
                price=price,
                term=term,
            )
            return JsonResponse(
                {"enrolled": True, "message": "You have responded to the order"},
                status=status.HTTP_201_CREATED,
            )
            # return Response({'enrolled': True, 'message': _('You have responded to the order')}, status=status.HTTP_201)
        else:
            return Response(
                {"error": "You need to pay the entrance fee"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # смена статуса с кандидат на исполнитель
    @action(
        detail=True, methods=["patch"], permission_classes=[permissions.IsAuthenticated]
    )
    def change_executor_status(self, request, *args, **kwargs):
        order = self.get_object()
        executor_id = request.data.get("executor_id")
        executor_status = request.data.get("executor_status")

        try:
            executor = User.objects.get(pk=executor_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"Status": False, "Error": "Кандидат не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if executor_status not in OrderResponse.ExecutorStatus.get_all_values():
            return JsonResponse(
                {"Status": False, "Error": "Не верный статус"},
                status=status.HTTP_201_CREATED,
            )

        order.change_executor_status(executor, executor_status)
        return JsonResponse({"status_changed": True}, status=status.HTTP_200_OK)

    # оставить отзыв
    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def review(self, request, *args, **kwargs):
        order = self.get_object()
        customer = self.request.user
        if order.customer != customer:
            raise PermissionDenied("you are not a customer")
        executor_obj = OrderResponse.objects.filter(
            order=order, executor_status=OrderResponse.ExecutorStatus.EXECUTOR
        ).first()
        if executor_obj:
            executor = executor_obj.executor
            description = request.data.get("description", "")
            review = Review.objects.create(
                order=order,
                customer=customer,
                executor=executor,
                description=description,
            )
            ratio = self.get_object().update_reviews_ratio()
            return JsonResponse(
                {"message": "review created"}, status=status.HTTP_201_CREATED
            )
        else:
            return JsonResponse({'message': 'not executor'}, status=status.HTTP_404_NOT_FOUND)