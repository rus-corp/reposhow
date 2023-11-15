from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import permissions
from django.utils import timezone
from datetime import timedelta
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, generics
from django_filters import rest_framework as filters
from knox.views import LoginView as KnoxLoginView
from django.utils.crypto import get_random_string


from .scheme.scheme import KnoxTokenScheme
from .scheme.parameters import uid_param, token_param
from .serializers import (
    LoginUserSerializer,
    RegisterUserSerializer,
    CustomUserSerializer,
    ResetPasswordLinkRequestSerializer,
    ResetPasswordSerializer,
    UserInfoCompanySerializer,
    CustomUserListSerializer,
    UserSpecializationSerializer,
)
from .scheme.responses import (
    resp_200,
    confirm_404_resp,
    login_200_resp,
    login_403_resp,
    reset_password_link_200_resp,
    reset_password_link_403_resp,
    reset_password_403_resp,
    register_403_resp,
)
from .emails import (
    new_user_register,
    password_reset_link_created,
)
from .models import (
    CustomUser,
    EmailToken,
    UserInfoCompany,
    UserSpecialization,
)
from .permissions import InfoOwner, CompanyOwner
from .filters import FreelancerFilter, NullsAlwaysLastOrderingFilter
from .services import CustomnUserService


class FreelancersPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = "page_size"
    max_page_size = 9


class RegisterView(APIView):
    """Регистрация пользователя. Нужно передать email, password"""

    @extend_schema(
        request=RegisterUserSerializer,
        responses={**resp_200, **register_403_resp},
    )
    def post(self, request, *args, **kwargs):
        if {"email", "password"}.issubset(request.data):
            try:
                validate_password(request.data["password"])
            except ValidationError as password_error:
                return JsonResponse(
                    {
                        "Status": False,
                        "Errors": {"password": password_error.messages},
                    }
                )

            email = request.data["email"]
            username = email.split("@")[0]
            user_serializer = CustomUserSerializer(data=request.data)
            while CustomUser.objects.filter(username=username).exists():
                username = f"{username}-{get_random_string(length=4)}"

            slug = CustomnUserService.get_username_slug(username=username)
            if user_serializer.is_valid():
                refer = str(kwargs.get("refer"))
                total_ref = f"https://clik-work.ru/registration/{refer}/"
                if refer:
                    try:
                        parent = CustomUser.objects.get(referal_link=total_ref)
                        user = user_serializer.save(username=username, slug=slug)
                        user.set_password(request.data["password"])
                        user.parent = parent
                        user.save()
                    except CustomUser.DoesNotExist:
                        return JsonResponse(
                            {"Status": False, "Errors": "User does not exist"}
                        )

                new_user_register.delay(user_id=user.id)

                new_user_register.delay(user_id=user.id)
                return JsonResponse({"Status": True}, status=200)
            else:
                return JsonResponse(
                    {"Status": False, "Errors": user_serializer.errors},
                    status=403,
                )
        else:
            return JsonResponse(
                {
                    "Status": False,
                    "Errors": "Не указаны все необходимые аргументы",
                },
                status=403,
            )


