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

    yearly_reports = {}
    for rep in reports_list:
        if yearly_reports.get(rep.year):
            yearly_reports[rep.year].append(rep)
        else:
            yearly_reports[rep.year] = [rep]

    the_reports = [{"year": k, "report": v} for k, v in yearly_reports.items()]


    week_14_plus = []
    week_14_customer = Report.objects.filter(week_number__gte=15)
    
    for rep in week_14_customer:
        week_14_plus.append(rep)
    
    print(week_14_plus)


    reports_dict = {    'yearly_reports' : the_reports,
                        'reports' : reports_list, 
                        't_revenue' : reports_revenue['revenue__sum'], 
                        't_partner_share' : reports_partner_share['partner_share__sum'],
                        't_contribution' : reports_contribution
    }

    #print to see what is inside variable

    return render(request, 'kpis/index.html', context=reports_dict)
