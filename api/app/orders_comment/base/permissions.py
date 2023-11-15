from app.base.permissions import BaseAppPermission
from app.orders.models import OrderResponseComment


class IsOrderResponseCommentOwner(BaseAppPermission):

    def has_object_permission(self, request, view, obj: OrderResponseComment):
        user_id = request.user.id
        return any([self._check_customer(user_id, obj), self._check_executor(user_id, obj)])
    
    def _check_customer(self, customer_id: int, obj: OrderResponseComment):
        return obj.order_response.order.customer == customer_id
    
    def _check_executor(self, executor_id: int, obj: OrderResponseComment):
        return len(obj.order_response.order.executor.filter(id=executor_id)) > 0