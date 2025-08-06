import logging
import time
from datetime import datetime
from django.http import HttpResponseForbidden
from collections import defaultdict


# 1. Logs all requests
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


# 2. Restricts access to chat between 6PM and 9PM
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Only allow between 18 (6PM) and 21 (9PM)
        if request.path.startswith('/chat/'):
            if current_hour < 18 or current_hour > 21:
                return HttpResponseForbidden("Access to chat is restricted at this time.")
        return self.get_response(request)


# 3. Limits POST chat messages to 5 per minute per IP
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_log = defaultdict(list)
        self.TIME_WINDOW = 60  # seconds
        self.REQUEST_LIMIT = 5  # max messages per minute per IP

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/chat/'):
            ip = self.get_client_ip(request)
            now = time.time()

            # Clean old timestamps
            self.request_log[ip] = [
                ts for ts in self.request_log[ip]
                if now - ts < self.TIME_WINDOW
            ]

            if len(self.request_log[ip]) >= self.REQUEST_LIMIT:
                return HttpResponseForbidden("Rate limit exceeded. Try again in a minute.")

            self.request_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
