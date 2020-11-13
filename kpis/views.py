from django import forms
from django.db.models import Sum, Avg
from django.shortcuts import render
from kpis.models import Report, Customer
from .filters import ReportFilter
import math, string


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

    customer_list = Customer.objects.all()
    report_list = Report.objects.all()
    report_filter = ReportFilter(request.GET, queryset=report_list)
    
    weekly_reports = {}
    for rep in report_filter.qs:
        if weekly_reports.get(rep.week_number):
            weekly_reports[rep.week_number].append(rep)
        else: weekly_reports[rep.week_number] = [rep]

    weekly_dict = [{"week" : k, "report": v} for k, v in weekly_reports.items()]

    customer_reports = {}
    
    for rep in report_filter.qs:
        print(rep.revenue)
        if customer_reports.get(rep.customer):
            customer_reports[rep.customer].append(rep)
        else: customer_reports[rep.customer] = [rep] #a list containing one report   
    
    customer_query = [{"customer" : k, "report" : v} for k, v in customer_reports.items()]

    customer_list1 = []
    customer_list2 = []
    customer_headsets = []
    customer_td_headsets = {}
    customer_tabledata = {}

# --- filtered data table for 'search' page ---    
    
    for rep in report_filter.qs:
        customer_list1.append(rep.customer.id)
        customer_headsets.append(rep.headsets)

        for i in customer_list1:
            total_rev_var = report_filter.qs.filter(customer=i).aggregate(Sum('revenue'))['revenue__sum']
            total_headset_var = round(report_filter.qs.filter(customer=i).aggregate(Avg('headsets'))['headsets__avg'])
            rev_per_headset_var = round(total_rev_var / total_headset_var)
            partner_share_var = (report_filter.qs.filter(customer=i).aggregate(Sum('partner_share'))['partner_share__sum'])
            # --- operations costs --- 
            staff_cost_var = report_filter.qs.filter(customer=i).aggregate(Sum('staff_costs'))['staff_costs__sum']
            rent_cost_var = report_filter.qs.filter(customer=i).aggregate(Sum('rent_cost'))['rent_cost__sum']
            marketing_cost_var = report_filter.qs.filter(customer=i).aggregate(Sum('marketing_cost'))['marketing_cost__sum']
            sundries_cost_var = report_filter.qs.filter(customer=i).aggregate(Sum('sundries_cost'))['sundries_cost__sum']
            operations_cost_var = (staff_cost_var + marketing_cost_var + rent_cost_var + sundries_cost_var)
            # --- profitability ratios
            contribution_var = total_rev_var - partner_share_var - operations_cost_var
            contribution_per_headset_var = round(contribution_var/total_headset_var) 
            margin_var = round((contribution_var / total_rev_var)*100)


            customer_tabledata[customer_list[i-1].customer_name] = {
                "total_revenue" : total_rev_var,
                "headsets" : total_headset_var,
                "revenue_per_headset" : rev_per_headset_var,
                "partner_share" : partner_share_var,
                "operations_cost" : operations_cost_var,
                "contribution" : contribution_var,
                "contribution_per_headset" : contribution_per_headset_var,
                "margin": margin_var,
                }

    customer_tabledict = [{"customer" : a, "table_info" : b,} for a, b in customer_tabledata.items()]

# --- sandbox ---
    explorer = report_filter.qs
    explorer2 = customer_tabledict
    explorer3 = customer_tabledata


# --- dictionaries ---
    return render(request, 'search/report_list.html', { 'report_filter': report_filter, 
                                                        'customer_query' : customer_query,
                                                        'weekly_dict' : weekly_dict,
                                                        'explorer' : explorer,
                                                        'explorer2' : explorer2,
                                                        'explorer3' : explorer3,
                                                        'customer_tabledata' : customer_tabledata,
                                                        'customer_tabledict' : customer_tabledict
                                                        })