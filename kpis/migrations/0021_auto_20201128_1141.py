# Generated by Django 3.1.3 on 2020-11-28 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpis', '0020_auto_20201121_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='fx_rate_test',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='gbp_revenue',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
