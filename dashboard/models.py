from django.db import models
from order.models import Order, OrderRequest
from account.models import Custom_User

class Site_Settings(models.Model):
    fav_icon = models.ImageField(upload_to='logo/', blank=True, null=True)
    logo = models.ImageField(upload_to='logo/', blank=True, null=True)
    invoice_logo =models.ImageField(upload_to='logo/', blank=True, null=True)
    website_name = models.CharField(max_length=200, blank=True, null=True)
    website_title = models.CharField(max_length=1000, blank=True, null=True)
    copyright_company = models.CharField(max_length=200)
    copyright_year = models.CharField(max_length=4)
    
    def __str__(self) -> str:
        return f'Settings {self.id}'


class Maintenance_Cost(models.Model):
    title = models.CharField(max_length=500)
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'Cost of {self.create_date} - {self.id}'


class Daily_Profit(models.Model):
    orders = models.ManyToManyField(Order)
    costs = models.ManyToManyField(Maintenance_Cost)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_sell = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField()
    last_update = models.DateField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
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





class Todo(models.Model):
    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )

    title = models.CharField(max_length=255)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    details = models.TextField(blank=True, null=True)
    work_assign = models.ForeignKey(Custom_User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='todo_assign')
    is_complete = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    last_update_user = models.ForeignKey(Custom_User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='todo_last_update_user')
    
    class Meta:
        ordering = ['-update_date']

    def __str__(self):
        return self.title


class Remainder(models.Model):
    date = models.DateField()
    note = models.TextField(blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='order_remainder')
    order_request = models.ForeignKey(OrderRequest, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='order_request_remainder')
    is_complete = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.date} | {self.order if self.order else None} - {self.order_request if self.order_request else None}'


class InvoiceColorDesign(models.Model):
    header_bg = models.CharField(max_length=10, blank=True, null=True)
    footer_bg = models.CharField(max_length=10, blank=True, null=True)
    footer_text_text = models.CharField(max_length=10, blank=True, null=True)
    header_text_color = models.CharField(max_length=10, blank=True, null=True)
    highlight_color = models.CharField(max_length=10, blank=True, null=True)
    table_header_text = models.CharField(max_length=10, blank=True, null=True)

    def __call__(self, *args, **kwds):
        return f"Invoice Color Config - {self.pk}"

