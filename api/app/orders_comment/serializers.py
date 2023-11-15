from typing import Protocol

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from app.orders.models import OrderResponseComment, OrderResponse
from .base.exception import NotOrderConsumerExecutorException


class IOrderResponseCommentSerializer(Protocol):
    
    @staticmethod
    def _validate_order_response_comment(user_id: int, order_response: OrderResponse) -> bool:
        ...


class OrderResponseCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(method_name='get_replies')

    class Meta:
        model = OrderResponseComment
        fields = ['id', 'text', 'created_at', 'user', 'order_response', 'replies', 'file1', 'file2', 'file3']
        read_only_fields = ['user', 'created_at']

    @extend_schema_field(list)
    def get_replies(self, obj):
        replies = obj.replies.all()
        serializer = OrderResponseCommentSerializer(instance=replies, many=True)
        return serializer.data
    
    @staticmethod
    def _validate_order_response_comment(user_id: int, order_response: OrderResponse) -> bool:
        if not OrderResponseCommentSerializer._check_comment_user(user_id, order_response):
            raise NotOrderConsumerExecutorException
    
    @staticmethod
    def _check_comment_user(user_id: int, order_response: OrderResponse) -> bool:
        return any([
            len(order_response.order.executor.filter(id=user_id)) > 0,
            order_response.order.customer == user_id
        ])
    

class OrderResponseCommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderResponseComment
        fields = ['text', 'order_response', 'file1', 'file2', 'file3']
    
    def create(self, validated_data):
        OrderResponseCommentSerializer._validate_order_response_comment(
                self.context['user_id'], self.validated_data['order_response']
            )
        
        if order_comments := OrderResponseComment.objects.filter(order_response=self.validated_data['order_response']):
            last_order_comment = order_comments.order_by("created_at").all().last()
            self.validated_data['parent'] = last_order_comment
            
        return super().create(validated_data)