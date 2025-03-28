from ab.utils import logger
from ab.core import api
from ab import app
from ab.utils.rate_limit import rate_limit
from ab.utils.rate_limit_by_second import rate_limit_by_second


# will expose an API as: /api/algorithm/add
@api()
# only can be called 5 times per day
# @rate_limit(5)
@rate_limit_by_second(15)
def add(a: int, b: int) -> int:
    logger.info("enter algorithm {}, {} ".format(a, b))
    return a + b

@api()
def error(a: int, b: int) -> int:
    print(1/0)
    return 2

@api()
def custom_response(a: int, b: int) -> int:
    logger.info("enter algorithm {}, {} ".format(a, b))
    from flask import Response
    response = Response(f"Hello, {a - b}", status=200, mimetype='text/plain')
    return response


@api()
def compress() -> int:
    return "this is a hello world text file, glad to meet you, bye ~this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye this is a hello world text file, glad to meet you, bye "
