# Generated by Django 5.1.1 on 2024-10-07 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_site_settings_website_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maintenance_Cost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=5)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]