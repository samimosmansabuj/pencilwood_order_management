import threading

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
