from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from providers import CurrencyBeaconProvider 

class LatestCurrencyRateView(APIView):
    """
    API View to fetch the latest exchange rates for EUR, USD, CHF, GBP.
    """
    def get(self, request):
        provider = CurrencyBeaconProvider()
        rates = provider.get_latest_exchange_rates()

        if rates is None:
            return Response(
                {"error": "Failed to fetch latest exchange rates."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"base_currency": source_currency, "rates": rates}, status=status.HTTP_200_OK)


class HistoricalCurrencyRateListView(APIView):
    """
    API View to fetch historical exchange rates for EUR, USD, CHF, GBP in a date range.
    """
    def get(self, request):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        if not date_from or not date_to:
            return Response(
                {"error": "Both 'date_from' and 'date_to' parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        provider = CurrencyBeaconProvider()
        rates = provider.get_historical_exchange_rates(date_from, date_to)

        return Response({"base_currency": source_currency, "rates": rates}, status=status.HTTP_200_OK)

class ConvertAmountView(APIView):
    """
    Convert amount from source currency to exchanged currency using the latest exchange rate.
    """

    def get(self, request, *args, **kwargs):
        # Obtener parámetros de la consulta
        source_currency_code = request.query_params.get("source_currency")
        exchanged_currency_code = request.query_params.get("exchanged_currency")
        amount = request.query_params.get("amount")

        # Validaciones
        if not source_currency_code or not exchanged_currency_code or not amount:
            return Response({"error": "source_currency, exchanged_currency, and amount are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
        except ValueError:
            return Response({"error": "Amount must be a valid number."}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener las monedas de la base de datos
        source_currency = get_object_or_404(Currency, code=source_currency_code.upper())
        exchanged_currency = get_object_or_404(Currency, code=exchanged_currency_code.upper())

        # Buscar la última tasa de cambio registrada
        latest_rate = CurrencyExchangeRate.objects.filter(
            source_currency=source_currency,
            exchanged_currency=exchanged_currency
        ).order_by('-valuation_date').first()

        if not latest_rate:
            return Response({"error": "Exchange rate not found."}, status=status.HTTP_404_NOT_FOUND)

        # Calcular la cantidad convertida
        converted_amount = amount * latest_rate.rate_value

        return Response({
            "source_currency": source_currency.code,
            "exchanged_currency": exchanged_currency.code,
            "rate_value": latest_rate.rate_value,
            "original_amount": amount,
            "converted_amount": round(converted_amount, 2),
            "valuation_date": latest_rate.valuation_date.strftime("%Y-%m-%d")
        }, status=status.HTTP_200_OK)