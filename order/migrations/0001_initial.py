# Generated by Django 5.1.2 on 2024-11-03 11:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_ID', models.CharField(blank=True, max_length=6, null=True)),
                ('company', models.CharField(blank=True, max_length=250, null=True)),
                ('name', models.CharField(max_length=250)),
                ('phone_number', models.CharField(max_length=20)),
                ('second_phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('source', models.CharField(choices=[('Facebook', 'Facebook'), ('Whatsapp', 'Whatsapp'), ('Website', 'Website'), ('Others', 'Others')], default='Others', max_length=50)),
                ('logo', models.URLField(blank=True, max_length=1000, null=True)),
                ('picture1', models.URLField(blank=True, max_length=1000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_ID', models.CharField(blank=True, max_length=5, null=True, unique=True)),
                ('company', models.CharField(blank=True, max_length=250, null=True)),
                ('name', models.CharField(max_length=250)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('second_phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('source', models.CharField(choices=[('Facebook', 'Facebook'), ('Whatsapp', 'Whatsapp'), ('Website', 'Website'), ('Others', 'Others')], default='Others', max_length=50)),
                ('status', models.CharField(choices=[('None', 'None'), ('Design', 'Design'), ('Correction', 'Correction'), ('Call', 'Call'), ('Knock', 'Knock'), ('Other', 'Other'), ('Done', 'Done'), ('Hold', 'Hold'), ('Cancel', 'Cancel'), ('Mockup', 'Mockup')], default='None', max_length=50)),
                ('remark', models.TextField(blank=True, null=True)),
                ('order_created', models.BooleanField(default=False)),
                ('logo', models.URLField(blank=True, max_length=1000, null=True)),
                ('picture1', models.URLField(blank=True, max_length=1000, null=True)),
                ('picture2', models.URLField(blank=True, max_length=1000, null=True)),
                ('picture3', models.URLField(blank=True, max_length=1000, null=True)),
                ('picture4', models.URLField(blank=True, max_length=1000, null=True)),
                ('picture5', models.URLField(blank=True, max_length=1000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('request_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('work_assign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_request_assign', to=settings.AUTH_USER_MODEL)),
                ('product', models.ManyToManyField(to='order.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_ID', models.CharField(blank=True, max_length=6, null=True, unique=True)),
                ('delivery_address', models.CharField(blank=True, max_length=500, null=True)),
                ('special_instructions', models.TextField(blank=True, null=True)),
                ('design_file', models.FileField(blank=True, null=True, upload_to='order-design-files/')),
                ('deal_value', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('advance_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('due_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('delivery_charge', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('delivery_charge_cost', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('extra_cost', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('payment_number', models.CharField(blank=True, max_length=13, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=30, null=True)),
                ('payment_method', models.CharField(blank=True, choices=[('COD', 'COD'), ('Bkash', 'Bkash'), ('Nagod', 'Nagod'), ('Rocket', 'Rocket'), ('Upay', 'Upay')], max_length=20, null=True)),
                ('payment_status', models.CharField(choices=[('Unpaid', 'Unpaid'), ('Partial', 'Partial'), ('Paid', 'Paid')], default='Unpaid', max_length=50)),
                ('status', models.CharField(blank=True, choices=[('None', 'None'), ('Got Design', 'Got Design'), ('Sample', 'Sample'), ('Cutting', 'Cutting'), ('Cutout Ready', 'Cutout Ready'), ('Engrave', 'Engrave'), ('Finishing', 'Finishing'), ('Packaging', 'Packaging'), ('Delivered', 'Delivered'), ('Return', 'Return')], default='Pending', max_length=50, null=True)),
                ('remark', models.TextField(blank=True, null=True)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('work_assign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_assign', to=settings.AUTH_USER_MODEL)),
                ('order_customer', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='order.ordercustomer')),
                ('order_item', models.ManyToManyField(related_name='order_items', to='order.orderitem')),
                ('request_order', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='order.orderrequest')),
            ],
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='orderitem_product', to='order.product'),
        ),
        migrations.AddField(
            model_name='ordercustomer',
            name='product',
            field=models.ManyToManyField(to='order.product'),
        ),
    ]
