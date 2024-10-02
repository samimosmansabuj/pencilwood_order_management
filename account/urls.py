from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LogIn, name='login'),
    path('logout/', Logout, name='logout'),
    
    path('add-new-user/', addNewUser, name='addNewUser'),
    path('member/delete/<int:pk>/', MemberDeleteView.as_view(), name='user_delete'),
    
    path('member-list/', member_list, name='member_list'),
    path('member/<int:id>/', member_view, name='member_view'),
    path('my-profile/', my_profile, name='my_profile'),
]