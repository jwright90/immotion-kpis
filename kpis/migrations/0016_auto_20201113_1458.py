# Generated by Django 3.1.3 on 2020-11-13 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kpis', '0015_auto_20201113_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='headsets_additions',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='headsets_basecount',
        ),
    ]
