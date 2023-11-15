from rest_framework import permissions


class BaseAppPermission(permissions.BasePermission):
    
    def __init__(self) -> None:
        super().__init__()