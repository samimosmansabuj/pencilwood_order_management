from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    
    path('add-new-user/', AddNewUserView.as_view(), name='addNewUser'),
    path('member/delete/<int:pk>/', MemberDeleteView.as_view(), name='user_delete'),
    
    path('member-list/', MemberListView.as_view(), name='member_list'),
    path('member/<int:id>/', MemberUpdateView.as_view(), name='member_view'),
    path('my-profile/', MyProfileView.as_view(), name='my_profile'),
]