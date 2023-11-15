from django.shortcuts import render
from rest_framework import viewsets, status, permissions, generics, serializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from .contract import genereate_contract_text
from .models import Region, Country, Contract
from .serializers import CustomUserPersonalAccount, RegionSerializer, CountrySerializer, ContractSerializer
from app.main_users.permissions import IsOwner
from app.main_users.models import CustomUser


class UserPersonalAccountViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserPersonalAccount
    permission_classes = (IsOwner,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.id)

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)



class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class CountryView(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer





class ContractCreatView(generics.ListCreateAPIView):
    queryset = Contract.objects.none()
    serializer_class = ContractSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Contract.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        user = self.request.user
        contract_text = genereate_contract_text(user)
        if contract_text:    
            serializer.save(user=user, text=contract_text)
        else:
            raise serializers.ValidationError('Для формирования договора необходимо внести личную информацию')




class ContractDetailView(generics.UpdateAPIView):
    serializer_class = ContractSerializer
    permission_classes = (IsOwner,)
    
    def get_object(self):
        user = self.request.user
        return get_object_or_404(Contract, user=user)
    
    def perform_update(self, serializer):
        user = self.request.user
        contract_text = genereate_contract_text(user)
        if contract_text:
            serializer.instance.text = contract_text
            serializer.instance.save()





# еуеыфыв

# НЕ АКУТАЛЬНО

# class UserDocsViewSets(viewsets.ModelViewSet):
#     """Документы юзера"""
#     queryset = UserDoc.objects.all()
#     serializer_class = UserDocsSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwner)

#     def get_queryset(self):
#         return UserDoc.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# class BankAccountViewSet(viewsets.ModelViewSet):
#     """Банковские реквизиты юзера"""
#     queryset = BankAccount.objects.all()
#     serializer_class = BankAccountSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwner,)

#     def get_queryset(self):
#         return BankAccount.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)



# class UserInfoViewSet(viewsets.ModelViewSet):
#     queryset = UserInfo.objects.all()
#     serializer_class = UserInfoSerializer
#     permission_classes = (permissions.IsAuthenticated, IsOwner,)

#     def get_queryset(self):
#         return UserInfo.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)