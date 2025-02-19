from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import date
from .models import Currency, CurrencyExchangeRate
from .serializers import CurrencySerializer, CurrencyExchangeRateSerializer
from .providers import CurrencyBeaconProvider, MockExchangeRateProvider, get_exchange_rate_data

class CurrencyViewSet(viewsets.ModelViewSet):
    """API for managing currencies."""
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class ExchangeRateViewSet(viewsets.ViewSet):
    """API to get exchange rates."""

    @action(detail=False, methods=['get'])
    def rates(self, request):
        """Get exchange rates for a specific time period."""
        source_currency = request.query_params.get('source_currency')
        start_date = request.query_params.get('date_from')
        end_date = request.query_params.get('date_to')

        if not source_currency or not start_date or not end_date:
            return Response({'error': 'Missing parameters'}, status=400)

        rates = CurrencyExchangeRate.objects.filter(
            source_currency__code=source_currency,
            valuation_date__range=[start_date, end_date]
        )
        return Response(CurrencyExchangeRateSerializer(rates, many=True).data)

    @action(detail=False, methods=['get'])
    def convert(self, request):
        """Convert currency amounts."""
        source_currency = request.query_params.get('source_currency')
        exchanged_currency = request.query_params.get('exchanged_currency')
        amount = request.query_params.get('amount')

        if not source_currency or not exchanged_currency or not amount:
            return Response({'error': 'Missing parameters'}, status=400)

        rate = get_exchange_rate_data(source_currency, exchanged_currency, date.today(), CurrencyBeaconProvider())
        if rate:
            converted_amount = float(amount) * rate
            return Response({'rate': rate, 'converted_amount': converted_amount})
        return Response({'error': 'Exchange rate not available'}, status=404)
