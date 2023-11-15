from django.conf import settings
from rest_framework.status import HTTP_404_NOT_FOUND

from app.base.exception import BaseAppException


class BestWorkLimitExceedException(BaseAppException):
    default_detail = f"Количество лучших работ не более {settings.ACCEPT_BEST_WORKS}"
    status_code = HTTP_404_NOT_FOUND
    

class WorkStatusNotCompletedException(BaseAppException):
    default_detail = "Заказ не выполнен"
    status_code = HTTP_404_NOT_FOUND
    

class OrderAlreadyInCurrentWorkException(BaseAppException):
    default_detail = "Работа уже присутсвует в текущих"
    status_code = HTTP_404_NOT_FOUND
    

class NotOwnerOfOrderException(BaseAppException):
    default_detail = "Заказ выполнен не вами"
    status_code = HTTP_404_NOT_FOUND


class TablePlaceOutOfRangeException(BaseAppException):
    default_detail = "Номер заказа указан не верно"
    status_code = HTTP_404_NOT_FOUND

class TablePlaceAlreadyTakenException(BaseAppException):
    default_detail = "Место в таблице уже занято"
    status_code = HTTP_404_NOT_FOUND