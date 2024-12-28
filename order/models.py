from django.db.models.signals import pre_delete
from .middleware import get_current_user
from account.models import Custom_User
from django.utils.text import slugify
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
import random, string


class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name


class OrderRequest(models.Model):
    STATUS_CHOICES = (
        ('None', 'None'),
        ('Design', 'Design'),
        ('Correction', 'Correction'),
        ('Call', 'Call'),
        ('Knock', 'Knock'),
        ('Other', 'Other'),
        ('Done', 'Done'),
        ('Hold', 'Hold'),
        ('Cancel', 'Cancel'),
        ('Mockup', 'Mockup'),
    )
    SOURCE = (
        ('Facebook', 'Facebook'),
        ('Whatsapp', 'Whatsapp'),
        ('Website', 'Website'),
        ('Others', 'Others'),
    )
    created_by = models.ForeignKey(Custom_User, on_delete=models.SET_NULL, blank=True, null=True, related_name='request_created_by')
    last_updated_by = models.ForeignKey(Custom_User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='request_last_updated_by')
    tracking_ID = models.CharField(max_length=5, unique=True, blank=True, null=True)
    
    company = models.CharField(max_length=250, blank=True, null=True)
    name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    second_phone_number = models.CharField(max_length=20, blank=True, null=True)
    source = models.CharField(choices=SOURCE, max_length=50, default='Others')
    product = models.ManyToManyField(Product)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='None')
    remark = models.TextField(blank=True, null=True)
    work_assign = models.ForeignKey(Custom_User, on_delete=models.CASCADE, blank=True, null=True, related_name='order_request_assign')
    order_created = models.BooleanField(default=False)
    urgent = models.BooleanField(blank=True, null=True)
    
    logo = models.URLField(max_length=1000, blank=True, null=True)
    picture1 = models.URLField(max_length=1000, blank=True, null=True)
    picture2 = models.URLField(max_length=1000, blank=True, null=True)
    picture3 = models.URLField(max_length=1000, blank=True, null=True)
    picture4 = models.URLField(max_length=1000, blank=True, null=True)
    picture5 = models.URLField(max_length=1000, blank=True, null=True)
    
    created_at = models.DateField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"OrderRequest#{self.tracking_ID} from {self.company} ({self.name})"
    
    def save(self, *args, **kwargs):
        if not self.pk or not self.created_by_id:
            self.created_by = get_current_user()
        self.last_updated_by = get_current_user()
        
        if not self.tracking_ID:
            unique = False
            while not unique:
                tracking_ID_candidate = ''.join(random.choices(string.digits, k=5))
                if not OrderRequest.objects.filter(tracking_ID=tracking_ID_candidate).exists():
                    self.tracking_ID = tracking_ID_candidate
                    unique = True
        super().save(*args, **kwargs)
            


class OrderCustomer(models.Model):
    SOURCE = (
        ('Facebook', 'Facebook'),
        ('Whatsapp', 'Whatsapp'),
        ('Website', 'Website'),
        ('Others', 'Others'),
    )
    tracking_ID = models.CharField(max_length=6, blank=True, null=True)
    company = models.CharField(max_length=250, blank=True, null=True)
    name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=20)
    second_phone_number = models.CharField(max_length=20, blank=True, null=True)
    source = models.CharField(choices=SOURCE, max_length=50, default='Others')
    product = models.ManyToManyField(Product)
    
    logo = models.URLField(max_length=1000, blank=True, null=True)
    picture1 = models.URLField(max_length=1000, blank=True, null=True)
    created_at = models.DateField(blank=True, null=True)
    
    
    def save(self, *args, **kwargs):
        if not self.tracking_ID:
            self.tracking_ID = ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)
        
        if Order.objects.filter(order_customer=self).exists():
            Order.objects.get(order_customer=self).save()
        
    
    def __str__(self):
        return f"Order#{self.tracking_ID} from {self.company} ({self.name})"
 



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='orderitem_product')
    quantity = quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    
    def save(self, *args, **kwargs):
        quantity = self.quantity or 0
        unit_price = self.unit_price or 0
        self.total = unit_price * quantity
        super(OrderItem, self).save(*args, **kwargs)
    
    def __str__(self):
        order = self.order_items.first()
        order_tracking_id = order.tracking_ID if order else "No Order"
        return f"Order#{order_tracking_id} - {self.product.name}"


