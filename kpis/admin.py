from django.contrib import admin
from .models import *

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
	list_display = ('customer', 'year', 'week_number', 'revenue', 'partner_share', 'staff_costs')	
	list_filter = ('year', 'week_number', 'customer', 'estimate')
	ordering = ['-year', '-week_number', 'customer__customer_name']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ('customer_name', 'default_headsets', 'category', 'currency', 'expected_rev_per_gp', 'active',)
	list_filter = ('active',)
	prepopulated_fields = { 'slug' : ('customer_name',)}
	ordering = ['customer_name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('category_name',)
	ordering = ['category_name']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
	list_display = ('location',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = ('customer', 'name', 'email', 'department', 'notes')
	ordering = ['customer']