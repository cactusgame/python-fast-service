# Health Check

## Principle

After the service starts, it performs a health check every `periodSeconds` seconds, beginning `initialDelaySeconds` seconds after startup. If it fails to respond within `timeoutSeconds` for `failureThreshold` consecutive checks, the service is considered unresponsive, and the main process is killed. The Docker `restart=always` mechanism then restarts the service.

This is the default liveness check configuration. You can choose to disable the health check or adjust the check frequency.

If the health check continues to fail, the main process will be terminated. The Docker `restart=always` mechanism is relied upon to achieve service restarts.

Additionally, health checks can serve as a form of pre-warming the service. This is especially beneficial in high memory-consuming services, where proper configuration of parameters like `initialDelaySeconds` can help achieve this goal.

## Configuration

```python
ENABLE_LIVENESS_PROB = True
LIVENESS_PROB = {
    # The number of seconds to wait after container startup before initiating the liveness and readiness probes. Minimum value is 0.
    "initialDelaySeconds": 180,
    # The interval (in seconds) between probe executions. Minimum value is 1.
    "periodSeconds": 60,
    # The timeout (in seconds) to wait before marking the probe as failed. Minimum value is 1.
    "timeoutSeconds": 1,
    # Number of consecutive failures after which the container will be restarted.
    "failureThreshold": 5,
}
```

