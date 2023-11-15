from rest_framework.status import HTTP_404_NOT_FOUND

from app.base.exception import BaseAppException


class NotOrderConsumerExecutorException(BaseAppException):
    default_detail = "Вы не являетесь заказчиком или исполнителем"
    status_code = HTTP_404_NOT_FOUND