from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

# Weeks
## Each report has one week, each week has many reports
## I want the user to enter the year and week number for each report

# Reports
# Customers
# Categories
# Locations

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

class Customer(models.Model):
    customer_name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=250, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer_name

class Report(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    year = models.IntegerField(validators = [MinValueValidator(2018), MaxValueValidator(2100)])
    week_number = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(53)])
    headsets = models.IntegerField()
    revenue = models.IntegerField()
    partner_share = models.IntegerField()
    staff_costs = models.IntegerField()
    rent_cost = models.IntegerField()
    marketing_cost = models.IntegerField()
    sundries_cost = models.IntegerField()

    def contribution(self):
        return self.revenue - self.partner_share

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['year', 'week_number'], name="unique_period")
        ]