from ab.utils import logger
from ab.core import api
from ab import app
from ab.utils.rate_limit import rate_limit


# will expose an API as: /api/algorithm/add
@api()
# only can be called 5 times per day
@rate_limit(5)
def add(a: int, b: int) -> int:
    logger.info("enter algorithm {}, {} ".format(a, b))
    return a + b


@api()
def custom_response(a: int, b: int) -> int:
    logger.info("enter algorithm {}, {} ".format(a, b))
    from flask import Response
    response = Response(f"Hello, {a - b}", status=200, mimetype='text/plain')
    return response


@api()
def compress() -> int:
    return "this is a hello world text file, glad to meet you, bye ~this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye "
