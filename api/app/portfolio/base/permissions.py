from app.base.permissions import BaseAppPermission
from app.portfolio.models import Work


class IsPortfolioOwner(BaseAppPermission):

    def has_object_permission(self, request, view, obj: Work):
        return request.user == obj.user