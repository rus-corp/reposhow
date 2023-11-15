from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin

from app.main_users.permissions import EmailUserOwner
from app.main_users.models import CustomUser
from app.mails.serializers import MailPermissionSerializer
from app.mails.models import UserMailPermissions


class MailAcceptionViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = MailPermissionSerializer
    permission_classes = (EmailUserOwner,)
    lookup_field = 'user__slug'

    def get_queryset(self):
        user = get_object_or_404(
            CustomUser,
            Q(status__in=('FR', 'CS'))
            & Q(slug=self.kwargs.get('user__slug'))
        )
        UserMailPermissions.objects.get_or_create(
            user=user
        )
        return UserMailPermissions.objects.filter(user=user)
