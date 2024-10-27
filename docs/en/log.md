# Rolling Logs

## Logging

Logging is standardized by using the `logger`. Here’s how to use it:

```python
from ab.utils import logger

# https://docs.python.org/3/library/logging.html#module-logging
logger.debug/info/warning/error/exception/critical('hello', 'world')
```

Logs have levels, with `debug` being the lowest (more frequent but less critical) and `critical` being the highest (less frequent but very important).

Setting `LOG_LEVEL` in the configuration to a specific level will prevent any logs below that level from being printed.

The default log level is `INFO`.

**Avoid using `print` for logging. Content printed with `print` will not be displayed by default. The framework does not guarantee that `print` outputs will be saved in local logs, making it difficult to troubleshoot issues.**

## Log Files

Since the Docker container has cron service installed, log files can be rotated daily and kept for up to 30 days.

- By default, as specified in `config_prod.py`, logs are saved in the following files. The default naming convention includes a timestamp based on the service start time.

```python
accesslog='logs/access.log'
errorlog='logs/error.log'
```

- In some cases, you might want the log file names to remain constant. To achieve this, include the string `fix` in the file name, which will prevent a timestamp from being appended.

```python
accesslog='logs/fixaccess.log'
errorlog='logs/fixerror.log'
```
