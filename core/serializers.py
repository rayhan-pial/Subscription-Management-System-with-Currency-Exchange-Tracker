from rest_framework import serializers
from .models import Subscription, ExchangeRateLog


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = ("user", "end_date")


class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRateLog
        fields = "__all__"
        read_only_fields = ("rate", "fetched_at")
