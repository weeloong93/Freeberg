from django.db import models

# Create your models here.

class Stock(models.Model):
    company_name = models.CharField(max_length = 100)
    ticker = models.CharField(max_length=10)
    bloom_ticker = models.CharField(max_length=10, null=True)
    lastprice = models.CharField(max_length = 10000000, default ='-')
    open = models.FloatField(blank=True, default = 1)
    close = models.FloatField(blank=False, default = 1)
    volume = models.IntegerField(blank=True, default = 1)
    description = models.TextField(null=True)
    start_date = models.DateField(null=True)
    price_change = models.FloatField(blank=True, default = 1)
    market_cap = models.FloatField(blank=True, default = 1)
    get_high = models.FloatField(blank=True, default = 1)
    get_low = models.FloatField(blank=True, default = 1)
    pb_ratio = models.FloatField(blank=True, default = 1)
    ebitda = models.FloatField(blank=True, default = 1)
    dividend = models.FloatField(blank=True, default = 1)

    def __str__(self):
        return self.ticker

