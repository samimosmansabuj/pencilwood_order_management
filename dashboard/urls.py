from django.urls import path
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('settings/', settings, name='settings'),
    
    
    path('product-list/', ProductListView.as_view(), name='product_list'),
    path('product-create/', ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    
    
    
    path('maintenance-cost/', MaintenanceCostListView.as_view(), name='maintenance_cost_list'),
    path('maintenance-cost/create/', MaintenanceCostCreateView, name='maintenance_cost_create'),
    path('maintenance-cost/update/<int:pk>/', MaintenanceCostUpdateView.as_view(), name='maintenance_cost_update'),
    path('maintenance-cost/delete/<int:pk>/', MaintenanceCostDeleteView.as_view(), name='maintenance_cost_delete'),
    
    
    path('daily-profit/', DailyProfitListView.as_view(), name='daily_profit_list'),
    path('daily-profit/create/', TodayProfitCreate, name='today_profit_create'),
    path('daily-profit/update/<int:pk>/', DailyProfitUpdateView.as_view(), name='daily_profit_update'),
    path('daily-profit/delete/<int:pk>/', DailyProfitDeleteView.as_view(), name='daily_profit_delete'),
]