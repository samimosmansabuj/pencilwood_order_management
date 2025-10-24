from django.contrib import admin
from .models import *

@admin.register(Custom_User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type', 'first_name', 'phone_number']
    list_filter = ['user_type']
    search_fields = ["*"]




admin.site.register(SteadFastAPI)
