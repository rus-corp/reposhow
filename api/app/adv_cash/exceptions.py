from rest_framework import exceptions

from django.utils.translation import gettext_lazy as _

class InsufficientFundsWithdrawalException(exceptions.APIException):
    default_detail = _("Недостаточность средств для вывода средств")
    status_code = 400


class AccountBalanceDoesNotExists(exceptions.APIException):
    default_detail = _("Выбранный счет не найден")
    status_code = 400

class InvalidTransactionSignature(exceptions.APIException):
    default_detail = _("Недопустимая подпись")
    status_code = 400
