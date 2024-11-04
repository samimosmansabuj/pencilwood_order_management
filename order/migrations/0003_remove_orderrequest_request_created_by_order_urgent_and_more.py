# Generated by Django 5.1.2 on 2024-11-04 16:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_created_by_order_last_updated_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderrequest',
            name='request_created_by',
        ),
        migrations.AddField(
            model_name='order',
            name='urgent',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderrequest',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='request_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderrequest',
            name='last_updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='request_last_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='last_updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_last_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]