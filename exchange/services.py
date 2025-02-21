import importlib
from .models import Provider

class ExchangeRateService:
    """Handles provider selection and fallback mechanism."""

    PROVIDERS_MODULE = "exchange.providers"

    def __init__(self):
        self.providers = self.load_active_providers()

    def load_active_providers(self):
        """Carga los proveedores activos dinámicamente desde la base de datos."""
        providers = Provider.objects.filter(is_active=True).order_by("priority")
        provider_instances = []

        for provider in providers:
            class_name = provider.name.replace(" ", "") + "Provider"
            try:
                module = importlib.import_module(self.PROVIDERS_MODULE)
                provider_class = getattr(module, class_name)
                provider_instances.append(provider_class())  
            except (ImportError, AttributeError) as e:
                print(f"Error loading provider '{provider.name}': {e}")

        return provider_instances

    def fetch_from_providers(self, method_name, *args):
        """Generic method to call the appropriate provider's method."""
        for provider in self.providers:
            method = getattr(provider, method_name, None)
            if callable(method):
                result = method(*args)
                if result:
                    return result
        return None

    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date=None):
        return self.fetch_from_providers("get_exchange_rate", source_currency, exchanged_currency, valuation_date)

    def get_historical_exchange_rates(self, source_currency, exchanged_currency, date):
        return self.fetch_from_providers("get_historical_exchange_rates", source_currency, exchanged_currency, date)

    def get_exchange_rates_list(self, source_currency, start_date, end_date, exchanged_currencies):
        return self.fetch_from_providers("get_exchange_rates_list", source_currency, start_date, end_date, exchanged_currencies)

    def convert_currency(self, source_currency, exchange_currency, amount):
        return self.fetch_from_providers("convert_currency", source_currency, exchange_currency, amount)
