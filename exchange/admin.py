import requests
from django.http import JsonResponse
from django.urls import path
from datetime import date
from django.contrib import admin
from .models import Currency, CurrencyExchangeRate, Provider
from .forms import CurrencyConversionForm
from .providers import CurrencyBeaconProvider


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "symbol")
    change_list_template = "admin/currency_changelist.html"

    def changelist_view(self, request, extra_context=None):
        """
        Modificamos la vista del Admin para incluir la lista de monedas en el contexto.
        """
        from .models import Currency  # Importación dentro del método para evitar problemas de importación circular
        extra_context = extra_context or {}
        extra_context['currencies'] = Currency.objects.all()  # Pasamos todas las monedas al template
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('convert/', self.admin_site.admin_view(self.convert_currency), name='convert_currency'),
            path('latest/', self.admin_site.admin_view(self.get_latest_rate), name='get_latest_rate'),
        ]
        return custom_urls + urls

    def convert_currency(self, request):
        """
        Fetches live exchange rates, converts the amount, and saves the result to the database.
        """
        if request.method == "POST":
            form = CurrencyConversionForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"error": "Invalid form data"}, status=400)

        source_currency = form.cleaned_data["source_currency"]
        exchanged_currency = form.cleaned_data["exchanged_currency"]
        amount = form.cleaned_data["amount"]

        # Obtener la URL base del provider y agregar '/convert'
        provider = CurrencyBeaconProvider()
        convert_url = f"{provider.API_URL}/convert?api_key={provider.API_KEY}"
        params = {
            "from": source_currency.code,
            "to": exchanged_currency.code,
            "amount": amount,
        }
        try:
            response = requests.get(convert_url, params=params)
            response.raise_for_status()
            data = response.json()
            converted_amount = data.get("value")

            if converted_amount is None:
                return JsonResponse({"error": "Conversion value not found in API response"}, status=400)

            # Calcular la tasa de conversión
            rate_value = round(float(converted_amount) / float(amount), 6)

            # Guardar en la base de datos
            CurrencyExchangeRate.objects.create(
                source_currency=source_currency,
                exchanged_currency=exchanged_currency,
                valuation_date=date.today(),
                rate_value=rate_value
            )

            return JsonResponse({
                "source_currency": source_currency.code,
                "exchanged_currency": exchanged_currency.code,
                "rate": rate_value,
                "original_amount": float(amount),
                "converted_amount": converted_amount,
                "message": "Exchange rate successfully saved."
            })

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"API request failed: {str(e)}"}, status=400)

    def get_latest_rate(self, request):
        """
        Fetches the latest exchange rate from CurrencyBeacon API.
        """
        if request.method != "POST":
            return JsonResponse({"error": "Invalid request method"}, status=400)

        source_currency_code = request.POST.get("source_currency")
        exchanged_currency_code = request.POST.get("exchanged_currency")

        if not source_currency_code or not exchanged_currency_code:
            return JsonResponse({"error": "Both source_currency and exchanged_currency are required."}, status=400)

        provider = CurrencyBeaconProvider()
        latest_url = f"{provider.API_URL}/latest?api_key={provider.API_KEY}"
        params = {
            "base": source_currency_code,
            "symbols": exchanged_currency_code,
        }

        try:
            response = requests.get(latest_url, params=params)
            response.raise_for_status()
            data = response.json()
            rate_value = data.get("rates", {}).get(exchanged_currency_code)

            if rate_value is None:
                return JsonResponse({"error": "Exchange rate not found in API response"}, status=400)

            return JsonResponse({
                "source_currency": source_currency_code,
                "exchanged_currency": exchanged_currency_code,
                "rate": rate_value,
                "message": "Latest exchange rate fetched successfully."
            })

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"API request failed: {str(e)}"}, status=400)

class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    list_display = ("source_currency", "exchanged_currency", "valuation_date", "rate_value")

class ProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "priority", "is_active")
    list_editable = ("priority", "is_active")

# Registrar los modelos en el Django Admin
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(CurrencyExchangeRate, CurrencyExchangeRateAdmin)
admin.site.register(Provider, ProviderAdmin)
