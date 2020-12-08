from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('export/', views.export, name='export'),
    url(r'^search/$', views.search, name='search'),
    path('report/<int:pk>', views.report, name='report'),
    path('editreports', views.edit_reports, name='edit_reports'),
    path('week/<int:wk>/<int:yr>/', views.week, name='week'),
    path('weekly/<int:yr>/', views.weekly, name='weekly'),
    path('newreport', views.report_form, name='report_form'),
    path('editreport/<int:pk>', views.update_report, name='update_report'),
    path('deletereport/<int:pk>', views.delete_report, name='delete_report'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('<slug:customer_slug>/', views.show_customer, name='show_customer'),
]

