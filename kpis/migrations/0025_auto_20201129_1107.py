# Generated by Django 3.1.3 on 2020-11-29 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpis', '0024_customer_default_headsets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='customer_report_received',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
