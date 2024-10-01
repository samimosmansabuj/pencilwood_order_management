from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Order, OrderRequest
from django.contrib import messages
from django.utils import timezone
from .forms import OrderForm, OrderRequestForm, OrderRequestStatusUpdateForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView, DeleteView

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
    return render(request, 'order/order.html', {'order': order})


@login_required
def order_view(request, id):
    order = get_object_or_404(Order, id=id)
    
    if request.method == 'POST':
        if request.POST['status'] == 'Received':
            if order.pay_for == 'Pickup':
                order.shipping_charge_paid = True
        elif request.POST['status'] == 'Delivered':
            order.shipping_charge_paid = True
        
        order.status = request.POST['status']
        order.status_details = request.POST['status_comment']
        order.order_update = request.POST['update_date_time']
        order.save()
        messages.success(request, 'Order Update Successfully!')
        return redirect(request.META['HTTP_REFERER'])
    return render(request, 'order/order_view.html', {'order': order})


@login_required
def add_new_order(request):
    form = OrderForm()
    return render(request, 'order/add_new_order.html', {'form': form})





class OrderRequestListView(ListView):
    model = OrderRequest
    template_name = 'request/order_request_list.html'  # Define your template here
    context_object_name = 'order_requests'
    ordering = ['-id']

class OrderRequestCreateView(CreateView):
    model = OrderRequest
    form_class = OrderRequestForm
    template_name = 'request/order_request_form.html'
    success_url = reverse_lazy('order_request_list')
    
    def form_valid(self, form):
        form.instance.request_at = self.request.user  # Automatically set request_at
        return super().form_valid(form)


class OrderRequestDeleteView(DeleteView):
    model = OrderRequest
    template_name = 'request/order_request_confirm_delete.html'
    success_url = reverse_lazy('order_request_list')

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
        form = OrderRequestStatusUpdateForm(instance=order_request)
        
    return render(request, 'request/order_request_view.html', {'order_request': order_request, 'form': form})

