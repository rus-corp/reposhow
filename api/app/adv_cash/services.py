import hashlib
from typing import Any, Type
from datetime import datetime
from hashlib import sha256
from zeep.client import Client
from decimal import Decimal

from django.db import transaction
from django.conf import settings

from app.adv_cash.exceptions import (
    InsufficientFundsWithdrawalException,
    AccountBalanceDoesNotExists,
    InvalidTransactionSignature,
)
from app.adv_cash.models import (
    Transaction,
    WithdrawalEcurrencyTransaction,
    BlackListTransactionsHash,
)
from app.accounts.models import Account


class AdvCashAPIClient:
    __transaction_model = Transaction
    __user_acc_model = Account

    wsdl = "https://wallet.advcash.com/wsm/merchantWebService?wsdl"

    USD = "USD"
    RUR = "RUR"
    EUR = "EUR"
    GBP = "GBP"
    UAH = "UAH"
    KZT = "KZT"
    BRL = "BRL"

    def __init__(self, api_name: str, api_secret: str, account_email: str):
        self.api_name = api_name
        self.api_secret = api_secret
        self.account_email = account_email
        self.client = Client(self.wsdl)

    def make_auth_token(self) -> str:
        """
        Делает sha256 из пароля API:Дата UTC в формате YYYYMMDD:Время UTC в формате HH (только часы, не минуты)
        как это требуется для Merchant API
        :return: str
        """
        now_str = datetime.utcnow().strftime("%Y%m%d:%H")
        encoded_string = "{}:{}".format(self.api_secret, now_str).encode("utf8")
        return sha256(encoded_string).hexdigest()

    def make_auth_params(self) -> dict:
        return {
            "apiName": self.api_name,
            "authenticationToken": self.make_auth_token(),
            "accountEmail": self.account_email,
        }

    def make_request(self, action_name: str, params: dict = None):
        action = getattr(self.client.service, action_name)
        if params:
            response = action(self.make_auth_params(), params)
            return response
        return action(self.make_auth_params())

    def get_balances(self) -> dict:
        """
        :return: dict {"account number": amount, ...}
        """
        response = self.make_request("getBalances")
        print(response)
        return {i["id"]: i["amount"] for i in response}

    def send_money(self, to: str, amount: Any, currency: str, note: str = "") -> str:
        """
        :param to: str номер счета или e-mail
        :param amount: Любая с точностью до 2 пунктов
        :param валюта: str одна из доступных валют
        :param note: str примечание к транзакции
        :return: str идентификатор транзакции
        """
        params = {
            "amount": amount,
            "currency": currency,
            "note": note,
            "savePaymentTemplate": False,
        }
        if "@" in to:
            params.update(email=to)
        else:
            params.update(walletId=to)
        return self.make_request("sendMoney", params)

    @classmethod
    def _save_transaction(
        cls,
        user,
        currency,
        amount,
        bank_card,
        expiry_month,
        expiry_year,
        note,
        user_acc,
    ) -> None:
        cls.__transaction_model.objects.create(
            user=user,
            currency=currency,
            amount=amount,
            bank_card=bank_card,
            expiry_month=expiry_month,
            expiry_year=expiry_year,
            note=note,
            user_acc=user_acc,
        )

    @transaction.atomic
    def send_to_bank_card(
        self,
        user,
        bank_card: str,
        amount: Any,
        currency: str,
        expiry_month: int,
        expiry_year: int = None,
        note: str = None,
        save_payment_template: bool = False,
    ):
        params = {
            "amount": amount,
            "currency": currency,
            "cardNumber": bank_card,
            "expiryMonth": expiry_month,
            "expiryYear": expiry_year,
            "note": note,
            "savePaymentTemplate": save_payment_template,
        }
        response = self.make_request("sendMoneyToBankCard", params)
        if response:
            try:
                account = user
                account = self.update_balance(user, currency, amount)
                self._save_transaction(
                    user=user,
                    currency=currency,
                    amount=amount,
                    bank_card=bank_card,
                    expiry_month=expiry_month,
                    expiry_year=expiry_year,
                    note=note,
                    user_acc=account,
                )
            except self.__user_acc_model.DoesNotExist:
                pass
        return response

    def update_balance(self, user, currency, amount):
        if currency == "RUR":
            user.rub_acc.balance -= Decimal(amount)
            user.rub_acc.save()
            return user.rub_acc
        elif currency == "USD":
            user.usd_acc.balance -= Decimal(amount)
            user.usd_acc.save()
            return user.usd_acc
        elif currency == "EUR":
            user.eur_acc.balance -= Decimal(amount)
            user.eur_acc.save()
            return user.eur_acc


