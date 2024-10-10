from django.urls import path
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('settings/', SettingsView.as_view(), name='settings'),
    
    
    path('product-list/', ProductListView.as_view(), name='product_list'),
    path('product-create/', ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    
    
    
    path('maintenance-cost/', MaintenanceCostListView.as_view(), name='maintenance_cost_list'),
    path('maintenance-cost/create/', MaintenanceCostCreateView, name='maintenance_cost_create'),
    path('maintenance-cost/update/<int:pk>/', MaintenanceCostUpdateView.as_view(), name='maintenance_cost_update'),
    path('maintenance-cost/delete/<int:pk>/', MaintenanceCostDeleteView.as_view(), name='maintenance_cost_delete'),
    
    
    path('daily-profit/', DailyProfitListView.as_view(), name='daily_profit_list'),
    # path('daily-profit/create/', TodayProfitCreate, name='today_profit_create'),
    
    
    path('todos/', TodoListView.as_view(), name='todo_list'),
    path('todos/new/', TodoCreateView.as_view(), name='todo_create'),
    path('todos/edit/<int:pk>/', TodoUpdateView.as_view(), name='todo_update'),
    path('todos/delete/<int:pk>/', TodoDeleteView.as_view(), name='todo_delete'),  # Add this line
]