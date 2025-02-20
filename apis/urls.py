from django.urls import path
from .views import HistoricalCurrencyRateListView, LatestCurrencyRateView, ListExchangeRatesView, ConvertAmountView

urlpatterns = [
    path('currency-rates/latest/', LatestCurrencyRateView.as_view(), name='currency-rates-latest'),
    path('currency-rates/historical/', HistoricalCurrencyRateListView.as_view(), name='currency-rates-historical'),
    path('currency-rates/timeseries/', ListExchangeRatesView.as_view(), name='currency-rates-list'),
    path('currency-rates/convert/', ConvertAmountView.as_view(), name='convert_amount'),
]