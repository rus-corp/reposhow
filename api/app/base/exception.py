from rest_framework.exceptions import APIException


class BaseAppException(APIException):
    
    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)