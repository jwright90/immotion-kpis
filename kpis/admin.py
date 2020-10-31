from django.contrib import admin
from .models import Report, Customer, Category, Location


# Register your models here.

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
	list_display = ('customer', 'year', 'week_number', 'revenue', 'partner_share', 'staff_costs')	
	list_filter = ('year', 'week_number')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ('customer_name', 'slug')
	prepopulated_fields = { 'slug' : ('customer_name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('category_name',)

@admin.register(Location)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('location',)
