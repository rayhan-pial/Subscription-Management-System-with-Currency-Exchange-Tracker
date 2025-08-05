from django.urls import path
from core.views import (
    CreateSubscriptionView,
    UserSubscriptionsView,
    CancelSubscriptionAPIView,
    ExchangeRateAPIView,
)

urlpatterns = [
    path("subscribe/", CreateSubscriptionView.as_view(), name="create_subscription"),
    path("subscriptions/", UserSubscriptionsView.as_view(), name="user_subscriptions"),
    path("cancel/", CancelSubscriptionAPIView.as_view(), name="cancel_subscription"),
    path("exchange-rate/", ExchangeRateAPIView.as_view(), name="exchange_rate"),
]
