from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.db.models import Sum, Avg
from .models import *
from .forms import ReportForm
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

    reports_dict = {    'yearly_reports' : the_reports,
                        'reports' : reports_list, 
                        't_revenue' : reports_revenue['revenue__sum'], 
                        't_partner_share' : reports_partner_share['partner_share__sum'],
                        't_contribution' : reports_contribution,
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
    explorer2 = customer_tabledict
    explorer3 = customer_tabledata

# --- dictionaries ---
    return render(request, 'kpis/report_list.html', { 'report_filter': report_filter, 
                                                        'customer_query' : customer_query,
                                                        'weekly_dict' : weekly_dict,
                                                        'explorer2' : explorer2,
                                                        'explorer3' : explorer3,
                                                        'customer_tabledata' : customer_tabledata,
                                                        'customer_tabledict' : customer_tabledict
                                                        })


def week(request, wk, yr):
    
    reports = Report.objects.filter(week_number=wk, year=yr).order_by('customer__customer_name')
    week_number = wk
    year = yr
    prv_1year = yr - 1

    #TOTALS
    reports_revenue = reports.aggregate(Sum('revenue'))['revenue__sum']
    reports_hs = reports.aggregate(Sum('headsets'))['headsets__sum']
    reports_partner_share = reports.aggregate(Sum('partner_share'))['partner_share__sum']
    reports_rhs = round(reports_revenue / reports_hs)

    ###Operating costs
    reports_staff = reports.aggregate(Sum('staff_costs'))['staff_costs__sum']
    reports_rent = reports.aggregate(Sum('rent_cost'))['rent_cost__sum']
    reports_marketing = reports.aggregate(Sum('marketing_cost'))['marketing_cost__sum']
    reports_sundries = reports.aggregate(Sum('sundries_cost'))['sundries_cost__sum']
    reports_ops = reports_staff + reports_rent + reports_marketing + reports_sundries

    ###Contribution
    reports_contr = reports_revenue - reports_ops - reports_partner_share


    ###Margin
    reports_margin = round((reports_contr / reports_revenue)*100)


    #Previous week's reports
    prev_wk_reports = Report.objects.filter(week_number=wk-1, year=yr)

    #ENTERTAINMENT CATEGORY
    rep_ent = reports.filter(customer__category__category_name="Entertainment")
    rep_ent_rev = rep_ent.aggregate(Sum('revenue'))['revenue__sum']
    rep_ent_hs = rep_ent.aggregate(Sum('headsets'))['headsets__sum']
    rep_ent_rphs = round(rep_ent_rev / rep_ent_hs)
    rep_ent_ps = rep_ent.aggregate(Sum('partner_share'))['partner_share__sum']
    
    ###Operating costs
    rep_ent_staff = rep_ent.aggregate(Sum('staff_costs'))['staff_costs__sum']
    rep_ent_rent = rep_ent.aggregate(Sum('rent_cost'))['rent_cost__sum']
    rep_ent_marketing = rep_ent.aggregate(Sum('marketing_cost'))['marketing_cost__sum']
    rep_ent_sundries = rep_ent.aggregate(Sum('sundries_cost'))['sundries_cost__sum']
    rep_ent_ops = rep_ent_staff + rep_ent_rent + rep_ent_marketing + rep_ent_sundries

    ###Contribution
    rep_ent_contr = rep_ent_rev - rep_ent_ps - rep_ent_ops
    rep_ent_contr_hs = round(rep_ent_contr / rep_ent_hs)

    ###Margin
    rep_ent_margin = round((rep_ent_contr / rep_ent_rev)*100)

    #AQUARIUM CATEGORY
    rep_aqu = reports.filter(customer__category__category_name="Aquarium")

    if rep_aqu:
        rep_aqu_rev = rep_aqu.aggregate(Sum('revenue'))['revenue__sum']
        rep_aqu_hs = rep_aqu.aggregate(Sum('headsets'))['headsets__sum']
        rep_aqu_rphs = round(rep_aqu_rev / rep_aqu_hs)
        rep_aqu_ps = rep_aqu.aggregate(Sum('partner_share'))['partner_share__sum']
        
        ###Operating costs
        rep_aqu_staff = rep_aqu.aggregate(Sum('staff_costs'))['staff_costs__sum']
        rep_aqu_rent = rep_aqu.aggregate(Sum('rent_cost'))['rent_cost__sum']
        rep_aqu_marketing = rep_aqu.aggregate(Sum('marketing_cost'))['marketing_cost__sum']
        rep_aqu_sundries = rep_aqu.aggregate(Sum('sundries_cost'))['sundries_cost__sum']
        rep_aqu_ops = rep_aqu_staff + rep_aqu_rent + rep_aqu_marketing + rep_aqu_sundries

        ###Contribution
        rep_aqu_contr = rep_aqu_rev - rep_aqu_ps - rep_aqu_ops
        rep_aqu_contr_hs = round(rep_aqu_contr / rep_aqu_hs)

        ###Margin
        rep_aqu_margin = round((rep_aqu_contr / rep_aqu_rev)*100)
    
    else:
        rep_aqu_rev = 0
        rep_aqu_hs = 0
        rep_aqu_rphs = 0
        rep_aqu_ps = 0
        
        ###Operating costs
        rep_aqu_staff = 0
        rep_aqu_rent = 0
        rep_aqu_marketing = 0
        rep_aqu_sundries = 0
        rep_aqu_ops = 0

        ###Contribution
        rep_aqu_contr = 0
        rep_aqu_contr_hs = 0

        ###Margin
        rep_aqu_margin = 0

    context = { 'reports' : reports, 'week_number' : week_number, 'year' : year, 'prv_1year' : prv_1year,
                'reports_revenue' : reports_revenue, 'reports_contr' : reports_contr,
                'reports_hs' : reports_hs, 'reports_rhs' : reports_rhs,
                'reports_margin' : reports_margin,
                'prev_wk_reports' : prev_wk_reports,
                'rep_ent' : rep_ent, 'rep_ent_rev' : rep_ent_rev, 'rep_ent_hs' : rep_ent_hs,
                'rep_ent_rphs' : rep_ent_rphs, 'rep_ent_ps' : rep_ent_ps,
                'rep_ent_ops' : rep_ent_ops, 'rep_ent_contr' : rep_ent_contr,
                'rep_ent_contr_hs' : rep_ent_contr_hs, 'rep_ent_margin' : rep_ent_margin,
                'rep_aqu' : rep_aqu, 'rep_aqu_rev' : rep_aqu_rev, 'rep_aqu_hs' : rep_aqu_hs,
                'rep_aqu_rphs' : rep_aqu_rphs, 'rep_aqu_ps' : rep_aqu_ps,
                'rep_aqu_ops' : rep_aqu_ops, 'rep_aqu_contr' : rep_aqu_contr,
                'rep_aqu_contr_hs' : rep_aqu_contr_hs, 'rep_aqu_margin' : rep_aqu_margin,
                 }

    return render(request, 'kpis/week.html', context)



def report_form(request):
    if request.method == 'POST':
        filled_form = ReportForm(request.POST)
        if filled_form.is_valid():
            success_note = 'Report posted.'
            filled_form.save()
            new_form = ReportForm()
            return render(request, 'kpis/report_form.html', {'report_form' : new_form, 'success_note' : success_note})
    else:
        fail_note = 'Report not posted.'
        new_form = ReportForm()
        return render(request, 'kpis/report_form.html', {'report_form' : new_form, 'fail_note' : fail_note })
