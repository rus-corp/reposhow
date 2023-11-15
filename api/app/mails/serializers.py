from rest_framework import serializers

from app.mails.models import UserMailPermissions


class MailPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMailPermissions
        fields = (
            "account_refill",
            "customers_offers",
            "freelancers_responses",
            "reviews",
            "votes",
            "chat",
            "news",
        )
        lookup_field = 'user__slug'

    def update(self, instance, validated_data):
        [setattr(
            instance, field, value
        ) for field, value in validated_data.items()]
        instance.save()
        return super().update(instance, validated_data)
