from app.raiting.serializers import RatingSerializer
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework import permissions

from app.raiting.models import Rating
from app.main_users.permissions import IsOwner


class RatingViewSet(RetrieveAPIView, UpdateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsOwner, permissions.IsAuthenticatedOrReadOnly)
    http_method_names = ['get', 'patch']

    def get_object(self):
        return Rating.objects.get(freelancer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            freelancer=self.request.user
        )
