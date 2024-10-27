# Best Practices

## How to Start the Service
To start the service, execute the following command in the root directory of the [framework-based project](./../../examples/simple):

```bash
pfs
```

## How to Debug the AB Service
[debug](debug.jpg)

## How to Change the Service Port
- When debugging locally, some ports on your machine might be occupied. You can modify the `PORT` variable in the config (default is 8000) to any other port for debugging purposes.
- During Docker deployment, `gunicorn` must use port 8000 because the final service exposure is handled by the built-in nginx in Docker, not gunicorn.
- The actual routing situation in the production environment is: user request -> nginx (port 80) -> gunicorn (port 8000).
- The version of nginx is 1.14.2.

```bash
docker run -p xxxx:80 your-image
```

## How to Build the Image
To build the default Docker image, execute the following command in the root directory of the algorithm project:

```bash
sh build.sh
```

By default, Python 3.8 is used. If you must use another Python version, modify the base image in the `Dockerfile`.

## How to Start the Container
- In actual projects, memory and CPU limits should be added manually.
- The host machine port needs to be modified according to the actual situation, while the container internal port is fixed at 80.

```bash
docker run -it -v $PWD/logs:/root/app/logs -p 8888:80 --restart=always your-image
```

## How to Debug Problematic Images
- The following command allows you to enter the container without starting the gunicorn service.

```bash
docker run -it --entrypoint bash <your-image>
```

Or

```bash
docker run -it your-image debug
```

## Testing Trilogy
When encountering issues, follow these steps to troubleshoot:

### Step 1: Execute Test Cases
- Install and activate the virtual environment with the framework.
- For example, run pytest in the console.

```bash
pytest -e dev tests/test_demo.py
```

- Or use IDE testing (supports debugging)
  [pytest](pytest.jpg)

### Step 2: Service Testing
- In the console, navigate to the project root directory and start the service using `pfs xxx` (where `xxx` is the configuration environment being used).
- Access the local service using tools like `curl`.
  Example of `curl` invocation:

```bash
curl --location --request POST 'localhost:8000/api/algorithm/add' \
--header 'Content-Type: application/json' \
--data-raw '{
	"args": {"a": 1, "b": 2}
}'
```

Example of Java invocation:

```java
OkHttpClient client = new OkHttpClient().newBuilder()
  .build();
MediaType mediaType = MediaType.parse("application/json");
RequestBody body = RequestBody.create(mediaType, "{\n\t\"args\": {\"a\": 1, \"b\": 2}\n}");
Request request = new Request.Builder()
  .url("localhost:2333/api/algorithm/add")
  .method("POST", body)
  .addHeader("Content-Type", "application/json")
  .build();
Response response = client.newCall(request).execute();
```

### Step 3: Test Using Containers
- Use the "Start Container" method mentioned above to start the container.
- Test externally through tools like `curl`.

