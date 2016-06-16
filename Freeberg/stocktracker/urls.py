from django.conf.urls import url
from . import views

app_name = 'stocktracker'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^allstocks/$', views.allstocks, name='allstocks'),
    url(r'^(?P<stock_id>[0-9]+)/$', views.individual_stock, name='individual_stock'),

]
