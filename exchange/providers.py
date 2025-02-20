import requests
import random
from urllib.parse import urlencode
from datetime import date, datetime, timedelta
from .models import Currency


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
        endpoint = "/latest"
        if source_currency is None:
            try:
                source_currency = Currency.objects.get(default=True).code  # Se obtiene el código
            except Currency.DoesNotExist:
                raise ValueError("No default currency is set in the database.")

        exchanged_currencies = list(
            Currency.objects.exclude(code=source_currency).values_list("code", flat=True)
        )
        symbols_param = ",".join(exchanged_currencies)
        
        params = {
            'api_key': self.API_KEY,
            'base': source_currency,
            'symbols': symbols_param,
            
        }
        
        # If there is valuation date we add it
        if valuation_date:
            params['date'] = valuation_date.strftime("%Y-%m-%d")
        
        url = f"{self.API_URL}{endpoint}?{urlencode(params)}"
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", {})

            if isinstance(rates, list):
                rates = {entry["code"]: entry["rate"] for entry in rates}

            return rates
        
        return None  # If API not respond propery we return None

    def get_historical_exchange_rates(self, source_currency, exchanged_currency, date):
        """
        Retrieves historical exchange rates for a date range.
        """
        endpoint = "/latest"
        current_date = datetime.today().date()
        if source_currency is None:
            try:
                source_currency = Currency.objects.get(default=True).code  # Se obtiene el código
            except Currency.DoesNotExist:
                raise ValueError("No default currency is set in the database.")

        exchanged_currencies = list(
            Currency.objects.exclude(code=source_currency).values_list("code", flat=True)
        )
        symbols_param = ",".join(exchanged_currencies)
        
        formatted_date = date.strftime("%Y-%m-%d")
        params = {
            'api_key': self.API_KEY,
            'base': source_currency,
            'date': formatted_date,
            'symbols': exchanged_currency,
        }
        
        url = f"{self.API_URL}{endpoint}?{urlencode(params)}"

        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", {})

            if isinstance(rates, list):
                rates = {entry["code"]: entry["rate"] for entry in rates}

            current_date += timedelta(days=1)
            return rates
        
        return None
    
    def get_exchange_rates_list(self, source_currency=None, start_date=None, end_date=None, exchanged_currencies=None):
        """
        Retrieves exchange rates for a given time period.
        - If `source_currency` is None, fetches the default currency from DB.
        - If `exchanged_currencies` is None, fetches all except `source_currency`.
        """
        endpoint = "/timeseries"

        if source_currency is None:
            try:
                source_currency = Currency.objects.get(default=True).code
            except Currency.DoesNotExist:
                raise ValueError("No default currency is set in the database.")

        if start_date is None or end_date is None:
            raise ValueError("Both 'start_date' and 'end_date' must be provided.")

        if exchanged_currencies is None:
            exchanged_currencies = list(
                Currency.objects.exclude(code=source_currency).values_list("code", flat=True)
            )

        symbols_param = ",".join(exchanged_currencies)

  
        params = {
            'api_key': self.API_KEY,
            'base': source_currency,
            'start_date': start_date.strftime("%Y-%m-%d"),
            'end_date': end_date.strftime("%Y-%m-%d"),
            'symbols': symbols_param,
        }

        url = f"{self.API_URL}{endpoint}"

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data.get("response", {})

        return None

    def convert_currency(self, source_currency, exchange_currency, amount):
        """
        Converts an amount from one currency to another using CurrencyBeacon API.
        """
        endpoint = "/convert"
        if source_currency is None:
            try:
                source_currency = Currency.objects.get(default=True).code
            except Currency.DoesNotExist:
                raise ValueError("No default currency is set in the database.")
        else:
            source_currency


        if exchange_currency is None:
            raise ValueError("No exchange currency provided.")
        
        if amount is None:
            raise ValueError("Can get any amount")

        
        params = {
            "api_key": self.API_KEY,
            "from": source_currency,
            "to": exchange_currency,
            "amount": amount
        }

        url = f"{self.API_URL}{endpoint}?{urlencode(params)}"

        try:
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                if "error" in data:
                    return None
                return data.get("value")

            return None

        except requests.exceptions.RequestException as e:
            return {"error": f"Request Exception: {str(e)}"}

class MockExchangeRateProvider(ExchangeRateProvider):
    """Generate random exchange rate for testing."""

    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        return round(random.uniform(0.5, 1.5), 6)


# Function to get data using the provider
def get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider):
    return provider.get_exchange_rate(source_currency, exchanged_currency, valuation_date)
