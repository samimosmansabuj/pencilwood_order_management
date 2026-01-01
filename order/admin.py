from django.contrib import admin
from .models import *

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = []

# @admin.register(OrderRequest)
# class OrderRequestAdmin(admin.ModelAdmin):
#     # list_display = []
#     search_fields = ['company', 'created_at', 'id', 'last_update', 'logo', 'name', 'order', 'phone_number', 'picture1', 'picture2', 'picture3', 'picture4', 'picture5', 'remark', 'request_created_by', 'request_created_by_id', 'second_phone_number', 'source', 'status', 'tracking_ID', 'work_assign']


@admin.register(OrderRequest)
class OrderRequestAdmin(admin.ModelAdmin):
    search_fields = [
        "company",
        "created_at",
        "id",
        "last_update",
        "logo",
        "name",
        "order_created",
        "phone_number",
        "picture1",
        "picture2",
        "picture3",
        "picture4",
        "picture5",
        "remark",
        "second_phone_number",
        "source",
        "status",
        "tracking_ID",
    ]

    # Additional configuration if needed
    list_display = [
        "tracking_ID",
        "name",
        "company",
        "status",
        "created_at",
        "last_update",
    ]
    list_filter = ["status", "source", "order_created", "work_assign"]

    # Use this to display the ManyToManyField
    filter_horizontal = ("product",)


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = []


admin.site.register(Product)
# admin.site.register(OrderRequest)
admin.site.register(OrderCustomer)
admin.site.register(Order)
admin.site.register(OrderItem)


from django.contrib import admin
from django.utils.html import format_html
import json
from .models import SteadFastWebhookLog


@admin.register(SteadFastWebhookLog)
class SteadFastWebhookLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "account",
        "status",
        "tracking_message",
        "payload",
        "received_at",
    )
    list_filter = ("type", "account", "received_at")
    search_fields = ("account", "tracking_message", "payload")
    ordering = ("-received_at",)
    readonly_fields = ("received_at", "formatted_payload")
    exclude = ("payload",)
    fieldsets = (
        (
            "Log Metadata",
            {"fields": ("type", "account", "tracking_message", "received_at")},
        ),
        (
            "Payload Data",
            {
                "fields": ("formatted_payload",),
                "classes": ("collapse",),  # Makes this section collapsible
            },
        ),
    )

    def formatted_payload(self, obj):
        try:
            data = json.dumps(obj.payload, indent=4)
            # Render inside a pre tag for code-like formatting
            return format_html(
                '<pre style="background: #2b2b2b; color: #f8f8f2; padding: 15px; border-radius: 5px; overflow-x: auto;">{}</pre>',
                data,
            )
        except Exception:
            return "-"

    formatted_payload.short_description = "Full JSON Payload"

    def has_add_permission(self, request):
        return False
