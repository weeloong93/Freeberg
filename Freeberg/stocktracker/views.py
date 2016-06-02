from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import loader
from .models import Stock
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
import ystockquote
from datetime import datetime


# Create your views here.

def index(request):
    return render(request, 'stocktracker/index.html')

def detail(request, stock_id):
    stocks = Stock.objects.all()

    #Stock Information per Stock
    for stock1 in stocks:
        stock1.lastprice = ystockquote.get_price(stock1)
        # Retrieve live data YYYY-MM-DD
        historical_price = ystockquote.get_historical_prices(stock1, '2010-01-24', '2016-05-26')

        correct_order = sorted(historical_price)
        stock_prices = []
        dates = []
        for values in correct_order:
            stock_prices.append(historical_price[values]['Adj Close'])
            dates.append(values)

        # Convert to Float
        for p in range(len(stock_prices)):
            stock_prices[p] = float(stock_prices[p])

        # Convert to Datetime Format
        dates_objects = []
        for d in dates:
            dates_objects.append(datetime.strptime(d,'%Y-%m-%d'))

        # Line Graph - Values are [x,y}
        TOOLS = 'box_zoom,box_select,crosshair,resize,hover, reset'

        plot = figure(x_axis_type="datetime", tools = TOOLS)
        plot.line(dates_objects,stock_prices)

        script, div = components(plot, CDN)

    context = {'stocks':stocks,
               'hprice': stock_prices,
               'the_script': script,
               'the_div':div,
               'thedate': dates_objects}

    return render(request, 'stocktracker/detail.html', context)



