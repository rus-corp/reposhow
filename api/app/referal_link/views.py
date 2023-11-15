from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from app.referal_link.models import ReferalLinkResponse
from app.main_users.models import CustomUser
from app.referal_link.serializers import ReferalLinkSerializer


class ReferalLinkViewSet(RetrieveAPIView, UpdateAPIView):
    queryset = ReferalLinkResponse.objects.all()
    serializer_class = ReferalLinkSerializer
    lookup_field = None

    @staticmethod
    def get_founders_list():
        return list(
            CustomUser.objects.filter(founder=True).extra(order_by=("id",))
        )

    def get_object(self):
        if ReferalLinkResponse.objects.first():
            return ReferalLinkResponse.objects.first()
        user = ReferalLinkViewSet.get_founders_list()[0]
        return ReferalLinkResponse.objects.create(
            user=user, referal_link=user.referal_link
        )

    def perform_update(self, serializer, user):
        serializer.save(user=user, referal_link=user.referal_link)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, instance=self.get_object()
        )
        if serializer.is_valid():
            founder_list = ReferalLinkViewSet.get_founders_list()
            founder_index = founder_list.index(self.get_object().user)
            if founder_index + 1 == len(founder_list):
                founder_index = -1
            self.perform_update(
                serializer, user=founder_list[founder_index + 1]
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@transaction.atomic()
def check_over():
    list_over = []
    clients = CustomUser.objects.all()
    for client in clients:
        status_old = client.status.id
        client.status_update(constans_reference.CLIENT_NOT_PAYMENT)
        client. save()
        Overdue.objects.get_or_create(telegram_id=client. telegram_id)
        if status_old in [constans_reference. TEST_CLIENT, constans_reference. CLIENT_PAYMENT]:
            send_message = SendMessage(telegram_id=client.telegram_id)
            send_message. send message ("Bawa nognmcka BAKOHYMMACb)
        list_overdue.append(client.telegram_id)
        overdue_handler (list_overdue)
        return True