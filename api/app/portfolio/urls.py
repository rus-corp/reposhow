from django.urls import path

from .views import (
    WorkCreateApiView,
    WorkListApiView,
    WorkRetrieveApiView,
    WorkUpdateApiView,
    WorkDestroyApiView,
    CurrentWorkCreateApiView,
    CurrentWorkListApiView,
    CurrentWorkRetrieveApiView,
    CurrentWorkUpdateApiView,
    CurrentWorkDestroyApiView,
)

urlpatterns = [
    # Best Works
    path("list/<int:user_id>/", WorkListApiView.as_view(), name="work_list"),
    path("<int:id>/", WorkRetrieveApiView.as_view(), name="work_retrieve"),
    path("update/<int:id>/", WorkUpdateApiView.as_view(), name="work_patch"),
    path("destroy/<int:id>/", WorkDestroyApiView.as_view(), name="work_destroy"),
    path("create/", WorkCreateApiView.as_view(), name="work_create"),
] + [
    # Current Works
    path("current/list/<int:user_id>/", CurrentWorkListApiView.as_view(), name="current_work_list"),
    path("current/<int:id>/", CurrentWorkRetrieveApiView.as_view(), name="current_work_retrieve"),
    path("current/update/<int:id>/", CurrentWorkUpdateApiView.as_view(), name="current_work_patch"),
    path("current/destroy/<int:id>/", CurrentWorkDestroyApiView.as_view(), name="current_work_destroy"),
    path("current/create/", CurrentWorkCreateApiView.as_view(), name="current_work_create"),
]
