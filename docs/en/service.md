# Custom API Endpoints

## Quick Start

In the `api` directory of your project root, add the `@api` decorator to your method. Once the service is started, the endpoint can be accessed at `/api/add`.

```python
from ab.utils import logger
from ab.utils.algorithm import algorithm
from ab import app

@api()
def add(a, b):
    logger.warning("enter algorithm {}, {} ".format(a, b))
    return a + b
```

# API Format

## Custom Return Format

By default, all endpoints return data in the following structure: `{"code": 0, "data": xxx}`.

If you want a custom response format, you can return a `flask.Response` object directly, and the framework will not alter it.

## Returning Binary Files

To return a binary file:

```python
from flask import make_response
response = make_response(YOUR_CONTENT)
response.headers['Content-Type'] = 'application/octet-stream'
response.headers['Content-Disposition'] = f'attachment; filename={YOUR_FILENAME}'
return response
```

## Returning Exceptions

1. The framework provides a default exception class. Common usage is shown below:

```python
from ab.utils.exceptions import AlgorithmException

try:
    1 / 0
except Exception as e:
    # "from e" must be included to avoid losing the exception stack in logs
    raise AlgorithmException(code=-100, data=YOUR_MSG) from e
```

With this, the client will receive the following response:

```json
{
    "code": -100,
    "data": "YOUR_MSG"
}
```

2. If an uncaught exception is thrown, the client will receive:

```json
{
    "code": -1,
    "data": "Exception Stack Trace"
}
```

For more information, see [Exception and Error Handling](error.md).
