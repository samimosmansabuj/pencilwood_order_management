from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, OrderItem, Order
from .forms import OrderCustomerForm, OrderForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dashboard.models import InvoiceColorDesign

@login_required
def add_new_order2(request):
    products = Product.objects.all()
    if request.method == 'POST':
        order_customer_form = OrderCustomerForm(request.POST)
        order_form = OrderForm(request.POST, request.FILES)

        product = Product.objects.filter(slug__in=request.POST.getlist("slug"))
        product_unit_price_lsit = request.POST.getlist("unit_price")
        product_quantity_lsit = request.POST.getlist("quantity")
        if not (len(product) == len(product_unit_price_lsit) == len(product_quantity_lsit)):
            messages.warning(request, f"Something problem for product added!")
            return redirect(request.META['HTTP_REFERER'])

        if order_customer_form.is_valid() and order_form.is_valid():
            order_customer = order_customer_form.save()
            order = order_form.save(commit=False)
            order.order_customer=order_customer
            order.save()

            order_items = [
                OrderItem.objects.create(
                    product=p,
                    quantity=q,
                    unit_price=u
                )
                for p, q, u in zip(product, product_quantity_lsit, product_unit_price_lsit)
            ]

            order.order_item.add(*order_items)
            order.save()
            return redirect('order_success', id=order.id)
        else:
            messages.warning(request, f"{order_customer_form.errors} and {order_form.errors}")
            return redirect(request.META['HTTP_REFERER'])
    
    order_customer_form = OrderCustomerForm()
    order_form = OrderForm()

    return render(request, "orderr/add_new_order2.html", {'products': products, 'order_customer_form': order_customer_form, 'order_form': order_form})


@login_required
def new_generate_invoice(request, id):
    design = InvoiceColorDesign.objects.all().first()
    order = get_object_or_404(Order, id=id)
    context = {'order': order, 'design': design}

    print("header_bg: ", design.header_bg)
    return render(request, 'invoices/invoice.html', context)
