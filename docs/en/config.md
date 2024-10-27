# Multi-environment Configuration

All configurations are placed in the `config` directory at the root of the project.

## Configuration Loading Priority (from high to low)
- Load key-value pairs from environment variables to override configurations.
- Load environment-specific configurations from `config_xxx.py` in the `config` directory, where `xxx` represents the specific environment.
- Load configurations from `config.py` in the `config` directory.
- Load the default configurations provided by the framework.

### Examples  
- Start the service using the default configuration:

```
pfs
```

- Start the service using the `test` environment configuration, which inherits from the default configuration:

```
pfs test
```

- Start the service using the `daily` environment configuration, inheriting from the default configuration, and set the number of workers to 4:

```
workers=4 pfs daily
```

- Start the service using both `local` and `daily` configurations, where `local` (on the left) has higher priority, while also inheriting from the default configuration:

```
pfs local daily
```

*Please note, `debug` is a reserved keyword in the framework and cannot be used as an environment name. For example, `config_debug.py` will not take effect.*

### Using Configurations in Containers

- When the container starts, it defaults to using the `prod` environment configuration (i.e., prioritizes configurations from `config_prod.py`):

```
docker run your-image
```   

- Start the container using a specified environment (e.g., `local`), with support for `local`, `daily`, and `prod` environments by default:

```
docker run your-image local
```

## Accessing Configuration Items

Configuration items are injected into Flask’s `config`. The recommended way to access them is as follows:

```python
from ab import app

app.config['YOUR_CONFIG_KEY']
# or
app.config.YOUR_CONFIG_KEY
```

# Complete Configuration

## What’s Included in the Configuration
- Framework plugin configurations
- [Flask configuration items](http://flask.pocoo.org/docs/1.0/config/#builtin-configuration-values) (all uppercase)
- [Gunicorn configuration items](http://docs.gunicorn.org/en/stable/settings.html) (all lowercase)
- User-defined configurations

## Detailed Configuration Items

The `config` inherits settings from Flask and Gunicorn, with additional custom configurations from `ab`. Therefore, all configurations can be written in the same `config.py` file.

Supported configuration items:
* APP_NAME: The algorithm name used for registration in Spring Cloud. Ensure each algorithm has a unique name.
  since v2.4.2: The separator should be `-` instead of `_`.
  Must be changed when deploying to a server. Required field.
* PORT: The port number can no longer be modified. Inside Docker, Nginx uses a fixed port 80 to access Gunicorn on port 8000.
* HOST: Specifies which IP to bind to. Typically use `localhost` for local testing, and `0.0.0.0` for server deployment. Default is 'localhost'.
  Reference: [What is the difference between 0.0.0.0, 127.0.0.1, and localhost?](https://stackoverflow.com/questions/20778771/what-is-the-difference-between-0-0-0-0-127-0-0-1-and-localhost)
* DEBUG: Whether to enable Flask and Gunicorn debug mode, default is `False`.
  Setting `DEBUG=True` allows the execution of arbitrary code. Avoid using the combination of `HOST=0.0.0.0` and `DEBUG=True` when deploying to a server.
* LOG_LEVEL: The global default logging level, which relies on Python’s logging module.
  See [logging levels](https://docs.python.org/3/library/logging.html#levels) for level details.
  If unspecified, the default level is `INFO`.
