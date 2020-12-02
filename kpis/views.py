from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.db.models import Sum, Avg, Count
from .models import *
from .forms import ReportForm
from .filters import ReportFilter
import math, string, requests, json
from requests.exceptions import HTTPError


def index(request):

    fx_rates = requests.get('https://api.exchangeratesapi.io/latest?symbols=USD,EUR,CNY,AUD&base=GBP')
    
    reports_list = Report.objects.order_by('-year', 'week_number')
    reports_revenue = Report.objects.aggregate(Sum('revenue'))
    reports_partner_share = Report.objects.aggregate(Sum('partner_share'))
    reports_contribution = reports_revenue['revenue__sum'] - reports_partner_share['partner_share__sum']

    yearly_reports = {}
    for rep in reports_list:
        if yearly_reports.get(rep.year):
            #If the report year exists within the yearly reports dictionary, then
            yearly_reports[rep.year].append(rep)
                #Append the Report object to the key with value of report year
        else:
            yearly_reports[rep.year] = [rep]
            # Inserts rep.year as key with the Report object as a value

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
                        'fx_rates' : fx_rates,
    }

    #print to see what is inside variable

    return render(request, 'kpis/index.html', context=reports_dict)

def weekly(request, yr):
    reports = Report.objects.all().filter(year=yr)
    year = yr
    weekly_reports = {}
    weekly_revenues = {}
    weekly_headsets = {}

    for i in range(1, 54):
        if reports.filter(week_number=i):
            weekly_reports[i] = reports.filter(week_number=i)
            weekly_revenues[i] = reports.filter(week_number=i).aggregate(Sum('revenue'))['revenue__sum']
            weekly_headsets[i] = reports.filter(week_number=i).aggregate(Sum('headsets'))['headsets__sum']
        else:
            pass

    total_revenue = reports.aggregate(Sum('revenue'))['revenue__sum']

    context = { 'weekly_reports' : weekly_reports,
                'weekly_revenues' : weekly_revenues,
                'weekly_headsets' : weekly_headsets,
                'year' : year,
                'total_revenue' : total_revenue
                }

    return render(request, 'kpis/weekly.html', context)

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

def report(request, pk):

    report = Report.objects.get(id=pk)
    customer = report.customer
    customer_reports = Report.objects.filter(customer__customer_name=str(customer)).order_by('-year', '-week_number')
    week = report.week_number
    year = report.year

    context = {
        'report' : report,
        'customer' : customer,
        'customer_reports' : customer_reports,
        'week' : week,
        'year' : year,
    }

    return render(request, 'kpis/report.html', context)

def all_reports(request):

    reports = Report.objects.all().order_by('-estimate', '-year', '-week_number')

    context = {
        'reports' : reports,
    }

    return render(request, 'kpis/all_reports.html', context)

