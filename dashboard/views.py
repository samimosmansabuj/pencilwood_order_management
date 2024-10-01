from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import Custom_User
from order.models import Order
from .models import Site_Settings
from .forms import WebsiteSettingsForm, ProductForm
from django.utils import timezone
from order.models import Product
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import os

@login_required
def dashboard(request):
    order = Order.objects.all().order_by('-id')
    user = Custom_User.objects.all()
    
    today = timezone.now().date()
    today_orders = order.filter(order_date__date=today)
    
    context = {
        'user': user, 'order': order, 'today_orders': today_orders
    }
    return render(request, 'dashboard/dashboard.html', context)

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



# List View
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product/product_list.html'  # Your template for listing
    context_object_name = 'products'

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


