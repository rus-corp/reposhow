from django.urls import path

from .views import ContractCreatView, ContractDetailView



urlpatterns = [
    path('', ContractCreatView.as_view(), name='contract'),
    path('user-contract/' ,ContractDetailView.as_view(), name='user-contract'),
]