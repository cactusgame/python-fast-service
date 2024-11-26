from flask import Flask, request, jsonify
from functools import wraps
from datetime import datetime
from ab.utils.exceptions import AlgorithmException

import threading


# format: { 'YYYY-MM-DD': { 'ip_address': { 'endpoint': count } } }
rate_limit_data = {}
lock = threading.Lock()


def rate_limit(max_requests_per_day):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = get_remote_address()
            endpoint = request.endpoint
            today = datetime.utcnow().strftime('%Y-%m-%d')

            with lock:
                if today not in rate_limit_data:
                    rate_limit_data.clear()
                    rate_limit_data[today] = {}

                ip_data = rate_limit_data[today].get(client_ip, {})
                count = ip_data.get(endpoint, 0)

                if count >= max_requests_per_day:
                    raise AlgorithmException(code=5004,
                                             data=f"({max_requests_per_day} per day).")

                ip_data[endpoint] = count + 1
                rate_limit_data[today][client_ip] = ip_data

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def get_remote_address():
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0].split(',')[0]
    else:
        return request.remote_addr
