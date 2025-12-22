from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, When, Value, Case, BooleanField, F
from .utils import SteadFastOrderCreateAPI
from django.db import transaction
from django.http import JsonResponse
from .models import Product, OrderItem, Order
from .forms import OrderCustomerForm, OrderForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dashboard.models import InvoiceColorDesign
from http import HTTPStatus
from django.views import View
import json

@login_required
def add_new_order2(request):
    products = Product.objects.all()
    if request.method == 'POST':
        order_customer_form = OrderCustomerForm(request.POST)
        order_form = OrderForm(request.POST, request.FILES)

        product = Product.objects.filter(slug__in=request.POST.getlist("slug"))
        product_unit_price_lsit = request.POST.getlist("unit_price")
        product_quantity_lsit = request.POST.getlist("quantity")
        if not (len(product) == len(product_unit_price_lsit) == len(product_quantity_lsit)):
            messages.warning(request, f"Something problem for product added!")
            return redirect(request.META['HTTP_REFERER'])

        if order_customer_form.is_valid() and order_form.is_valid():
            order_customer = order_customer_form.save()
            order = order_form.save(commit=False)
            order.order_customer=order_customer
            order.save()

            order_items = [
                OrderItem.objects.create(
                    product=p,
                    quantity=q,
                    unit_price=u
                )
                for p, q, u in zip(product, product_quantity_lsit, product_unit_price_lsit)
            ]

            order.order_item.add(*order_items)
            order.save()
            return redirect('order_success', id=order.id)
        else:
            messages.warning(request, f"{order_customer_form.errors} and {order_form.errors}")
            return redirect(request.META['HTTP_REFERER'])
    
    order_customer_form = OrderCustomerForm()
    order_form = OrderForm()

    return render(request, "orderr/add_new_order2.html", {'products': products, 'order_customer_form': order_customer_form, 'order_form': order_form})


@login_required
def new_generate_invoice(request, id):
    design = InvoiceColorDesign.objects.all().first()
    order = get_object_or_404(Order, id=id)
    context = {'order': order, 'design': design}
    return render(request, 'invoices/invoice.html', context)

@login_required
def token_generate(request, id):
    order = get_object_or_404(Order, id=id)
    context = {'order': order}
    return render(request, 'invoices/token.html', context)





# ====================API Endpoint View====================
# -----------------Bulk Order Status Update Start-----------------------
class OrderBulkUpdateView(View):
    def get_delivery_type(self, type):
        return 1 if type.lower() == "point" else 0
    
    def get_account_type(self, deliverySupport):
        deliverySupport__ = deliverySupport.split("-")
        if deliverySupport__[0] in ("kid", "pencilwood") and deliverySupport__[1] in ("home", "point"):
            return self.get_delivery_type(deliverySupport__[1]), deliverySupport__[0]
        

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            ids = data.get("order_ids", [])
            update_status = data.get("status")
            deliverySupport = data.get("deliverySupport")
            workAssign = data.get("workAssign")
            
            # For Status Update======
            if update_status:
                with transaction.atomic():
                    if update_status in ['Delivered', 'Return']:
                        Order.objects.filter(id__in=ids).update(status=update_status, urgent=False)
                    else:
                        Order.objects.filter(id__in=ids).update(status=update_status)
                    return JsonResponse(
                        {
                            "status": True,
                            "message": "Bulk  Status Update Successfully!"
                        }, status=HTTPStatus.OK
                    )
            
            # For Bulk Steadfast Parcel Create======
            if deliverySupport:
                success, failed = 0, 0
                delivery_type, account = self.get_account_type(deliverySupport)
                steadfast_api = SteadFastOrderCreateAPI(account=account)
                for id in ids:
                    try:
                        with transaction.atomic():
                            order = Order.objects.select_for_update().get(id=id)
                            recipient = order.request_order or order.order_customer
                            order_data = {
                                "invoice": order.tracking_ID,
                                "recipient_name":recipient.name,
                                "recipient_phone":recipient.phone_number,
                                "alternative_phone": recipient.second_phone_number,
                                "recipient_email": recipient.email,
                                "recipient_address": order.delivery_address,
                                "cod_amount": float(order.due_amount),
                                "note": order.special_instructions,
                                "item_description": order.remark,
                                # "total_lot": sum(item.quantity for item in order.order_item.all()),
                                "delivery_type": delivery_type
                            }
                            response = steadfast_api.create_order(order_data)
                            
                            consignment = response.get("consignment", {})
                            if response.get("status") == 200 and consignment:
                                order.steadfast_parcel_id = consignment.get("consignment_id")
                                order.status = 'Delivered'
                                order.save()
                                success += 1
                            else:
                                failed += 1
                    except:
                        failed += 1
                        continue
                return JsonResponse(
                    {
                        "status": True,
                        "message": "Bulk Delivery Parcel Created!",
                        "report": {
                            "total": len(ids),
                            "successful": success,
                            "failed": failed
                        }
                    }, status=HTTPStatus.OK
                )
            
            if workAssign and len(ids) > 0:
                with transaction.atomic():
                    Order.objects.filter(id__in=ids).update(work_assign_id=workAssign)
                    return JsonResponse(
                        {
                            "status": True,
                            "message": "Bulk Work Assign Update Successfully!"
                        }, status=HTTPStatus.OK
                    )
        except Exception as e:
            return JsonResponse(
                {
                    "status": False,
                    "message": str(e),
                }, statuss=HTTPStatus.BAD_REQUEST
            )

# -----------------Bulk Order Status Update End-----------------------
