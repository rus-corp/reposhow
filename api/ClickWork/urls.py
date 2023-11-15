from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from app.main_users.views import (
    RegisterView,
    email_token,
    LoginView,
    ChangePassword,
    reset_password_link_view,
    ResetPasswordView,
    FreelancersViewSet,
    UserSpecializationCreateViewSet,
    UserInfoCompanyViewSet,
)
from app.chat.views import ThreadViewSet, CommentViewSet, ChatViewSet
from app.referal_link.views import ReferalLinkViewSet
from app.user_docs.views import (
    UserPersonalAccountViewSet,
    RegionViewSet,
    CountryView,
)
from app.mails.views import MailAcceptionViewSet
from app.orders.views import OrdersViewSet
from app.voiting.views import VoiteViewSet
from app.tickets.views import TicketViewSet
from app.faq.views import QuestionViewSet
from app.news.views import NewsViewSet
from app.categories.views import (
    CategApiView,
    ActivityApiView,
    SpecializationApiView,
)
from app.raiting.views import RatingViewSet


router = DefaultRouter()


# UserCompanyInfo
router.register("company", UserInfoCompanyViewSet)
# UserDocs
# router.register('user_docs', UserDocsViewSets)
# router.register('banck_account', BankAccountViewSet)
# router.register('userinfo', UserInfoViewSet)
router.register("region", RegionViewSet)
router.register("country", CountryView)
# User personal account
router.register("personal-account", UserPersonalAccountViewSet)
router.register("user-specialization", UserSpecializationCreateViewSet)

# Orders
router.register("orders", OrdersViewSet, basename="orders")

# Voiting
router.register("voiting", VoiteViewSet)

router.register("threads", ThreadViewSet, basename="threads")
router.register(
    r"threads/(?P<thread_id>\d+)/comments", CommentViewSet, basename="comments"
)

# Tickets
router.register("tickets", TicketViewSet)


# FAQ
router.register("faq", QuestionViewSet, basename="faq")

# News
router.register("news", NewsViewSet)

# Users List
router.register("freelancers", FreelancersViewSet)


urlpatterns = [
    path("api/v1/register/<str:refer>/", RegisterView.as_view()),
    re_path(
        "api/v1/emailtoken/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{10,51})/",
        email_token,
        name="email_token",
    ),
    path("api/v1/login/", LoginView.as_view(), name="knox_login"),
    path(
        "api/v1/resetpassword/",
        ChangePassword.as_view(),
        name="reset-password",
    ),
    re_path(
        r"api/v1/resetpassword/link(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{10,51})/",
        reset_password_link_view,
        name="reset_password_link_view",
    ),
    path(
        "api/v1/resetpassword-confirm/",
        ResetPasswordView.as_view(),
        name="password_confirm",
    ),
    path("admin/", admin.site.urls),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/schema/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/v1/", include(router.urls)),
    path("api/v1/activity/", ActivityApiView.as_view(), name="activity"),
    path(
        "api/v1/activity/<str:activity>/categories/",
        CategApiView.as_view(),
        name="categories",
    ),
    path(
        "api/v1/categories/<str:categories>/specializations/",
        SpecializationApiView.as_view(),
        name="specializations",
    ),
    path("api/v1/contract/", include("app.user_docs.urls")),
    path("api/v1/works/", include("app.portfolio.urls")),
    path("api/v1/reviews/", include("app.reviews.urls")),
    path("api/v1/company_docs/", include("app.company_docs.urls")),
    path("api/v1/orders/comment/", include("app.orders_comment.urls")),
    path(
        "api/v1/mail/<str:user__slug>/",
        MailAcceptionViewSet.as_view({"patch": "update"}),
        name="user_mails",
    ),
    path("api/v1/operations/", include("app.accounts.urls")),
    path("api/v1/payment/", include("app.adv_cash.urls")),
    path(
        "api/v1/chats/<int:chat_id>/",
        ChatViewSet.as_view({"get": "list"}),
        name="chats",
    ),
    path(
        "api/v1/chats/<int:chat_id>/message/",
        ChatViewSet.as_view({"post": "send_message"}),
        name="messages",
    ),
    path(
        "api/v1/chats/",
        ChatViewSet.as_view({"get": "list", "post": "create"}),
        name="chats_list",
    ),
    path("api/v1/referal-link/", ReferalLinkViewSet.as_view()),
    path(
        "api/v1/rating/",
        RatingViewSet.as_view(),
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
