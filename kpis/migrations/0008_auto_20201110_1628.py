# Generated by Django 3.1.3 on 2020-11-10 16:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpis', '0007_auto_20201110_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='year',
            field=models.PositiveIntegerField(default=2020, validators=[django.core.validators.MinValueValidator(2018), django.core.validators.MaxValueValidator(2100)]),
        ),
    ]