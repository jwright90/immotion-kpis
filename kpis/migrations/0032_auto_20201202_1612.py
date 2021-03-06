# Generated by Django 3.1.3 on 2020-12-02 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpis', '0031_customer_contact_accounts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='contact_accounts',
            new_name='contact_accounts_email',
        ),
        migrations.AddField(
            model_name='customer',
            name='contact_first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='contact_last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