class WithdrawFundsService(object):
    @classmethod
    def check_account_balance(cls, user, currency, amount):
        currency_to_balance = {
            "RUR": user.rub_acc.balance,
            "USD": user.usd_acc.balance,
            "EUR": user.eur_acc.balance,
        }
        if not currency in currency_to_balance:
            raise AccountBalanceDoesNotExists()
        if currency_to_balance[currency] < amount:
            raise InsufficientFundsWithdrawalException()

    @classmethod
    def validate_send_to_bank_card(cls, data):
        user = data.get("user")
        currency = data.get("currency")
        amount = data.get("amount")
        cls.check_account_balance(user=user, currency=currency, amount=amount)


class WithdrawalEcurrencyOperationsService(object):
    def _is_exact_amount(data) -> bool:
        return "amount" in data and "currency" in data

    def _is_ecurrency(data) -> bool:
        return "ecurrency" in data

    def _is_ripple(ecurrency) -> bool:
        return ecurrency == "RIPPLE"


class WithdrawalEcurrencyOperationsService(object):
    __ecurrency_transaction_model = WithdrawalEcurrencyTransaction

    @classmethod
    @transaction.atomic
    def create_ecurrency_withdrawal(
        cls, client: Type[AdvCashAPIClient], data: dict, user
    ) -> bool:
        amount = (
            data.get("amount") if "amount" in data else data.get("cryptoCurrencyAmount")
        )

        WithdrawFundsService.check_account_balance(
            user=user, currency=data.get("currency"), amount=amount
        )

        user_acc = client.update_balance(
            user=user, currency=data.get("currency"), amount=amount
        )

        params = {
            "receiver": data.get("receiver"),
            "orderId": data.get("orderId"),
            "note": data.get("note"),
            "currency": data.get("currency"),
        }

        if "amount" in data:
            params["amount"] = data["amount"]
        else:
            params["cryptoCurrencyAmount"] = data["cryptoCurrencyAmount"]

        if "ecurrency" in data:
            params["ecurrency"] = data["ecurrency"]
            if data.get("ecurrency") == "RIPPLE":
                params["destinationTag"] = data.get("destinationTag")
        cls._save_ecurrency_transaction(
            user=user,
            user_acc=user_acc,
            amount=data.get("amount"),
            cryptoCurrencyAmount=data.get("cryptoCurrencyAmount"),
            currency=data.get("currency"),
            ecurrency=data.get("ecurrency"),
            receiver=data.get("receiver"),
            destinationTag=data.get("destinationTag"),
            orderId=data.get("orderId"),
            note=data.get("note"),
        )
        return client.make_request("sendMoneyToEcurrency", params)

    @classmethod
    def _save_ecurrency_transaction(cls, **kwargs):
        cls.__ecurrency_transaction_model.objects.create(**kwargs)


class AdvCashDepositFundsCallbackService:
    __black_list_model = BlackListTransactionsHash

    CURRENCY_ACCOUNT_MAP = {
        "RUR": "rub_acc",
        "USD": "usd_acc",
        "EUR": "eur_acc",
    }

    @classmethod
    @transaction.atomic
    def is_valid_transaction_signature(cls, data, user):
        signature_string = (
            f"{data['ac_transfer']}:{data['ac_start_date']}:{data['ac_sci_name']}:"
            f"{data['ac_src_wallet']}:{data['ac_dest_wallet']}:{data['ac_order_id']}:"
            f"{data['ac_amount']}:{data['ac_currency']}:{settings.ADV_PASSWORD}"
        )
        generated_signature = hashlib.sha256(
            signature_string.encode("utf-8")
        ).hexdigest()
        if generated_signature != data.get("ac_hash"):
            raise InvalidTransactionSignature()
        if cls.__black_list_model.objects.filter(ac_hash=generated_signature).exists():
            raise InvalidTransactionSignature()

        cls._replenish_account(
            currency=data["ac_currency"], amount=data["ac_amount"], user=user
        )
        cls.__black_list_model.objects.create(ac_hash=generated_signature)

    @classmethod
    def _replenish_account(cls, currency, amount, user) -> None:
        account_attribute = cls.CURRENCY_ACCOUNT_MAP.get(currency)

        if not account_attribute:
            raise AccountBalanceDoesNotExists()
        account = getattr(user, account_attribute)
        account.balance += Decimal(amount)
        account.save()

        return account
