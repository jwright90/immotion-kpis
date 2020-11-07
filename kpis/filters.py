from .models import Report
import django_filters

class ReportFilter(django_filters.FilterSet):
    week_number = django_filters.RangeFilter(
        field_name='week_number',
        widget=django_filters.widgets.RangeWidget(
            attrs={'placeholder': 'enter week number'})
    )
    
    class Meta:
        model = Report
        fields =    {   'year' :        ['exact' ], 
                        'week_number' : ['exact' ]
                    }

