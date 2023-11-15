from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status, filters

from app.chat.models import Thread, Comment, ChatRoom
from app.chat.serializers import (
    ThreadSerializer,
    CommentSerializer,
    ChatSerializer,
    MessageSerializer,
)
from app.main_users.permissions import (
    IsFreelancerOrCustomer,
    IsFreelancerOrCustomerOrReadOnly,
)


User = get_user_model()


class ThreadViewSet(viewsets.ModelViewSet):
    http_method_names = ("get", "post")
    permission_classes = (IsFreelancerOrCustomerOrReadOnly,)
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("created_at",)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsFreelancerOrCustomerOrReadOnly,)
    http_method_names = ("get", "post")
    serializer_class = CommentSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("created_at",)

    def perform_create(self, serializer):
        thread = get_object_or_404(Thread, id=self.kwargs.get("thread_id"))
        serializer.save(commentator=self.request.user, thread=thread)

    def get_queryset(self):
        return Comment.objects.filter(thread_id=self.kwargs.get("thread_id"))


class ChatViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.none()
    http_method_names = ("get", "post")
    permission_classes = (IsFreelancerOrCustomer,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("created_at",)

    def get_serializer(self, *args, **kwargs):
        serializer_class = ChatSerializer
        if "chat_id" in self.kwargs:
            kwargs.setdefault("context", self.get_serializer_context())
            kwargs["many"] = False
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        user_1 = self.request.user
        if "chat_id" in self.kwargs:
            return ChatRoom.objects.filter(
                Q(id=self.kwargs.get("chat_id"))
                & (Q(user_1=user_1) | Q(user_2=user_1))
            ).first()
        return ChatRoom.objects.filter(
            Q(
                user_1=user_1,
            )
            | Q(
                user_2=user_1,
            )
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_1 = User.objects.get(email=self.request.user.email)
            user_2 = User.objects.get(id=self.request.data.get("user_2"))
            if user_2.status not in ("CS", "FR"):
                return Response(
                    {"error": "you cant send messages to unpaid users."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            if user_1 == user_2 or ChatRoom.objects.filter(
                Q(user_1=user_1, user_2=user_2)
                & Q(user_1=user_2, user_2=user_1)
            ).exists():
                return Response(
                    {
                        "Error": "Cant create a chat between these two users, its already exists."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save(
                name=f"{user_1.email}x{user_2.email}_chat",
                user_1=user_1,
                user_2=user_2,
            )
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=MessageSerializer)
    def send_message(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                room=self.get_queryset(),
                sender=User.objects.get(email=self.request.user.email),
            )
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
