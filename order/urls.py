from django.urls import path
from .views import *
from .views import OrderListView

urlpatterns = [
    path('order-list/', OrderListView.as_view(), name='order_list'),
    path('update-order/<int:pk>/', update_order, name='update_order'),
    path('order/delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
    path('order/add-new/', add_new_order, name='add_new_order'),
    #logistic Company api connect========
    path('order/create-pathao-parcel/<int:id>/', create_pathao_parcel, name='create_pathao_parcel'),
    path('order/create-steadfast-parcel/<int:id>/', create_steadfast_parcel, name='create_steadfast_parcel'),
    #logistic Company api connect========
    
    path('order/item/delete/<int:id>/', DeleteOrderItem, name='DeleteOrderItem'),
    path('order/add-success/<int:id>/', order_success, name='order_success'),
    path('order/<int:id>/', order_view, name='order_view'),
    path('order/payment-update/<int:pk>/', orderPaymentUpdate, name='orderPaymentUpdate'),
    path('order/customer-info-update/<int:pk>/', CustomerOrderInfoUpdate, name='CustomerOrderInfoUpdate'),
    
    
    path('order-request/create/', OrderRequestCreateView.as_view(), name='order_request_create'),
    path('order-request/', OrderRequestListView.as_view(), name='order_request_list'),
    path('update-order-request/<int:pk>/', update_order_request, name='update_order_request'),
    path('order-request/delete/<int:pk>/', OrderRequestDeleteView.as_view(), name='order_request_delete'),
    path('order-request/view/<int:pk>/', order_request_view, name='order_request_view'),
    path('request-to-order-create/<int:pk>/', request_to_order, name='request_to_order'),
    path('order-request/picture-update/<int:pk>/', PictureUpdate, name='PictureUpdate'),
    
    
    
    path('order/<int:id>/invoice/', print_invoice, name='generate_pdf'),
]
