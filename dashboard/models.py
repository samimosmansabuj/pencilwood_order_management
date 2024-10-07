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
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'Cost of {self.create_date} - {self.id}'


class Daily_Profit(models.Model):
    orders = models.ManyToManyField(Order)
    maintenance_cost = models.ManyToManyField(Maintenance_Cost)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_sell = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    note = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)
    
    def save(self, *args, **kwargs):
        today_orders = Order.objects.filter(order_date__date=self.date)
        today_maintenance_costs = Maintenance_Cost.objects.filter(create_date__date=self.date)
        
        super(Daily_Profit, self).save(*args, **kwargs)
        self.orders.set(today_orders)
        self.maintenance_cost.set(today_maintenance_costs)

        # Calculate total_sell & cost
        self.total_sell = today_orders.aggregate(total_sell=models.Sum('total_amount'))['total_sell'] or 0
        self.cost = today_maintenance_costs.aggregate(total_cost=models.Sum('cost'))['total_cost'] or 0
        self.profit = self.total_sell - self.cost
        
        super(Daily_Profit, self).save(update_fields=['total_sell', 'cost', 'profit', 'last_update', 'note'])

    def __str__(self) -> str:
        return f"Date: {self.date} total Profit - {self.profit}"


