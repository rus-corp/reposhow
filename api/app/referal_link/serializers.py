from rest_framework import serializers
from app.referal_link.models import ReferalLinkResponse


class ReferalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferalLinkResponse
        fields = ('referal_link', 'user')
        read_only_fields = ('referal_link', 'user')
