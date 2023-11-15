from rest_framework import generics
from rest_framework import permissions
from django.db.models import QuerySet

from .models import Work, CurrentWork
from .serializers import (
    WorkSerializer,
    WorkCreateSerializer,
    WorkUpdateSerializer,
    CurrentWorkSerializer,
    CurrentWorkCreateSerializer,
    CurrentWorkUpdateSerializer
)
from .base import permissions as app_permissions


# Best Works
class WorkCreateApiView(generics.CreateAPIView):
    queryset = Work.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WorkCreateSerializer

    def perform_create(self, serializer: WorkCreateSerializer) -> None:
        user = self.request.user
        serializer.save(user=user)

    def get_serializer_context(self) -> dict:
        return {'user_id': self.request.user.id}


class WorkRetrieveApiView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = WorkSerializer
    queryset = Work.objects.all()
    lookup_field = "id"


class WorkListApiView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = WorkSerializer

    def get_queryset(self) -> QuerySet:
        return Work.objects.filter(user=self.kwargs.get('user_id'))


class WorkUpdateApiView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, app_permissions.IsPortfolioOwner]
    serializer_class = WorkUpdateSerializer
    queryset = Work.objects.all()
    lookup_field = "id"

    def get_serializer_context(self) -> dict:
        return {'user_id': self.request.user.id}


class WorkDestroyApiView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, app_permissions.IsPortfolioOwner]
    queryset = Work.objects.all()
    lookup_field = "id"
    serializer_class = WorkSerializer


# Current Works
class CurrentWorkCreateApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CurrentWorkCreateSerializer

    def perform_create(self, serializer: CurrentWorkCreateSerializer) -> None:
        user = self.request.user
        serializer.save(user=user)

    def get_serializer_context(self) -> dict:
        return {'user_id': self.request.user.id}


class CurrentWorkRetrieveApiView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CurrentWorkSerializer
    queryset = CurrentWork.objects.all()
    lookup_field = "id"


class CurrentWorkListApiView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CurrentWorkSerializer

    def get_queryset(self) -> QuerySet:
        return CurrentWork.objects.filter(user=self.kwargs.get('user_id'))


class CurrentWorkUpdateApiView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, app_permissions.IsPortfolioOwner]
    serializer_class = CurrentWorkUpdateSerializer
    queryset = CurrentWork.objects.all()
    lookup_field = "id"


class CurrentWorkDestroyApiView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, app_permissions.IsPortfolioOwner]
    queryset = CurrentWork.objects.all()
    lookup_field = "id"
    serializer_class = CurrentWorkSerializer




