from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Order, OrderRequest
from django.contrib import messages
from django.utils import timezone
from .forms import *
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def order_list(request):
    filter = request.GET.get('filter')
    
    if filter == 'active':
        order = Order.objects.filter(
                Q(status='Got Design') | Q(status='Cutting') | Q(status='Cutout Ready') | Q(status='Engrave') | Q(status='Finishing') | Q(status='Packaging') | Q(status='Delivered')).order_by('-id')
    elif filter == 'pending':
        order = Order.objects.filter(status='Pending').order_by('-id')
    elif filter == 'today':
        today = timezone.now().date()
        order = Order.objects.filter(order_date__date=today).order_by('-id')
        # order = Order.objects.filter(status='Pending').order_by('-id')
    elif filter == 'delivered':
        order = Order.objects.filter(status='Delivered').order_by('-id')
    else:
        order = Order.objects.all().order_by('-id')
    
    return render(request, 'order/order.html', {'orders': order})


@login_required
def order_view(request, id):
    order = get_object_or_404(Order, id=id)
    
    if request.method == 'POST':
        form = OrderStatusUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order Update Successfully!')
        else:
            messages.error(request, 'Somethings is wrong, please try again!')
        return redirect(request.META['HTTP_REFERER'])
    else:
        form = OrderStatusUpdateForm(instance=order)
    
    return render(request, 'order/order_view.html', {'order': order, 'form': form})


@login_required
def add_new_order(request):
    if request.method == 'POST':
        order_customer_form = OrderCustomerForm(request.POST)
        order_form = OrderForm(request.POST)

        if order_customer_form.is_valid() and order_form.is_valid():
            order_customer = order_customer_form.save()

            order = order_form.save(commit=False)
            order.order_customer = order_customer
            order.save()

            return redirect('order_success')
        else:
            messages.warning(request, f"{order_customer_form.errors} and {order_form.errors}")
            return redirect(request.META['HTTP_REFERER'])
    else:
        order_customer_form = OrderCustomerForm()
        order_form = OrderForm()

    return render(request, 'order/add_new_order.html', {
        'order_customer_form': order_customer_form,
        'order_form': order_form
    })

def order_success(request):
    return render(request, 'order/order_success.html')





class OrderRequestListView(LoginRequiredMixin, ListView):
    model = OrderRequest
    template_name = 'request/order_request_list.html'  # Define your template here
    context_object_name = 'order_requests'
    ordering = ['-id']

class OrderRequestCreateView(LoginRequiredMixin, CreateView):
    model = OrderRequest
    form_class = OrderRequestForm
    template_name = 'request/order_request_form.html'
    success_url = reverse_lazy('order_request_list')
    
    def form_valid(self, form):
        form.instance.request_created_by = self.request.user  # Automatically set request_at
        return super().form_valid(form)


class OrderRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = OrderRequest
    template_name = 'request/order_request_confirm_delete.html'
    success_url = reverse_lazy('order_request_list')

@login_required
def order_request_view(request, pk):
    order_request = get_object_or_404(OrderRequest, id=pk)
    
    if request.method == 'POST':
        form = OrderRequestStatusUpdateForm(request.POST, instance=order_request)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, 'Somethings is wrong, please try again!')
        return redirect('order_request_view', pk=order_request.pk)
    else:
        form2 = OrderForm()
        form = OrderRequestStatusUpdateForm(instance=order_request)
        
    return render(request, 'request/order_request_view.html', {'order_request': order_request, 'form': form, 'form2': form2})

@login_required
def request_to_order(request, pk):
    if request.method == 'POST':
        order_request = get_object_or_404(OrderRequest, id=pk)
        if Order.objects.get(tracking_ID=order_request.tracking_ID):
            messages.success(request, "Order already created!")
            return redirect('order_request_view', pk=order_request.pk)
        else:
            form2 = OrderForm(request.POST)
            if form2.is_valid():
                order = form2.save()
                order.request_order = order_request
                order.tracking_ID = order_request.tracking_ID
                order.remark = order_request.remark
                order.save()
                
                order_request.order_created = True
                order_request.save()
                
                messages.success(request, 'Order created successfully.')
                return redirect('order_list')
            else:
                messages.success(request, form2.errors)
                return redirect('order_request_view', pk=order_request.pk)

  

