from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

from .serializers import OperationSerializer
from app.main_users.permissions import IsOwner
from .services import OperationServices



@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='currency', description='Filter by currency (EUR, USD, RUB)', type=str, required=True),
            OpenApiParameter(name='max_date', description='Filter by minimum date (YYYY-MM-DD)', type=str),
            OpenApiParameter(name='min_date', description='Filter by maximum date (YYYY-MM-DD)', type=str),
        ]
    )
)
class OperationView(generics.ListAPIView):
    serializer_class = OperationSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    
    def get_queryset(self):
        return OperationServices.get_operations(
            params=self.request.query_params,
            user=self.request.user
        )        