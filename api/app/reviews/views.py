from rest_framework import generics
from rest_framework import permissions
from django_filters import rest_framework as rest_filters
from django.db.models import QuerySet

from .models import Review
from .serializers import (
    ReviewSerializer,
    ReviewCreateSerializer,
    ReviewUpdateSerializer
)
from .base import permissions as app_permissions


class ReviewCreateApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewCreateSerializer


class ReviewRetrieveApiView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    lookup_field = "id"


class ReviewListApiView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ReviewSerializer
    filter_backends = [rest_filters.DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self) -> QuerySet:
        return Review.objects.filter(executor=self.kwargs.get("executor_id"))


class ReviewUpdateApiView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, app_permissions.IsReviewOwner]
    serializer_class = ReviewUpdateSerializer
    queryset = Review.objects.all()
    lookup_field = "id"


class ReviewDestroyApiView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, app_permissions.IsReviewOwner]
    queryset = Review.objects.all()
    lookup_field = "id"
    serializer_class = ReviewSerializer