# Test Cases

## About pytest and tox

[pytest](https://docs.pytest.org/en/latest/) is an automated testing framework;  
[tox](https://tox.readthedocs.io/en/latest/) can start a virtual environment (venv) and execute various scripts. It supports multiprocessing, which makes testing faster.

Together, pytest and tox allow you to create a virtual environment and then run pytest to execute test scripts.

Currently, the framework is configured to run tests with 8 threads by default.

#### Developing Test Cases

Requirements:
1. Place all test code in the `tests` directory, with files starting with `test_` and test functions also starting with `test_`. This is a pytest convention.
2. Copy `tests/__init__.py` and `tox.ini` into your new project.
   Make sure to keep the `tests/__init__.py` file; otherwise, errors may occur.
3. Endpoint test functions should accept a `client` parameter and use `get_data`/`post_data` functions to simulate user GET/POST requests. Each endpoint should have at least one test function.
4. By default, pytest uses the user 'gs1/gs1' for login and test execution. If you need to use another user, create a `tests/conftest.py` file and add the following:

   ```python
   import pytest

   @pytest.fixture(scope="session")
   def login_info():
       return {'username': 'YOUR_USERNAME', 'password': 'YOUR_PASSWORD'}
   ```

#### Running Tests

1. Install `tox` and `pytest`:

   ```bash
   pip3 install tox pytest
   ```

2. To run a single test file, execute the following command in the **root directory**:

   ```bash
   pytest -e CONFIG -s --disable-warnings tests/xxx.py
   ```

   - `-e`: Loads a specific configuration file. For example, `-e dev` loads `config/config_dev.py`. (Since v2.5.0)
   - `-s`: Displays console and logger output.
   - `--disable-warnings`: Ignores warnings.

3. To run all test cases, simply execute `tox` in the **root directory**.

**Note: You do not need to start the service manually; the testing framework will handle it automatically.**

**To use multiprocessing for testing, Redis must be configured, or login will fail.**
