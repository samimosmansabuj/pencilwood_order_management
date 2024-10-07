from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
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



@login_required
def settings(request):
    site_settings = Site_Settings.objects.all().first()
    if request.method == 'POST':
        form = WebsiteSettingsForm(request.POST, request.FILES, instance=site_settings)
        if form.is_valid():
            setting = form.save(commit=False)
            
            # If there are new files (logo or favicon), they will be saved
            if 'logo' in request.FILES:
                if site_settings and site_settings.logo:
                    os.remove(site_settings.logo.path)
                setting.logo = request.FILES['logo']
            if 'fav_icon' in request.FILES:
                if site_settings and site_settings.fav_icon:
                    os.remove(site_settings.fav_icon.path)
                setting.fav_icon = request.FILES['fav_icon']
            
            setting.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, f'{form.errors}')
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = WebsiteSettingsForm(instance=site_settings)
    return render(request, 'dashboard/settings.html', {'form': form})



# -----------------Product Section Start---------------------
# List View
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product/product_list.html'  # Your template for listing
    context_object_name = 'products'
    paginate_by = 3
    
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
# List view
class MaintenanceCostListView(LoginRequiredMixin, ListView):
    model = Maintenance_Cost
    template_name = 'finance_section/maintenance_cost_list.html'
    context_object_name = 'costs'
    paginate_by = 4
    
    
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
        
        # Count today's orders
        today = timezone.now().date()
        context['today_costs'] = Maintenance_Cost.objects.filter(create_date__date=today)
        
        # Get the queryset
        queryset = self.get_queryset()
        
        # Add totals to the context
        total_cost = queryset.aggregate(Sum('cost'))['cost__sum'] or 0
        context['total_cost'] = total_cost
        
        return context

# Create view
def MaintenanceCostCreateView(request):
    if request.method == 'POST':
        form = MaintenanceCostForm(request.POST)
        if form.is_valid():
            form.save()
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
        context = super().get_context_data(**kwargs) # Add products to the context for dropdown/filter options
        context['AddForm'] = MaintenanceCostForm()
        return context

# Delete view
class MaintenanceCostDeleteView(LoginRequiredMixin, DeleteView):
    model = Maintenance_Cost
    template_name = 'finance_section/maintenance_cost_confirm_delete.html'
    success_url = reverse_lazy('maintenance_cost_list')

# -----------------Maintenance Cost Section End---------------------






# -----------------Daily Profit Section Start---------------------
class DailyProfitListView(ListView):
    model = Daily_Profit
    template_name = 'daily_profit/list.html'
    context_object_name = 'profits'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        print(queryset)
        today = localdate()
        print(today)
        context['today_profit_added'] = queryset.filter(date=today).exists()
        print(context['today_profit_added'])
        return context


def TodayProfitCreate(request):
    if request.method == "POST":
        today = localdate()
        existing_profit = Daily_Profit.objects.filter(date=today).exists()
        if existing_profit:
            messages.warning(request, 'Daily Profit for today already exists.')
        else:
            Daily_Profit.objects.create(note="Create Successfully!")
    else:
        messages.warning(request, 'Somethings wrong!')
    return redirect('daily_profit_list')


class DailyProfitUpdateView(UpdateView):
    model = Daily_Profit
    form_class = DailyProfitForm
    template_name = 'daily_profit/form.html'
    success_url = reverse_lazy('daily_profit_list')

class DailyProfitDeleteView(DeleteView):
    model = Daily_Profit
    template_name = 'daily_profit/confirm_delete.html'
    success_url = reverse_lazy('daily_profit_list')

# -----------------Daily Profit Section Start---------------------

