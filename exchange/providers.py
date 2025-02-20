import requests
import random
from datetime import date


class ExchangeRateProvider:
    """Base class for exchange rate providers."""

    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        raise NotImplementedError("This method should be implemented in subclasses.")


class CurrencyBeaconProvider:
    """Fetch exchange rates from CurrencyBeacon API."""

    API_URL = "https://api.currencybeacon.com/v1"
    API_KEY = "WIzPqKNxhGUaoztYMz7v4NPTtTUPWR8q"

    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date=None):
        """
        Fetches exchange rate from CurrencyBeacon API.
        If `valuation_date` is None, fetches the latest rate.
        """
        endpoint = "/latest" if valuation_date is None else "/historical"
        params = {
            'base': source_currency,
            'symbols': exchanged_currency,
            'apikey': self.API_KEY
        }
        
        # If there is valuation date we add it
        if valuation_date:
            params['date'] = valuation_date.strftime("%Y-%m-%d")

        response = requests.get(f"{self.API_URL}{endpoint}", params=params)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('rates', {}).get(exchanged_currency)
        
        return None  # If API not respond propery we return None

    def get_historical_exchange_rates(self, source_currency, exchanged_currency, date_from, date_to):
        """
        Retrieves historical exchange rates for a date range.
        """
        rates = {}
        current_date = datetime.strptime(date_from, "%Y-%m-%d")

        while current_date <= datetime.strptime(date_to, "%Y-%m-%d"):
            formatted_date = current_date.strftime("%Y-%m-%d")
            params = {
                'base': source_currency,
                'symbols': exchanged_currency,
                'date': formatted_date,
                'apikey': self.API_KEY
            }
            response = requests.get(f"{self.API_URL}/historical", params=params)
            
            if response.status_code == 200:
                data = response.json()
                rates[formatted_date] = data.get('rates', {}).get(exchanged_currency)
            else:
                rates[formatted_date] = None  # Manejo de error
            
            current_date += timedelta(days=1)

        return rates


class MockExchangeRateProvider(ExchangeRateProvider):
    """Generate random exchange rate for testing."""

    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        return round(random.uniform(0.5, 1.5), 6)


# Function to get data using the provider
def get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider):
    return provider.get_exchange_rate(source_currency, exchanged_currency, valuation_date)
