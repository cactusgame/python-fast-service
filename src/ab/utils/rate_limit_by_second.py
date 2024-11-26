import time
from flask import Flask, jsonify, request
from ab.utils.exceptions import AlgorithmException
from functools import wraps


def rate_limit_by_second(interval):
    """
    :param interval: seconds
    """
    last_request_time = [0]  # 使用列表来实现闭包

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            if current_time - last_request_time[0] < interval:
                raise AlgorithmException(code=5005)
            last_request_time[0] = current_time  # 更新最后请求时间
            return f(*args, **kwargs)

        return wrapper

    return decorator
