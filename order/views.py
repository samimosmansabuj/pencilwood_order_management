from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Order, OrderRequest
from dashboard.models import Maintenance_Cost, Daily_Profit
from django.contrib import messages
from django.utils.dateparse import parse_date
from .forms import *
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Sum
import openpyxl
import csv
from django.http import HttpResponse
import os

# ------------Order Section Start------------
class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order/order.html'
    paginate_by = 10
    context_object_name = 'orders'
    ordering = ['-order_date']
    
    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.GET.get('status')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        search_query = self.request.GET.get('search')
        product_id = self.request.GET.get('product')
        work_assign = self.request.GET.get('work_assign')
        today_orders = self.request.GET.get('today_orders')

        # Filter by today order
        if today_orders:
            today = timezone.localtime().date()
            
            queryset = queryset.filter(order_date__date=today)
            return queryset

        # Filter by status
        if status and status != 'All':
            queryset = queryset.filter(status=status)

        # Filter by date range
        if start_date:
            start_date = parse_date(start_date)
            queryset = queryset.filter(order_date__gte=start_date)
        if end_date:
            end_date = parse_date(end_date)
            queryset = queryset.filter(order_date__lte=end_date)

        # Filter by Search
        if search_query:
            queryset = queryset.filter(
                Q(tracking_ID__icontains=search_query) |
                Q(request_order__name__icontains=search_query) |
                Q(request_order__company__icontains=search_query) |
                Q(request_order__phone_number__icontains=search_query) |
                Q(request_order__product__name__icontains=search_query) |
                Q(order_customer__name__icontains=search_query) |
                Q(order_customer__company__icontains=search_query) |
                Q(order_customer__phone_number__icontains=search_query) |
                Q(order_customer__product__name__icontains=search_query)
            )
        
        # Filter by Product
        if product_id and product_id.isdigit():
            queryset = queryset.filter(
                Q(request_order__product__id__icontains=product_id) |
                Q(order_customer__product__id__icontains=product_id)
            ).distinct()
            
        if work_assign and work_assign.isdigit():
            queryset = queryset.filter(work_assign__id__icontains=work_assign).distinct()

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['work_assign_choices'] = Custom_User.objects.all()
        
        # Count today's orders
        # today = timezone.now().date()
        # context['today_orders'] = Order.objects.filter(order_date__date=today)
        
        queryset = self.get_queryset()
        context['total_deal_value'] = queryset.aggregate(Sum('deal_value'))['deal_value__sum'] or 0
        context['total_due_amount'] = queryset.aggregate(Sum('due_amount'))['due_amount__sum'] or 0
        
        return context
    
    
    def render_to_response(self, context, **response_kwargs):
        export_format = self.request.GET.get('export')
        queryset = self.get_queryset()  # Get the filtered queryset without pagination
        headers = ['ID', 'Company', 'Name', 'Phone Number', 'delivery_address', 'special_instructions', 'Source', 'Product(s)', 'Work Assign', 'Status', 'remark', 'logo', 'picture1', 'picture2', 'picture3', 'picture4', 'picture5', 'quantity', 'unit_price', 'deal_value', 'advance_amount', 'due_amount', 'delivery_charge', 'delivery_charge_cost', 'extra_cost', 'total_amount', 'payment_number', 'transaction_id', 'payment_method', 'payment_status', 'delivery_date', 'Last Update', 'order_date']
        
        if export_format == 'xlsx':
            return self.export_to_xlsx(queryset, headers)
        elif export_format == 'csv':
            return self.export_to_csv(queryset, headers)

        return super().render_to_response(context, **response_kwargs)

    def export_to_xlsx(self, orders, headers):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = f'Orders - {timezone.now().date()}'

        sheet.append(headers)

        for order in orders:
            
            if order.request_order:
                products = ', '.join([product.name for product in order.request_order.product.all()])
                sheet.append([
                    order.tracking_ID,
                    order.request_order.company,
                    order.request_order.name,
                    order.request_order.phone_number,
                    order.delivery_address,
                    order.special_instructions,
                    order.request_order.source,
                    products,
                    str(order.work_assign),
                    order.status,
                    order.remark,
                    order.request_order.logo,
                    order.request_order.picture1,
                    order.request_order.picture2,
                    order.request_order.picture3,
                    order.request_order.picture4,
                    order.request_order.picture5,
                    
                    order.quantity,
                    order.unit_price,
                    order.deal_value,
                    order.advance_amount,
                    order.due_amount,
                    order.delivery_charge,
                    order.delivery_charge_cost,
                    order.extra_cost,
                    order.total_amount,
                    order.payment_number,
                    order.transaction_id,
                    order.payment_method,
                    order.payment_status,
                    order.delivery_date,
                    order.last_update,
                    order.order_date,
                    
                ])
            if order.order_customer:
                products = ', '.join([product.name for product in order.order_customer.product.all()])
                sheet.append([
                    order.tracking_ID,
                    order.order_customer.company,
                    order.order_customer.name,
                    order.order_customer.phone_number,
                    order.delivery_address,
                    order.special_instructions,
                    order.order_customer.source,
                    products,
                    str(order.work_assign),
                    order.status,
                    order.remark,
                    order.order_customer.logo,
                    order.order_customer.picture1,
                    None,
                    None,
                    None,
                    None,
                    
                    order.quantity,
                    order.unit_price,
                    order.deal_value,
                    order.advance_amount,
                    order.due_amount,
                    order.delivery_charge,
                    order.delivery_charge_cost,
                    order.extra_cost,
                    order.total_amount,
                    order.payment_number,
                    order.transaction_id,
                    order.payment_method,
                    order.payment_status,
                    str(order.delivery_date),
                    str(order.last_update),
                    str(order.order_date),
                    
                ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=Orders - {timezone.now().date()}.xlsx'
        workbook.save(response)
        return response

    def export_to_csv(self, orders, headers):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=orders - {timezone.now().date()}.csv'

        writer = csv.writer(response)
        writer.writerow(headers)

        for order in orders:
            if order.request_order:
                products = ', '.join([product.name for product in order.request_order.product.all()])
                writer.writerow([
                    order.tracking_ID,
                    order.request_order.company,
                    order.request_order.name,
                    order.request_order.phone_number,
                    order.delivery_address,
                    order.special_instructions,
                    order.request_order.source,
                    products,
                    str(order.work_assign),
                    order.status,
                    order.remark,
                    order.request_order.logo,
                    order.request_order.picture1,
                    order.request_order.picture2,
                    order.request_order.picture3,
                    order.request_order.picture4,
                    order.request_order.picture5,
                    
                    order.quantity,
                    order.unit_price,
                    order.deal_value,
                    order.advance_amount,
                    order.due_amount,
                    order.delivery_charge,
                    order.delivery_charge_cost,
                    order.extra_cost,
                    order.total_amount,
                    order.payment_number,
                    order.transaction_id,
                    order.payment_method,
                    order.payment_status,
                    order.delivery_date,
                    order.last_update,
                    order.order_date,
                    
                ])
            
            if order.order_customer:
                products = ', '.join([product.name for product in order.order_customer.product.all()])
                writer.writerow([
                    order.tracking_ID,
                    order.order_customer.company,
                    order.order_customer.name,
                    order.order_customer.phone_number,
                    order.delivery_address,
                    order.special_instructions,
                    order.order_customer.source,
                    products,
                    str(order.work_assign),
                    order.status,
                    order.remark,
                    order.order_customer.logo,
                    order.order_customer.picture1,
                    None,
                    None,
                    None,
                    None,
                    
                    order.quantity,
                    order.unit_price,
                    order.deal_value,
                    order.advance_amount,
                    order.due_amount,
                    order.delivery_charge,
                    order.delivery_charge_cost,
                    order.extra_cost,
                    order.total_amount,
                    order.payment_number,
                    order.transaction_id,
                    order.payment_method,
                    order.payment_status,
                    str(order.delivery_date),
                    str(order.last_update),
                    str(order.order_date),
                    
                ])
            

        return response




def daily_profit_update(object):
    date = timezone.localtime(object.order_date).date()
    daily_profit, created = Daily_Profit.objects.get_or_create(date=date)
    daily_profit.orders.add(object)
    daily_profit.save()


@login_required
def add_new_order(request):
    if request.method == 'POST':
        order_customer_form = OrderCustomerForm(request.POST)
        order_form = OrderForm(request.POST, request.FILES)

        if order_customer_form.is_valid() and order_form.is_valid():
            order_customer = order_customer_form.save()

            order = order_form.save(commit=False)
            order.order_customer = order_customer
            order.save()
            
            daily_profit_update(order)

            return redirect('order_success')
        else:
            messages.warning(
                request, f"{order_customer_form.errors} and {order_form.errors}")
            return redirect(request.META['HTTP_REFERER'])
    else:
        order_customer_form = OrderCustomerForm()
        order_form = OrderForm()

    return render(request, 'order/add_new_order.html', {
        'order_customer_form': order_customer_form,
        'order_form': order_form
    })

@login_required
def order_success(request):
    return render(request, 'order/order_success.html')


@login_required
def order_view(request, id):
    order = get_object_or_404(Order, id=id)
    context = {'order': order}

    if request.method == 'POST':
        form = OrderStatusUpdateForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order Update Successfully!')
        else:
            messages.error(request, f'Somethings is wrong: {form.errors}')
        return redirect(request.META['HTTP_REFERER'])
    else:
        form = OrderStatusUpdateForm(instance=order)
        form2 = OrderPaymentUpdateForm(instance=order)
        context['form'] = form
        context['form2'] = form2
        if order.order_customer and order.request_order is None:
            form3 = OrderCustomerForm(instance=order.order_customer)
            form3.fields['product'].required = False
            context['form3'] = form3
        
    return render(request, 'order/order_view.html', context)

@login_required
def orderPaymentUpdate(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form2 = OrderPaymentUpdateForm(request.POST, instance=order)
        if form2.is_valid():
            object = form2.save()
            
            daily_profit_update(object)
            
            messages.success(request, 'Payment details updated successfully!')
            return redirect('order_view', id=order.pk)
        else:
            messages.error(request, f'Something went wrong: {form2.errors}')
            return redirect('order_view', id=order.pk)
    else:
        return redirect('order_view', id=order.pk)

@login_required
def CustomerOrderInfoUpdate(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form3 = OrderCustomerForm(request.POST, instance=order.order_customer)
        if form3.is_valid():
            form3.save()
            messages.success(request, 'Order Customer Info updated successfully!')
        else:
            messages.error(request, f'Something went wrong: {form3.errors}')
    return redirect('order_view', id=order.pk)

# ------------Order Section End------------





class OrderRequestListView(LoginRequiredMixin, ListView):
    model = OrderRequest
    template_name = 'request/order_request_list.html'
    context_object_name = 'order_requests'
    paginate_by = 10  # Pagination works for normal listing
    ordering = ['-id']

    def get_queryset(self):
        """
        Retrieves the queryset for displaying and also used when exporting.
        """
        queryset = super().get_queryset()

        # Get filter parameters from the request
        status = self.request.GET.get('status')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        search_query = self.request.GET.get('search')
        product_id = self.request.GET.get('product')
        work_assign = self.request.GET.get('work_assign')
        today_order_requests = self.request.GET.get('today_order_requests')

        # Apply filters
        if today_order_requests:
            today = timezone.now().date()
            queryset = queryset.filter(created_at__date=today)

        if status and status != 'All':
            queryset = queryset.filter(status=status)

        if start_date:
            start_date = parse_date(start_date)
            queryset = queryset.filter(created_at__gte=start_date)

        if end_date:
            end_date = parse_date(end_date)
            queryset = queryset.filter(created_at__lte=end_date)

        if search_query:
            queryset = queryset.filter(
                Q(tracking_ID__icontains=search_query) |
                Q(name__icontains=search_query) |
                Q(company__icontains=search_query) |
                Q(phone_number__icontains=search_query) |
                Q(source__icontains=search_query) |
                Q(status__icontains=search_query) |
                Q(remark__icontains=search_query) |
                Q(product__name__icontains=search_query)
            )

        if product_id and product_id.isdigit():
            queryset = queryset.filter(product__id__icontains=product_id).distinct()
            
        if work_assign and work_assign.isdigit():
            queryset = queryset.filter(work_assign__id__icontains=work_assign).distinct()
        
        
        return queryset

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the template.
        """
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['work_assign_choices'] = Custom_User.objects.all()
        return context

    def render_to_response(self, context, **response_kwargs):
        export_format = self.request.GET.get('export')
        queryset = self.get_queryset()  # Get the filtered queryset without pagination
        
        if export_format == 'xlsx':
            return self.export_to_xlsx(queryset)
        elif export_format == 'csv':
            return self.export_to_csv(queryset)

        return super().render_to_response(context, **response_kwargs)

    def export_to_xlsx(self, order_requests):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = f'Order Requests - {timezone.now().date()}'

        headers = ['Created By', 'ID', 'Company', 'Name', 'Phone Number', 'Source', 'Product(s)', 'Status', 'remark', 'Work Assign', 'Order Created', 'Last Update', 'Created At', 'logo', 'picture1', 'picture2', 'picture3', 'picture4', 'picture5']
        sheet.append(headers)

        for order_request in order_requests:
            products = ', '.join([product.name for product in order_request.product.all()])
            sheet.append([
                str(order_request.request_created_by),
                order_request.tracking_ID,
                order_request.company,
                order_request.name,
                order_request.phone_number,
                order_request.source,
                products,
                order_request.status,
                order_request.remark,
                str(order_request.work_assign),
                order_request.order_created,
                str(order_request.last_update),
                str(order_request.created_at.date()),
                order_request.logo,
                order_request.picture1,
                order_request.picture2,
                order_request.picture3,
                order_request.picture4,
                order_request.picture5
            ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=order_requests - {timezone.now().date()}.xlsx'
        workbook.save(response)
        return response

    def export_to_csv(self, order_requests):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=order_requests - {timezone.now().date()}.csv'

        writer = csv.writer(response)
        writer.writerow(['Created By', 'ID', 'Company', 'Name', 'Phone Number', 'Source', 'Product(s)', 'Status', 'remark', 'Work Assign', 'Order Created', 'Last Update', 'Created At', 'logo', 'picture1', 'picture2', 'picture3', 'picture4', 'picture5'])

        for order_request in order_requests:
            products = ', '.join([product.name for product in order_request.product.all()])
            writer.writerow([
                order_request.request_created_by,
                order_request.tracking_ID,
                order_request.company,
                order_request.name,
                order_request.phone_number,
                order_request.source,
                products,
                order_request.status,
                order_request.remark,
                order_request.work_assign,
                order_request.order_created,
                order_request.last_update,
                order_request.created_at.date(),
                order_request.logo,
                order_request.picture1,
                order_request.picture2,
                order_request.picture3,
                order_request.picture4,
                order_request.picture5
            ])

        return response



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
        form = OrderRequestStatusUpdateForm(
            request.POST, instance=order_request)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, f'Something went wrong: {form.errors}')
        return redirect('order_request_view', pk=order_request.pk)
    else:
        form = OrderRequestStatusUpdateForm(instance=order_request)
        form2 = OrderForm()
        form3 = OrderRequestPictureUpdateForm(instance=order_request)

    return render(request, 'request/order_request_view.html', {'order_request': order_request, 'form': form, 'form2': form2, 'form3': form3})


@login_required
def request_to_order(request, pk):
    if request.method == 'POST':
        order_request = get_object_or_404(OrderRequest, id=pk)
        if Order.objects.filter(tracking_ID=order_request.tracking_ID).exists():
            messages.success(request, "Order already created!")
            return redirect('order_request_view', pk=order_request.pk)
        else:
            form2 = OrderForm(request.POST, request.FILES)
            if form2.is_valid():
                order = form2.save()
                order.request_order = order_request
                order.tracking_ID = order_request.tracking_ID
                if order.remark is None:
                    order.remark = order_request.remark
                order.save()

                order_request.order_created = True
                order_request.save()
                
                daily_profit_update(order)

                messages.success(request, 'Order created successfully.')
                return redirect('order_list')
            else:
                messages.success(request, form2.errors)
                return redirect('order_request_view', pk=order_request.pk)


@login_required
def PictureUpdate(request, pk):
    order_request = get_object_or_404(OrderRequest, pk=pk)
    if request.method == 'POST':
        form3 = OrderRequestPictureUpdateForm(request.POST, instance=order_request)
        if form3.is_valid():
            form3.save()
            messages.success(request, 'Picture details updated successfully!')
        else:
            messages.error(request, f'Something went wrong: {form3.errors}')
    return redirect('order_request_view', pk=order_request.pk)

