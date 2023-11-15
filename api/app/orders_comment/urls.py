from django.urls import path

from .views import (
    OrderResponseCommentCreateApiView,
    OrderResponseCommentRetrieveApiView
)

urlpatterns = [
    path("<int:id>", OrderResponseCommentRetrieveApiView.as_view(), name="order_comment_retrieve"),
    path("create", OrderResponseCommentCreateApiView.as_view(), name="order_comment_create")
]