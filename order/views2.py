from django.shortcuts import render, redirect
from .models import Product
from .forms import OrderCustomerForm, OrderForm

def add_new_order2(request):
    products = Product.objects.all()
    order_customer_form = OrderCustomerForm()
    order_form = OrderForm()
    return render(request, "add_new_order2.html", {'products': products, 'order_customer_form': order_customer_form, 'order_form': order_form})


