from django.urls import path

from .views import (
    ReviewListApiView,
    ReviewRetrieveApiView,
    ReviewUpdateApiView,
    ReviewDestroyApiView,
    ReviewCreateApiView
)

urlpatterns = [
    path("list/<int:executor_id>/", ReviewListApiView.as_view(), name="review_list"),
    path("<int:id>/", ReviewRetrieveApiView.as_view(), name="review_retrieve"),
    path("update/<int:id>/", ReviewUpdateApiView.as_view(), name="review_patch"),
    path("destroy/<int:id>/", ReviewDestroyApiView.as_view(), name="review_destroy"),
    path("create/", ReviewCreateApiView.as_view(), name="review_create")
]