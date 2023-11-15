from enum import Enum


class RestAction(str, Enum):
    LIST = "list"
    CREATE = "create"
    RETRIEVE = "retrieve"
    UPDATE = "update"
    PARTIAL_UPDATE = "partial_update"
    DESTROY = "destroy"


class HttpMethods(str, Enum):
    POST = "post"
    GET = "get"
    PATCH = "patch"
    DELETE = "delete"
    