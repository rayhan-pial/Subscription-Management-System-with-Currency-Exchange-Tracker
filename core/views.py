from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)
from core.models import Subscription, Plan
from rest_framework.response import Response
from core.serializers import SubscriptionSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from rest_framework.views import APIView
import requests
from subscription_project.settings import EXCHANGE_RATE_API_KEY, EXCHANGE_RATE_API_URL


class CreateSubscriptionView(CreateAPIView):

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        current_datetime = datetime.now()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan = get_object_or_404(Plan, pk=request.data.get("plan"))
        end_date = current_datetime + timedelta(days=plan.duration_days)

        subscription = serializer.save(user=request.user, end_date=end_date)

        return Response(
            {
                "message": "Subscription created successfully.",
                "subscription": SubscriptionSerializer(subscription).data,
            },
            status=HTTP_201_CREATED,
        )


class UserSubscriptionsView(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response({"subscriptions": serializer.data})


class CancelSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        subscription_id = request.data.get("subscription_id")

        if not subscription_id:
            return Response(
                {"error": "A 'subscription_id' must be provided."},
                status=HTTP_400_BAD_REQUEST,
            )

        try:
            subscription = Subscription.objects.get(
                id=subscription_id, user=request.user
            )
        except Subscription.DoesNotExist:
            return Response(
                {
                    "error": "Subscription not found or you do not have permission to cancel it."
                },
                status=HTTP_404_NOT_FOUND,
            )

        subscription.status = Subscription.CANCELLED
        subscription.save()

        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=HTTP_200_OK)


class ExchangeRateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        base_currency = request.query_params.get("base_currency").upper()
        target_currency = request.query_params.get("target_currency").upper()

        if not base_currency or not target_currency:
            return Response(
                {"error": "Both base and target currencies are required."},
                status=HTTP_400_BAD_REQUEST,
            )

        try:

            url = f"{EXCHANGE_RATE_API_URL}/{EXCHANGE_RATE_API_KEY}/latest/{base_currency}"

            response = requests.get(url, timeout=10)
            data = response.json()

            if data.get("result") != "success":
                raise Exception("Something went wrong while fetching exchange rate.")

            conversion_rates = data.get("conversion_rates", {})

            if target_currency not in conversion_rates:
                return Response(
                    {"error": "Exchange rate not found."}, status=HTTP_400_BAD_REQUEST
                )

            exchange_rate = conversion_rates[target_currency]
            return Response(
                {"message": f"1 {base_currency} = {exchange_rate} {target_currency}."},
                status=HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
