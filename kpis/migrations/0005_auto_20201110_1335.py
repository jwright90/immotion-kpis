# Generated by Django 3.1.3 on 2020-11-10 13:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpis', '0004_auto_20201110_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='year',
            field=models.IntegerField(default='setyear', validators=[django.core.validators.MinValueValidator(2018), django.core.validators.MaxValueValidator(2100)]),
        ),
    ]
