from django.conf.urls import url
from . import views

app_name = 'stocktracker'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<stock_id>[0-9]+)/$', views.detail, name='detail'),

]
