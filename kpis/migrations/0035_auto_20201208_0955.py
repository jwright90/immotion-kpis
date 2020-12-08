# Generated by Django 3.1.3 on 2020-12-08 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpis', '0034_auto_20201202_1614'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'get_latest_by': 'year'},
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='accounts_contact_first_name',
            new_name='accounts_contact_name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='accounts_contact_last_name',
        ),
        migrations.AlterField(
            model_name='customer',
            name='currency',
            field=models.CharField(blank=True, choices=[('USD', 'USD'), ('GBP', 'GBP'), ('RMB', 'RMB'), ('EUR', 'EUR'), ('AED', 'AED'), ('AUD', 'AUD')], max_length=3, null=True),
        ),
    ]