class Order(models.Model):
    STATUS = (
        ('None', 'None'),
        ('Got Design', 'Got Design'),
        ('Processing', 'Processing'),
        ('Sample', 'Sample'),
        ('Packaging', 'Packaging'),
        ('Delivered', 'Delivered'),
        ('Return', 'Return'),
    )
    PAYMENT_STATUS = (
        ('Unpaid', 'Unpaid'),
        ('Partial', 'Partial'),
        ('Paid', 'Paid'),
    )
    PAYMENT_METHOD = (
        ('COD', 'COD'),
        ('Bkash', 'Bkash'),
        ('Nagod', 'Nagod'),
        ('Rocket', 'Rocket'),
        ('Upay', 'Upay'),
    )
    request_order = models.OneToOneField(OrderRequest, on_delete=models.CASCADE, blank=True, null=True, related_name='order')
    order_customer = models.OneToOneField(OrderCustomer, on_delete=models.CASCADE, blank=True, null=True, related_name='order')
    
    tracking_ID = models.CharField(max_length=6, blank=True, null=True, unique=True)
    pathao_parcel_id = models.CharField(max_length=20, blank=True, null=True)
    delivery_address = models.CharField(max_length=500, blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)
    design_file = models.FileField(upload_to='order-design-files/', blank=True, null=True)
    order_item = models.ManyToManyField(OrderItem, related_name='order_items')
    
    deal_value = models.DecimalField(max_digits=9, blank=True, null=True, decimal_places=2, default=0)
    advance_amount = models.DecimalField(max_digits=9, blank=True, null=True, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=9, blank=True, null=True, decimal_places=2, default=0)
    delivery_charge = models.DecimalField(max_digits=9, blank=True, null=True, decimal_places=2, default=0)
    delivery_charge_cost = models.DecimalField(max_digits=9, blank=True, null=True, decimal_places=2, default=0)
    extra_cost = models.DecimalField(max_digits=9, blank=True, null=True, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=9, blank=True, null=True, decimal_places=2, default=0)
    
    
    payment_number = models.CharField(max_length=13, blank=True, null=True)
    transaction_id = models.CharField(max_length=30, blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, blank=True, null=True)
    payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=50, default='Unpaid')
    
    status = models.CharField(choices=STATUS, max_length=50, blank=True, null=True)
    urgent = models.BooleanField(blank=True, null=True)
    work_assign = models.ForeignKey(Custom_User, on_delete=models.CASCADE, blank=True, null=True, related_name='order_assign')
    remark = models.TextField(blank=True, null=True)
    
    created_by = models.ForeignKey(Custom_User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='order_created_by')
    last_updated_by = models.ForeignKey(Custom_User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='order_last_updated_by')
    order_date = models.DateField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
    delivery_date = models.DateField(blank=True,null=True)
    return_date = models.DateField(blank=True,null=True)
    
    def total_quantity(self):
        return sum(item.quantity for item in self.order_item.all())
    
    def get_status_choices(self):
        return self.STATUS
    
    def add_missing_order_items(self):
        products = set()
        if self.order_customer:
            products = self.order_customer.product.all()
        elif self.request_order:
            products = self.request_order.product.all()
        
        existing_products = {item.product for item in self.order_item.all()}
        for product in products:
            if product not in existing_products:
                order_item = OrderItem.objects.create(product=product)
                self.order_item.add(order_item)
    
    def save(self, *args, **kwargs):
        if not self.pk or not self.created_by_id:
            self.created_by = get_current_user()
        self.last_updated_by = get_current_user()
        
        super(Order, self).save(*args, **kwargs)
        self.add_missing_order_items()
        
        deal_value = sum(item.total for item in self.order_item.all())
        advance_amount = self.advance_amount or 0
        delivery_charge = self.delivery_charge or 0
        delivery_charge_cost = self.delivery_charge_cost or 0
        due_amount = (deal_value + delivery_charge) - advance_amount
        extra_cost = delivery_charge_cost - delivery_charge
        
        self.deal_value = deal_value
        self.due_amount = due_amount
        self.extra_cost = extra_cost
        self.total_amount = deal_value - extra_cost
        
        if self.request_order:
            self.tracking_ID = self.request_order.tracking_ID
            self.request_order.order_created = True
            self.request_order.save()
        elif self.order_customer:
            self.tracking_ID = self.order_customer.tracking_ID
        
        if self.status == 'Delivered' or self.status == 'Return':
            self.urgent = False
        
        super(Order, self).save(*args, **kwargs)
        
        from dashboard.models import Daily_Profit
        # date = timezone.localtime(self.order_date).date()
        date = self.order_date
        daily_profit, created = Daily_Profit.objects.get_or_create(date=date)
        daily_profit.orders.add(self)
        daily_profit.save()
        
        # if self.order_customer:
        #     customer_order = self.order_customer
        #     customer_order.created_at = date
        #     customer_order.save()
        
        
    def __str__(self):
        if self.request_order:
            return f"Order#{self.tracking_ID} for {self.request_order}"
        elif self.order_customer:
            return f"Order#{self.tracking_ID} with {self.order_customer}"
        else:
            return f"Order#{self.tracking_ID}"


@receiver(pre_delete, sender=Order)
def reset_order_created(sender, instance, **kwargs):
    if instance.request_order:
        instance.request_order.order_created = False
        instance.request_order.save()
    
    from dashboard.models import Daily_Profit
    date = instance.order_date
    daily_profit, created = Daily_Profit.objects.get_or_create(date=date)
    daily_profit.orders.remove(instance)
    daily_profit.save()
    
    if instance.order_item:
        for order_item in instance.order_item.all():
                order_item.delete()
    
    if instance.order_customer:
        pre_delete.disconnect(reset_order_created, sender=Order)
        try:
            instance.order_customer.delete()
            print(instance.order_item.all())
        finally:
            # Reconnect the signal after deletion is complete
            pre_delete.connect(reset_order_created, sender=Order)




