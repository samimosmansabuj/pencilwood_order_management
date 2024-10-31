from django.urls import path
from .views import *
from .views import OrderListView

urlpatterns = [
    # path('order/', order_list, name='order_list'),
    path('order-list/', OrderListView.as_view(), name='order_list'),
    path('order/add-new/', add_new_order, name='add_new_order'),
    path('order/add-success/', order_success, name='order_success'),
    path('order/<int:id>/', order_view, name='order_view'),
    path('order/payment-update/<int:pk>/', orderPaymentUpdate, name='orderPaymentUpdate'),
    path('order/customer-info-update/<int:pk>/', CustomerOrderInfoUpdate, name='CustomerOrderInfoUpdate'),
    
    
    path('order-request/create/', OrderRequestCreateView.as_view(), name='order_request_create'),
    path('order-request/', OrderRequestListView.as_view(), name='order_request_list'),
    path('order-request/delete/<int:pk>/', OrderRequestDeleteView.as_view(), name='order_request_delete'),
    path('order-request/view/<int:pk>/', order_request_view, name='order_request_view'),
    path('request-to-order-create/<int:pk>/', request_to_order, name='request_to_order'),
    path('order-request/picture-update/<int:pk>/', PictureUpdate, name='PictureUpdate'),
    
    
    
    path('order/<int:id>/invoice/', print_invoice, name='generate_pdf'),
]
