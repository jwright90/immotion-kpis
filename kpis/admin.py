from django.contrib import admin
from .models import Report, Customer, Category, Location

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
	list_display = ('customer', 'year', 'week_number', 'revenue', 'partner_share', 'staff_costs')	
	list_filter = ('year', 'week_number', 'customer_report_received')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ('customer_name', 'slug', 'active')
	list_filter = ('active',)
	prepopulated_fields = { 'slug' : ('customer_name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('category_name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
	list_display = ('location',)
