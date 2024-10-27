# Errors and Exceptions

## Normal

HTTP status code 200, response code 0.

## Message

HTTP status code 200, response code -100.

```python
raise Message(msg="the error is caused by xxx")
```

Response:

```json
{
  "code": -100,
  "data": "the error is caused by xxx"
}
```

## Exception Without Stack Trace

In most cases, business-related exceptions should be thrown in this way. The HTTP status code is 500, response code is -1, and no error stack is returned.

```python
from ab.utils.exceptions import AlgorithmException
raise AlgorithmException(data="this is an exception")
```

Response:

```json
{
  "code": -1,
  "data": "this is an exception"
}
```

## Exception With Stack Trace

Why might you need to return an exception stack trace to the front end? Some deployment environments are very restrictive, making it difficult to log in to the server. Returning error information to the front end can facilitate remote maintenance, though this is generally insecure.

### Type 1 Exception

HTTP status code 500, response code -1, with an error stack trace returned.

```python
i = 1 / 0
```

Response:

```json
{
  "code": -1,
  "data": [
    "Traceback (most recent call last): ",
    " File \"/Users/xxx/miniconda3/envs/ab/lib/python3.7/site-packages/flask/app.py\", line 1950, in full_dispatch_request rv = self.dispatch_request() ",
    " File \"/Users/xxx/miniconda3/envs/ab/lib/python3.7/site-packages/flask/app.py\", line 1936, in dispatch_request return self.view_functions[rule.endpoint](**req.view_args) ",
    " File \"/Users/xxx/Documents/project/algorithm-base/src/ab/utils/prometheus.py\", line 30, in inner ret = func(*args, **kwargs) ",
    " File \"/Users/xxx/Documents/project/algorithm-base/src/ab/controllers/algorithm.py\", line 119, in run_algorithm_backend return run_algorithm(body) ",
    " File \"/Users/xxx/Documents/project/algorithm-base/src/ab/controllers/algorithm.py\", line 101, in run_algorithm result = algorithm.run_algorithm(request_body) ",
    " File \"/Users/xxx/Documents/project/algorithm-base/src/ab/services/algorithm.py\", line 19, in run_algorithm result = task.run() ",
    " File \"/Users/xxx/Documents/project/algorithm-base/src/ab/utils/task.py\", line 141, in run ret = self.run_algorithm() ",
    " File \"/Users/xxx/Documents/project/algorithm-base/src/ab/utils/task.py\", line 121, in run_algorithm result = self.algorithm.run(self.kwargs) ",
    " File \"/Users/xxx/Documents/project/algorithm-base/src/ab/utils/algorithm.py\", line 52, in run ret = self.main(*main_args) ",
    " File \"/Users/xxx/Documents/project/algorithm-base/src/ab/utils/prometheus.py\", line 61, in inner return func(*args, **kwargs) ",
    " File \"/Users/xxx/Documents/project/algorithm-base-demos/simple/api/demo.py\", line 29, in unknown print(1 / 0) ",
    "ZeroDivisionError: division by zero "
  ]
}
```

### Type 2 Exception

If the `data` attribute is not specified, the stack trace is included in the response by default.

```python
from ab.utils.exceptions import AlgorithmException
raise AlgorithmException()
```

Response:

```json
{
  "code": -1,
  "data": [
    "Traceback (most recent call last): ",
    " File \"/Users/xxx/miniconda3/envs/ab/lib/python3.7/site-packages/flask/app.py\", line 1950, in full_dispatch_request rv = self.dispatch_request() ",
    " File \"/Users/xxx/miniconda3/envs/ab/lib/python3.7/site-packages/flask/app.py\", line 1936, in dispatch_request return self.view_functions[rule.endpoint](**req.view_args) ",
    " File \"/Users/xxx/Documents/project/algorithm-base/src/ab/utils/prometheus.py\", line 30, in inner ret = func(*args, **kwargs) ",
    " File \"/Users/xxx/Documents/project/algorithm-base/src/ab/controllers/algorithm.py\", line 119, in run_algorithm_backend return run_algorithm(body) ",
    " File \"/Users/xxx/Documents/project/algorithm-base/src/ab/controllers/algorithm.py\", line 101, in run_algorithm result = algorithm.run_algorithm(request_body) ",
    " File \"/Users/xxx/Documents/project/algorithm-base/src/ab/services/algorithm.py\", line 19, in run_algorithm result = task.run() ",
    " File \"/Users/xxx/Documents/project/algorithm-base/src/ab/utils/task.py\", line 141, in run ret = self.run_algorithm() ",
    " File \"/Users/xxx/Documents/project/algorithm-base/src/ab/utils/task.py\", line 121, in run_algorithm result = self.algorithm.run(self.kwargs) ",
    " File \"/Users/xxx/Documents/project/algorithm-base/src/ab/utils/algorithm.py\", line 52, in run ret = self.main(*main_args) ",
    " File \"/Users/xxx/Documents/project/algorithm-base/src/ab/utils/prometheus.py\", line 61, in inner return func(*args, **kwargs) ",
    " File \"/Users/xxx/Documents/project/algorithm-base-demos/simple/api/demo.py\", line 29, in unknown print(1 / 0) ",
    "ZeroDivisionError: division by zero "
  ]
}
```
