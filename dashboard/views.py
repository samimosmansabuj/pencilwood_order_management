from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from account.models import Custom_User
from order.models import Order, OrderRequest
from .models import *
from .forms import *
from django.utils import timezone
from order.models import Product
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Sum
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.utils.timezone import localdate
import os


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch orders and order requests
        order = Order.objects.all().order_by('-id')
        order_request = OrderRequest.objects.all().order_by('-id')
        user = Custom_User.objects.all()

        # Get today's date
        today = timezone.now().date()

        # Filter today's orders
        today_orders = order.filter(order_date__date=today)

        # Calculate total deal value for today’s orders and all orders
        today_total_deal_value = today_orders.aggregate(total=Sum('deal_value'))['total'] or 0
        all_order_total_deal_value = order.aggregate(total=Sum('deal_value'))['total'] or 0

        # Pass values to the context
        context['user'] = user
        context['order'] = order
        context['today_orders'] = today_orders
        context['order_request'] = order_request
        context['today_total_deal_value'] = today_total_deal_value
        context['all_order_total_deal_value'] = all_order_total_deal_value

        return context


class SettingsView(LoginRequiredMixin, UpdateView):
    model = Site_Settings
    form_class = WebsiteSettingsForm
    template_name = 'dashboard/settings.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return Site_Settings.objects.first()

    def form_valid(self, form):
        setting = form.save(commit=False)
        if 'logo' in self.request.FILES:
            if setting.logo:
                os.remove(setting.logo.path)
            setting.logo = self.request.FILES['logo']
        
        if 'fav_icon' in self.request.FILES:
            if setting.fav_icon:
                os.remove(setting.fav_icon.path)
            setting.fav_icon = self.request.FILES['fav_icon']

        setting.save()
        messages.success(self.request, 'Your settings were updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle the logic for an invalid form submission."""
        messages.error(self.request, f'Error updating settings: {form.errors}')
        return super().form_invalid(form)

    def get_success_url(self):
        return self.request.META['HTTP_REFERER']




# -----------------Product Section Start---------------------
# List View
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product/product_list.html'  # Your template for listing
    context_object_name = 'products'
    paginate_by = 5
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query) |
                Q(name__icontains=search_query) |
                Q(slug__icontains=search_query) |
                Q(created_date__icontains=search_query)
            )
        
        return queryset

# Create View
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'  # Your template for create/update form
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        return super().form_valid(form)

# Update View
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('product_list')

# Delete View
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product/product_confirm_delete.html'  # Template for delete confirmation
    success_url = reverse_lazy('product_list')

# -----------------Product Section End---------------------




# -----------------Maintenance Cost Section Start---------------------
from django.utils import timezone
def daily_profit_cost_update(object):
    date = timezone.localtime(object.create_date).date()
    daily_profit, created = Daily_Profit.objects.get_or_create(date=date)
    daily_profit.costs.add(object)
    daily_profit.save()

# List view
class MaintenanceCostListView(LoginRequiredMixin, ListView):
    model = Maintenance_Cost
    template_name = 'finance_section/maintenance_cost_list.html'
    context_object_name = 'costs'
    paginate_by = 4
    ordering = ['-id']
    
    def get_queryset(self):
        queryset = super().get_queryset()

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        search_query = self.request.GET.get('search')
        today_costs = self.request.GET.get('today_costs')

        # Filter by today order
        if today_costs:
            today = timezone.now().date()
            queryset = queryset.filter(create_date__date=today)
            return queryset

        # Filter by date range
        if start_date:
            start_date = parse_date(start_date)
            queryset = queryset.filter(create_date__gte=start_date)
        if end_date:
            end_date = parse_date(end_date)
            queryset = queryset.filter(create_date__lte=end_date)

        # Filter by Search
        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(cost__icontains=search_query) |
                Q(create_date__icontains=search_query) |
                Q(last_update__icontains=search_query)
            )

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MaintenanceCostForm()
        
        total_cost = self.get_queryset().aggregate(Sum('cost'))['cost__sum'] or 0
        context['total_cost'] = total_cost
        return context

# Create view
def MaintenanceCostCreateView(request):
    if request.method == 'POST':
        form = MaintenanceCostForm(request.POST)
        if form.is_valid():
            object = form.save()
            daily_profit_cost_update(object)
            messages.success(request, 'Cost Added!')
        else:
            messages.error(request, f'Something wrong: {form.errors}')
    return redirect('maintenance_cost_list')

# Update view
class MaintenanceCostUpdateView(LoginRequiredMixin, UpdateView):
    model = Maintenance_Cost
    form_class = MaintenanceCostForm
    template_name = 'finance_section/maintenance_cost_form.html'
    success_url = reverse_lazy('maintenance_cost_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['AddForm'] = MaintenanceCostForm()
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        daily_profit_cost_update(self.object)
        messages.success(self.request, 'Maintenance cost updated successfully!')
        return response

# Delete view
class MaintenanceCostDeleteView(LoginRequiredMixin, DeleteView):
    model = Maintenance_Cost
    template_name = 'finance_section/maintenance_cost_confirm_delete.html'
    success_url = reverse_lazy('maintenance_cost_list')
    
    def delete(self, request, *args, **kwargs):
        maintenance_cost = self.get_object()
        daily_profit = Daily_Profit.objects.get(date=timezone.localtime(maintenance_cost.create_date).date())
        print(daily_profit)

        if daily_profit:
            daily_profit.costs.remove(maintenance_cost)
            daily_profit.save()
        
        # Call the parent delete method to actually delete the object
        return super().delete(request, *args, **kwargs)

# -----------------Maintenance Cost Section End---------------------






# -----------------Daily Profit Section Start---------------------
class DailyProfitListView(ListView):
    model = Daily_Profit
    template_name = 'daily_profit/list.html'
    context_object_name = 'profits'
    ordering = ['-date']
    paginate_by = 4
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        search_query = self.request.GET.get('search')

        # Filter by date range
        if start_date:
            start_date = parse_date(start_date)
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            end_date = parse_date(end_date)
            queryset = queryset.filter(date__lte=end_date)

        # Filter by Search
        if search_query:
            queryset = queryset.filter(
                Q(note__icontains=search_query) |
                Q(date__icontains=search_query)
            )

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        today = localdate()
        context['today_profit_added'] = queryset.filter(date=today).exists()
        
        context['total_sell_amount'] = queryset.aggregate(Sum('total_sell'))['total_sell__sum'] or 0
        context['total_cost'] = queryset.aggregate(Sum('cost'))['cost__sum'] or 0
        context['total_profit'] = queryset.aggregate(Sum('profit'))['profit__sum'] or 0
        
        return context
 

# -----------------Daily Profit Section Start---------------------

