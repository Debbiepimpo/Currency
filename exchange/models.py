from django.db import models

class Currency(models.Model):
    CURRENCY_CHOICES = [
            ("EUR", "EUR"),
            ("CHF", "CHF"),
            ("USD", "USD"),
            ("GBP", "GBP"),
    ]

    code = models.CharField(max_length=3, choices=CURRENCY_CHOICES, unique=True)
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} - {self.name}"

class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey(Currency, related_name='exchanges', on_delete=models.CASCADE)
    exchanged_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(db_index=True, decimal_places=6, max_digits=18)

    def __str__(self):
        return f"{self.source_currency.code} to {self.exchanged_currency.code} on {self.valuation_date}"



class Provider(models.Model):
    name = models.CharField(max_length=50, unique=True)
    priority = models.IntegerField(default=1) 
    is_active = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.name} (Priority: {self.priority}, Active: {self.is_active})"
    
class InstantConverter:
    """ 
        Fake Model to put the instant converter in Admin site
    """
    class Meta:
        verbose_name = "Instant Converter"
        verbose_name_plural = "Instant Converter"
