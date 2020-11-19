
from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    path('week/<int:wk>/<int:yr>/', views.week, name='week'),
    path('newreport', views.report_form, name='report_form'),
]

