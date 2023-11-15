from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ReferalLinkView, CompanyDocViewSet, FounderAgreementView, FounderRevokeView, PrivateCompanyDocs


router = DefaultRouter()
router.register('comapny_docs', CompanyDocViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('docs/<str:slug>/', PrivateCompanyDocs.as_view(), name="private-docs"),
    path('referal_link/', ReferalLinkView.as_view(), name='referal_link'),
    path('founder_agreement/', FounderAgreementView.as_view(), name='founder_agrement'),
    path('founder_revoke/', FounderRevokeView.as_view(), name='founder_revoke')
]