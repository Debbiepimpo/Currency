import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime
from exchange.models import Provider, Currency

@pytest.mark.django_db
class TestCurrencyAPI:
    """
    Test suite for currency exchange API.
    """

    def setup_method(self):
        """Setup test data before each test."""
        self.client = APIClient()

        # Create test currencies
        self.currency_eur = Currency.objects.create(code="EUR", name="Euro")
        self.currency_usd = Currency.objects.create(code="USD", name="US Dollar")
        self.currency_gbp = Currency.objects.create(code="GBP", name="British Pound")
        self.currency_chf = Currency.objects.create(code="CHF", name="Swiss Franc")

        # Create providers (CurrencyBeacon & Mock)
        self.provider_cb = Provider.objects.create(name="CurrencyBeacon", priority=1, is_active=True)
        self.provider_mock = Provider.objects.create(name="Mock", priority=2, is_active=True)

    def test_latest_exchange_rates_currency_beacon(self):
        """Test fetching latest exchange rates using CurrencyBeaconProvider."""
        response = self.client.get(reverse("latest-currency-rates"), {"base": "EUR", "symbols": "USD,GBP,CHF"})
        assert response.status_code == 200
        assert "rates" in response.json()

    def test_latest_exchange_rates_mock_provider(self):
        """Test fetching latest exchange rates using MockProvider."""
        # Deactivate CurrencyBeacon to force Mock usage
        self.provider_cb.is_active = False
        self.provider_cb.save()

        response = self.client.get(reverse("latest-currency-rates"), {"base": "EUR", "symbols": "USD,GBP,CHF"})
        assert response.status_code == 200
        assert "rates" in response.json()

    def test_historical_exchange_rates_currency_beacon(self):
        """Test fetching historical exchange rates using CurrencyBeaconProvider."""
        response = self.client.get(reverse("historical-currency-rates"), {
            "base": "EUR",
            "symbols": "USD,GBP,CHF",
            "date": "2025-02-15"
        })
        assert response.status_code == 200
        assert "rates" in response.json()

    def test_historical_exchange_rates_mock_provider(self):
        """Test fetching historical exchange rates using MockProvider."""
        # Deactivate CurrencyBeacon
        self.provider_cb.is_active = False
        self.provider_cb.save()

        response = self.client.get(reverse("historical-currency-rates"), {
            "base": "EUR",
            "symbols": "USD,GBP,CHF",
            "date": "2025-02-15"
        })
        assert response.status_code == 200
        assert "rates" in response.json()

    def test_exchange_rates_list_currency_beacon(self):
        """Test fetching exchange rates over a date range using CurrencyBeaconProvider."""
        response = self.client.get(reverse("list-exchange-rates"), {
            "base": "EUR",
            "start_date": "2025-02-15",
            "end_date": "2025-02-20",
            "symbols": "USD,GBP,CHF"
        })
        assert response.status_code == 200
        assert "list" in response.json()

    def test_exchange_rates_list_mock_provider(self):
        """Test fetching exchange rates over a date range using MockProvider."""
        # Deactivate CurrencyBeacon
        self.provider_cb.is_active = False
        self.provider_cb.save()

        response = self.client.get(reverse("list-exchange-rates"), {
            "base": "EUR",
            "start_date": "2025-02-15",
            "end_date": "2025-02-20",
            "symbols": "USD,GBP,CHF"
        })
        assert response.status_code == 200
        assert "list" in response.json()

    def test_currency_conversion_currency_beacon(self):
        """Test converting an amount using CurrencyBeaconProvider."""
        response = self.client.get(reverse("convert-amount"), {
            "from": "USD",
            "to": "EUR",
            "amount": 100
        })
        assert response.status_code == 200
        assert "converted_amount" in response.json()

    def test_currency_conversion_mock_provider(self):
        """Test converting an amount using MockProvider."""
        # Deactivate CurrencyBeacon
        self.provider_cb.is_active = False
        self.provider_cb.save()

        response = self.client.get(reverse("convert-amount"), {
            "from": "USD",
            "to": "EUR",
            "amount": 100
        })
        assert response.status_code == 200
        assert "converted_amount" in response.json()
