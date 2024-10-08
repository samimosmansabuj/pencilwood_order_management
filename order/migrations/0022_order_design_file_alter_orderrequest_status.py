# Generated by Django 5.1.1 on 2024-10-08 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0021_order_extra_cost_order_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='design_file',
            field=models.FileField(blank=True, null=True, upload_to='design-files/'),
        ),
        migrations.AlterField(
            model_name='orderrequest',
            name='status',
            field=models.CharField(choices=[('None', 'None'), ('Design', 'Design'), ('Correction', 'Correction'), ('Call', 'Call'), ('Knock', 'Knock'), ('Other', 'Other'), ('Done', 'Done'), ('Sample', 'Sample'), ('Hold', 'Hold'), ('Cancel', 'Cancel'), ('Mockup', 'Mockup')], default='None', max_length=50),
        ),
    ]