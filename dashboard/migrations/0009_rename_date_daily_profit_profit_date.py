# Generated by Django 5.1.1 on 2024-10-07 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_daily_profit_created_date_alter_daily_profit_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='daily_profit',
            old_name='date',
            new_name='profit_date',
        ),
    ]
