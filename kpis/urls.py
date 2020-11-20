
from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    path('report/<int:pk>', views.report, name='report'),
    path('all_reports', views.all_reports, name='all_reports'),
    path('week/<int:wk>/<int:yr>/', views.week, name='week'),
    path('newreport', views.report_form, name='report_form'),
]

