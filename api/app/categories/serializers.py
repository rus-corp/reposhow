import logging

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field


from .models import Activity, Category, Specialization
from app.main_users.models import CustomUser


log = logging.getLogger(__name__)


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ["id", "name", "slug"]


class CategorySerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True)
    user_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "user_count", "activity"]


    @extend_schema_field(serializers.IntegerField())
    def get_user_count(self, category):
        try:
            return CustomUser.objects.filter(
                user_info__specialization__category__slug=category.slug
            ).count()
        except AttributeError as e:
            log.error(e, self, category)
            return None


class SpecializationSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    user_count = serializers.SerializerMethodField()

    class Meta:
        model = Specialization
        fields = [
            "id",
            "name",
            "slug",
            "user_count",
            "category",
        ]
        read_only_fields = ["slug"]

    @extend_schema_field(serializers.IntegerField())
    def get_user_count(self, obj):
        try:
            return CustomUser.objects.filter(
                user_info__specialization__slug=obj.slug
            ).count()
        except AttributeError as e:
            log.error(e, self, obj)
            return None
