from django.db import models
import random, string
from django.utils.text import slugify
from account.models import Custom_User


class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
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
        ('Get Design', 'Get Design'),
        ('Done', 'Done'),
        ('Sample', 'Sample'),
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
    request_created_by = models.ForeignKey(Custom_User, on_delete=models.SET_NULL, blank=True, null=True)
    tracking_ID = models.CharField(max_length=10, blank=True, null=True)
    
    company = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=20)
    source = models.CharField(choices=SOURCE, max_length=50, default='Others')
    product = models.ManyToManyField(Product)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='None')
    remark = models.TextField(blank=True, null=True)
    order_created = models.BooleanField(default=False)
    
    logo = models.URLField(max_length=300, blank=True, null=True)
    picture1 = models.URLField(max_length=300, blank=True, null=True)
    picture2 = models.URLField(max_length=300, blank=True, null=True)
    picture3 = models.URLField(max_length=300, blank=True, null=True)
    picture4 = models.URLField(max_length=300, blank=True, null=True)
    picture5 = models.URLField(max_length=300, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"OrderRequest#{self.tracking_ID} from {self.company} ({self.name})"
    
    def save(self, *args, **kwargs):
        if not self.tracking_ID:
            self.tracking_ID = ''.join(random.choices(string.digits, k=10))
        super().save(*args, **kwargs)




class OrderCustomer(models.Model):
    SOURCE = (
        ('Facebook', 'Facebook'),
        ('Whatsapp', 'Whatsapp'),
        ('Website', 'Website'),
        ('Others', 'Others'),
    )
    tracking_ID = models.CharField(max_length=12, blank=True, null=True)
    company = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=20)
    source = models.CharField(choices=SOURCE, max_length=50, default='Others')
    product = models.ManyToManyField(Product)
    
    logo = models.URLField(max_length=1000, blank=True, null=True)
    picture1 = models.URLField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.tracking_ID:
            self.tracking_ID = ''.join(random.choices(string.digits, k=12))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order#{self.tracking_ID} from {self.company} ({self.name})"
    

class Order(models.Model):
    STATUS = (
        ('None', 'None'),
        ('Got Design', 'Got Design'),
        ('Cutting', 'Cutting'),
        ('Cutout Ready', 'Cutout Ready'),
        ('Engrave', 'Engrave'),
        ('Finishing', 'Finishing'),
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
    tracking_ID = models.CharField(max_length=12, blank=True, null=True)
    delivery_address = models.CharField(max_length=500)
    special_instructions = models.TextField(blank=True, null=True)
    
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=9, blank=True, null=True, decimal_places=2)
    deal_value = models.DecimalField(max_digits=9, blank=True, null=True, decimal_places=2)
    advance_amount = models.DecimalField(max_digits=9, blank=True, null=True, decimal_places=2)
    due_amount = models.DecimalField(max_digits=9, blank=True, null=True, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=9, blank=True, null=True, decimal_places=2)
    
    payment_number = models.CharField(max_length=13, blank=True, null=True)
    transaction_id = models.CharField(max_length=30, blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, blank=True, null=True)
    payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=50, default='Unpaid')
    
    status = models.CharField(choices=STATUS, max_length=50, default='Pending')
    work_assign = models.ForeignKey(Custom_User, on_delete=models.CASCADE, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    
    order_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    delivery_date = models.DateField(blank=True,null=True)
    return_date = models.DateField(blank=True,null=True)
    
    def save(self, *args, **kwargs):
        unit_price = self.unit_price or 0
        quantity = self.quantity or 0
        
        advance_amount = self.advance_amount or 0
        delivery_charge = self.delivery_charge or 0
        
        self.deal_value = unit_price * quantity
        self.due_amount = (unit_price * quantity + delivery_charge) - advance_amount
        
        if self.request_order:
            self.tracking_ID = self.request_order.tracking_ID
            self.request_order.order_created = True
            self.request_order.save()
        elif self.order_customer:
            self.tracking_ID = self.order_customer.tracking_ID
        super(Order, self).save(*args, **kwargs)
    
    def __str__(self):
        if self.request_order:
            return f"Order#{self.tracking_ID} for {self.request_order}"
        elif self.order_customer:
            return f"Order#{self.tracking_ID} with {self.order_customer}"
        else:
            return f"Order#{self.tracking_ID}"


class OrderUpdateNote(models.Model):
    order = models.ManyToManyField(Order, related_name='order_note')
    note = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.note:
            self.note = f'Update this order status to {self.order.status} at {self.date}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.order} | {self.date}'


