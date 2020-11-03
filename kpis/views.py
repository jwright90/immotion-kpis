from django.db.models import Sum
from django.shortcuts import render
from kpis.models import Report
import math
from .filters import ReportFilter


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

    weekly_reports = {}
    for rep in reports_list:
        if weekly_reports.get(rep.week_number):
            weekly_reports[rep.week_number].append(rep)
        else: weekly_reports[rep.week_number] = [rep]

    the_weekly_reports = [{"week" : k, "report": v} for k, v in weekly_reports.items()]

    explorer = reports_list.filter(year=2020, week_number=15)

    #print(the_weekly_reports)

    # week_14_plus = []
    # week_14_customer = Report.objects.filter(week_number__gte=15)
    
    # for rep in week_14_customer:
    #     week_14_plus.append(rep)
    
    # print(week_14_plus)


    reports_dict = {    'yearly_reports' : the_reports,
                        'reports' : reports_list, 
                        't_revenue' : reports_revenue['revenue__sum'], 
                        't_partner_share' : reports_partner_share['partner_share__sum'],
                        't_contribution' : reports_contribution,
                        'explorer' : explorer,
    }

    #print to see what is inside variable

    return render(request, 'kpis/index.html', context=reports_dict)

def search(request):
    report_list = Report.objects.all()

    # {Week 1: {}, Week 2: {}, Week 3: {}}

    report_filter = ReportFilter(request.GET, queryset=report_list)
    

    weekly_reports = {}
    for rep in report_filter.qs:
        if weekly_reports.get(rep.week_number):
            weekly_reports[rep.week_number].append(rep)
        else: weekly_reports[rep.week_number] = [rep]

    explorer = [{"week" : k, "report": v} for k, v in weekly_reports.items()]

    customer_reports = {}
    for rep in report_filter.qs:
        if customer_reports.get(rep.customer):
            customer_reports[rep.customer].append(rep)
        else: customer_reports[rep.customer] = [rep]
    
    customer_query = [{"customer" : k, "report" : v} for k, v in customer_reports.items()]

    return render(request, 'search/report_list.html', { 'report_filter': report_filter, 
                                                        'customer_query' : customer_query,
                                                        'explorer' : explorer
                                                        })

