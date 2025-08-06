import logging
from datetime import datetime
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        path = request.path
        log_message = f"{datetime.now()} - User: {user} - Path: {path}"
        logging.info(log_message)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Restrict access before 6PM (18) or after 9PM (21)
        if current_hour < 18 or current_hour > 21:
            return HttpResponseForbidden("Access to chat is restricted at this time.")

        return self.get_response(request)