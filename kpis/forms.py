from django import forms
from .models import Report
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['customer'].queryset = self.fields['customer'].queryset.order_by('customer_name')

    base_revenue = forms.IntegerField(
        label = "Revenue (Base Currency)",
    )

    revenue = forms.IntegerField(
        label = "Revenue (GBP)",
    )

    class Meta:
        model = Report
        fields = '__all__'