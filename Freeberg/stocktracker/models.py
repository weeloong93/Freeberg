from django.db import models

# Create your models here.

class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    lastprice = models.CharField(max_length = 10000000, default ='-')
    open = models.FloatField(null=True)
    close = models.FloatField(null=True)
    volume = models.IntegerField(null=True)

    def __str__(self):
        return self.ticker

