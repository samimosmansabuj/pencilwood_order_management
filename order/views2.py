from django.shortcuts import render, redirect
from .models import Product

def add_new_order2(request):
    products = Product.objects.all()
    return render(request, "add_new_order2.html", {'products': products})


