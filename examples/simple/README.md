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
```
curl --location --request POST 'localhost:8000/api/add' \
--header 'Content-Type: application/json' \
--data-raw '{
	"args": {"a": 1, "b": 2}
}'
```

# Build docker image
```
sh build.sh
```

# Launch docker image
```
docker run -it -v $PWD/logs:/root/app/logs -p <your-host-port>:80 --restart=always <your-image-name>
```
