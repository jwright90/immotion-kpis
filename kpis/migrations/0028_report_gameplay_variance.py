# Generated by Django 3.1.3 on 2020-11-29 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpis', '0027_customer_expected_rev_per_gp'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='gameplay_variance',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
