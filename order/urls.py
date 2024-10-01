from django.urls import path
from .views import *

urlpatterns = [
    path('order/', order_list, name='order_list'),
    path('add-new-order/', add_new_order, name='add_new_order'),
    path('order/<int:id>/', order_view, name='order_view'),
    
    
    path('order-request/create/', OrderRequestCreateView.as_view(), name='order_request_create'),
    path('order-request/', OrderRequestListView.as_view(), name='order_request_list'),
    path('order-request/delete/<int:pk>/', OrderRequestDeleteView.as_view(), name='order_request_delete'),
    path('order-request/view/<int:pk>/', order_request_view, name='order_request_view'),
]
