from celery import shared_task
from datetime import timedelta, date
from .models import Currency, CurrencyExchangeRate
from .providers import CurrencyBeaconProvider

from celery import shared_task

@shared_task
def sample_task():
    return "Celery is working!"

@shared_task
def fetch_historical_data():
    """Fetch and store historical exchange rates."""
    provider = CurrencyBeaconProvider()
    today = date.today()
    currencies = Currency.objects.all()

    for currency in currencies:
        for target_currency in currencies:
            if currency != target_currency:
                rate = provider.get_exchange_rate(currency.code, target_currency.code, today)
                if rate:
                    CurrencyExchangeRate.objects.create(
                        source_currency=currency,
                        exchanged_currency=target_currency,
                        valuation_date=today,
                        rate_value=rate
                    )