def week(request, wk, yr):
    
    reports = Report.objects.filter(week_number=wk, year=yr).order_by('customer__customer_name')
    week_number = wk
    year = yr

    mandalay_bay = Report.objects.filter(week_number=wk, year=yr, customer__customer_name='Mandalay Bay')

    def prev_yr():
        if yr == 1:
            prev_yr = yr
        else:
            prev_yr = yr - 1
        return prev_yr

    def prev_wk():
        if wk == 1:
            prev_wk = week_number
        else:
            prev_wk = week_number - 1
        return prev_wk

    if reports:
        reports_prev_wk = Report.objects.filter(week_number=prev_wk(), year=yr)
        reports_prev_yr = Report.objects.filter(week_number=wk, year=prev_yr())

        #TOTALS
        reports_revenue = reports.aggregate(Sum('revenue'))['revenue__sum']
        reports_hs = reports.aggregate(Sum('headsets'))['headsets__sum']
        reports_partner_share = reports.aggregate(Sum('partner_share'))['partner_share__sum']
        reports_rhs = round(reports_revenue / reports_hs)
        reports_revenue_prev_wk = reports_prev_wk.aggregate(Sum('revenue'))['revenue__sum']
        reports_revenue_prev_yr = reports_prev_yr.aggregate(Sum('revenue'))['revenue__sum']
        def reports_rev_prev_wk_diff():
            if type(reports_revenue_prev_wk) == int:
                reports_rev_prev_wk_diff = round((reports_revenue/(reports_revenue_prev_wk)-1)*100)
            else:
                reports_rev_prev_wk_diff = "None"
            return reports_rev_prev_wk_diff
        def reports_rev_prev_yr_diff():
            if type(reports_revenue_prev_yr) == int:
                reports_rev_prev_yr_diff = round((reports_revenue/(reports_revenue_prev_yr)-1)*100)
            else:
                reports_rev_prev_yr_diff = "None"
            return reports_rev_prev_yr_diff

        ###Operating costs
        reports_staff = reports.aggregate(Sum('staff_costs'))['staff_costs__sum']
        reports_rent = reports.aggregate(Sum('rent_cost'))['rent_cost__sum']
        reports_marketing = reports.aggregate(Sum('marketing_cost'))['marketing_cost__sum']
        reports_sundries = reports.aggregate(Sum('sundries_cost'))['sundries_cost__sum']
        reports_ops = reports_staff + reports_rent + reports_marketing + reports_sundries

        ###Contribution
        reports_contr = reports_revenue - reports_ops - reports_partner_share
        reports_contr_hs = round(reports_contr / reports_hs)

        ###Margin
        reports_margin = round((reports_contr / reports_revenue)*100)
    
    else:
        reports_prev_wk = 0
        reports_prev_yr = 0

        #TOTALS
        reports_revenue = 0
        reports_hs = 0
        reports_partner_share = 0
        reports_rhs = 0
        reports_revenue_prev_wk = 0
        reports_revenue_prev_yr = 0
        reports_rev_prev_wk_diff = 0
        reports_rev_prev_yr_diff = 0

        ###Operating costs
        reports_staff = 0
        reports_rent = 0
        reports_marketing = 0
        reports_sundries = 0
        reports_ops = 0

        ###Contribution
        reports_contr = 0
        reports_contr_hs = 0

        ###Margin
        reports_margin = 0

    #ENTERTAINMENT CATEGORY
    rep_ent = reports.filter(customer__category__category_name="Entertainment")
    
    if rep_ent:
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
    
    else:
        rep_ent_rev = 0
        rep_ent_hs = 0
        rep_ent_rphs = 0
        rep_ent_ps = 0
        
        ###Operating costs
        rep_ent_staff = 0
        rep_ent_rent = 0
        rep_ent_marketing = 0
        rep_ent_sundries = 0
        rep_ent_ops = 0

        ###Contribution
        rep_ent_contr = 0
        rep_ent_contr_hs = 0

        ###Margin
        rep_ent_margin = 0
    
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

    context = { 'reports' : reports, 'week_number' : week_number, 'year' : year, 'prev_yr' : prev_yr,
                'reports_revenue' : reports_revenue, 'reports_contr' : reports_contr, 'reports_partner_share' : reports_partner_share,
                'reports_hs' : reports_hs, 'reports_rhs' : reports_rhs, 'reports_ops' : reports_ops,
                'reports_contr_hs' : reports_contr_hs, 'reports_margin' : reports_margin,
                'reports_prev_wk' : reports_prev_wk, 'reports_revenue_prev_wk' : reports_revenue_prev_wk,
                'reports_prev_yr' : reports_prev_yr, 'reports_revenue_prev_yr' : reports_revenue_prev_yr,
                'reports_rev_prev_wk_diff' : reports_rev_prev_wk_diff, 'reports_rev_prev_yr_diff' : reports_rev_prev_yr_diff,
                'rep_ent' : rep_ent, 'rep_ent_rev' : rep_ent_rev, 'rep_ent_hs' : rep_ent_hs,
                'rep_ent_rphs' : rep_ent_rphs, 'rep_ent_ps' : rep_ent_ps,
                'rep_ent_ops' : rep_ent_ops, 'rep_ent_contr' : rep_ent_contr,
                'rep_ent_contr_hs' : rep_ent_contr_hs, 'rep_ent_margin' : rep_ent_margin,
                'rep_aqu' : rep_aqu, 'rep_aqu_rev' : rep_aqu_rev, 'rep_aqu_hs' : rep_aqu_hs,
                'rep_aqu_rphs' : rep_aqu_rphs, 'rep_aqu_ps' : rep_aqu_ps,
                'rep_aqu_ops' : rep_aqu_ops, 'rep_aqu_contr' : rep_aqu_contr,
                'rep_aqu_contr_hs' : rep_aqu_contr_hs, 'rep_aqu_margin' : rep_aqu_margin,
                'mandalay_bay' : mandalay_bay,
                 }

    return render(request, 'kpis/week.html', context)