@extend_schema(
    parameters=[uid_param, token_param],
    responses={**resp_200, **confirm_404_resp},
)
@api_view(["GET"])
def email_token(request, uidb64, token):
    """Подтверждение почты"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        token_obj = EmailToken.objects.filter(user_id=uid, key=token).first()
    except (TypeError, ValueError, OverflowError, EmailToken.DoesNotExist):
        token_obj = None

    if token_obj:
        match token_obj.purpose:
            case "confirm":
                token_obj.user.is_active = True
                token_obj.user.email_confirm = True
            case "email":
                token_obj.user.email = request.GET.get("new_email")
        token_obj.user.save()
        token_obj.delete()
        return JsonResponse({"Status": True}, status=200)
    else:
        return JsonResponse(
            {"Status": False, "Errors": "Ссылка активации недействительна"},
            status=404,
            json_dumps_params={"ensure_ascii": False},
        )


class LoginView(KnoxLoginView):
    """Логин пользователя по email и password
    Получение токена"""

    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        request=LoginUserSerializer,
        responses={**login_200_resp, **login_403_resp},
    )
    def post(self, request, format=None, *args, **kwargs):
        if {"email", "password"}.issubset(request.data):
            user = authenticate(
                request,
                username=request.data["email"],
                password=request.data["password"],
            )
            if user is not None:
                if user.is_active:
                    request.user = user
                    return super(LoginView, self).post(request, format=None)
                else:
                    return JsonResponse(
                        {"Status": False, "error": "Пользователь не найден"}
                    )
            else:
                return JsonResponse(
                    {"Status": False, "Errors": "Не удалось авторизировать."},
                    status=403,
                )
        else:
            return JsonResponse(
                {
                    "Status": False,
                    "Errors": "Не указаны все необходимые аргументы.",
                },
                status=403,
            )


class ChangePassword(generics.CreateAPIView):
    @extend_schema(
        request=ResetPasswordLinkRequestSerializer,
        responses={**resp_200, **reset_password_link_403_resp},
    )
    def post(self, request, *args, **kwargs):
        if {"email"}.issubset(request.data):
            user = CustomUser.objects.filter(email=request.data["email"]).first()
            if user:
                password_reset_link_created(user_id=user.id)
                return JsonResponse({"Status": True}, status=200)
            else:
                return JsonResponse(
                    {"Status": False, "error": "Данный email не найден"},
                    status=403,
                )
        else:
            return JsonResponse({"Error": "Укажите Email"}, status=403)


@extend_schema(
    parameters=[uid_param, token_param],
    responses={**reset_password_link_200_resp, **reset_password_link_403_resp},
)
@api_view(["GET"])
def reset_password_link_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        token_obj = EmailToken.objects.filter(
            user_id=uid, key=token, purpose="reset_link"
        ).first()

        if token_obj:
            return JsonResponse(
                {"Status": True, "uid": uidb64, "token": token}, status=200
            )
        else:
            return JsonResponse(
                {
                    "Status": False,
                    "Errors": "Ссылка сброса пароля недействительна",
                },
                status=404,
                json_dumps_params={"ensure_ascii": False},
            )
    except (TypeError, ValueError, OverflowError, EmailToken.DoesNotExist):
        return JsonResponse(
            {"Status": False, "error": "Ссылка сброса пароля недействительна"},
            status=404,
            json_dumps_params={"ensure_ascii": False},
        )


class ResetPasswordView(APIView):
    @extend_schema(
        request=ResetPasswordSerializer,
        responses={**resp_200, **reset_password_403_resp},
    )
    def post(self, request, *args, **kwargs):
        if {"new_password", "new_password2"}.issubset(request.data):
            email_token = request.data.pop("token")
            uid_enc = request.data.pop("uid")
            try:
                uid = force_str(urlsafe_base64_decode(uid_enc))
                token = EmailToken.objects.filter(
                    user_id=uid, key=email_token, purpose="reset_link"
                ).first()
            except (
                TypeError,
                ValueError,
                OverflowError,
                EmailToken.DoesNotExist,
            ):
                token = None
            if token:
                now_minus_expiry_time = timezone.now() - timedelta(minutes=55)
                if token.created_at <= now_minus_expiry_time:
                    token.delete()
                    return JsonResponse(
                        {
                            "Status": False,
                            "Errors": "Срок действия токена истек и он был удален",
                        },
                        status=403,
                    )

                else:
                    if "new_password" in request.data:
                        serializer = ResetPasswordSerializer(data=request.data)
                        if serializer.is_valid():
                            new_password = serializer.validated_data["new_password"]
                            token.user.set_password(new_password)
                            token.user.save()
                            token.delete()
                            return JsonResponse({"Status": True}, status=200)
                        else:
                            return JsonResponse(
                                {
                                    "Status": False,
                                    "error": "пароли не совпадают",
                                },
                                status=403,
                            )
                    else:
                        return JsonResponse(
                            {
                                "Status": False,
                                "Errors": "Введите новый пароль",
                            },
                            status=403,
                        )
            else:
                return JsonResponse(
                    {"Status": False, "Errors": "Неверный uid или токен"},
                    status=403,
                )
        else:
            return JsonResponse(
                {
                    "Status": False,
                    "Errors": "Не указаны все необходимые аргументы",
                },
                status=403,
            )


class FreelancersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.filter(status__in=("FR", "CS"))
    serializer_class = CustomUserListSerializer
    pagination_class = FreelancersPagination
    lookup_field = "slug"
    filter_backends = (
        filters.DjangoFilterBackend,
        NullsAlwaysLastOrderingFilter,
        SearchFilter,
    )
    ordering_fields = (
        "ratings__reviews",
        "user_info__cost_of_hour_work",
        "ratings__reg_time",
        "ratings__summary",
    )
    search_fields = (
        "username",
        "user_info__company__company_name",
        "user_info__company__short_company_name",
        "user_info__company__employee_position",
        "user_info__first_name",
        "user_info__last_name",
        "user_info__father_name",
        "user_info__skill",
        "user_info__profile_description",
        "user_info__country__name",
        "user_info__specialization__name",
        "user_info__specialization__slug",
        "user_info__specialization__category__name",
        "user_info__specialization__category__slug",
        "user_info__specialization__category__activity__name",
        "user_info__specialization__category__activity__slug",
    )
    filterset_class = FreelancerFilter


class UserInfoCompanyViewSet(viewsets.ModelViewSet):
    queryset = UserInfoCompany.objects.all()
    serializer_class = UserInfoCompanySerializer
    permission_classes = [
        permissions.IsAuthenticated,
        CompanyOwner,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserSpecializationCreateViewSet(viewsets.ModelViewSet):
    queryset = UserSpecialization.objects.all()
    serializer_class = UserSpecializationSerializer
    permission_classes = (permissions.IsAuthenticated, InfoOwner)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        if self.action in ["update", "partial_update"]:
            return {"user": self.request.user, "id": self.kwargs.get("pk")}
        return super().get_serializer_context()


# class AccountDataView(APIView):
#     @extend_schema(request=None, responses=CustomUserSerializer)
#     def get(self, request, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             return JsonResponse({"Status": False, "Errors": "Требуется вход"})
#         serializer = CustomUserSerializer(self.request.user)
#         return JsonResponse(serializer.data)

#     @extend_schema(
#         request=CustomUserSerializer, responses={**resp_200, **account_data_403_resp}
#     )
#     def put(self, request, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             return JsonResponse(
#                 {"Status": False, "Errors": "Требуется вход"}, status=403
#             )
#         user_serializer = CustomUserSerializer(
#             self.request.user, data=self.request.data, partial=True
#         )
#         if user_serializer.is_valid():
#             if "email" in self.request.data:
#                 if self.request.data["email"] != request.email:
#                     current_site = get_current_site(request)
#                     user_email_change.delay(
#                         user_id=self.request.user.id,
#                         domain=str(current_site.domain),
#                         new_email=request.data["email"],
#                     )
#                     return JsonResponse({"Status": True}, status=200)
#                 else:
#                     return JsonResponse(
#                         {
#                             "Status": False,
#                             "Error": "Нельзя сменить адрес электронной почты на тот же самый",
#                         },
#                         status=403,
#                     )
#             user = user_serializer.save()
#             if "password" in request.data:
#                 try:
#                     validate_password(request.data["password"])
#                 except ValidationError:
#                     return JsonResponse({"Status": False, "Error": "password to easy"})

#                 user.set_password(request.data["password"])
#                 user.save()
#                 return JsonResponse({"Status": True}, status=200)
#             else:
#                 return JsonResponse({"Status": True}, status=200)

#         else:
#             return JsonResponse(
#                 {"Status": False, "Errors": user_serializer.errors}, status=403
#             )


# class ResetPasswordSecureToken(APIView):
#     @extend_schema(
#         request=ResetPasswordSecureTokenSerializer,
#         responses={**resp_200, **reset_password_secure_token_403_resp},
#     )
#     def post(self, request, *args, **kwargs):
#         if {"uid", "link_token"}.issubset(request.data):
#             uid = None
#             try:
#                 uid = force_str(urlsafe_base64_decode(request.data["uid"]))
#                 link_token = EmailToken.objects.filter(
#                     user_id=uid, key=request.data["link_token"], purpose="reset_link"
#                 ).first()
#             except (TypeError, ValueError, OverflowError, EmailToken.DoesNotExist):
#                 link_token = None
#             now_minus_expiry_time = timezone.now() - timedelta(hours=24)
#             if link_token:
#                 if link_token.created_at <= now_minus_expiry_time:
#                     link_token.delete()
#                     return JsonResponse(
#                         {
#                             "Status": False,
#                             "Errors": "Срок действия токена истек и он был удален",
#                         },
#                         status=403,
#                     )
#                 else:
#                     if link_token.number_of_checks == 0:
#                         link_token.number_of_checks += 1
#                         link_token.save()
#                         token = EmailToken.objects.create(user_id=uid, purpose="reset")
#                         response = JsonResponse({"Status": True}, status=200)
#                         response.set_cookie("Token", token.key, max_age=900)
#                         response.set_cookie("uid", request.data["uid"], max_age=900)
#                         link_token.delete()
#                         return response
#                     else:
#                         return JsonResponse(
#                             {"Status": False, "Errors": "Превышен лимит проверок"},
#                             status=403,
#                         )
#             else:
#                 return JsonResponse(
#                     {"Status": False, "Errors": "Неверный uid или токен"}, status=403
#                 )
#         return JsonResponse(
#             {"Status": False, "Errors": "Не указаны все необходимые аргументы"},
#             status=403,
#         )


# class ResetPasswordRequestLinkView(APIView):
#     @extend_schema(
#         request=ResetPasswordLinkRequestSerializer,
#         responses={**resp_200, **reset_password_link_403_resp},
#     )
#     def post(self, request, *args, **kwargs):
#         if {"email"}.issubset(request.data):
#             user = CustomUser.objects.filter(email=request.data["email"]).first()
#             if user:
#                 current_site = get_current_site(request)
#                 password_reset_link_created(
#                     user_id=user.id, domain=str(current_site.domain)
#                 )
#                 return JsonResponse({"Status": True}, status=200)
#             else:
#                 return JsonResponse(
#                     {"Status": False, "Errors": "Данный email не найден"}, status=403
#                 )
#         else:
#             return JsonResponse(
#                 {"Status": False, "Errors": "Не указаны все необходимые аргументы"},
#                 status=403,
#             )
