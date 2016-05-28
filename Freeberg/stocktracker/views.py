from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import loader
from .models import Stock
import ystockquote


# Create your views here.
def index(request):
    stocks = Stock.objects.all()
    for stock1 in stocks:
        stock1.lastprice = ystockquote.get_price(stock1)
        # YYYY-MM-DD
        historical_price = ystockquote.get_historical_prices(stock1, '2016-05-24', '2016-05-26')
        hprice = []
        for values in historical_price:
            hprice.append(historical_price[values]['Close'])

    template = loader.get_template('stocktracker/index.html')
    context = {'stocks':stocks}
    return render(request, 'stocktracker/index.html', context)

def detail(request, stock_id):
    return render(request, 'stocktracker/detail.html')

