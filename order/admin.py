from django.contrib import admin
from .models import *

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = []

# @admin.register(OrderRequest)
# class OrderRequestAdmin(admin.ModelAdmin):
#     # list_display = []
#     search_fields = ['company', 'created_at', 'id', 'last_update', 'logo', 'name', 'order', 'phone_number', 'picture1', 'picture2', 'picture3', 'picture4', 'picture5', 'remark', 'request_created_by', 'request_created_by_id', 'second_phone_number', 'source', 'status', 'tracking_ID', 'work_assign']


@admin.register(OrderRequest)
class OrderRequestAdmin(admin.ModelAdmin):
    search_fields = [
        'company', 'created_at', 'id', 'last_update', 'logo', 'name', 'order_created', 
        'phone_number', 'picture1', 'picture2', 'picture3', 'picture4', 'picture5', 'remark', 
        'second_phone_number', 'source', 'status', 'tracking_ID'
    ]

    # Additional configuration if needed
    list_display = ['tracking_ID', 'name', 'company', 'status', 'created_at', 'last_update']
    list_filter = ['status', 'source', 'order_created', 'work_assign']

    # Use this to display the ManyToManyField
    filter_horizontal = ('product',)

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = []


admin.site.register(Product)
# admin.site.register(OrderRequest)
admin.site.register(OrderCustomer)
admin.site.register(Order)
admin.site.register(OrderItem)
