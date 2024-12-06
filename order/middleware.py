import threading
from datetime import timedelta
from django.utils.timezone import localtime


_user = threading.local()

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.user = request.user
        response = self.get_response(request)
        return response

def get_current_user():
    return getattr(_user, 'user', None)



class UpdateUrgentOrdersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        four_days_ago = localtime().date() - timedelta(days=4)
        from .models import Order
        Order.objects.filter(
            delivery_date__lte=four_days_ago,
            status__in=['None', 'Got Design', 'Processing', 'Sample', 'Packaging'],
            urgent=False
        ).update(urgent=True)

        response = self.get_response(request)
        return response

