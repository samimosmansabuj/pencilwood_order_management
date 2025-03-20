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
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.db.models import Count

def create_remainder(date, note):
    remainder = Remainder.objects.create(date=date, note=note)
    return remainder

def create_order_remainder(request, id):
    if request.method == 'POST':
        order = Order.objects.get(id=id)
        date = request.POST.get('date')
        remainder_note = request.POST.get('remainder_note')
        remainder = create_remainder(date, remainder_note)
        remainder.order = order
        remainder.save()
        return redirect(request.META['HTTP_REFERER'])

def create_order_request_remainder(request, id):
    if request.method == 'POST':
        order_request = OrderRequest.objects.get(id=id)
        date = request.POST.get('date')
        remainder_note = request.POST.get('remainder_note')
        remainder = create_remainder(date, remainder_note)
        remainder.order_request = order_request
        remainder.save()
        return redirect(request.META['HTTP_REFERER'])


def remainder_list(request):
    remainders = Remainder.objects.all()
    return render(request, 'remainder/list.html')

class RemainderListView(LoginRequiredMixin, ListView):
    model = Remainder
    template_name = 'remainder/list.html'
    context_object_name = 'remainders'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # search_query = self.request.GET.get('search')

        # if search_query:
        #     queryset = queryset.filter(
        #         Q(id__icontains=search_query) |
        #         Q(name__icontains=search_query) |
        #         Q(slug__icontains=search_query) |
        #         Q(created_date__icontains=search_query)
        #     )
        
        return queryset


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch orders and order requests
        order = Order.objects.all().order_by('-id')
        order_request = OrderRequest.objects.all().order_by('-id')
        user = Custom_User.objects.all()

        # Get today's date
        today = timezone.localtime().date()
        today_orders = order.filter(order_date=today)

        # Calculate total deal value for today’s orders and all orders
        today_total_deal_value = today_orders.aggregate(total=Sum('deal_value'))['total'] or 0
        all_order_total_deal_value = order.aggregate(total=Sum('deal_value'))['total'] or 0
        
        
        
        # Fetch todos assigned to the current user
        todos = Todo.objects.filter(work_assign=self.request.user).order_by('-create_date')
        priority = self.request.GET.get('priority')
        is_complete = self.request.GET.get('is_complete')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        search_query = self.request.GET.get('search')

        # Filter todos by priority
        if priority and priority != 'All':
            todos = todos.filter(priority=priority)

        # Filter todos by is_complete
        if is_complete:
            todos = todos.filter(is_complete=is_complete)

        # Filter todos by date range
        if start_date:
            start_date = parse_date(start_date)
            todos = todos.filter(create_date__gte=start_date)
        if end_date:
            end_date = parse_date(end_date)
            todos = todos.filter(create_date__lte=end_date)

        # Filter todos by search query
        if search_query:
            todos = todos.filter(
                Q(id__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(priority__icontains=search_query) |
                Q(details__icontains=search_query) |
                Q(create_date__icontains=search_query) |
                Q(update_date__icontains=search_query)
            )

        
        # Add pagination
        page = self.request.GET.get('page', 10)
        paginator = Paginator(todos, 5)  # Show 10 todos per page
        try:
            todos_paginated = paginator.page(page)
        except PageNotAnInteger:
            todos_paginated = paginator.page(1)
        except EmptyPage:
            todos_paginated = paginator.page(paginator.num_pages)
        
        
        order_status_counts = order.values('status').annotate(count=Count('id')).order_by('status')
        order_status_counts_dict = {item['status']: item['count'] for item in order_status_counts}
        request_status_counts = order_request.values('status').annotate(count=Count('id')).order_by('status')
        request_status_counts_dict = {item['status']: item['count'] for item in request_status_counts}
        
        
        # Pass values to the context
        context['order_status_counts'] = order_status_counts_dict
        context['request_status_counts'] = request_status_counts_dict
        context['user'] = user
        context['order'] = order
        context['today_orders'] = today_orders
        context['order_request'] = order_request
        context['today_total_deal_value'] = today_total_deal_value
        context['all_order_total_deal_value'] = all_order_total_deal_value
        context['todos'] = todos_paginated
        context['work_assign_choices'] = Custom_User.objects.all()

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
    paginate_by = 10
    
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
    paginate_by = 10
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
    paginate_by = 10
    
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
 
# -----------------Daily Profit Section End---------------------




# -----------------Todo Section Start---------------------
class TodoListView(ListView):
    model = Todo
    template_name = 'todo/todo_list.html'
    context_object_name = 'todos'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = super().get_queryset()

        priority = self.request.GET.get('priority')
        is_complete = self.request.GET.get('is_complete')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        search_query = self.request.GET.get('search')
        work_assign = self.request.GET.get('work_assign')
        
        # Filter by priority
        if priority and priority != 'All':
            queryset = queryset.filter(priority=priority)
        
        # Filter by is_complete
        if is_complete:
            queryset = queryset.filter(is_complete=is_complete)

        # Filter by date range
        if start_date:
            start_date = parse_date(start_date)
            queryset = queryset.filter(create_date__gte=start_date)
        if end_date:
            end_date = parse_date(end_date)
            queryset = queryset.filter(create_date__lte=end_date)
        
        # Filter by work_assign
        # if work_assign and work_assign.isdigit():
        #     queryset = queryset.filter(work_assign__id__icontains=work_assign)
        if work_assign:
            queryset = queryset.filter(work_assign_id=work_assign)

        # Filter by Search
        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(priority__icontains=search_query) |
                Q(details__icontains=search_query) |
                Q(create_date__icontains=search_query) |
                Q(update_date__icontains=search_query)
            )

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TodoForm()
        context['work_assign_choices'] = Custom_User.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.last_update_user = request.user  # Set the last_update_user
            todo.save()
            messages.success(request, 'Todo added successfully!')
            return redirect(reverse('todo_list'))
        else:
            messages.error(request, 'There was an error adding the Todo. Please check the form and try again.')
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)



class TodoCreateView(CreateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todo/todo_form.html'
    success_url = reverse_lazy('todo_list')
    
    def form_valid(self, form):
        form.instance.last_update_user = self.request.user  # Set last_update_user to the current user
        return super().form_valid(form)


class TodoUpdateView(UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todo/todo_form.html'
    success_url = reverse_lazy('todo_list')
    
    def form_valid(self, form):
        form.instance.last_update_user = self.request.user  # Update last_update_user on edit
        return super().form_valid(form)


class TodoDeleteView(DeleteView):
    model = Todo
    template_name = 'todo/todo_confirm_delete.html'
    success_url = reverse_lazy('todo_list')

# -----------------Todo Section End-----------------------
