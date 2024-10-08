from django.db import models
from order.models import Order

class Site_Settings(models.Model):
    fav_icon = models.ImageField(upload_to='logo/', blank=True, null=True)
    logo = models.ImageField(upload_to='logo/', blank=True, null=True)
    website_name = models.CharField(max_length=200, blank=True, null=True)
    website_title = models.CharField(max_length=1000, blank=True, null=True)
    copyright_company = models.CharField(max_length=200)
    copyright_year = models.CharField(max_length=4)
    
    def __str__(self) -> str:
        return f'Settings {self.id}'


class Maintenance_Cost(models.Model):
    title = models.CharField(max_length=500)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'Cost of {self.create_date} - {self.id}'


class Daily_Profit(models.Model):
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_sell = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    note = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"Date: {self.date} total Profit - {self.profit}"


