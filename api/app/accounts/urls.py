from django.urls import path


from .views import OperationView


urlpatterns = [
    path('', OperationView.as_view(), name='operations')
]