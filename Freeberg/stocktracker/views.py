from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import loader
from django.db.models import Q
from .models import Stock
from bokeh.io import vform
from bokeh.plotting import figure, ColumnDataSource
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import HoverTool, CrosshairTool, CustomJS, Slider
import ystockquote
import datetime as dt
from datetime import datetime


# Last Weekday
def weekday():
    wtoday = dt.date.today()
    if wtoday.isoweekday == 6:
        day_today = wtoday.day - 1
        working_day = wtoday.replace(day=day_today)
        return working_day

    elif wtoday.isoweekday == 7:
        day_today = wtoday.day - 1
        working_day = wtoday.replace(day=day_today)
        return working_day

    else:
        return wtoday

# Create your views here.

def index(request):
    return render(request, 'stocktracker/index.html')

def allstocks(request):
    stocks = Stock.objects.all()

    query = request.GET.get('q')
    if query:
        stocks = stocks.filter(Q(ticker__icontains=query)|
                               Q(company_name__icontains=query)).distinct()

    context = {'stocks': stocks}

    return render(request, 'stocktracker/allstocks.html', context)

def individual_stock(request, stock_id):

    stock1 = get_object_or_404(Stock, pk=stock_id)

    # Stock Information per Stock
    stock1.lastprice = ystockquote.get_price(stock1)
    stock1.volume = ystockquote.get_volume(stock1)
    price_change = ystockquote.get_change(stock1)
    market_cap = ystockquote.get_market_cap(stock1)
    get_high = ystockquote.get_52_week_high(stock1)
    get_low = ystockquote.get_52_week_low(stock1)
    pb_ratio = ystockquote.get_price_book_ratio(stock1)
    ebitda = ystockquote.get_ebitda(stock1)
    dividend = ystockquote.get_dividend_yield(stock1)

    # Graph

    # Last known weekday
    current_day = weekday().isoformat()

    # Retrieve live data YYYY-MM-DD
    historical_price = ystockquote.get_historical_prices(stock1, '2010-01-24', current_day)
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

    source = ColumnDataSource(data=dict(x=dates_objects,y=stock_prices, time=dates))

    # Tools
    hover = HoverTool(tooltips=[('Stock Price','@y'),('time','@time'),], mode='vline')
    crosshair = CrosshairTool(dimensions=['height'])

    TOOLS = [hover, crosshair]

    plot = figure(x_axis_type="datetime", responsive = True ,plot_height=250, tools = TOOLS, toolbar_location=None)
    plot.line('x','y',source=source)

    callback = CustomJS(args=dict(source=source), code="""
        var data = source.get('data');
        var f = cb_obj.get('value')
        x = data['x']
        y = data['y']
        for (i = 0; i < x.length; i++) {
            y[i] = x[i]
        }
        source.trigger('change');
    """)

    slider = vform(Slider(start=0, end=100, value=1, step=.1, title="power", callback=callback))

    widget_script, widget_div = components(slider)
    script, div = components(plot)

    stock1.save()
    context = {'stock':stock1,
               'hprice': stock_prices,
               'widget_script': widget_script,
               'widget_div': widget_div,
               'the_script': script,
               'the_div':div,
               'thedate': dates_objects,
               'dates':dates
               }

    return render(request, 'stocktracker/individual.html', context)



#lol