from .models import Report, Customer
from django import forms
from django.forms import MultiWidget, NumberInput
import django_filters

class ReportFilter(django_filters.FilterSet):
    week_number = django_filters.RangeFilter(
        field_name='week_number',
        widget= MultiWidget(widgets={'from' : NumberInput, 'to' : NumberInput}),
    )
    
    class Meta:
        model = Report
        fields =    {   'year' :        ['exact' ], 
                        'week_number' : ['exact' ],
                        'customer__category' : ['exact'],
                    }