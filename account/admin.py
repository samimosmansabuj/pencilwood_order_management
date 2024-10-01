from django.contrib import admin
from .models import Custom_User, Login_Code

@admin.register(Custom_User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type', 'first_name', 'phone_number']
    list_filter = ['user_type']
    search_fields = ["*"]

# admin.site.register(Custom_User)
admin.site.register(Login_Code)
