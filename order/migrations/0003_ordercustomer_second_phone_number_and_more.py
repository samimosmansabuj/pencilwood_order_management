# Generated by Django 5.1.1 on 2024-10-29 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_orderrequest_work_assign_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordercustomer',
            name='second_phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='orderrequest',
            name='second_phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
