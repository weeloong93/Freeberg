from django.db import models

# Create your models here.

class Stock(models.Model):
    company_name = models.CharField(max_length = 100)
    ticker = models.CharField(max_length=10)
    bloom_ticker = models.CharField(max_length=10, null=True)
    lastprice = models.CharField(max_length = 10000000, default ='-')
    open = models.FloatField(blank=True)
    close = models.FloatField(blank=False)
    volume = models.IntegerField(blank=True)
    description = models.TextField(null=True)
    start_date = models.DateField(null=True)

    def __str__(self):
        return self.ticker

