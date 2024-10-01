from django.contrib import admin
from .models import *

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = []

# @admin.register(OrderRequest)
# class OrderRequestAdmin(admin.ModelAdmin):
#     list_display = []

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = []

admin.site.register(Product)
admin.site.register(OrderRequest)
admin.site.register(Order)
admin.site.register(OrderUpdateNote)
