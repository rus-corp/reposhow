from rest_framework.status import HTTP_404_NOT_FOUND

from app.base.exception import BaseAppException


class CustomerExecutorSameException(BaseAppException):
    default_detail = "Исполнитель не может оставить отзыв на свой заказ"
    status_code = HTTP_404_NOT_FOUND
    

class NotExecutorOrderException(BaseAppException):
    default_detail = "Нельзя добавить отзыв на заказ, который не принадлежит исполнителю"
    status_code = HTTP_404_NOT_FOUND
    
    
class NotCustomerOrderException(BaseAppException):
    default_detail = "Нельзя добавить отзыв на заказ, который не принадлежит заказчику"
    status_code = HTTP_404_NOT_FOUND
    
    
class CustomerReviewAlreadyExistException(BaseAppException):
    default_detail = "Отзыв заказчика на данный заказ уже существует"
    status_code = HTTP_404_NOT_FOUND