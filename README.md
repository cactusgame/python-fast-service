[中文](README_zh)   [[English]](README)

# Introduction

This project can quickly package your Python code into a production-ready service, providing the following main features:

- Implements API interfaces in a unified manner with standardized request and response formats
- Provides useful features like monitoring, logging, and multi-environment configuration
- Supports requirements like encryption and licensing for private delivery
- Assists in building Docker images

This project was originally developed as the [algorithm-base framework](https://github.com/aliyun/algorithm-base) by my colleagues and me while working at Alibaba Cloud. Due to the need to meet commercial project requirements, the framework included redundant logic. After leaving Alibaba Cloud, I forked the project, retained the most commonly used features, and made certain optimizations.

# Quick Start

Here is a minimal example to build an image for your `API` and deploy the service.

## Install the Framework

- The current framework only supports MacOS and Linux on X86 architecture
- It has only been tested with Python 3.8
- See [Installation](docs/en/install.md) for details

```
pip install python-fast-service
```


## Write a Hello World Service

Navigate to the `examples/simple` directory. This serves as the template for creating future projects, as well as the Hello World program.

For the `simple` project, you need to implement your API (the `controller` layer of the service) in the `api` directory. The example provides a `demo.py` file with several `API` implementations. In the following code, the method decorated with `@api` will be automatically exposed as a RESTful API with the path `/api/add`. See [Service and API](docs/en/service.md) for more details.

```python
from ab.core import api

@api()
def add(a: int, b: int) -> int:
    """
    A simple addition algorithm example
    :param a: First parameter
    :param b: Second parameter
    :return:
    """
    return a + b
```

## Start the Service and Test

In the `simple` root directory, ensure port 8000 is free, and start the service by entering the following command:

```commandline
pfs
```


After the service starts successfully, you will see output similar to the following, indicating that the service has started:

```
[2023-02-01 13:07:33 +0800] [12257] [INFO] Starting gunicorn 20.0.4
[2023-02-01 13:07:33 +0800] [12257] [DEBUG] Arbiter booted
[2023-02-01 13:07:33 +0800] [12257] [INFO] Listening at: http://0.0.0.0:8000 (12257)
[2023-02-01 13:07:33 +0800] [12257] [INFO] Using worker: sync
[2023-02-01 13:07:33 +0800] [12267] [INFO] Booting worker with pid: 12267
[2023-02-01 13:07:33] [12267] [DEBUG] algorithms: {('add', 'python'): add(a: int, b: int) -> int,
[2023-02-01 13:07:33] [12267] [DEBUG] fixtures: {}
[2023-02-01 13:07:33 +0800] [12257] [DEBUG] 2 workers
[2023-02-01 13:07:33] [12268] [DEBUG] algorithms: {('add', 'python'): add(a: int, b: int) -> int,
[2023-02-01 13:07:33] [12268] [DEBUG] fixtures: {}
```

You can access the previously defined API with the following command:

```
curl --location --request POST 'localhost:8000/api/add' \
--header 'Content-Type: application/json' \
--data-raw '{
	"args": {"a": 1, "b": 2}
}'
```


The output below shows the result of the addition algorithm:

```
{"code":0,"data":3}
```


### Modifying the API Path

The Fast Service framework defaults to exposing APIs under the `/api` path, but you can add new paths as well. You need to create a Python module, such as `endpoint.py`, in the `api` folder in the project’s root directory, allowing you to access this API at `/api/document/add`.

```python
from ab.endpoint.registry import register_endpoint

register_endpoint('/api/document/<string:api_name>')
```

### Customizing the Response Structure
You can return a Flask Response object to replace the default Fast Service response structure. See Custom Response Structure for details

```
 from flask import Response
 return Response(f"Hello, {a - b}", status=200, mimetype='text/plain')
```


## Build Docker Image

In the simple project root directory, enter the following command:
```
sh build.sh
```

At this point, you should have a basic understanding of the Fast Service framework. For detailed documentation, see the User Guide.

- [Installation](docs/en/install.md)
- Service
  - [service and API](docs/en/service.md)
- Performance
  - [http compression](docs/en/compress.md)
- OPS
  - [multiple environment configuration](docs/en/config.md)
  - [health check](docs/en/health_check.md)
  - [monitoring](docs/en/monitoring.md)
  - [exception and error handling](docs/en/error.md)
  - [test case](docs/en/test.md)
- Best Practices
  - [how to create a new project](docs/en/new-project.md)
  - [how to custom the response structure](docs/en/custom-response-format.md)
  - [FAQ](docs/en/best-practice.md)
  - [why gunicorn worker timeout](https://zhuanlan.zhihu.com/p/370330463)
  - [gunicorn configuration](https://zhuanlan.zhihu.com/p/371115835)




