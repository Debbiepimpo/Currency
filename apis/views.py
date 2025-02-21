from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from exchange.services import ExchangeRateService  


class LatestCurrencyRateView(APIView):
    """
    API View to fetch the latest exchange rates for specified currencies.
    """

    def get(self, request):
        base_currency = request.query_params.get("base")
        symbols = request.query_params.get("symbols") 
        
        if not base_currency or not symbols:
            return Response(
                {"error": "Parameters 'base' and 'symbols' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        service = ExchangeRateService()
        rates = service.get_exchange_rate(base_currency, symbols)

        if rates is None:
            return Response(
                {"error": "Failed to fetch latest exchange rates."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"base_currency": base_currency, "rates": rates}, status=status.HTTP_200_OK)


class HistoricalCurrencyRateListView(APIView):
    """
    API View to fetch historical exchange rates for a specific date.
    """

    def get(self, request):
        source_currency = request.query_params.get("base")
        exchange_currency = request.query_params.get("symbols")
        date_str = request.query_params.get("date")

        if not source_currency or not exchange_currency or not date_str:
            return Response(
                {"error": "Parameters 'base', 'symbols', and 'date' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        service = ExchangeRateService()
        rates = service.get_historical_exchange_rates(source_currency, exchange_currency, date)

        if rates is None:
            return Response(
                {"error": "Failed to fetch historical exchange rates."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"base_currency": source_currency, "date": date_str, "rates": rates}, status=status.HTTP_200_OK)


class ListExchangeRatesView(APIView):
    """
    API View to fetch exchange rates for a specific time period.
    """

    def get(self, request):
        source_currency = request.query_params.get("base")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        exchange_currency = request.query_params.get("symbols")

        if not source_currency or not start_date or not end_date or not exchange_currency:
            return Response(
                {"error": "Parameters 'base', 'start_date', 'end_date', and 'symbols' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        service = ExchangeRateService()
        rates = service.get_exchange_rates_list(source_currency, start_date, end_date, exchange_currency)

        if rates is None:
            return Response(
                {"error": "Failed to fetch exchange list."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"base_currency": source_currency, "list": rates}, status=status.HTTP_200_OK)


class ConvertAmountView(APIView):
    """
    Convert amount from source currency to exchanged currency using the latest exchange rate.
    """

    def get(self, request):
        source_currency = request.query_params.get("from")
        exchange_currency = request.query_params.get("to")
        amount = request.query_params.get("amount")

        if not source_currency or not exchange_currency or not amount:
            return Response(
                {"error": "Parameters 'from', 'to', and 'amount' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount = float(amount)
        except ValueError:
            return Response(
                {"error": "Invalid amount. Please provide a numeric value."},
                status=status.HTTP_400_BAD_REQUEST
            )

        service = ExchangeRateService()
        conversion_result = service.convert_currency(source_currency, exchange_currency, amount)

        if conversion_result is None:
            return Response(
                {"error": "Failed to convert currency."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            "from": source_currency,
            "to": exchange_currency,
            "amount": amount,
            "converted_amount": conversion_result
        }, status=status.HTTP_200_OK)
