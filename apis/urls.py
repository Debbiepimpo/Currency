from django.urls import path
from .views import HistoricalCurrencyRateListView, LatestCurrencyRateView

urlpatterns = [
    path('currency-rates/latest/', LatestCurrencyRateView.as_view(), name='currency-rates-latest'),
    path('currency-rates/historical/', HistoricalCurrencyRateListView.as_view(), name='currency-rates-historical'),
    path('convert/', ConvertAmountView.as_view(), name='convert_amount'),
]