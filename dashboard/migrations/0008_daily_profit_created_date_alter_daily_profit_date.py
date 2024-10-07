# Generated by Django 5.1.1 on 2024-10-07 17:32

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_remove_daily_profit_created_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='daily_profit',
            name='created_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='daily_profit',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]
