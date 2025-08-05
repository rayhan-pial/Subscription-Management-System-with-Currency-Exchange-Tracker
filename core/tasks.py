from celery import shared_task
from subscription_project.settings import EXCHANGE_RATE_API_KEY, EXCHANGE_RATE_API_URL
from decimal import Decimal
import requests
from .models import ExchangeRateLog


@shared_task
def fetch_usd_to_bdt_rate():
    """
    Periodic task to fetch USD to BDT exchange rate
    """
    try:
        base_currency = "USD"
        target_currency = "BDT"

        url = f"{EXCHANGE_RATE_API_URL}/{EXCHANGE_RATE_API_KEY}/latest/{base_currency}"

        response = requests.get(url, timeout=10)

        data = response.json()

        if data.get("result") != "success":
            raise Exception("Something went wrong while fetching exchange rate.")

        conversion_rates = data.get("conversion_rates", {})

        if target_currency not in conversion_rates:
            raise Exception(f"Rate for {target_currency} not found in response")

        exchange_rate = Decimal(conversion_rates[target_currency])

        ExchangeRateLog.objects.create(
            base_currency=base_currency,
            target_currency=target_currency,
            rate=exchange_rate,
        )

        return {"message": "Saved exchange rate"}

    except Exception as e:
        response = {"status": "Failed", "error": str(e)}
