from django import forms
import requests
from .models import Currency
 
class CurrencyConversionForm(forms.Form):
    source_currency = forms.ModelChoiceField(queryset=Currency.objects.all(), label="Source Currency")
    exchanged_currency = forms.ModelChoiceField(queryset=Currency.objects.all(), label="Exchanged Currency")
    amount = forms.DecimalField(label="Amount", decimal_places=2)