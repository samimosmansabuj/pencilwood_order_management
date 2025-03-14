# Generated by Django 5.1.2 on 2025-03-14 13:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Maintenance_Cost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=15)),
                ('note', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Site_Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fav_icon', models.ImageField(blank=True, null=True, upload_to='logo/')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logo/')),
                ('website_name', models.CharField(blank=True, max_length=200, null=True)),
                ('website_title', models.CharField(blank=True, max_length=1000, null=True)),
                ('copyright_company', models.CharField(max_length=200)),
                ('copyright_year', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Daily_Profit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_sell', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('profit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('date', models.DateField()),
                ('last_update', models.DateField(auto_now=True)),
                ('orders', models.ManyToManyField(to='order.order')),
                ('costs', models.ManyToManyField(to='dashboard.maintenance_cost')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('priority', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium', max_length=10)),
                ('details', models.TextField(blank=True, null=True)),
                ('is_complete', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('last_update_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='todo_last_update_user', to=settings.AUTH_USER_MODEL)),
                ('work_assign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='todo_assign', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-update_date'],
            },
        ),
    ]
