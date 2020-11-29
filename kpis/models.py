from django.db import models
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from datetime import datetime

class Category(models.Model):
    category_name = models.CharField(max_length=30)
    #perhaps give different options here
    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Categories'

class Location(models.Model):
    location = models.CharField(max_length=30)

    def __str__(self):
        return self.location

#--- Customer model ---

class Customer(models.Model):
    CURRENCIES = (
        ('USD', 'USD'),
        ('GBP', 'GBP'),
        ('RMB', 'RMB'),
        ('EUR', 'EUR'),
        ('AED', 'AED'),
    )

    customer_name = models.CharField(max_length=30)
    default_headsets = models.PositiveIntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=250, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    active = models.BooleanField(blank=True, default=True)
    currency = models.CharField(max_length=3, choices=CURRENCIES, null=True, blank=True)   

    def save(self, *args, **kwargs):
        self.slug = slugify(self.customer_name)
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.customer_name

#--- Report model ---#

def default_year():
    return int(datetime.now().year)

def default_week():
    week_number = int(datetime.now().isocalendar()[1])
    if week_number == 1:
        return week_number
    else:
        return (week_number - 1)

class Report(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(validators = [MinValueValidator(2018), MaxValueValidator(2100)], default=default_year)
    week_number = models.PositiveIntegerField(validators = [MinValueValidator(1), MaxValueValidator(53)], default=default_week)
    headsets = models.PositiveIntegerField()
    gameplays = models.PositiveIntegerField(null=True, blank=True)
    customer_report_received = models.BooleanField(default=False, null=True, blank=True)
    base_revenue = models.IntegerField(blank=True, null=True)
    fx_rate = models.FloatField(blank=True, null=True)
    revenue = models.IntegerField()
    estimate = models.BooleanField(default=False)
    partner_share = models.PositiveIntegerField(default=0)
    staff_costs = models.PositiveIntegerField(default=0)
    rent_cost = models.PositiveIntegerField(default=0)
    marketing_cost = models.PositiveIntegerField(default=0)
    sundries_cost = models.PositiveIntegerField(default=0)
    
    def revenue_per_headset(self):
        return round(self.revenue / self.headsets)

    def operating_costs(self):
        return round(self.staff_costs + self.rent_cost 
                        + self.marketing_cost + self.sundries_cost )

    def contribution(self):
        return round(self.revenue - self.partner_share)

    def contribution_per_headset(self):
        return round((self.revenue - self.partner_share) / self.headsets)

    def margin(self):
        return round(((self.revenue - self.partner_share) / self.revenue) *100)
        
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer', 'year', 'week_number'], name="unique_period")
        ]