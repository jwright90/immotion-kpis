
from django.conf.urls import url
from django.urls import path
from kpis import views

app_name = 'kpis'

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^search/$', views.search, name='search')
]