def report_form(request):
    customers = Customer.objects.all().order_by('customer_name')
    customer_fx_list = []

    for customer in customers:
        customer_fx_list.append({"customer" : customer.customer_name, 
        "currency" : customer.currency, "headsets" : customer.default_headsets,
        "exp_rev_per_gp" : customer.expected_rev_per_gp, "partner_share_perc" : customer.partner_share_perc})

    json_fx = json.dumps(customer_fx_list)

    if request.method == 'POST':
        filled_form = ReportForm(request.POST)
        if filled_form.is_valid():
            success_note = 'Success! The report has been posted.'
            filled_form.save()
            new_form = ReportForm()
            return render(request, 'kpis/report_form.html', 
            {'customers' : customers, 'customer_fx_list' : customer_fx_list,
            'success_note' : success_note,
            'json_fx' : json_fx,
            'report_form' : new_form, 'success_note' : success_note})
        else:
            fail_note = 'Error: Report not posted, please check whether the report already exists for this week.'
            new_form = ReportForm()
            return render(request, 'kpis/report_form.html', 
            {'customers' : customers, 'customer_fx_list' : customer_fx_list,
            'fail_note' : fail_note,
            'json_fx' : json_fx,
            'report_form' : new_form })

    else:
        new_form = ReportForm()
        return render(request, 'kpis/report_form.html', 
        {'customers' : customers, 'customer_fx_list' : customer_fx_list,
        'json_fx' : json_fx,
        'report_form' : new_form })

def update_report(request, pk):
    customers = Customer.objects.all().order_by('customer_name')
    customer_fx_list = []

    for customer in customers:
        customer_fx_list.append({"customer" : customer.customer_name, 
        "currency" : customer.currency, "headsets" : customer.default_headsets,
        "exp_rev_per_gp" : customer.expected_rev_per_gp, "partner_share_perc" : customer.partner_share_perc})

    json_fx = json.dumps(customer_fx_list)

    report = Report.objects.get(id=pk)
    form = ReportForm(instance=report)

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'customers' : customers, 'customer_fx_list' : customer_fx_list, 'json_fx' : json_fx, 'report_form' : form }
    return render(request, 'kpis/edit_form.html', context)

def show_customer(request, customer_slug):
    context = {}

    try:
        customer = Customer.objects.get(slug=customer_slug)
        customer_reports = Report.objects.filter(customer__customer_name=customer.customer_name).order_by('-year','-week_number')

        
        context['customer'] = customer
        context['customer_reports'] = customer_reports
    
    except Customer.DoesNotExist:
        context['customer'] = None
    
    return render(request, 'kpis/customer.html', context)

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('/register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('/register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.info(request, 'User succesfully created!')
                return redirect('/register')

        else:
            print('Password not matching')
            return redirect('/register')

    else:
        return render(request, 'kpis/register.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/all_reports")
        else:
            messages.info(request, 'Invalid credentials')
            return redirect("login")

    else:
        return render(request, 'kpis/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

    