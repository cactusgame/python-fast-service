# Monitoring

## Support for Prometheus Monitoring

Accessing the service at `http://[host]:[port]/metrics` allows you to view algorithm and method-level statistical information.


### Prometheus Monitoring Metrics

The current monitoring metrics are primarily designed to provide a clear view of the service's status and assist in debugging, focusing on quality rather than quantity. The basic approach is to log incoming system events, such as HTTP requests; record critical logic/functions within the system; and log outgoing events, such as database access and calls to other system interfaces.

In addition to these standard metrics, each project should also log unique metrics based on its own requirements, such as the size of the process pool, the number of threads waiting for a key resource, and so on.

#### HTTP-related Metrics

These are black-box metrics used to record information related to incoming HTTP requests.

1. **Counter**: `http_requests_total(method, url, code)`
    - Logs the total number of accesses for each HTTP endpoint.
    - `method`: HTTP method (GET/POST/PUT/DELETE).
    - `url`: The path of the accessed URL (only the path, no parameters needed).
    - `code`: The response code of the endpoint (e.g., 200, 500).

2. **Histogram**: `http_request_duration_seconds(method, url)`
    - Logs the processing time for each HTTP endpoint.
    - `method`: HTTP method (GET/POST/PUT/DELETE).
    - `url`: The path of the accessed URL.

3. **Gauge**: `inprogress_http_requests(method, url)`
    - Logs the number of HTTP requests being processed simultaneously.
    - `method`: HTTP method (GET/POST/PUT/DELETE).
    - `url`: The path of the accessed URL.

#### Key Function/Method-related Metrics

These are white-box metrics used to track indicators for specific critical functions/methods and outgoing requests, such as database access and remote calls to other systems.

1. **Counter**: `func_call_errors_total(name)`
    - Logs the total number of exceptions for functions/methods.
    - `name`: The function/method name.

2. **Counter**: `func_calls_total(name)`
    - Logs the total number of requests to functions/methods.
    - `name`: The function/method name.

3. **Histogram**: `func_call_duration_seconds(name)`
    - Logs the total processing time for functions/methods.
    - `name`: The function/method name.

4. **Gauge**: `inprogress_func_calls(name)`
    - Logs the number of functions/methods currently being processed.
    - `name`: The function/method name.
