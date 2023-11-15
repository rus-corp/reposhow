from rest_framework import permissions

from app.main_users.models import CustomUser


class IsOwner(permissions.BasePermission):
    """Проверка на запись, относящаяся к данному юзеру
    используется в :
    user_docs
    orders"""

    def has_object_permission(self, request, view, obj):
        return request.user == obj


class EmailUserOwner(permissions.BasePermission):
    """Проверка владельца модели EmailPermissions."""
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class InfoOwner(permissions.BasePermission):
    """проверка владельца через User Info"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user_info = obj.user.user.pk
        custom_user = request.user.pk
        return user_info == custom_user


class CompanyOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user.user_info.company


class IsFreelancerOrCustomerOrReadOnly(permissions.BasePermission):
    """Проверка аккаунта на активацию для доступа к закрытым функциям."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (
                CustomUser.objects.get(email=request.user.email).status in ('FR', 'CS')
            )


class IsFreelancerOrCustomer(permissions.BasePermission):
    """Проверка аккаунта на активацию для доступа к закрытым функциям."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                CustomUser.objects.get(email=request.user.email).status in ('FR', 'CS')
            )


class IsFounder(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.founder