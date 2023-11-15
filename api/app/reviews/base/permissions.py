from app.base.permissions import BaseAppPermission
from app.reviews.models import Review


class IsReviewOwner(BaseAppPermission):

    def has_object_permission(self, request, view, obj: Review):
        return request.user.pk == obj.customer.id