from django.shortcuts import render
from kpis.models import Report
from django.db.models import Sum
import math


# Create your views here.

def index(request):
    reports_list = Report.objects.order_by('-year', 'week_number')
    reports_revenue = Report.objects.aggregate(Sum('revenue'))
    reports_partner_share = Report.objects.aggregate(Sum('partner_share'))
    reports_contribution = reports_revenue['revenue__sum'] - reports_partner_share['partner_share__sum']

    reports = { }


    for report in reports_list:
        #print(report.year)
        #each variable accessible with .
        #make keys for year and weeks

        week = { }
        week[report.week_number] = { 'revenue' : report.revenue }
    
        print (week)

        #reports[str(report.year)][str(report.week_number)] = { 'revenue' : report.revenue }  


    reports_dict = {    'reports' : reports_list, 
                        't_revenue' : reports_revenue['revenue__sum'], 
                        't_partner_share' : reports_partner_share['partner_share__sum'],
                        't_contribution' : reports_contribution
    }




    #print to see what is inside variable
    print(reports_revenue)
    print(reports_partner_share)

    return render(request, 'kpis/index.html', context=reports_dict)
