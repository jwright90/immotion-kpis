
from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    path('report/<int:pk>', views.report, name='report'),
    path('all_reports', views.all_reports, name='all_reports'),
    path('week/<int:wk>/<int:yr>/', views.week, name='week'),
    path('newreport', views.report_form, name='report_form'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('<slug:customer_slug>/', views.show_customer, name='show_customer'),
]

