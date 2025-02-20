from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from exchange.providers import CurrencyBeaconProvider 


class LatestCurrencyRateView(APIView):
    """
    API View to fetch the latest exchange rates for specified currencies.
    """

    def get(self, request):
        base_currency = request.query_params.get("base")
        symbols = request.query_params.get("symbols") 
        
        provider = CurrencyBeaconProvider()
        rates = provider.get_exchange_rate(base_currency, symbols)

        if rates is None:
            return Response(
                {"error": "Failed to fetch latest exchange rates."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"base": base_currency, "rates": rates}, status=status.HTTP_200_OK)



class HistoricalCurrencyRateListView(APIView):
    """
    API View to fetch historical exchange rates for EUR, USD, CHF, GBP in a date range.
    """
    def get(self, request):

        source_currency = request.query_params.get("base")
        exchange_currency = request.query_params.get("symbols")
        date_str = request.query_params.get("date")

        if not source_currency:
            return Response(
                {"error": "Parameter 'base_currency' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not exchange_currency:
            return Response(
                {"error": "Parameter 'symbols' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not date_str:
            return Response(
                {"error": "Parameter 'date' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        provider = CurrencyBeaconProvider()
        rates = provider.get_historical_exchange_rates(source_currency, exchange_currency, date)

        if rates is None:
            return Response(
                {"error": "Faisled to fetch historical exchange rates."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response({"base": source_currency, "rates": rates}, status=status.HTTP_200_OK)


class ListExchangeRatesView(APIView):
    """
    API View to fetch exchange rates for a specific time period.
    """

    def get(self, request):

        provider = CurrencyBeaconProvider()

        source_currency = request.query_params.get("base")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        exchange_currency = request.query_params.get("symbols")


        if not start_date or not end_date:
            return Response({"error": "Both 'start_date' and 'end_date' are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."},
                            status=status.HTTP_400_BAD_REQUEST)

        
        if exchange_currency is None:
            exchange_currency = None  
        elif isinstance(exchange_currency, str): 
            exchange_currency = exchange_currency.replace(" ", "").split(",")

        response = provider.get_exchange_rates_list(source_currency, start_date, end_date, exchange_currency)

        if response is None:
            return Response({"error": "Failed to fetch exchange list."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"base": source_currency, "list": response},
                        status=status.HTTP_200_OK)


class ConvertAmountView(APIView):
    """
    Convert amount from source currency to exchanged currency using the latest exchange rate.
    """

    def get(self, request):
        source_currency = request.query_params.get("from")
        exchange_currency = request.query_params.get("to")
        amount = request.query_params.get("amount")

        if not source_currency:
            return Response(
                {"error": "Parameter 'from' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not exchange_currency:
            return Response(
                {"error": "Parameter 'to' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not amount:
            return Response(
                {"error": "Parameter 'amount' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount = float(amount)
        except ValueError:
            return Response(
                {"error": "Invalid amount. Please provide a numeric value."},
                status=status.HTTP_400_BAD_REQUEST
            )

        provider = CurrencyBeaconProvider()
        conversion_result = provider.convert_currency(source_currency, exchange_currency, amount)

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

