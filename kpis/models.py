from datetime import datetime
from django.db import models
from django.db.models import Sum, Avg, Count
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.template.defaultfilters import slugify

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
        ('AUD', 'AUD'),
    )

    customer_name = models.CharField(max_length=30)
    default_headsets = models.PositiveIntegerField(blank=True, null=True)
    partner_share_perc = models.PositiveIntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=250, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    active = models.BooleanField(blank=True, default=True)
    currency = models.CharField(max_length=3, choices=CURRENCIES, null=True, blank=True)
    expected_rev_per_gp = models.FloatField(null=True, blank=True)
    accounts_contact_first_name = models.CharField(max_length=100, null=True, blank=True)
    accounts_contact_last_name = models.CharField(max_length=100, null=True, blank=True)
    accounts_contact_email = models.EmailField(null=True, blank=True)   

    def save(self, *args, **kwargs):
        self.slug = slugify(self.customer_name)
        if self.expected_rev_per_gp:
            self.expected_rev_per_gp = round(self.expected_rev_per_gp, 2)
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
    base_revenue = models.PositiveIntegerField(blank=True, null=True)
    fx_rate = models.FloatField(blank=True, null=True)
    revenue = models.PositiveIntegerField()
    estimate = models.BooleanField(default=False)
    partner_share = models.PositiveIntegerField(default=0)
    staff_costs = models.PositiveIntegerField(default=0)
    rent_cost = models.PositiveIntegerField(default=0)
    marketing_cost = models.PositiveIntegerField(default=0)
    sundries_cost = models.PositiveIntegerField(default=0)
    gameplay_variance = models.IntegerField(null=True, blank=True)
    
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