# Instructions
A demo and template for new project
  
# Structure
```
├── api
├── config
│   └── config.py
│   └── config_dev.py
├── tests
│   ├── test_xxx.py
├── docker
│   ├── Dockerfile
├── setup
│   ├── requirements.txt
```

- `api`: the place to define your API. 
- `config`: configurations for different env
- `tests`: test cases
- `docker`: scripts for docker
- `setup`: 

# Calling
- sync api
```
curl --location --request POST 'localhost:8000/api/add' \
--header 'Content-Type: application/json' \
--data-raw '{
	"args": {"a": 1, "b": 2}
}'
```

- async api
  - step1: commit your async task, return the task id.
```
curl --location --request POST 'http://127.0.0.1:8000/api/async_add' \
--header 'Content-Type: application/json' \
--data-raw '{
        "mode": "async",
        "args": {
            "a": 3,
            "b": 6,
            "run_seconds": 20
        }
}'
```
  - step2: check the status and result of your task.

```

GET http://127.0.0.1:8000/api/task/{task_id}/


curl --location --request GET 'http://127.0.0.1:8000/api/task/d83621aa9fdb4988a246ad4404305223'
```

# Build docker image
```
sh build.sh
```

# Launch docker image
```
docker run -it -v $PWD/logs:/root/app/logs -p <your-host-port>:80 --restart=always <your-image-name>
```
