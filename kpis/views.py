from django.shortcuts import render
from kpis.models import Report

# Create your views here.

def index(request):
    reports_list = Report.objects.order_by('-year', 'week_number')
    reports_dict = { 'reports' : reports_list }

    return render(request, 'kpis/index.html', context=reports_dict)