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
    orders = models.ManyToManyField(Order, blank=True, null=True)
    costs = models.ManyToManyField(Maintenance_Cost, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_sell = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.pk:
            total_sell_sum = sum(order.total_amount for order in self.orders.all())
            self.total_sell = total_sell_sum
            
            cost_sum = sum(cost_item.cost for cost_item in self.costs.all())
            self.cost = cost_sum
            
            self.profit = self.total_sell - self.cost if self.total_sell or self.cost else None

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Date: {self.date} total Profit - {self.profit}"


