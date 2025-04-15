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

- thread async api
  - step1: commit your async task, return the task id.
```
curl --location --request POST 'http://127.0.0.1:8000/api/async_add' --header 'Content-Type: application/json' --data-raw '{
        "mode": "thread",
        "args": {
            "a": 3,
            "b": 6,
            "run_seconds": 2
        }
}'

response: 
{"code":0,"data":"099eee0a6c42499781b726cf11f5c548"}

```
  - step2: check the status and result of your task.

```

GET http://127.0.0.1:8000/api/task/{task_id}/


for example: 
curl --location --request GET 'http://127.0.0.1:8000/api/task/f93246f830eb4eb9ae7e842092c8a504'

response:
{"id":28,"task_id":"f93246f830eb4eb9ae7e842092c8a504","code":2,"feature":9,"gmt_create":"2025-04-15 17:03:47.000","gmt_modified":null}
```

# Build docker image
```
sh build.sh
```

# Launch docker image
```
docker run -it -v $PWD/logs:/root/app/logs -p <your-host-port>:80 --restart=always <your-image-name>
```
