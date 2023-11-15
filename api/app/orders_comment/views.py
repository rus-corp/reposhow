from rest_framework import permissions, generics

from app.orders.models import OrderResponseComment
from app.orders_comment.serializers import (
    OrderResponseCommentSerializer,
    OrderResponseCommentCreateSerializer
)
from .base import permissions as app_permissions


class OrderResponseCommentCreateApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderResponseCommentCreateSerializer
    
    def perform_create(self, serializer: OrderResponseCommentCreateSerializer):
        user = self.request.user
        serializer.save(user=user)
        return super().perform_create(serializer)
    
    def get_serializer_context(self) -> dict:
        return {'user_id': self.request.user.id}
    

class OrderResponseCommentRetrieveApiView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, app_permissions.IsOrderResponseCommentOwner]
    serializer_class = OrderResponseCommentSerializer
    queryset = OrderResponseComment.objects.all()
    lookup_field = "id"