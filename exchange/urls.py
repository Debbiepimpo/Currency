from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurrencyViewSet, ExchangeRateViewSet

router = DefaultRouter()
router.register(r'currencies', CurrencyViewSet)
router.register(r'exchange_rates', ExchangeRateViewSet, basename='exchange_rate')

urlpatterns = [
    path('', include(router.urls)),
]
