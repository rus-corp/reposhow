from django.shortcuts import render
from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework import permissions, views
from decimal import Decimal
from drf_spectacular.utils import extend_schema, OpenApiParameter
import uuid
from datetime import datetime

from app.accounts.models import Account
from app.accounts.operations import transfer_money
from .serializers import (
    CurrencySerializer,
    PaymentAgregatorSerializer,
    PaymentMethodSerializer,
    TransferMoneyToUserSerializer,
    TinkofDataRequestSerializer,
    WithdrawalEcurrencySerializer,
    WithdrawFundsSerializer,
    AdvCashDepositFundsCallbackSerializer,
)

from .models import PaymentMethod, PaymentAgregator, TinkofPayment, Currency
from .pay import create_payment_session
from app.accounts.operations import transfer_money, generate_payment_purpose
from app.main_users.models import CustomUser

from app.adv_cash.services import (
    AdvCashAPIClient,
    WithdrawFundsService,
    WithdrawalEcurrencyOperationsService,
    AdvCashDepositFundsCallbackService,
)
from app.adv_cash.exceptions import InsufficientFundsWithdrawalException


class TransferMoneyToUserView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TransferMoneyToUserSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        currency = request.data.get("currency")
        try:
            amount = Decimal(request.data.get("amount"))
            if currency == "RUB":
                from_acc = user.rub_acc
            elif currency == "USD":
                from_acc = user.usd_acc
            else:
                from_acc = user.eur_acc

            to_acc = request.data.get("to_account")

            try:
                to_acc = Account.objects.get(account_name=to_acc, currency=currency)
                if from_acc.balance < amount:
                    return Response(
                        {"Error": _("not enough funds in the account")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                transfer_money(
                    from_acc=from_acc,
                    to_acc=to_acc,
                    amount=amount,
                    currency=currency,
                    purpose="TU",
                )
                return Response(
                    {"Status": True, "message": _("transfer completed")},
                    status=status.HTTP_200_OK,
                )
            except Account.DoesNotExist:
                return Response(
                    {"Status": False, "error": _("Account not found")},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError:
            return Response(
                {"Status": False, "error": _("Invalid amount")},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PaymentCurrencyView(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (permissions.IsAuthenticated,)


class PaymentMethodView(generics.ListAPIView):
    queryset = PaymentMethod.objects.none()
    serializer_class = PaymentMethodSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, currency):
        user = request.user
        user_currency_data = {
            "paid_rub": user.paid_entrance_rub,
            "paid_usd": user.paid_entrance_usd,
            "paid_eur": user.paid_entrance_eur,
        }

        try:
            currency = Currency.objects.get(name=currency)
        except Currency.DoesNotExist:
            return Response({"Status": False, "error": "Currency does not exist"})
        method = PaymentMethod.objects.filter(currency=currency)
        serializer = PaymentMethodSerializer(method, many=True)
        serializer_data = serializer.data
        for method_data in serializer_data:
            method_data.update(user_currency_data)
        return Response(serializer_data)


class PaymentAgregatorView(generics.ListAPIView):
    queryset = PaymentAgregator.objects.none()
    serializer_class = PaymentAgregatorSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, method):
        user = request.user.id
        try:
            method = PaymentMethod.objects.get(name=method)
        except PaymentMethod.DoesNotExist:
            return Response({"Status": False, "error": "Payment method does not exist"})
        agregator = PaymentAgregator.objects.filter(method=method)
        serializer = PaymentAgregatorSerializer(agregator, many=True)
        return Response(serializer.data)


# class TinkofPaymentRequestView(views.APIView):
#     permission_classes = (permissions.IsAuthenticated,)

#     def post(self, request, format=None):
#         user = request.user
#         amount_req = request.data.get("amount")
#         amount_str = str(amount_req) + "00"
#         amount = int(amount_str)
#         agregator = PaymentAgregator.objects.get(name="TINKOFF")
#         order_date = datetime.now().strftime("%d%m%H%M")
#         order_id = f"{agregator.account}{user.rub_acc}{order_date}"
#         user_payment_data = {
#             "RUB": user.paid_entrance_rub,
#             "USD": user.paid_entrance_usd,
#             "EUR": user.paid_entrance_eur,
#         }
#         user_payment_one_true = any(user_payment_data.values())
#         if user_payment_one_true:
#             description = generate_payment_purpose("RA", user.rub_acc)
#         else:
#             description = generate_payment_purpose("EF", user.rub_acc)
#         tinkof_pay = TinkofPayment.objects.create(
#             user_acc=user.rub_acc,
#             order_id=order_id,
#             order_status="NEW",
#             amount=amount_req,
#             description=description,
#         )

#         response = create_payment_session(
#             amount=amount, order_id=order_id, description=description
#         )
#         if not response["Success"]:
#             return Response(
#                 {"Status": False, "error": "Payment has not been made"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         else:
#             link = response["PaymentURL"]
#             return Response({"Status": True, "link": link}, status=status.HTTP_200_OK)


# class TinkofPaymentResultView(generics.CreateAPIView):
#     serializer_class = TinkofDataRequestSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             validated_data = serializer.validated_data
#             order_id = validated_data["OrderId"]
#             order_status = validated_data["Status"]
#             amount_req = validated_data["Amount"]
#             amount_without_cop = amount_req // 100
#             amount = int(amount_without_cop / 1.0253)
#             agregator = order_id[:14]
#             user_acc = order_id[14:29]
#             agregator_acc = Account.objects.get(account_name=agregator)
#             user_account = Account.objects.get(account_name=user_acc)
#             payment = TinkofPayment.objects.get(order_id=order_id)
#             if order_status == "CONFIRMED":
#                 if payment.confirmed:
#                     return Response(status=status.HTTP_200_OK)
#                 else:
#                     user = user_account.rub_acc
#                     payment.confirmed = True
#                     payment.save()
#                     agregator_acc.balance += amount
#                     agregator_acc.save()
#                     if "Оплата" in payment.description:
#                         transfer_money(
#                             from_acc=agregator_acc,
#                             to_acc=user_account,
#                             amount=amount_without_cop,
#                             currency="RUB",
#                             purpose="EF",
#                         )
#                         user.money_transfer_to_fund_parent("RUB")
#                         user.save()
#                     else:
#                         transfer_money(
#                             from_acc=agregator_acc,
#                             to_acc=user_account,
#                             amount=amount,
#                             currency="RUB",
#                             purpose="RA",
#                         )
#                     static_status = 'OK'
#                     return Response(status=status.HTTP_200_OK)
#             else:
#                 return Response({"Status": False, "error": "Payment has not been made"})
#         else:
#             return Response(
#                 {"Status": False, "error": serializer.error_messages},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )


class WithdrawFundsView(generics.CreateAPIView):
    serializer_class = WithdrawFundsSerializer
    adv_cash_client = AdvCashAPIClient(
        api_name=settings.ADV_API_NAME,
        api_secret=settings.ADV_PASSWORD,
        account_email=settings.ADV_ACCOUNT_EMAIL,
    )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = self.request.user

            try:
                WithdrawFundsService.check_account_balance(
                    user=user, currency=data.get("currency"), amount=data.get("amount")
                )

                self.adv_cash_client.send_to_bank_card(
                    user=user,
                    bank_card=data.get("bank_card"),
                    amount=data.get("amount"),
                    currency=data.get("currency"),
                    expiry_month=data.get("expiry_month"),
                    expiry_year=data.get("expiry_year"),
                    note=data.get("note"),
                )

                return Response(
                    {"detail": "Средства успешно выведены"}, status=status.HTTP_200_OK
                )
            except InsufficientFundsWithdrawalException:
                return Response(
                    {"detail": "Недостаточно средств на счете"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawalEcurrencyAPIView(generics.CreateAPIView):
    serializer_class = WithdrawalEcurrencySerializer
    adv_cash_client = AdvCashAPIClient(
        api_name=settings.ADV_API_NAME,
        api_secret=settings.ADV_PASSWORD,
        account_email=settings.ADV_ACCOUNT_EMAIL,
    )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            user = self.request.user
            try:
                WithdrawalEcurrencyOperationsService.create_ecurrency_withdrawal(
                    client=self.adv_cash_client, data=data, user=user
                )
                return Response(
                    {"detail": "Средства успешно выведены"}, status=status.HTTP_200_OK
                )
            except InsufficientFundsWithdrawalException:
                return Response(
                    {"detail": "Недостаточно средств на счете"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class AdvCashDepositFundsCallbackView(generics.CreateAPIView):
    serializer_class = AdvCashDepositFundsCallbackSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            user = self.request.user
            try:
                AdvCashDepositFundsCallbackService.is_valid_transaction_signature(
                    data=data, user=user
                )
                return Response({"detail": "Успешно"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
