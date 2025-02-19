from django.test import TestCase
from .models import Currency


class CurrencyTestCase(TestCase):
    def setUp(self):
        Currency.objects.create(code="USD", name="US Dollar", symbol="$")

    def test_currency_creation(self):
        usd = Currency.objects.get(code="USD")
        self.assertEqual(usd.name, "US Dollar")
