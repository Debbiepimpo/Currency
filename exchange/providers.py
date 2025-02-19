import requests
import random
from datetime import date


class ExchangeRateProvider:
    """Base class for exchange rate providers."""

    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        raise NotImplementedError("This method should be implemented in subclasses.")


class CurrencyBeaconProvider(ExchangeRateProvider):
    """Fetch exchange rates from CurrencyBeacon API."""

    API_URL = "https://api.currencybeacon.com/v1/latest"
    API_KEY = "WIzPqKNxhGUaoztYMz7v4NPTtTUPWR8q"

    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        params = {
                'base'   : source_currency,
                'symbols': exchanged_currency,
                'apikey' : self.API_KEY
        }
        response = requests.get(self.API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get('rates', {}).get(exchanged_currency)
        return None


class MockExchangeRateProvider(ExchangeRateProvider):
    """Generate random exchange rate for testing."""

    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        return round(random.uniform(0.5, 1.5), 6)


# Function to get data using the provider
def get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider):
    return provider.get_exchange_rate(source_currency, exchanged_currency, valuation_date)
