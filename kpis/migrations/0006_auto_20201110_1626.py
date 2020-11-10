# Generated by Django 3.1.3 on 2020-11-10 16:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpis', '0005_auto_20201110_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='estimate',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='report',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(2018), django.core.validators.MaxValueValidator(2100)]),
        ),
    ]
