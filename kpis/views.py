from django.shortcuts import render
from kpis.models import Report
from django.db.models import Sum
import math


# Create your views here.

def index(request):
    reports_list = Report.objects.order_by('-year', 'week_number')
    reports_revenue = Report.objects.aggregate(Sum('revenue'))
    reports_partner_share = Report.objects.aggregate(Sum('partner_share'))

    reports_dict = {    'reports' : reports_list, 
                        't_revenue' : reports_revenue, 
                        't_partner_share' : reports_partner_share,
    }

    return render(request, 'kpis/index.html', context=reports_dict)
