from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from http import HTTPStatus
from django.db import transaction
from .models import Order, SteadFastWebhookLog
import json


# Logistic / Delivery Company API Integration Code==========================
@method_decorator(csrf_exempt, name="dispatch")
class SteadfastWebhookAPIView(View):
    def get_order(self, consignment_id):
        try:
            return Order.objects.select_for_update().get(
                steadfast_parcel_id=consignment_id
            )
        except Order.DoesNotExist:
            return None

    def order_validation(self, order, status_value, invoice, cod_amount):
        validation_invoice = order.tracking_ID == invoice
        validation_order_cod = float(order.due_amount) == cod_amount
        validation_order_status = True if status_value.lower() in ("delivered", "partial_delivered") and order.status != "Delivered" else \
                                  True if status_value == "pending" and order.status != "Parcel Created" else False
        if order and validation_order_status and (validation_invoice or validation_order_cod):
            return True
        return False

    def partial_workflow(self, data):
        status_value = data.get("status")
        invoice = data.get("invoice")
        cod_amount = data.get("cod_amount")
        order = self.get_order(data.get("consignment_id"))
        order_validation_result = self.order_validation(order, status_value, invoice, cod_amount)
        if order_validation_result:
            with transaction.atomic():
                new_status = "Delivered" if status_value.lower() in ("delivered", "partial_delivered") else "Parcel Created"
                Order.objects.filter(id=order.id).update(status=new_status, urgent=False)
        return True
    
    def create_log_entry(self, data, notification_type, account):
        SteadFastWebhookLog.objects.create(
            type=notification_type,
            account=account,
            payload=data,
            tracking_message=data.get("tracking_message", ""),
        )

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode("utf-8"))
            notification_type = data.get("notification_type")
            account = request.GET.get("account", "pencilwood")
            self.create_log_entry(data, notification_type, account)
            if notification_type == "delivery_status":
                self.partial_workflow(data)
                return JsonResponse(
                    {"status": True, "message": "Webhook Received Successfully"},
                    status=HTTPStatus.OK,
                )
            else:
                return JsonResponse(
                    {"status": False, "message": "Unsupported Notification Type"},
                    status=HTTPStatus.BAD_REQUEST,
                )
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": False, "message": "Invalid JSON payload"},
                status=HTTPStatus.BAD_REQUEST,
            )
        except Exception as e:
            return JsonResponse(
                {"status": False, "message": str(e)},
                status=HTTPStatus.BAD_REQUEST,
            )

    def get(self, request, *args, **kwargs):
        return JsonResponse(
            {"status": False, "message": "Invalid Request Method"},
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )

# Logistic / Delivery Company API Integration Code==========================