from rest_framework import serializers
from django.db.models import Sum

from app.raiting.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    summary = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = (
            'reg_time',
            'orders',
            'contest',
            'peace_orders',
            'arbit',
            'wins',
            'wins_1_place_value',
            'wins_2_place_value',
            'wins_3_place_value',
            'reviews',
            'review_positive_value',
            'review_negative_value',
            'reply_time',
            'vote_participation',
            'vote_participation_value',
            'vote_ignore_value',
            'freelancer',
            'summary',
        )
        extra_kwargs = {
            'freelancer': {'write_only': True},
        }

    def get_summary(self, instance):
        _sum = 0
        values = [
            instance.reg_time,
            instance.orders,
            instance.peace_orders,
            instance.arbit,
            instance.contest,
            instance.wins,
            instance.reviews,
            instance.reply_time,
            instance.vote_participation,
        ]
        for value in values:
            if value:
                _sum += value
        return _sum
